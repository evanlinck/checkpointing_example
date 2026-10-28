#!/usr/bin/env python3
"""
Plot one run from its metrics log: training and validation loss, epoch ends, restarts and
checkpoints. The log is append-only and travels with the job, so a run that was stopped and
resumed many times still gives one continuous curve, with each restart marked.

    python3 plot_run.py outputs                 # writes outputs/loss_curve.png
    python3 plot_run.py outputs --out run1.png

Needs matplotlib (on your laptop, if the access point doesn't have it).
"""
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outputs", help="an outputs directory, or its metrics.jsonl")
    ap.add_argument("--out", help="where to write the plot (default: loss_curve.png next to the log)")
    ap.add_argument("--title", default="Recipe 2: GPT-2 small on FineWeb-Edu")
    args = ap.parse_args()
    path = os.path.join(args.outputs, "metrics.jsonl") if os.path.isdir(args.outputs) else args.outputs

    train, val, epoch_ends, resumes = {}, {}, [], []
    with open(path) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "train":
                train[e["step"]] = e["loss"]          # a step trained twice: the last time counts
            elif e["event"] == "eval":
                val[e["step"]] = e["val_loss"]
                if "epoch" in e:                     # the evaluation at the end of an epoch
                    epoch_ends.append(e["step"])
            elif e["event"] == "resumed":
                resumes.append((e["step"], e["reason"]))

    fig, ax = plt.subplots(figsize=(10, 5))
    steps = sorted(train)
    losses = [train[s] for s in steps]
    h = len(losses) // 100                           # mean over 2h+1 neighbouring points: easier to read
    smooth = [sum(losses[max(0, i - h):i + h + 1]) / len(losses[max(0, i - h):i + h + 1])
              for i in range(len(losses))]
    ax.plot(steps, losses, lw=0.5, color="#c6dbef", label="training loss")
    ax.plot(steps, smooth, lw=1.5, color="#2171b5", label="training loss (smoothed)")
    vs = sorted(val)
    ax.plot(vs, [val[s] for s in vs], "o-", ms=3, lw=1, color="#cb181d", label="validation loss")
    for i, s in enumerate(sorted(set(epoch_ends))):
        ax.axvline(s, color="#999999", ls=":", lw=1, label="epoch end" if i == 0 else None)
    for i, (s, _) in enumerate(resumes):
        ax.axvline(s, color="#fd8d3c", ls="--", lw=1, label="restart (after a save)" if i == 0 else None)
    ax.set_xlabel("step")
    ax.set_ylabel("loss")
    # Leave out the first few percent of steps when scaling the axis: the loss starts very high
    # (~11 for a fresh GPT-2) and would flatten everything after it.
    rest = losses[len(losses) // 20:] or losses
    low = min(rest + [val[s] for s in vs])
    ax.set_ylim(low - 0.05 * abs(low), max(rest) * 1.1)
    ax.set_title("%s: %d steps, %d restarts, final val loss %s"
                 % (args.title, max(steps + vs), len(resumes), "%.4f" % val[vs[-1]] if vs else "-"))
    ax.legend(fontsize=8)
    fig.tight_layout()
    out = args.out or os.path.join(os.path.dirname(path) or ".", "loss_curve.png")
    fig.savefig(out, dpi=120)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
