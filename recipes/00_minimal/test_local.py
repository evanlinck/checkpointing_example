#!/usr/bin/env python3
"""
Local tests for recipe 0. No HTCondor needed. Runs on CPU in about a minute.

    python test_local.py            # all tests; writes resume_equivalence.png if matplotlib is installed

1. Resume equivalence: an uninterrupted run and a run stopped with SIGTERM several
   times (and restarted each time) must log identical losses.
2. Timed exit: --max-runtime-seconds makes the job save and exit 85, and the rerun resumes.
3. Interrupted save: a half-written checkpoint.pt.tmp (what a kill -9 in the middle of
   a save leaves behind) is ignored, and the job resumes from the complete checkpoint.
"""
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = os.path.join(HERE, "train.py")
COMMON = ["--epochs", "2", "--log-every", "1"]  # 2 epochs x 313 steps


def run(workdir, extra=(), kill_after=None):
    """Run train.py in workdir. If kill_after is set, send SIGTERM after that many seconds."""
    p = subprocess.Popen([sys.executable, TRAIN] + COMMON + list(extra), cwd=workdir,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    head = ""
    if kill_after is not None:
        # Wait until training has started: importing torch takes a moment, and a SIGTERM
        # before the handler is installed would simply kill the process.
        while True:
            line = p.stdout.readline()
            head += line
            if not line or line.startswith(("STARTING", "RESUMED")):
                break
        time.sleep(kill_after)
        p.send_signal(signal.SIGTERM)  # what HTCondor does on a vacate
    out, _ = p.communicate()
    return p.returncode, head + out


def losses(out):
    return {int(m.group(1)): m.group(2) for m in re.finditer(r"^step (\d+) epoch \d+ loss (\S+)$", out, re.M)}


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        sys.exit(1)


def test_resume_equivalence(tmp):
    ref_dir, int_dir = os.path.join(tmp, "uninterrupted"), os.path.join(tmp, "interrupted")
    os.makedirs(ref_dir), os.makedirs(int_dir)
    rc, out = run(ref_dir)
    check(rc == 0, "uninterrupted run exits 0")
    reference = losses(out)

    interrupted, stops = {}, []
    random.seed(1)
    for i in range(4):  # 4 SIGTERMs at random moments, then let it finish
        rc, out = run(int_dir, ["--step-delay", "0.003"], kill_after=random.uniform(0.15, 0.4))
        check(rc == 85, "SIGTERM #%d: job saves and exits 85" % (i + 1))
        saved = re.search(r"SAVED step (\d+) \(reason: signal\)", out)
        check(saved is not None, "SIGTERM #%d: the save happened after the signal" % (i + 1))
        stops.append(int(saved.group(1)))
        interrupted.update(losses(out))
    rc, out = run(int_dir)
    check(rc == 0 and "RESUMED from step %d" % stops[-1] in out, "final run resumes from step %d and exits 0" % stops[-1])
    interrupted.update(losses(out))
    check(any(s % 313 for s in stops), "at least one stop was mid-epoch (stops at steps %s)" % stops)
    check(interrupted == reference,
          "losses identical at all %d steps (uninterrupted vs. %d interruptions)" % (len(reference), len(stops)))
    plot(reference, interrupted, stops)


def test_timed_exit(tmp):
    d = os.path.join(tmp, "timed")
    os.makedirs(d)
    rc, out = run(d, ["--max-runtime-seconds", "0.5", "--step-delay", "0.003"])
    check(rc == 85 and "reason: timed" in out, "runtime limit: saves and exits 85")
    rc, out = run(d)
    check(rc == 0 and "saved because: timed" in out, "rerun resumes from the timed checkpoint and finishes")


def test_interrupted_save(tmp):
    d = os.path.join(tmp, "halfsave")
    os.makedirs(d)
    rc, out = run(d, ["--step-delay", "0.003"], kill_after=0.5)
    check(rc == 85, "setup: a first checkpoint exists")
    saved_step = int(re.search(r"SAVED step (\d+)", out).group(1))
    # Simulate kill -9 in the middle of the next save: a half-written checkpoint.pt.tmp.
    with open(os.path.join(d, "checkpoints", "checkpoint.pt.tmp"), "wb") as f:
        f.write(b"\0" * 1000)
    rc, out = run(d)
    check(rc == 0 and "RESUMED from step %d" % saved_step in out,
          "the half-written .tmp file is ignored: resumes from the complete checkpoint (step %d)" % saved_step)


def plot(reference, interrupted, stops):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed: skipping resume_equivalence.png)")
        return
    steps = sorted(reference)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(steps, [float(reference[s]) for s in steps], lw=3, color="#9ecae1", label="uninterrupted")
    ax.plot(steps, [float(interrupted[s]) for s in steps], lw=1, color="#08519c", label="stopped and resumed")
    for i, s in enumerate(stops):
        ax.axvline(s, color="#cb181d", ls="--", lw=1, label="SIGTERM → save → exit 85" if i == 0 else None)
    ax.set_xlabel("step")
    ax.set_ylabel("training loss")
    ax.set_title("Resume equivalence: identical losses after %d interruptions" % len(stops))
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "resume_equivalence.png"), dpi=120)
    print("wrote resume_equivalence.png")


if __name__ == "__main__":
    tmp = tempfile.mkdtemp(prefix="recipe0-test-")
    try:
        test_resume_equivalence(tmp)
        test_timed_exit(tmp)
        test_interrupted_save(tmp)
        print("all tests passed")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
