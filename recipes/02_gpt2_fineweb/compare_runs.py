#!/usr/bin/env python3
"""
Resume equivalence on a real GPU: compare the losses of a run that was stopped and resumed
with those of runs that never stopped.

    ./test_htcondor.sh reference                  # twice: two uninterrupted runs
    ./test_htcondor.sh vacate                     # timed exits plus one save after SIGTERM
    python3 compare_runs.py --reference <ref1 run dir>/outputs --reference <ref2 run dir>/outputs \\
                            --resumed <vacate run dir>/outputs --plot resume_equivalence_gpu.png

(The run directories are on /staging, under $RECIPE2_TEST_DIR; each test prints its own.)
Each argument is an outputs directory (or its metrics.jsonl). Only the standard library is
needed; the plot also needs matplotlib (or copy the outputs directories to your laptop).

Why two references? On a GPU, two runs of the same code with the same seed can differ a
little even with deterministic=true. Different GPU models (or driver/library versions) run
different kernels, and bf16 rounding differences grow as training goes on. The second
reference measures that "noise floor". A correct resume differs from a reference by no more
than the references differ from each other. A real checkpointing bug (a lost optimizer state,
a skipped or repeated batch, a reset learning rate) shows up as a jump right after a restart.
"""
import argparse
import json
import os
import sys


def load(path):
    """train loss and val loss per step, the GPU of each execution, and the restarts.
    A step trained twice (after a hard kill, the job redoes steps since its last checkpoint)
    counts the last time, as it does for the model."""
    if os.path.isdir(path):
        path = os.path.join(path, "metrics.jsonl")
    run = {"name": path, "train": {}, "val": {}, "gpus": [], "resumes": []}
    with open(path) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "train":
                run["train"][e["step"]] = e["loss"]
            elif e["event"] == "eval":
                run["val"][e["step"]] = e["val_loss"]
            elif e["event"] == "first_step":
                run["gpus"].append(e.get("gpu", "not logged (older train.py)"))
            elif e["event"] == "resumed":
                run["resumes"].append((e["step"], e["reason"]))
    if not run["train"]:
        sys.exit("%s has no training steps" % path)
    return run


def differences(a, b, key):
    """|a - b| at every step both runs logged."""
    steps = sorted(set(a[key]) & set(b[key]))
    return [(s, abs(a[key][s] - b[key][s])) for s in steps]


def summary(label, a, b):
    """Print how far apart two runs are; return the largest val-loss difference."""
    train, val = differences(a, b, "train"), differences(a, b, "val")
    first = next((s for s, d in train if d > 1e-6), None)
    print("%-28s train loss: max |diff| %.4f, mean %.4f over %d steps; %s"
          % (label, max(d for _, d in train), sum(d for _, d in train) / len(train), len(train),
             "first differs at step %d" % first if first is not None else "identical"))
    if not val:
        sys.exit("no evaluations in common: run with eval_every_steps > 0")
    print("%-28s val loss:   max |diff| %.4f over %d evaluations; at the last one (step %d) %.4f"
          % ("", max(d for _, d in val), len(val), val[-1][0], val[-1][1]))
    return max(d for _, d in val)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reference", action="append", required=True, help="an uninterrupted run (once or twice)")
    ap.add_argument("--resumed", required=True, help="a run that was stopped and resumed")
    ap.add_argument("--tolerance", type=float, default=0.01,
                    help="allowed val-loss difference at any evaluation (default 0.01; see the README)")
    ap.add_argument("--plot", help="write an overlay plot here (needs matplotlib)")
    args = ap.parse_args()
    refs = [load(p) for p in args.reference]
    resumed = load(args.resumed)

    for r in refs + [resumed]:
        print("%s\n    GPUs: %s" % (r["name"], "; ".join(sorted(set(r["gpus"]))) or "?"))
    print("    restarts of the resumed run: %s"
          % (", ".join("step %d (%s)" % sr for sr in resumed["resumes"]) or "none"))
    if not resumed["resumes"]:
        print("WARNING: the 'resumed' run never resumed, so this compares two uninterrupted runs")
    print()

    floor = summary("reference 1 vs reference 2", refs[0], refs[1]) if len(refs) > 1 else None
    worst = max(summary("resumed vs reference %d" % (i + 1), resumed, r) for i, r in enumerate(refs))

    # Judge on the largest val-loss difference, not just the last: the damage from a bad
    # resume can fade as training goes on. Val loss is measured on the same batches every
    # time, so it is far less noisy than the per-step training loss.
    print()
    allowed = max(args.tolerance, 2 * floor) if floor is not None else args.tolerance
    if floor is not None:
        print("noise floor: two uninterrupted runs differ by up to %.4f in val loss" % floor)
    ok = worst <= allowed
    print("%s: the resumed run's val loss differs by up to %.4f (allowed: %.4f = %s)"
          % ("PASS" if ok else "FAIL", worst, allowed,
             "the tolerance" if allowed == args.tolerance else "twice the noise floor"))
    if args.plot:
        plot(refs, resumed, args.plot)
    sys.exit(0 if ok else 1)


def plot(refs, resumed, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed: no plot)")
        return
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    styles = [dict(lw=3, color="#9ecae1"), dict(lw=2, color="#c7e9c0")]
    for i, r in enumerate(refs):
        steps = sorted(r["train"])
        top.plot(steps, [r["train"][s] for s in steps], label="uninterrupted %d" % (i + 1), **styles[i])
    steps = sorted(resumed["train"])
    top.plot(steps, [resumed["train"][s] for s in steps], lw=1, color="#08519c", label="stopped and resumed")
    vs = sorted(resumed["val"])
    top.plot(vs, [resumed["val"][s] for s in vs], "o", color="#08519c", ms=4, label="val loss (resumed)")
    for ax in (top, bottom):
        for i, (s, reason) in enumerate(resumed["resumes"]):
            # An eviction shows as "signal", or as "stop_file" under launch.py (multi-GPU runs).
            evicted = reason in ("signal", "stop_file")
            kind = "an eviction (%s)" % reason if evicted else "a %s save" % reason
            ax.axvline(s, color="#cb181d" if evicted else "#fd8d3c", ls="--", lw=1,
                       label=("restart after %s" % kind) if ax is top and reason not in
                       [x[1] for x in resumed["resumes"][:i]] else None)
    for i, r in enumerate(refs):
        d = differences(resumed, r, "train")
        bottom.plot([s for s, _ in d], [x for _, x in d], lw=1, label="|resumed - uninterrupted %d|" % (i + 1))
    if len(refs) > 1:
        d = differences(refs[1], refs[0], "train")
        bottom.plot([s for s, _ in d], [x for _, x in d], lw=1, color="#999999", label="|uninterrupted 2 - 1| (noise floor)")
    top.set_ylabel("training loss")
    top.legend(fontsize=8)
    bottom.set_ylabel("|loss difference|")
    bottom.set_xlabel("step")
    bottom.legend(fontsize=8)
    fig.suptitle("Resume equivalence on GPUs (recipe 2, test settings)")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print("wrote %s" % path)


if __name__ == "__main__":
    main()
