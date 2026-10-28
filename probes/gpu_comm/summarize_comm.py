#!/usr/bin/env python3
"""summarize_comm.py RUN_DIR OUT_DIR: one table from comm_bench's .out/.err files.

For each job: machine (GPU type and count), NCCL setting, whether the start-up check passed,
the transport NCCL chose (from the NCCL_DEBUG lines in .err), bus bandwidth at 1 GB shards,
and the estimated communication time per FSDP step for a 7B model."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from redact import redact  # noqa: E402  (probes/redact.py: no user names or IPs in reports)


def main(run_dir, out_dir):
    rows = []
    for out in sorted(glob.glob(os.path.join(run_dir, "comm_*.out"))):
        recs = [json.loads(l[5:]) for l in open(out, errors="replace") if l.startswith("COMM ")]
        if not recs:
            continue
        start = next((r for r in recs if r["event"] == "start"), {})
        check = next((r for r in recs if r["event"] == "check"), None)
        bench = {(r["op"], r["shard_mb"]): r["busbw_gb_s"] for r in recs if r["event"] == "bench"}
        est = next((r for r in recs if r["event"] == "fsdp_estimate"), {})
        err = open(out[:-4] + ".err", errors="replace").read() if os.path.exists(out[:-4] + ".err") else ""
        transports = sorted(set(re.findall(r"via (P2P/\S+|SHM/\S+|NET/\S+)", err)))
        topo = start.get("topology", "")
        links = "NVLink" if re.search(r"\bNV\d+\b", topo) else ("PCIe" if topo.strip() else "?")
        gpus = start.get("gpus") or ["?"]
        rows.append({"job": os.path.basename(out)[5:-4], "gpu": gpus[0], "n": start.get("world"),
                     "links": links, "p2p": start.get("nccl_p2p_level"),
                     "check": "OK" if check and check.get("ok") else "HUNG/FAILED",
                     "transport": ", ".join(transports) or "?",
                     "ag": bench.get(("all_gather", 1024)), "rs": bench.get(("reduce_scatter", 1024)),
                     "step": est.get("seconds_per_step"), "shm": start.get("dev_shm_gb"),
                     "nccl": start.get("nccl")})
    md = ["# GPU communication benchmark", "",
          "From `probes/gpu_comm/` (%d jobs). Bus bandwidth in GB/s at 1 GB per-GPU shards (bf16). "
          "\"FSDP s/step\": estimated communication time per step for a 7.3B model (2 all-gathers of bf16 "
          "weights + 1 reduce-scatter of fp32 gradients), before any overlap with compute." % len(rows), "",
          "| GPU | GPUs | links | NCCL_P2P_LEVEL | start-up check | NCCL transport | all-gather | reduce-scatter "
          "| FSDP s/step | /dev/shm GB | NCCL |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["gpu"], r["n"] or 0, r["p2p"] or "")):
        md.append("| %(gpu)s | %(n)s | %(links)s | %(p2p)s | %(check)s | %(transport)s | %(ag)s | %(rs)s "
                  "| %(step)s | %(shm)s | %(nccl)s |" % r)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "summary.md"), "w") as f:
        f.write(redact("\n".join(md) + "\n"))
    print("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:3])
