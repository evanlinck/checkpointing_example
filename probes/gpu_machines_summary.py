#!/usr/bin/env python3
"""gpu_machines_summary.py RAW_DIR OUT_DIR: summarize gpu_machines.sh's snapshots.

Per GPU type and slot size (GPUs per machine): how many slots, GPU memory, host memory and
CPUs per slot, and how often 4 (or 2) GPUs were free on at least one of them at the same time.
"Fits recipe 3" = 4 GPUs of at least 75 GB on one machine ("tight" at 40-75 GB) (a 7B full fine-tune with FSDP;
see docs/03-fsdp-dcp-finetune.md). No machine names in the output."""
import glob
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redact import redact  # noqa: E402


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(raw_dir, out_dir):
    snaps = sorted(glob.glob(os.path.join(raw_dir, "snap_*.tsv")))
    groups = {}            # (gpu, total gpus, backfill) -> per-snapshot data
    for si, path in enumerate(snaps):
        lines = open(path).read().splitlines()
        header = lines[0].lstrip("# ").split()
        for line in lines[1:]:
            row = dict(zip(header, line.split("\t")))
            gpu = row.get("GPUs_DeviceName", "?").strip('"')
            total = int(num(row.get("TotalGpus")) or 0)
            backfill = row.get("BackfillSlot") == "true"
            g = groups.setdefault((gpu, total, backfill), {"slots": {}, "free4": set(), "free2": set()})
            g["slots"][row.get("Name")] = row
            free = int(num(row.get("Gpus")) or 0)
            if free >= 4:
                g["free4"].add(si)
            if free >= 2:
                g["free2"].add(si)
    md = ["# GPU machines", "",
          "From `probes/gpu_machines.sh`: %d snapshots (%s to %s). One row per GPU type, GPUs per slot and slot kind. "
          "Host memory and CPUs are the slot's totals. \"4 free\": share of snapshots in which at least one such "
          "slot had 4 GPUs free at once." % (len(snaps), os.path.basename(snaps[0])[5:-4] if snaps else "-",
                                              os.path.basename(snaps[-1])[5:-4] if snaps else "-"), "",
          "| GPU | GPU memory | GPUs per slot | slot | slots | host memory (GB) | CPUs | CUDA driver "
          "| 2 free | 4 free | fits recipe 3 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    n = max(len(snaps), 1)
    for (gpu, total, backfill), g in sorted(groups.items(), key=lambda kv: (kv[0][0], -kv[0][1], kv[0][2])):
        rows = list(g["slots"].values())
        mem = [num(r.get("TotalMemory")) / 1024 for r in rows if num(r.get("TotalMemory"))]
        cpus = [num(r.get("TotalCpus")) for r in rows if num(r.get("TotalCpus"))]
        gmem = statistics.median([num(r.get("GPUs_GlobalMemoryMb")) for r in rows if num(r.get("GPUs_GlobalMemoryMb"))] or [0])
        drv = sorted(set(r.get("CUDADriverVersion", "?") for r in rows))
        rng = lambda xs: ("%.0f" % min(xs) if min(xs) == max(xs) else "%.0f-%.0f" % (min(xs), max(xs))) if xs else "?"
        if total >= 4 and gmem >= 75000:
            fits = "yes"
        elif total >= 4 and gmem >= 40000:
            fits = "tight (measure)"      # ~40-45 GB per GPU estimated: L40S-class GPUs may just fit
        elif total >= 2 and gmem >= 75000:
            fits = "2 GPUs only"          # ~70 GB per GPU: the resharding test, not full runs
        else:
            fits = "no"
        md.append("| %s | %.0f GB | %d | %s | %d | %s | %s | %s | %.0f%% | %.0f%% | %s |" % (
            gpu, gmem / 1000, total, "backfill" if backfill else "GPU Lab", len(rows), rng(mem), rng(cpus),
            ", ".join(drv), 100 * len(g["free2"]) / n, 100 * len(g["free4"]) / n, fits))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "summary.md"), "w") as f:
        f.write(redact("\n".join(md) + "\n"))
    print("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:3])
