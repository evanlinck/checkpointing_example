#!/usr/bin/env python3
"""
analyze.py - turn one probe job's outputs into a short, readable answer.

Per test (run automatically as the DAG node's POST script):
    analyze.py --test-dir runs/<tag>/<site>/<test> [--job-id 1234.0]
Writes results/<tag>/<site>/<test>.md (and .json).

For a whole run (the DAG's FINAL node, or by hand):
    analyze.py --summary --run-dir runs/<tag>
Writes results/<tag>/summary.md.

Sources it combines (any may be missing):
  meta.json         which test, which question
  job.log           HTCondor's event log (AP clock)
  job.out           probe JSON lines ("PROBE {...}") and wrapper lines (EP clock)
  ckpt/ or out/history.jsonl   probe events that travelled with the checkpoint
  /staging/.../     heartbeat.log and staging checkpoints, read directly on the AP
  trigger.jsonl     when the eviction was fired (AP clock)
  history_ad.txt    one condor_history -long lookup, made here, once per job

Times from the AP and the EP come from different clocks; they are normally
NTP-synced, but treat sub-second differences between them with care.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eventlog  # noqa: E402
from redact import redact  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NOISY = {"tick", "child_alive"}


def read_jsonl(path, prefix=None):
    out = []
    try:
        with open(path, errors="replace") as f:
            for line in f:
                line = line.strip()
                if prefix:
                    if not line.startswith(prefix):
                        continue
                    line = line[len(prefix):]
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def submit_macro(job_dir, name, _depth=0):
    """Value of a simple `NAME = value` macro in job.sub, with $(OTHER) references expanded."""
    value = None
    try:
        with open(os.path.join(job_dir, "job.sub")) as f:
            for line in f:
                m = re.match(r"^\s*%s\s*=\s*(.*)$" % name, line)
                if m:
                    value = m.group(1).strip()  # last definition wins, as in condor_submit
    except OSError:
        pass
    if value and _depth < 5:
        value = re.sub(r"\$\((\w+)\)", lambda mm: submit_macro(job_dir, mm.group(1), _depth + 1) or mm.group(0), value)
    return value


def fetch_history_ad(job_dir, job_id):
    """One condor_history call per job, after it has left the queue. Cached in history_ad.txt.

    Right after a job ends (when the DAG's POST script runs) the schedd may not have
    written the history record yet, so an empty result is retried on the next call
    (the FINAL summary node), but never more than once per call.
    """
    path = os.path.join(job_dir, "history_ad.txt")
    if not job_id:
        return path
    if os.path.exists(path) and read_ad(path):
        return path
    try:
        p = subprocess.Popen(["condor_history", "-limit", "1", "-long", job_id],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = p.communicate(timeout=120)
        with open(path, "wb") as f:
            f.write(out)
    except Exception as e:
        with open(path, "w") as f:
            f.write("# condor_history failed: %s\n" % e)
    return path


def read_ad(path):
    ad = {}
    try:
        with open(path, errors="replace") as f:
            for line in f:
                if " = " in line:
                    k, v = line.split(" = ", 1)
                    ad[k.strip()] = v.strip().strip('"')
    except OSError:
        pass
    return ad


def fmt_t(t):
    return time.strftime("%H:%M:%S", time.localtime(t)) + ("%.1f" % (t % 1))[1:] if t else "?"


def analyze_test(job_dir, job_id=None):
    meta = {}
    try:
        with open(os.path.join(job_dir, "meta.json")) as f:
            meta = json.load(f)
    except (OSError, ValueError):
        meta = {"test": os.path.basename(job_dir), "site": os.path.basename(os.path.dirname(job_dir))}

    # ---- collect --------------------------------------------------------
    events = eventlog.read_events(os.path.join(job_dir, "job.log"))
    job = job_id or eventlog.latest_job_id(events)
    events = eventlog.for_job(events, job) if job else events

    stdout_recs = read_jsonl(os.path.join(job_dir, "job.out"), prefix="PROBE ")
    recs = list(stdout_recs)
    staging_runs = submit_macro(job_dir, "STAGING_RUNS")
    staging_job_dir = os.path.join(staging_runs, job) if (staging_runs and job) else None
    for p in [os.path.join(job_dir, "ckpt", "history.jsonl"), os.path.join(job_dir, "out", "history.jsonl")] + \
            ([os.path.join(staging_job_dir, "ckpt", "history.jsonl")] if staging_job_dir else []):
        recs += read_jsonl(p)
    seen, merged = set(), []
    for r in recs:
        key = (r.get("exec"), r.get("pid"), r.get("t"), r.get("event"))
        if key not in seen:
            seen.add(key)
            merged.append(r)
    recs = sorted(merged, key=lambda r: r.get("t", 0))

    heartbeats = {}  # exec -> last heartbeat time (from the /staging file, survives SIGKILL)
    if staging_job_dir:
        try:
            with open(os.path.join(staging_job_dir, "heartbeat.log")) as f:
                for line in f:
                    m = re.match(r"^([\d.]+) .*exec=(\w+)", line)
                    if m:
                        heartbeats[m.group(2)] = max(heartbeats.get(m.group(2), 0), float(m.group(1)))
        except OSError:
            pass

    wrapper_lines = []
    try:
        with open(os.path.join(job_dir, "job.out"), errors="replace") as f:
            wrapper_lines = [l.strip() for l in f if l.startswith("WRAPPER")]
    except OSError:
        pass

    err_tail = []
    try:
        with open(os.path.join(job_dir, "job.err"), errors="replace") as f:
            err_tail = [l.rstrip() for l in f.readlines()[-25:]]
    except OSError:
        pass

    trig = read_jsonl(os.path.join(job_dir, "trigger.jsonl"))
    fired = [r for r in trig if r.get("action") == "firing"]
    t_fire = fired[0]["t"] if fired else None

    hist_ad = read_ad(fetch_history_ad(job_dir, job)) if job else {}

    # ---- executions (one per process start of the main probe) -----------
    execs = []
    for r in recs:
        if r.get("event") == "start" and "-c" not in str(r.get("exec")):
            ex = {"exec": r["exec"], "t": r["t"], "host": r.get("host"), "rank": r.get("rank"),
                  "scratch": r.get("scratch_dir"), "marker": r.get("sandbox_marker_survived"),
                  "prev_starts": r.get("previous_starts_in_sandbox"),
                  "NumJobStarts": (r.get("job_ad") or {}).get("NumJobStarts")}
            mine = [x for x in recs if x.get("exec") == r["exec"]]
            rest = [x for x in mine if x.get("event") == "restore"]
            if rest:
                ex["restored_step"] = rest[0].get("step") if rest[0].get("found") else None
                ex["restored_reason"] = rest[0].get("saved_reason")
                ex["stale_tmp"] = rest[0].get("stale_tmp")
                ex["nested_ok"] = rest[0].get("nested_dir_ok")
            sigs = [x for x in mine if x.get("event") == "signal"]
            if sigs:
                ex["signal"] = sigs[0].get("signal")
                ex["signal_t"] = sigs[0].get("received_at")
                ex["n_signals"] = len(sigs)
            saves = [x for x in mine if x.get("event") == "save_done"]
            ex["saves"] = [(s.get("step"), s.get("reason"), s.get("seconds")) for s in saves]
            exits = [x for x in mine if x.get("event") == "exit"]
            if exits:
                ex["exit_code"] = exits[-1].get("code")
                ex["exit_t"] = exits[-1].get("t")
            ex["last_seen"] = max([x.get("t", 0) for x in mine] + [heartbeats.get(r["exec"], 0)])
            execs.append(ex)

    # ---- observations -----------------------------------------------------
    obs = []
    terminal = [e for e in events if e["name"] in ("terminated", "aborted", "held")]
    if meta.get("dry_run_rc") not in (None, 0):
        obs.append("condor_submit -dry-run REJECTED the submit file: %s"
                   % (meta.get("dry_run_output", "").strip().splitlines() or [""])[-1])
    if terminal:
        last = terminal[-1]
        detail = "; ".join(b for b in last["body"] if b)[:200]
        obs.append("Final job state: %s %s" % (last["name"], ("(" + detail + ")") if detail else ""))
    elif not events:
        obs.append("No HTCondor events found for this job (not submitted, or job.log missing).")

    n_exec_events = len([e for e in events if e["name"] == "executing"])
    obs.append("Executions seen by the probe: %d; 'executing' events in job.log: %d (an exit-85 restart "
               "in the same sandbox does not log one); NumJobStarts=%s, NumShadowStarts=%s (condor_history)."
               % (len(execs), n_exec_events, hist_ad.get("NumJobStarts", "?"), hist_ad.get("NumShadowStarts", "?")))

    for prev, cur in zip(execs, execs[1:]):
        how = "exit %s" % prev.get("exit_code") if "exit_code" in prev else (
            "killed (signal %s, no exit recorded)" % prev.get("signal") if prev.get("signal") else "ended without an exit record")
        gap = cur["t"] - (prev.get("exit_t") or prev["last_seen"])
        obs.append("Restart after %s: gap %.0f s, %s host, sandbox %s, restored step %s (saved by: %s)%s."
                   % (how, gap, "same" if cur["host"] == prev["host"] else "DIFFERENT",
                      "kept (marker file survived)" if cur.get("marker") else "NEW",
                      cur.get("restored_step"), cur.get("restored_reason"),
                      ", stale .tmp found: %s" % cur["stale_tmp"] if cur.get("stale_tmp") else ""))

    if t_fire:
        obs.append("Trigger %s fired at %s (AP clock)." % (meta.get("trigger", {}).get("action"), fmt_t(t_fire)))
        # The execution running at t_fire: the last one started before it, unless that one
        # had already exited on its own. (Its last *logged* moment can be up to one tick
        # interval before a hard kill, so last_seen is not a reliable upper bound.)
        started = [ex for ex in execs if ex["t"] <= t_fire]
        hit = [started[-1]] if started and not (started[-1].get("exit_t") and started[-1]["exit_t"] < t_fire - 1) else []
        if hit:
            ex = hit[-1]
            if ex.get("signal"):
                obs.append("Evicted execution received %s %.1f s after the trigger (includes any retirement time "
                           "and AP/EP clock offset); %d signal(s) total."
                           % (ex["signal"], ex["signal_t"] - t_fire, ex.get("n_signals", 1)))
                if "exit_code" not in ex:
                    obs.append("It never exited on its own: last sign of life %.1f s after the signal "
                               "= effective grace before SIGKILL." % (ex["last_seen"] - ex["signal_t"]))
                else:
                    obs.append("It exited with code %s, %.1f s after the signal." % (ex["exit_code"], ex["exit_t"] - ex["signal_t"]))
            else:
                obs.append("Evicted execution logged NO signal (hard kill, or signal not delivered); its last "
                           "logged moment was %+.1f s relative to the trigger (logging is every 1-10 s, so a "
                           "negative value is normal for an immediate kill)." % (ex["last_seen"] - t_fire))
            sig_saves = [s for s in ex["saves"] if s[1] == "signal"]
            after = [x for x in execs if x["t"] > ex["t"]]
            if after:
                nxt = after[0]
                verdict = ""
                if sig_saves:
                    verdict = (" -> the SIGTERM save (step %s) SURVIVED" % sig_saves[0][0]
                               if nxt.get("restored_step") == sig_saves[0][0]
                               else " -> the SIGTERM save (step %s) was LOST" % sig_saves[0][0])
                obs.append("Next execution restored step %s (saved by: %s)%s."
                           % (nxt.get("restored_step"), nxt.get("restored_reason"), verdict))
            else:
                obs.append("No later execution was observed.")
        else:
            obs.append("The trigger fired while no probe execution was running.")
    elif meta.get("trigger"):
        reason = [r for r in trig if r.get("action") == "gave_up"]
        obs.append("Trigger did not fire%s." % (": " + reason[-1].get("reason", "") if reason else " (no trigger.jsonl)"))

    if stdout_recs and execs:
        in_stdout = set(r.get("exec") for r in stdout_recs if r.get("event") == "start")
        obs.append("job.out contains output from %d of %d executions (tells whether stdout is kept across restarts)."
                   % (len([e for e in execs if e["exec"] in in_stdout]), len(execs)))

    # Process tree (P7)
    child_sigs = [r for r in recs if r.get("event") == "signal" and r.get("role") == "child"]
    child_exits = [r for r in recs if r.get("event") == "child_exit_seen"]
    if any(r.get("event") == "child_start" for r in recs):
        obs.append("Children that received a signal directly: %s; child exits seen by parent: %s."
                   % (sorted(set((r.get("child"), r.get("signal")) for r in child_sigs)) or "none",
                      [(r.get("child"), r.get("exitcode")) for r in child_exits] or "none"))
    ranks = sorted(set(r.get("rank") for r in recs if r.get("rank") is not None))
    if ranks:
        for rk in ranks:
            s = [r for r in recs if r.get("rank") == rk and r.get("event") == "signal"]
            e = [r for r in recs if r.get("rank") == rk and r.get("event") == "exit"]
            obs.append("torchrun rank %s: signal=%s, exit=%s" % (rk, s[0].get("signal") if s else None, e[-1].get("code") if e else None))
    if any("Traceback" in l or "Error" in l for l in err_tail):
        obs.append("job.err shows an error (see 'job.err (last lines)' below): "
                   + next(l for l in reversed(err_tail) if l.strip())[:200])
    if wrapper_lines:
        obs.append("Wrapper said: " + " | ".join(wrapper_lines)[:400])

    # Bench (P5a/b)
    bench = [r for r in recs if r.get("event") in ("bench", "bench_error")]
    for b in bench:
        if b["event"] == "bench":
            obs.append("bench %s: %d MB in %d file(s): write+fsync %.2f s (%.0f MB/s), rename %.3f s"
                       % (b["target"], b["mb"], b["files"], b["write_seconds"], b["mb_per_s"], b["rename_seconds"]))
        else:
            obs.append("bench %s %s MB: ERROR %s" % (b.get("target"), b.get("mb"), b.get("error")))

    # Fingerprint (P0)
    fp_path = os.path.join(job_dir, "out", "fingerprint.json")
    if os.path.exists(fp_path):
        with open(fp_path) as f:
            fp = json.load(f)
        mad = fp.get("machine_ad") or {}
        obs.append("Python %s; container: %s; scratch free %s GB."
                   % (fp.get("python", "?").split()[0], fp.get("container"), fp.get("scratch_free_gb")))
        obs.append("Machine ad: " + ", ".join("%s=%s" % (k, v) for k, v in sorted(mad.items())
                                              if re.search(r"Vacate|Retire|Backfill|Version|Staging|Pool|Site|CUDADeviceName|OpSysAndVer", k))[:900])
        obs.append("Paths: %s" % json.dumps(fp.get("paths")))
        obs.append("Internet: %s" % ", ".join("%s=%s" % (u.split("/")[2], v.get("ok")) for u, v in fp.get("internet", {}).items()))
        obs.append("condor_chirp: %s; chirp test: %s" % (fp.get("tools", {}).get("condor_chirp") or fp.get("tools", {}).get("condor_chirp_libexec"),
                                                       (fp.get("chirp_test") or {}).get("rc", "not run")))
        obs.append("Inherited signal masks: %s" % fp.get("signal_masks"))

    selected_ad = {k: v for k, v in hist_ad.items()
                   if re.search(r"^Num|Committed|WallClock|^Exit|Hold|Checkpoint|Ckpt|Vacate|Evict|LastRemoteHost|KillSig|TransferOut|TransferIn.*Time", k)}

    # ---- write -----------------------------------------------------------
    tag = meta.get("tag") or os.path.basename(os.path.dirname(os.path.dirname(job_dir)))
    out_dir = os.path.join(HERE, "results", tag, meta.get("site", "unknown"))
    os.makedirs(out_dir, exist_ok=True)
    md = ["# %s on %s" % (meta.get("test"), meta.get("site")), "",
          "**Question.** %s" % meta.get("question", ""), "",
          "Job: `%s`   Test dir: `%s`" % (job, job_dir), "", "## Observations", ""]
    md += ["- " + o for o in obs]
    md += ["", "## Executions", "",
           "| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |",
           "|---|---|---|---|---|---|---|---|---|"]
    for ex in execs:
        md.append("| %s | %s | %s | %s | %s | %s (%s) | %s | %s | %s |" % (
            ex["exec"], fmt_t(ex["t"]), ex["host"], ex.get("marker"), ex.get("NumJobStarts"),
            ex.get("restored_step"), ex.get("restored_reason"), ex.get("signal", ""),
            ex["saves"], ex.get("exit_code", "none (killed?)")))
    md += ["", "## HTCondor event log (AP clock)", ""]
    for e in events:
        if e["name"] == "image_size":
            continue
        body = "; ".join(b for b in e["body"] if b and not b.startswith(("Usage", "Request", "Allocated", "Partitionable", "Resources")))
        md.append("- %s `%03d %s` %s %s" % (fmt_t(e["t"]), e["code"], e["name"], e["text"][:120], ("— " + body[:300]) if body else ""))
    if selected_ad:
        md += ["", "## condor_history (selected)", "", "```"] + ["%s = %s" % kv for kv in sorted(selected_ad.items())] + ["```"]
    if err_tail:
        md += ["", "## job.err (last lines)", "", "```"] + err_tail + ["```"]
    md += ["", "## Probe timeline (EP clock; ticks omitted)", "", "```"]
    for r in recs:
        if r.get("event") in NOISY:
            continue
        extra = {k: v for k, v in r.items() if k not in ("t", "event", "test", "job", "host", "exec", "pid", "argv",
                                                          "job_ad", "signal_masks", "listing", "env", "ancestry")}
        md.append("%s %-8s %-22s %s" % (fmt_t(r.get("t")), r.get("exec"), r.get("event"), json.dumps(extra, default=str)[:300]))
    md += ["```", ""]
    if trig:
        md += ["## Trigger log (AP clock)", "", "```"] + \
              ["%s %s" % (fmt_t(r.get("t")), json.dumps({k: v for k, v in r.items() if k != "t"})[:300]) for r in trig] + ["```", ""]

    name = meta.get("test", os.path.basename(job_dir))
    # Reports are meant to be shared: strip user names, personal paths and IP addresses.
    with open(os.path.join(out_dir, name + ".md"), "w") as f:
        f.write(redact("\n".join(md)))
    with open(os.path.join(out_dir, name + ".json"), "w") as f:
        f.write(redact(json.dumps({"meta": meta, "job": job, "observations": obs, "executions": execs},
                                  indent=2, default=str)))
    return os.path.join(out_dir, name + ".md")


def summary(run_dir):
    tag = os.path.basename(os.path.normpath(run_dir))
    res_root = os.path.join(HERE, "results", tag)
    # Re-analyze every test: this fills in tests that never ran (e.g. rejected), and
    # retries condor_history for jobs whose record was not yet written at POST time.
    for meta_path in sorted(glob.glob(os.path.join(run_dir, "*", "*", "meta.json"))):
        analyze_test(os.path.dirname(meta_path))
    md = ["# Probe results: %s" % tag, "",
          "Generated %s. Per-test details are in the per-site folders." % time.strftime("%Y-%m-%d %H:%M"), ""]
    for site_dir in sorted(glob.glob(os.path.join(res_root, "*"))):
        if not os.path.isdir(site_dir):
            continue
        md += ["## %s" % os.path.basename(site_dir), ""]
        for jpath in sorted(glob.glob(os.path.join(site_dir, "*.json"))):
            with open(jpath) as f:
                d = json.load(f)
            md += ["### %s" % d["meta"].get("test"), "", "_%s_" % d["meta"].get("question", ""), ""]
            md += ["- " + o for o in d["observations"]] + [""]
    path = os.path.join(res_root, "summary.md")
    os.makedirs(res_root, exist_ok=True)
    with open(path, "w") as f:
        f.write(redact("\n".join(md)))
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--test-dir")
    ap.add_argument("--job-id", help="cluster.proc; DAGMan passes $JOBID")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--run-dir")
    args = ap.parse_args()
    try:
        if args.summary:
            print(summary(args.run_dir))
        else:
            job_id = args.job_id
            if job_id and re.match(r"^\d+\.\d+\.\d+$", job_id):  # DAGMan's $JOBID can be cluster.proc.subproc
                job_id = job_id.rsplit(".", 1)[0]
            print(analyze_test(os.path.abspath(args.test_dir), job_id))
    except Exception as e:  # never fail the DAG node because of analysis
        import traceback
        traceback.print_exc()
        print("analyze.py failed: %s" % e)
    sys.exit(0)


if __name__ == "__main__":
    main()
