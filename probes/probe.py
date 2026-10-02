#!/usr/bin/env python3
"""
probe.py - measure how HTCondor treats a self-checkpointing job.

This is NOT a training script. It pretends to train, one "step" per second, and
records everything that happens to it: where it runs, what state it finds on
start, which signals arrive and when, how long saves take, and how it exits.

Standard library only, Python >= 3.6, so it runs bare on execute points (EPs)
and inside a minimal container.

Every observation is a JSON object printed on one line, prefixed with "PROBE ",
and (when a checkpoint directory is in use) also appended to
<ckpt-dir>/history.jsonl, so the history travels with the checkpoint.
analyze.py turns these records into answers.

Modes
  --mode run          (default) the fake training loop
  --mode fingerprint  describe the EP / container and exit 0
  --mode bench        time checkpoint-sized writes to one or more directories
"""

import argparse
import json
import multiprocessing
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import uuid

EXIT_CHECKPOINT = 85  # "state saved, please restart me" (checkpoint_exit_code)
EXIT_DONE = 0

# Signals we listen for. HTCondor's default soft-kill signal is SIGTERM, but a
# submit file can change it with kill_sig, so we record any of these.
WATCHED_SIGNALS = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT,
                   signal.SIGUSR1, signal.SIGUSR2]

HOST = socket.gethostname()
EXEC_ID = uuid.uuid4().hex[:8]  # identifies this execution (one process start)
RANK = os.environ.get("RANK")   # set when launched by torchrun (test P7e)

# Filled in by the signal handler. The handler only appends to this list: no
# I/O, no logging. That mirrors what a real training job should do.
RECEIVED = []


def on_signal(signum, frame):
    RECEIVED.append((signum, time.time()))


def signame(signum):
    if isinstance(signum, str):
        return signum
    try:
        return signal.Signals(signum).name
    except ValueError:
        return str(signum)


# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------

