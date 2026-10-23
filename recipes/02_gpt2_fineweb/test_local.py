#!/usr/bin/env python3
"""
Local tests for recipe 2, on CPU, with a tiny model and made-up token shards (no download,
no GPU).

    python3 test_local.py          # one process: ~2 minutes
    python3 test_local.py --ddp    # also the multi-process tests (2 ranks under torchrun): ~5 more minutes

One process:
1. Resume equivalence: a run stopped by SIGTERM several times (at step boundaries and at
   random moments, which can fall between micro-batches) logs exactly the same losses as
   an uninterrupted run.
2. The timed exit: saves with reason "timed", exits 85, and the rerun resumes.
3. The data position: a shard too small for a whole step is skipped; a run crosses shards
   and passes.

Multi-process (--ddp), the way HTCondor runs the job: launch.py -> torchrun -> 2 workers,
with SIGTERM sent to launch.py only.
4. Both ranks stop at the same step, rank 0 saves, the job exits 85, and the resumed
   run finishes. Its losses match the uninterrupted 2-rank run's exactly.
5. 2 ranks vs. 1 process with the same global batch: the same losses within a small
   tolerance (the gradients are summed in a different order).
6. A save that takes 40 s: under launch.py it completes (exit 85). Under plain torchrun
   the workers are killed after torchrun's 30 s grace, and torchrun exits 1, not 85.
7. Resuming on a different number of ranks: warns and continues at the same step.
"""
import argparse
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
# Tiny GPT and batches: 16 sequences of 32 tokens per step (512 tokens).
TINY = ["n_layer=2", "n_head=2", "n_embd=64", "block_size=32", "total_batch_tokens=512", "micro_batch=4",
        "compile=false", "deterministic=true", "eval_every_steps=20", "eval_sequences=16", "log_every=1",
        "warmup_steps=10", "save_every_minutes=0", "max_runtime_seconds=100000"]
STEP_TOKENS = 512


