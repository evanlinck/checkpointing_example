#!/usr/bin/env python3
"""
Local tests for recipe 1, on CPU, with a tiny model and made-up token data (no download,
no GPU). About four minutes.

    python3 test_local.py        # writes resume_equivalence.png if matplotlib is installed

1. Resume equivalence, checkpoint_at=interval: a run stopped with SIGTERM several times
   logs exactly the same losses as an uninterrupted run.
2. The same for checkpoint_at=epoch, where a stop mid-epoch saves nothing and the
   restart redoes the epoch.
3. Timed checkpoints: interval mode saves mid-epoch; epoch mode waits for the epoch end.
4. A damaged newest checkpoint: resume falls back to the previous one.
5. Backups: a "resubmitted" job (empty sandbox) resumes from the backup directory.
6. Config changes: a different model shape is refused; other changes only warn.
"""
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
TINY = ["n_layer=2", "n_head=2", "n_embd=64", "block_size=32", "batch_size=8", "epochs=3",
        "compile=false", "deterministic=true", "sample_stories=false", "eval_every_steps=0",
        "eval_batches=2", "log_every=1", "warmup_steps=10", "dropout=0.1"]
STEPS_PER_EPOCH = None  # filled in by make_data


def make_data(d):
    """Made-up tokens with some structure (so the loss goes down)."""
    global STEPS_PER_EPOCH
    rng = np.random.default_rng(0)
    base = rng.integers(0, 2000, size=64)
    toks = np.concatenate([np.roll(base, k) for k in range(700)]).astype(np.uint16)  # 44,800 tokens
    toks.tofile(os.path.join(d, "train.bin"))
    toks[:4000].tofile(os.path.join(d, "val.bin"))
    STEPS_PER_EPOCH = ((len(toks) - 1) // 32) // 8


def run(work, data, sets=(), kill_after=None, kill_at_step=None, resume="auto"):
    """Run train.py in `work`. Send SIGTERM kill_after seconds after training starts, or as
    soon as it logs step kill_at_step (deterministic, whatever the machine's speed)."""
    args = [sys.executable, os.path.join(HERE, "train.py"), "--config", os.path.join(HERE, "config.yaml"),
            "--resume", resume]
    for s in TINY + ["data_dir=" + data, "ckpt_dir=checkpoints", "out_dir=outputs"] + list(sets):
        args += ["--set", s]
    p = subprocess.Popen(args, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    head = ""
    if kill_at_step is not None:
        while True:
            line = p.stdout.readline()
            head += line
            m = re.match(r"step (\d+) ", line)
            if not line or (m and int(m.group(1)) >= kill_at_step):
                break
        p.send_signal(signal.SIGTERM)
    elif kill_after is not None:
        while True:  # wait until training has started (imports take a moment)
            line = p.stdout.readline()
            head += line
            if not line or line.startswith(("STARTING", "RESUMED")):
                break
        time.sleep(kill_after)
        p.send_signal(signal.SIGTERM)  # what HTCondor does on a vacate
    out = head + p.communicate()[0]
    return p.returncode, out


def losses(work):
    """Training loss per step from outputs/metrics.jsonl. If a step was trained twice
    (epoch mode redoes an interrupted epoch), the last time counts."""
    result = {}
    with open(os.path.join(work, "outputs", "metrics.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "train":
                result[e["step"]] = e["loss"]
    return result


def check(cond, msg, out=""):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        print(out[-3000:])
        sys.exit(1)


def fresh(tmp, name):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    return d


def equivalence(tmp, data, mode, reference):
    work = fresh(tmp, "interrupted_" + mode)
    sets = ["checkpoint_at=" + mode]
    if mode == "interval":   # four stops at random steps, mostly mid-epoch
        random.seed(1)
        targets = sorted(random.sample(range(20, 3 * STEPS_PER_EPOCH - 20, 7), 4))
    else:                    # mid-epoch 1; mid-epoch 2 (epoch 1 saved); mid-epoch 3 (epoch 2 saved)
        targets = [100, 250, 420]
    stops = []
    for i, target in enumerate(targets):
        rc, out = run(work, data, sets, kill_at_step=target)
        check(rc == 85, "%s mode, SIGTERM #%d: exits 85" % (mode, i + 1), out)
        if mode == "interval":
            m = re.search(r"SAVED step (\d+) \(reason: signal\)", out)
            check(m is not None, "interval mode, SIGTERM #%d: saved after the signal" % (i + 1), out)
            stops.append(int(m.group(1)))
        else:
            check("epoch mode: not saving mid-epoch" in out or "reason: signal" in out,
                  "epoch mode, SIGTERM #%d: no mid-epoch save" % (i + 1), out)
            last = [int(s) for s in re.findall(r"^step (\d+) ", out, re.M)]
            stops.append(last[-1] if last else 0)
    rc, out = run(work, data, sets)
    check(rc == 0 and "DONE" in out, "%s mode: the final run finishes" % mode, out)
    if mode == "interval":
        check(any(s % STEPS_PER_EPOCH for s in stops), "interval mode: at least one stop mid-epoch (%s)" % stops)
    got = losses(work)
    if mode == "epoch":  # the last stop was mid-epoch 3, so the final run redoes epoch 3 from its start
        check("RESUMED from step %d " % (2 * STEPS_PER_EPOCH) in out,
              "epoch mode: the final run resumed from the end of epoch 2 (step %d)" % (2 * STEPS_PER_EPOCH), out)
    check(got == reference, "%s mode: losses identical at all %d steps after %d interruptions"
          % (mode, len(reference), len(stops)))
    return got, stops


def main():
    tmp = tempfile.mkdtemp(prefix="recipe1-test-")
    try:
        data = fresh(tmp, "data")
        make_data(data)

        ref = fresh(tmp, "reference")
        rc, out = run(ref, data, resume="none")
        check(rc == 0 and "DONE" in out, "uninterrupted run finishes", out)
        reference = losses(ref)
        check(len(reference) == 3 * STEPS_PER_EPOCH, "reference logged every step (%d)" % len(reference))

        curves = {m: equivalence(tmp, data, m, reference) for m in ("interval", "epoch")}

        # 3. timed checkpoints
        w = fresh(tmp, "timed_interval")
        rc, out = run(w, data, ["max_runtime_seconds=1", "step_delay=0.01"])
        m = re.search(r"SAVED step (\d+) \(reason: timed\)", out)
        check(rc == 85 and m and int(m.group(1)) % STEPS_PER_EPOCH != 0,
              "interval mode: the timed checkpoint is saved mid-epoch (step %s)" % (m.group(1) if m else "?"), out)
        w = fresh(tmp, "timed_epoch")
        rc, out = run(w, data, ["max_runtime_seconds=1", "step_delay=0.01", "checkpoint_at=epoch"])
        m = re.search(r"SAVED step (\d+) \(reason: timed\)", out)
        check(rc == 85 and m and int(m.group(1)) % STEPS_PER_EPOCH == 0,
              "epoch mode: the timed checkpoint waits for the epoch end (step %s)" % (m.group(1) if m else "?"), out)
        rc, out = run(w, data, ["checkpoint_at=epoch"])
        check(rc == 0 and "saved because: timed" in out, "epoch mode: resumes from the timed checkpoint", out)

        # 4. damaged newest checkpoint -> previous one
        w = fresh(tmp, "fallback")
        keep2 = ["keep_checkpoints=2", "step_delay=0.01"]
        rc1, out1 = run(w, data, keep2, kill_after=0.8)
        rc2, out2 = run(w, data, keep2, kill_after=0.8)
        steps = sorted(int(n.split("_")[1]) for n in os.listdir(os.path.join(w, "checkpoints")) if n.startswith("step_"))
        check(rc1 == 85 and rc2 == 85 and len(steps) == 2, "setup: two checkpoints kept (%s)" % steps, out2)
        newest = os.path.join(w, "checkpoints", "step_%08d" % steps[-1], "state.pt")
        with open(newest, "r+b") as f:
            f.truncate(100)                                   # damage the newest
        rc, out = run(w, data, ["keep_checkpoints=2"])
        check(rc == 0 and "WARNING: could not load checkpoint" in out and "RESUMED from step %d " % steps[0] in out,
              "a damaged newest checkpoint: warns and resumes from step %d" % steps[0], out)

        # 5. backups survive a "resubmit" (a new, empty sandbox)
        backups = os.path.join(tmp, "staging_backups")
        w1 = fresh(tmp, "sandbox_before_rm")
        rc, out = run(w1, data, ["max_runtime_seconds=1", "step_delay=0.01", "backup_dir=" + backups,
                                 "backup_every_hours=0"])
        check(rc == 85 and "BACKUP of step" in out, "a timed checkpoint is copied to the backup directory", out)
        w2 = fresh(tmp, "sandbox_after_resubmit")
        rc, out = run(w2, data, ["backup_dir=" + backups])
        check(rc == 0 and ("from " + backups) in out, "the resubmitted job resumes from the backup", out)

        # 6. config changes
        w = fresh(tmp, "config_change")
        run(w, data, ["step_delay=0.01"], kill_after=0.5)
        rc, out = run(w, data, ["n_layer=3"])
        check(rc != 0 and "model shape changed" in out, "a different model shape is refused", out)
        rc, out = run(w, data, ["epochs=4"])
        check(rc == 0 and "WARNING: setting changed since the checkpoint: epochs 3 -> 4" in out,
              "other config changes resume with a warning", out)

        plot(reference, curves)
        print("all tests passed")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def plot(reference, curves):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed: skipping resume_equivalence.png)")
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    steps = sorted(reference)
    for ax, (mode, (got, stops)) in zip(axes, curves.items()):
        ax.plot(steps, [reference[s] for s in steps], lw=3, color="#9ecae1", label="uninterrupted")
        ax.plot(steps, [got[s] for s in steps], lw=1, color="#08519c", label="stopped and resumed")
        for i, s in enumerate(stops):
            ax.axvline(s, color="#cb181d", ls="--", lw=1, label="SIGTERM" if i == 0 else None)
        for e in range(1, 3):
            ax.axvline(e * STEPS_PER_EPOCH, color="#999999", ls=":", lw=1, label="epoch end" if e == 1 else None)
        ax.set_title("checkpoint_at: %s" % mode)
        ax.set_xlabel("step")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("training loss")
    fig.suptitle("Resume equivalence: identical losses despite repeated SIGTERMs (tiny model, CPU)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "resume_equivalence.png"), dpi=120)
    print("wrote resume_equivalence.png")


if __name__ == "__main__":
    main()