class Log:
    def __init__(self, test, job_id):
        self.test = test
        self.job_id = job_id
        self.history_path = None  # set once the checkpoint dir is known

    def event(self, kind, **fields):
        rec = {
            "t": round(time.time(), 3),
            "event": kind,
            "test": self.test,
            "job": self.job_id,
            "exec": EXEC_ID,
            "host": HOST,
            "pid": os.getpid(),
        }
        if RANK is not None:
            rec["rank"] = RANK
        rec.update(fields)
        line = json.dumps(rec, sort_keys=True, default=str)
        print("PROBE " + line, flush=True)
        if self.history_path:
            try:
                with open(self.history_path, "a") as f:
                    f.write(line + "\n")
                    f.flush()
                    os.fsync(f.fileno())
            except OSError as e:
                print("PROBE-WARN cannot append history: %s" % e, flush=True)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def read_classad_file(path):
    """Parse a $_CONDOR_JOB_AD / $_CONDOR_MACHINE_AD file ("Attr = value" lines)."""
    if not path:
        return None
    ad = {}
    try:
        with open(path) as f:
            for line in f:
                if " = " in line:
                    k, v = line.split(" = ", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                        v = v[1:-1]
                    ad[k.strip()] = v
    except OSError:
        return None
    return ad


def fsync_dir(path):
    """fsync a directory so a rename inside it is durable. Not all filesystems allow it."""
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return False
    try:
        os.fsync(fd)
        return True
    except OSError:
        return False
    finally:
        os.close(fd)


def proc_signal_masks():
    """Signals ignored/blocked/caught at startup, from /proc (Linux only).

    If SIGTERM is already ignored when we start (inherited from a wrapper),
    our handler would still be installed, but it's useful to know.
    """
    out = {}
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith(("SigIgn", "SigBlk", "SigCgt")):
                    k, v = line.split(":", 1)
                    out[k] = v.strip()
    except OSError:
        pass
    return out


def process_ancestry():
    """Command lines of our parent processes (Linux only): shows wrappers, starters, apptainer."""
    chain = []
    pid = os.getpid()
    for _ in range(8):
        try:
            with open("/proc/%d/stat" % pid) as f:
                ppid = int(f.read().rsplit(")", 1)[1].split()[1])
            with open("/proc/%d/cmdline" % ppid, "rb") as f:
                cmd = f.read().replace(b"\0", b" ").decode(errors="replace").strip()
        except (OSError, ValueError, IndexError):
            break
        chain.append({"pid": ppid, "cmd": cmd[:200]})
        if ppid <= 1:
            break
        pid = ppid
    return chain


ONE_MB = os.urandom(1024 * 1024)  # reused block, so writing GBs doesn't cost CPU


def write_payload(dirpath, total_mb, nfiles):
    """Write total_mb of data spread over nfiles files, fsync each. Returns bytes written."""
    written = 0
    if total_mb <= 0 or nfiles <= 0:
        return 0
    per_file = max(1, total_mb // nfiles)
    for i in range(nfiles):
        path = os.path.join(dirpath, "payload_%03d.bin" % i)
        with open(path, "wb") as f:
            for _ in range(per_file):
                f.write(ONE_MB)
                written += len(ONE_MB)
            f.flush()
            os.fsync(f.fileno())
    return written


# --------------------------------------------------------------------------
# The sandbox marker: a file in the job's working directory that is NOT part
# of the checkpoint. If it is still there on the next start, the job
# restarted in the same sandbox.
# --------------------------------------------------------------------------

# One marker per rank: torchrun workers share a sandbox, and two processes rewriting the
# same file at the same moment race each other (seen in test P7e).
MARKER = "sandbox_marker%s.json" % (".rank" + RANK if RANK is not None else "")


def load_marker():
    try:
        with open(MARKER) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_marker(marker):
    tmp = "%s.%d.tmp" % (MARKER, os.getpid())
    with open(tmp, "w") as f:
        json.dump(marker, f)
    os.replace(tmp, MARKER)


# --------------------------------------------------------------------------
# Checkpoints: step_XXXXXXXX/ directories, written to *.tmp then renamed,
# plus a "latest" pointer file. Same protocol the recipes will use.
# --------------------------------------------------------------------------

def list_complete(ckpt_dir):
    try:
        names = os.listdir(ckpt_dir)
    except OSError:
        return []
    good = []
    for n in names:
        if re.match(r"^step_\d{8}$", n) and os.path.exists(os.path.join(ckpt_dir, n, "state.json")):
            good.append(n)
    return sorted(good)


def restore(ckpt_dir, log):
    """Find the newest complete checkpoint and describe it."""
    info = {"ckpt_dir": ckpt_dir, "exists": os.path.isdir(ckpt_dir)}
    if not info["exists"]:
        log.event("restore", found=False, **info)
        return 0
    try:
        listing = sorted(os.listdir(ckpt_dir))
    except OSError as e:
        listing = ["<error: %s>" % e]
    info["listing"] = listing

    # Stale .tmp directories mean a save was interrupted (e.g. SIGKILL mid-write).
    stale = [n for n in listing if n.endswith(".tmp")]
    if stale:
        info["stale_tmp"] = stale
        for n in stale:
            shutil.rmtree(os.path.join(ckpt_dir, n), ignore_errors=True)

    latest_name = None
    try:
        with open(os.path.join(ckpt_dir, "latest")) as f:
            latest_name = f.read().strip()
    except OSError:
        pass
    info["latest_pointer"] = latest_name

    complete = list_complete(ckpt_dir)
    chosen = latest_name if latest_name in complete else (complete[-1] if complete else None)
    if chosen is None:
        log.event("restore", found=False, **info)
        return 0

    with open(os.path.join(ckpt_dir, chosen, "state.json")) as f:
        state = json.load(f)
    nested_ok = os.path.exists(os.path.join(ckpt_dir, chosen, "nested", "deeper", "inner.txt"))
    log.event("restore", found=True, chosen=chosen, step=state["step"],
              saved_reason=state.get("reason"), saved_by_exec=state.get("exec"),
              saved_on_host=state.get("host"), saved_at=state.get("saved_at"),
              nested_dir_ok=nested_ok, **info)
    return int(state["step"])


def save(ckpt_dir, step, reason, args, log, wait_fn):
    """Atomic save: write step_X.tmp/, fsync, rename to step_X/, then update 'latest'."""
    name = "step_%08d" % step
    tmp = os.path.join(ckpt_dir, name + ".tmp")
    final = os.path.join(ckpt_dir, name)
    t0 = time.time()
    log.event("save_start", step=step, reason=reason, ckpt_mb=args.ckpt_mb, ckpt_files=args.ckpt_files)
    try:
        os.makedirs(ckpt_dir, exist_ok=True)
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(os.path.join(tmp, "nested", "deeper"))
        with open(os.path.join(tmp, "nested", "deeper", "inner.txt"), "w") as f:
            f.write("nested directory survived transfer\n")
        nbytes = write_payload(tmp, args.ckpt_mb, args.ckpt_files)
        state = {"step": step, "reason": reason, "saved_at": time.time(), "exec": EXEC_ID, "host": HOST}
        with open(os.path.join(tmp, "state.json"), "w") as f:
            json.dump(state, f)
            f.flush()
            os.fsync(f.fileno())
        fsync_dir(tmp)
        t_written = time.time()

        if args.save_seconds > 0:
            # Pretend the save is slow, so signals to the process tree can be
            # observed while a save is in progress (test P7).
            wait_fn(args.save_seconds)

        if os.path.exists(final):
            shutil.rmtree(final)
        os.rename(tmp, final)
        dir_fsync_ok = fsync_dir(ckpt_dir)
        ptr_tmp = os.path.join(ckpt_dir, "latest.tmp")
        with open(ptr_tmp, "w") as f:
            f.write(name + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(ptr_tmp, os.path.join(ckpt_dir, "latest"))
        fsync_dir(ckpt_dir)

        # Retention: keep the newest args.keep checkpoints.
        for old in list_complete(ckpt_dir)[:-args.keep]:
            shutil.rmtree(os.path.join(ckpt_dir, old), ignore_errors=True)
    except OSError as e:
        log.event("save_error", step=step, reason=reason, error=str(e), seconds=round(time.time() - t0, 3))
        return False
    log.event("save_done", step=step, reason=reason, bytes=nbytes,
              write_seconds=round(t_written - t0, 3), seconds=round(time.time() - t0, 3),
              dir_fsync_ok=dir_fsync_ok)
    return True


def prune_payload(ckpt_dir):
    """Before the final exit, delete bulky payload files so they aren't transferred back to the AP."""
    for root, _dirs, files in os.walk(ckpt_dir):
        for fn in files:
            if fn.startswith("payload_"):
                try:
                    os.remove(os.path.join(root, fn))
                except OSError:
                    pass


# --------------------------------------------------------------------------
# Child processes (test P7): do signals reach the whole process tree?
# --------------------------------------------------------------------------

def child_main(idx, behavior, test, job_id):
    """A stand-in for a DataLoader worker.

    behavior "ignore": logs the signal and keeps going (what our recipes will do).
    behavior "die":    logs the signal and exits 143 (what an unprepared worker does).
    """
    global EXEC_ID
    EXEC_ID = EXEC_ID + "-c%d" % idx
    for s in WATCHED_SIGNALS:
        signal.signal(s, on_signal)
    del RECEIVED[:]
    log = Log(test, job_id)
    log.event("child_start", child=idx, behavior=behavior, ppid=os.getppid())
    seen = 0
    last_beat = 0
    while True:
        time.sleep(0.1)
        while seen < len(RECEIVED):
            signum, t = RECEIVED[seen]
            seen += 1
            log.event("signal", role="child", child=idx, behavior=behavior, signal=signame(signum), received_at=t)
            if behavior == "die":
                log.event("exit", role="child", child=idx, code=143)
                os._exit(143)
        if time.time() - last_beat > 5:
            last_beat = time.time()
            log.event("child_alive", child=idx)


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

INTERESTING_AD_ATTRS = re.compile(
    r"(Vacate|Retire|Backfill|Resumable|Staging|GPU|CUDA|Pool|GLIDEIN_Site|Site|Version|OpSys|"
    r"Preempt|Kill|Checkpoint|Ckpt|JobStart|CurrentStart|SlotType|Container|Singularity|Apptainer|"
    r"Chirp|IOProxy|FileSystemDomain|UidDomain|^Arch$|^Name$|Memory|Disk|Cpus)", re.I)

SECRETS = re.compile(r"(TOKEN|SECRET|PASSWORD|CRED|KEY)", re.I)


def run_cmd(cmd, timeout=20):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = p.communicate(timeout=timeout)
        return {"rc": p.returncode, "out": out.decode(errors="replace")[:2000]}
    except Exception as e:  # missing binary, timeout, ...
        return {"error": str(e)}


def check_url(url):
    import urllib.request
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return {"ok": True, "status": r.status, "seconds": round(time.time() - t0, 2)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "seconds": round(time.time() - t0, 2)}


def mode_fingerprint(args, log):
    info = {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "uid": os.getuid(),
        "scratch_dir": os.environ.get("_CONDOR_SCRATCH_DIR"),
        "signal_masks": proc_signal_masks(),
        "ancestry": process_ancestry(),
    }
    info["env"] = {k: v for k, v in sorted(os.environ.items())
                   if k.startswith(("_CONDOR", "CONDOR", "APPTAINER", "SINGULARITY", "CUDA", "NVIDIA",
                                    "OSG", "GLIDEIN", "HOME", "PATH", "TMPDIR"))
                   and not SECRETS.search(k)}
    info["container"] = {
        "apptainer_env": bool(os.environ.get("APPTAINER_CONTAINER") or os.environ.get("SINGULARITY_CONTAINER")),
        "singularity_d": os.path.isdir("/.singularity.d"),
        "dockerenv": os.path.exists("/.dockerenv"),
    }

    os.makedirs("out", exist_ok=True)
    for label, var in (("job_ad", "_CONDOR_JOB_AD"), ("machine_ad", "_CONDOR_MACHINE_AD")):
        path = os.environ.get(var)
        ad = read_classad_file(path)
        info[label + "_readable"] = ad is not None
        if ad is not None:
            info[label] = {k: v for k, v in ad.items() if INTERESTING_AD_ATTRS.search(k)}
            shutil.copy(path, os.path.join("out", label + ".txt"))  # full ad, for later reading

    paths = {}
    for p in ["/staging", args.staging_dir, "/cvmfs", "/cvmfs/singularity.opensciencegrid.org"]:
        if p:
            paths[p] = {"exists": os.path.exists(p), "isdir": os.path.isdir(p)}
    if args.staging_dir and os.path.isdir(os.path.dirname(args.staging_dir.rstrip("/")) or "/"):
        try:
            os.makedirs(args.staging_dir, exist_ok=True)
            probe_file = os.path.join(args.staging_dir, "write_test_%s" % EXEC_ID)
            with open(probe_file, "w") as f:
                f.write("ok\n")
            os.remove(probe_file)
            paths[args.staging_dir]["writable"] = True
        except OSError as e:
            paths[args.staging_dir]["writable"] = False
            paths[args.staging_dir]["error"] = str(e)
    info["paths"] = paths

    du = shutil.disk_usage(".")
    info["scratch_free_gb"] = round(du.free / 1e9, 1)

    tools = {}
    for t in ["condor_chirp", "nvidia-smi", "apptainer", "singularity", "python3", "bash", "torchrun"]:
        tools[t] = shutil.which(t)
    for p in ["/usr/libexec/condor/condor_chirp", "/usr/lib/condor/libexec/condor_chirp"]:
        if os.path.exists(p):
            tools["condor_chirp_libexec"] = p
    info["tools"] = tools
    chirp = tools.get("condor_chirp") or tools.get("condor_chirp_libexec")
    if chirp:
        # Try a harmless chirp: read our own ClusterId. Needs +WantIOProxy = true.
        info["chirp_test"] = run_cmd([chirp, "get_job_attr", "ClusterId"])
    if tools.get("nvidia-smi"):
        info["nvidia_smi"] = run_cmd(["nvidia-smi", "-L"])

    info["internet"] = {u: check_url(u) for u in [
        "https://pypi.org/simple/pip/", "https://huggingface.co/api/models?limit=1", "https://github.com"]}

    with open(os.path.join("out", "fingerprint.json"), "w") as f:
        json.dump(info, f, indent=2, sort_keys=True, default=str)
    log.event("fingerprint", **info)
    log.event("exit", code=EXIT_DONE, reason="fingerprint done")
    return EXIT_DONE


def mode_bench(args, log):
    """Time writing checkpoint-sized data (fsync + rename) to each target directory."""
    sizes = [int(x) for x in args.bench_mb.split(",") if x]
    nfiles_list = [int(x) for x in args.bench_files.split(",") if x]
    for target in [t for t in args.bench_targets.split(",") if t]:
        base = os.path.join(target, "bench_%s" % EXEC_ID)
        try:
            os.makedirs(base, exist_ok=True)
        except OSError as e:
            log.event("bench_error", target=target, error=str(e))
            continue
        for mb in sizes:
            for nfiles in nfiles_list:
                d = os.path.join(base, "ck_%d_%d.tmp" % (mb, nfiles))
                try:
                    os.makedirs(d)
                    t0 = time.time()
                    nbytes = write_payload(d, mb, nfiles)
                    fsync_dir(d)
                    t1 = time.time()
                    os.rename(d, d[:-4])
                    fsync_dir(base)
                    t2 = time.time()
                    log.event("bench", target=target, mb=mb, files=nfiles, bytes=nbytes,
                              write_seconds=round(t1 - t0, 3), rename_seconds=round(t2 - t1, 3),
                              mb_per_s=round(nbytes / 1e6 / max(t1 - t0, 1e-6), 1))
                except OSError as e:
                    log.event("bench_error", target=target, mb=mb, files=nfiles, error=str(e))
                finally:
                    shutil.rmtree(d, ignore_errors=True)
                    shutil.rmtree(d[:-4], ignore_errors=True)
        shutil.rmtree(base, ignore_errors=True)
    log.event("exit", code=EXIT_DONE, reason="bench done")
    return EXIT_DONE


def mode_run(args, log, marker, job_ad):
    ckpt_dir = os.path.abspath(args.ckpt_dir)
    if RANK is not None:
        ckpt_dir = os.path.join(ckpt_dir, "rank%s" % RANK)
    os.makedirs(ckpt_dir, exist_ok=True)
    log.history_path = os.path.join(ckpt_dir, "history.jsonl")
    log.event("history_attached", ckpt_dir=ckpt_dir, store=args.store)

    step = restore(ckpt_dir, log)
    restored_step = step

    # Was this job rescheduled (vacated, then started again in a NEW sandbox)?
    # The job ad's NumJobStarts is not reliable for this: on CHTC it read 0 on every
    # start, and exit-85 restarts happen in the same sandbox without a new start.
    # Reliable sign: a checkpoint came back from spool, but our sandbox marker did not.
    starts = int(job_ad.get("NumJobStarts", "0") or 0) if job_ad else 0
    marker_survived = len(marker.get("starts", [])) > 1
    rescheduled = starts >= 1 or (restored_step > 0 and not marker_survived)
    if args.exit_on_restart and rescheduled:
        log.event("exit", code=EXIT_DONE, step=step,
                  reason="rescheduled (NumJobStarts=%d, restored step %d, sandbox marker survived=%s); "
                         "--exit-on-restart" % (starts, restored_step, marker_survived))
        return EXIT_DONE

    # Children for test P7. Half ignore the signal, half die on it.
    children = []
    if args.children > 0:
        ctx = multiprocessing.get_context("fork")
        for i in range(args.children):
            behavior = "ignore" if i % 2 == 0 else "die"
            p = ctx.Process(target=child_main, args=(i, behavior, args.test, args.job_id), daemon=True)
            p.start()
            children.append(p)
    child_state = {}

    heartbeat_path = None
    if args.heartbeat_dir:
        try:
            os.makedirs(args.heartbeat_dir, exist_ok=True)
            heartbeat_path = os.path.join(args.heartbeat_dir, "heartbeat.log")
            with open(heartbeat_path, "a") as f:
                f.write("%.3f start exec=%s host=%s\n" % (time.time(), EXEC_ID, HOST))
        except OSError as e:
            log.event("heartbeat_error", error=str(e))
            heartbeat_path = None

    seen_signals = [0]
    stop = [None]  # (signum, time) of the first signal

    def poll():
        """Log new signals and child exits. Called often, from the main loop only."""
        while seen_signals[0] < len(RECEIVED):
            signum, t = RECEIVED[seen_signals[0]]
            seen_signals[0] += 1
            first = stop[0] is None
            log.event("signal", role="parent", signal=signame(signum), received_at=t,
                      first=first, step=step, on_sigterm=args.on_sigterm)
            if first:
                stop[0] = (signum, t)
        for i, p in enumerate(children):
            if child_state.get(i) is None and not p.is_alive():
                child_state[i] = p.exitcode
                # Negative exitcode = killed by that signal, e.g. -9 means SIGKILL.
                log.event("child_exit_seen", child=i, exitcode=p.exitcode)

    def wait(seconds):
        end = time.time() + seconds
        while time.time() < end:
            time.sleep(0.1)
            poll()

    def finish(code, reason):
        poll()
        log.event("children_at_exit", alive=[p.is_alive() for p in children],
                  exitcodes=[p.exitcode for p in children])
        # SIGKILL, not terminate(): the "ignore" child ignores SIGTERM by design,
        # and multiprocessing would otherwise wait for it forever at exit.
        for p in children:
            if p.is_alive():
                os.kill(p.pid, signal.SIGKILL)
                p.join(5)
        if code == EXIT_CHECKPOINT and args.restart_file:
            # Tell a wrapper "state saved, please restart me": launchers such as torchrun
            # turn a worker's exit 85 into exit 1, so the code alone does not survive.
            with open(args.restart_file, "a") as f:
                f.write("%s rank=%s step=%d\n" % (EXEC_ID, RANK, step))
        marker.setdefault("exits", []).append({"exec": EXEC_ID, "code": code, "t": time.time()})
        save_marker(marker)
        log.event("exit", code=code, reason=reason, step=step)
        return code

    voluntary = set(int(x) for x in args.voluntary_exit_at.split(",") if x)
    last_beat = 0.0
    log.event("loop_start", step=step, restored_step=restored_step,
              voluntary_exit_at=sorted(voluntary), total_steps=args.total_steps)

    while True:
        wait(1.0)
        step += 1

        # Stop file (test P7h): a launcher-independent way to ask workers to stop. A wrapper
        # that received SIGTERM creates this file instead of forwarding the signal.
        if args.stop_file and stop[0] is None and os.path.exists(args.stop_file):
            stop[0] = ("STOPFILE", time.time())
            log.event("stop_file_seen", path=args.stop_file, step=step)

        now = time.time()
        if heartbeat_path:
            try:
                with open(heartbeat_path, "a") as f:
                    f.write("%.3f step=%d exec=%s\n" % (now, step, EXEC_ID))
                    f.flush()
                    os.fsync(f.fileno())
            except OSError:
                pass
        if now - last_beat >= args.heartbeat_every:
            last_beat = now
            log.event("tick", step=step)

        if stop[0] is not None and args.on_sigterm != "ignore":
            signum, t_sig = stop[0]
            if args.on_sigterm == "default" and not isinstance(signum, str):
                # Behave like an unprepared program: die from the signal.
                log.event("dying_by_signal", signal=signame(signum), step=step)
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum)
                time.sleep(5)  # not reached unless the default action is "ignore"
            ok = save(ckpt_dir, step, "signal", args, log, wait)
            code = EXIT_CHECKPOINT if args.on_sigterm == "save85" else EXIT_DONE
            log.event("signal_save_finished", ok=ok, seconds_since_signal=round(time.time() - t_sig, 3))
            return finish(code, "signal %s, on_sigterm=%s" % (signame(signum), args.on_sigterm))

        if step in voluntary and step > restored_step:
            n_vol = sum(1 for e in marker.get("exits", []) if e.get("code") == EXIT_CHECKPOINT)
            if args.max_voluntary_exits and n_vol >= args.max_voluntary_exits:
                log.event("voluntary_exit_skipped", step=step, reason="max_voluntary_exits reached in this sandbox")
            else:
                if args.empty_checkpoint:
                    # Test P8d: leave the checkpoint directory present but empty.
                    for n in os.listdir(ckpt_dir):
                        if n != "history.jsonl":
                            shutil.rmtree(os.path.join(ckpt_dir, n), ignore_errors=True)
                    log.event("emptied_checkpoint_dir", step=step)
                else:
                    save(ckpt_dir, step, "voluntary", args, log, wait)
                return finish(EXIT_CHECKPOINT, "voluntary exit at step %d" % step)

        if args.periodic_every and step % args.periodic_every == 0:
            save(ckpt_dir, step, "periodic", args, log, wait)

        if step >= args.total_steps:
            save(ckpt_dir, step, "final", args, log, wait)
            prune_payload(ckpt_dir)
            os.makedirs("out", exist_ok=True)
            try:
                shutil.copy(log.history_path, os.path.join("out", "history.jsonl"))
            except OSError:
                pass
            return finish(EXIT_DONE, "finished %d steps" % step)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--test", default="local", help="test name, recorded in every event")
    ap.add_argument("--job-id", default="local", help="$(Cluster).$(Process)")
    ap.add_argument("--mode", choices=["run", "fingerprint", "bench"], default="run")
    ap.add_argument("--store", default="spool", help="label only: spool, staging, scratch, destination")
    ap.add_argument("--ckpt-dir", default="ckpt", help="checkpoint directory (relative = in the job sandbox)")
    ap.add_argument("--keep", type=int, default=2, help="checkpoints to keep")
    ap.add_argument("--total-steps", type=int, default=300, help="one step per second; exit 0 after this many")
    ap.add_argument("--voluntary-exit-at", default="", help="comma list of steps at which to save and exit 85")
    ap.add_argument("--max-voluntary-exits", type=int, default=0,
                    help="stop doing voluntary exits after this many in the same sandbox (0 = no limit)")
    ap.add_argument("--periodic-every", type=int, default=0, help="save (without exiting) every N steps")
    ap.add_argument("--on-sigterm", choices=["save85", "save0", "default", "ignore"], default="save85",
                    help="what to do on the first watched signal")
    ap.add_argument("--save-seconds", type=float, default=0, help="extra artificial time spent inside each save")
    ap.add_argument("--ckpt-mb", type=int, default=1, help="payload size written into each checkpoint")
    ap.add_argument("--ckpt-files", type=int, default=1, help="number of payload files per checkpoint")
    ap.add_argument("--empty-checkpoint", action="store_true", help="exit 85 with an empty checkpoint dir (P8d)")
    ap.add_argument("--children", type=int, default=0, help="child processes to start (P7)")
    ap.add_argument("--heartbeat-dir", default="", help="also write a 1 s heartbeat file here (e.g. on /staging)")
    ap.add_argument("--heartbeat-every", type=float, default=10, help="seconds between 'tick' events on stdout")
    ap.add_argument("--exit-on-restart", action="store_true",
                    help="exit 0 at once if the job was rescheduled into a new sandbox (ends a test after its eviction). "
                         "Needs a spooled checkpoint, so combine with an early --voluntary-exit-at")
    ap.add_argument("--stop-file", default="", help="treat the appearance of this file like a stop signal (P7h)")
    ap.add_argument("--restart-file", default="", help="append to this file when exiting 85 (P7h)")
    ap.add_argument("--staging-dir", default="", help="fingerprint: directory to test for existence/writability")
    ap.add_argument("--bench-targets", default=".", help="bench: comma list of directories")
    ap.add_argument("--bench-mb", default="100,1000", help="bench: comma list of sizes in MB")
    ap.add_argument("--bench-files", default="1,64", help="bench: comma list of file counts")
    args = ap.parse_args()

    for s in WATCHED_SIGNALS:
        signal.signal(s, on_signal)

    log = Log(args.test, args.job_id)
    os.makedirs("out", exist_ok=True)

    marker = load_marker()
    marker_survived = marker is not None
    if marker is None:
        marker = {"created_by": EXEC_ID, "host": HOST, "t": time.time(), "starts": []}
    previous_starts = list(marker.get("starts", []))
    marker["starts"].append({"exec": EXEC_ID, "host": HOST, "t": time.time()})
    save_marker(marker)

    job_ad_path = os.environ.get("_CONDOR_JOB_AD")
    job_ad = read_classad_file(job_ad_path)
    ad_fields = {}
    if job_ad:
        for k in ("NumJobStarts", "NumShadowStarts", "JobCurrentStartDate", "JobStartDate",
                  "ClusterId", "ProcId", "CommittedTime", "KillSig", "JobMaxVacateTime"):
            if k in job_ad:
                ad_fields[k] = job_ad[k]
        try:
            ad_fields["job_ad_mtime"] = os.path.getmtime(job_ad_path)
        except OSError:
            pass

    log.event("start", mode=args.mode, argv=sys.argv[1:], cwd=os.getcwd(),
              scratch_dir=os.environ.get("_CONDOR_SCRATCH_DIR"),
              sandbox_marker_survived=marker_survived, sandbox_created_by=marker.get("created_by"),
              previous_starts_in_sandbox=len(previous_starts), job_ad=ad_fields,
              signal_masks=proc_signal_masks(), ppid=os.getppid(), python=platform.python_version())

    if args.mode == "fingerprint":
        code = mode_fingerprint(args, log)
    elif args.mode == "bench":
        code = mode_bench(args, log)
    else:
        code = mode_run(args, log, marker, job_ad)
    sys.stdout.flush()
    sys.exit(code)


if __name__ == "__main__":
    main()