def make_data(d):
    """Made-up shards with some structure (so the loss goes down), in prepare_data.py's layout:
    2 "input files" of 3 shards each, the last one too small for a whole step, plus val."""
    os.makedirs(d)
    rng = np.random.default_rng(0)
    base = rng.integers(0, 2000, size=64)

    def tokens(n, shift):
        return np.concatenate([np.roll(base, k + shift) for k in range(n // 64 + 1)])[:n].astype(np.uint16)

    files = {}
    for f in range(2):
        shards = []
        for k, n in enumerate([12000, 9000, 300]):           # 300 tokens: under one step (16 x 32 + 1)
            name = "train_f%02d_%03d.npy" % (f, k)
            np.save(os.path.join(d, name), tokens(n, 7 * f + k))
            shards.append([name, n])
        files["sample/10BT/%03d_00000.parquet" % f] = {"shards": shards, "documents": 0, "tokens": 0}
    np.save(os.path.join(d, "val_000.npy"), tokens(4000, 3))
    with open(os.path.join(d, "manifest.json"), "w") as fh:
        json.dump({"files": files, "val": [["val_000.npy", 4000]], "complete": True}, fh)
    # steps per pass: each full shard holds (n - 1) // 32 sequences, // 16 per step
    return sum(((n - 1) // 32) // 16 for n in (12000, 9000, 300)) * 2


def train_args(work, data, sets):
    args = ["--config", os.path.join(HERE, "config.yaml"), "--resume", "auto"]
    for s in TINY + ["data_dir=" + data, "ckpt_dir=" + os.path.join(work, "ckpt"),
                     "out_dir=" + os.path.join(work, "out")] + list(sets):
        args += ["--set", s]
    return args


def env():
    e = dict(os.environ, PYTHONPATH=ROOT + os.pathsep + os.environ.get("PYTHONPATH", ""), OMP_NUM_THREADS="1")
    e.pop("HTCONDOR_CKPT_STOP_FILE", None)
    e.pop("HTCONDOR_CKPT_RESTART_FILE", None)
    if sys.platform == "darwin":
        # The CPU backend (gloo) also connects through the host name unless told which
        # network interface to use: on a Mac, the loopback interface.
        e.setdefault("GLOO_SOCKET_IFNAME", "lo0")
    return e


def run(cmd, work, kill_at_step=None, kill_after=None):
    """Run cmd in `work`. Send SIGTERM to it (the top process only, as HTCondor does) when it
    logs step kill_at_step, or kill_after seconds after training starts."""
    os.makedirs(work, exist_ok=True)
    p = subprocess.Popen(cmd, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env())
    out = ""
    if kill_at_step is not None or kill_after is not None:
        while True:
            line = p.stdout.readline()
            out += line
            if not line:
                break
            m = re.match(r"step (\d+)/", line)
            if kill_at_step is not None and m and int(m.group(1)) >= kill_at_step:
                break
            if kill_after is not None and line.startswith(("STARTING", "RESUMED")):
                # Sleep, don't wait for output: the job prints at step boundaries, so a
                # signal sent right after a line would always land at a step boundary.
                time.sleep(kill_after)
                break
        p.send_signal(signal.SIGTERM)
    out += p.communicate()[0]
    return p.returncode, out


def one_process(work, data, sets=(), **kw):
    return run([sys.executable, os.path.join(HERE, "train.py")] + train_args(work, data, sets), work, **kw)


def free_port():
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def under_launcher(work, data, sets=(), nproc=2, wrapper=True, **kw):
    """launch.py -- torchrun --nproc_per_node=N train.py ..., as in job.sub.

    job.sub uses torchrun --standalone. Here we give torchrun an explicit local address
    instead: --standalone connects to the machine's host name, which on many laptops
    (macOS especially) doesn't resolve, and torchrun then waits 5 minutes and fails."""
    torchrun = [sys.executable, "-m", "torch.distributed.run", "--nnodes=1", "--nproc_per_node=%d" % nproc,
                "--master_addr=127.0.0.1", "--master_port=%d" % free_port(),
                os.path.join(HERE, "train.py")] + train_args(work, data, sets)
    cmd = [sys.executable, os.path.join(ROOT, "htcondor_ckpt", "launch.py"), "--"] + torchrun if wrapper else torchrun
    return run(cmd, work, **kw)


def losses(work):
    """Training loss per step from metrics.jsonl (a step trained twice: the last time counts)."""
    result = {}
    with open(os.path.join(work, "out", "metrics.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "train":
                result[e["step"]] = e["loss"]
    return result


def check(cond, msg, out=""):
    print(("PASS  " if cond else "FAIL  ") + msg, flush=True)
    if not cond:
        print(out[-4000:])
        sys.exit(1)


def single_process_tests(tmp, data, steps):
    ref = os.path.join(tmp, "reference")
    rc, out = one_process(ref, data)
    check(rc == 0 and "DONE" in out, "uninterrupted run finishes", out)
    reference = losses(ref)
    # By hand: 11,999 // 32 = 374 sequences = 23 steps; 8,999 // 32 = 281 = 17 steps; the 300-token
    # shard holds no whole step. Two input files: 2 x (23 + 17) = 80 steps.
    check(steps == 80 and len(reference) == 80, "it trained all 80 steps of the pass, skipping the tiny shards", out)

    # 1. resume equivalence: SIGTERMs at step boundaries, then at random moments
    work = os.path.join(tmp, "interrupted")
    random.seed(2)
    stops = []
    for i, target in enumerate((15, 38, 61)):   # spread over the run, across shard boundaries
        rc, out = one_process(work, data, kill_at_step=target)
        m = re.search(r"SAVED step (\d+) \(reason: signal\)", out)
        check(rc == 85 and m, "SIGTERM #%d (after step %d): saved with reason signal, exit 85" % (i + 1, target), out)
        stops.append(int(m.group(1)))
    rc, out = one_process(work, data)
    check(rc == 0 and "DONE" in out, "the final run finishes", out)
    check(losses(work) == reference, "losses identical at all %d steps after %d interruptions (stops at %s)"
          % (steps, len(stops), stops))

    # At random moments, in a run of their own (so there's always training left to interrupt),
    # until one falls between the micro-batches of a step, where most of a step's time goes:
    # that partial step must be discarded and redone after the resume.
    work = os.path.join(tmp, "interrupted_random")
    stops, mid_step = [], False
    for i in range(8):
        rc, out = one_process(work, data, kill_after=random.uniform(0.2, 0.8))
        if "DONE" in out:          # finished before the signal: a later signal can't matter
            break
        check(rc == 85 and "reason: signal" in out, "SIGTERM at a random moment #%d: saved, exit 85" % (i + 1), out)
        stops.append(int(re.search(r"SAVED step (\d+)", out).group(1)))
        if "between micro-batches" in out:
            mid_step = True
            break
    check(mid_step, "one of those SIGTERMs fell between micro-batches (the partial step was discarded)")
    rc, out = one_process(work, data)
    check(rc == 0 and "DONE" in out, "the final run finishes", out)
    check(losses(work) == reference, "losses identical again, after stops at %s" % stops)

    # 2. the timed exit
    work = os.path.join(tmp, "timed")
    rc, out = one_process(work, data, ["max_runtime_seconds=1", "step_delay=0.05"])
    check(rc == 85 and "SAVED" in out and "reason: timed" in out, "timed exit: saved (reason timed), exit 85", out)
    rc, out = one_process(work, data)
    check(rc == 0 and "saved because: timed" in out, "the rerun resumes from the timed checkpoint and finishes", out)
    check(losses(work) == reference, "and its losses match the uninterrupted run's")
    return reference


def ddp_tests(tmp, data, steps, reference_1proc):
    # 4. SIGTERM to launch.py only: both ranks stop at the same step
    ref2 = os.path.join(tmp, "ddp_reference")
    rc, out = under_launcher(ref2, data)
    check(rc == 0 and "DONE" in out, "2 ranks under launch.py + torchrun: uninterrupted run finishes", out)
    reference_2 = losses(ref2)
    work = os.path.join(tmp, "ddp_interrupted")
    for i, target in enumerate((20, 60)):
        rc, out = under_launcher(work, data, kill_at_step=target)
        stops = re.findall(r"\[rank (\d)\] stop: .*stopping at step (\d+)", out)
        same = len(stops) == 2 and len({s for _, s in stops}) == 1
        check(rc == 85 and same and "SAVED" in out,
              "SIGTERM #%d to launch.py: both ranks stopped at step %s, rank 0 saved, exit 85"
              % (i + 1, stops[0][1] if stops else "?"), out)
    rc, out = under_launcher(work, data)
    check(rc == 0 and "DONE" in out, "the resumed 2-rank run finishes", out)
    check(losses(work) == reference_2, "its losses match the uninterrupted 2-rank run's exactly")

    # 5. 2 ranks vs 1 process, same global batch
    common = sorted(set(reference_2) & set(reference_1proc))
    worst = max(abs(reference_2[s] - reference_1proc[s]) for s in common)
    check(worst < 1e-3, "2 ranks vs 1 process: largest loss difference %.2e over %d steps (tolerance 1e-3)"
          % (worst, len(common)))

    # 6. a 40 s save: completes under launch.py, killed under plain torchrun
    work = os.path.join(tmp, "slow_wrapper")
    rc, out = under_launcher(work, data, ["save_delay=40", "step_delay=0.05"], kill_at_step=10)
    check(rc == 85 and "SAVED" in out, "a 40 s save under launch.py: completed, exit 85", out)
    work = os.path.join(tmp, "slow_plain")
    rc, out = under_launcher(work, data, ["save_delay=40", "step_delay=0.05"], wrapper=False, kill_at_step=10)
    check(rc != 85 and "SAVED" not in out,
          "the same save under plain torchrun: cut off (no SAVED line) and exit %d, not 85" % rc, out)

    # 7. resume on a different number of ranks (2 -> 1)
    work = os.path.join(tmp, "world_change")
    rc, out = under_launcher(work, data, kill_at_step=30)
    saved = int(re.search(r"SAVED step (\d+)", out).group(1))
    rc, out = one_process(work, data)
    check(rc == 0 and "checkpoint was written by 2 GPUs, this run has 1" in out
          and "RESUMED from step %d " % saved in out,
          "resume 2 ranks -> 1: warns about the GPU count and continues from step %d" % saved, out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ddp", action="store_true", help="also run the multi-process tests (need torchrun)")
    args = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="recipe2-test-")
    try:
        data = os.path.join(tmp, "data")
        steps = make_data(data)
        reference = single_process_tests(tmp, data, steps)
        if args.ddp:
            ddp_tests(tmp, data, steps, reference)
        print("all tests passed" + ("" if args.ddp else " (one process; add --ddp for the multi-process tests)"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
