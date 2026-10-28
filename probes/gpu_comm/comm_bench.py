#!/usr/bin/env python3
"""
comm_bench.py - how fast can the GPUs of one machine exchange data?

FSDP (recipe 3) splits the model across the GPUs. Every training step, each GPU collects
the full weights of each layer from the others (all-gather), twice, and hands back its
share of the gradients (reduce-scatter). For a ~7B model that's ~60 GB moved per GPU per
step, so this speed matters far more than for DDP (recipe 2). It depends on the machine:
NVLink, PCIe directly between GPUs, or through host memory (NCCL_P2P_LEVEL=NVL).

Run under torchrun, one process per GPU (see comm_bench.sub):
    torchrun --standalone --nproc_per_node=4 comm_bench.py

Prints one line per result, starting with "COMM " (JSON), which summarize_comm.py reads.
Maintainer tooling: not part of the recipes.
"""
import datetime
import json
import os
import shutil
import socket
import subprocess
import sys
import time

import torch
import torch.distributed as dist

SIZES_MB = [16, 64, 256, 1024]   # per-GPU shard sizes; one layer of a 7B model is ~450 MB in bf16
WARMUP, ITERS = 3, 10
TIMEOUT_S = int(os.environ.get("COMM_TIMEOUT_S", "120"))   # a hang fails the job after this long
MODEL_PARAMS = 7.3e9             # OLMo 3 7B, for the per-step estimate

rank = int(os.environ.get("RANK", 0))
local_rank = int(os.environ.get("LOCAL_RANK", 0))
world = int(os.environ.get("WORLD_SIZE", 1))


def say(kind, **fields):
    """One JSON line from rank 0 (or from every rank, with all_ranks)."""
    if rank == 0:
        print("COMM " + json.dumps(dict(event=kind, host=socket.gethostname(), world=world, **fields),
                                   default=str), flush=True)


def machine_info():
    info = {"torch": torch.__version__, "cuda": torch.version.cuda,
            "nccl": ".".join(map(str, torch.cuda.nccl.version())),
            "gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
            "nccl_p2p_level": os.environ.get("NCCL_P2P_LEVEL", "(default)"),
            "dev_shm_gb": round(shutil.disk_usage("/dev/shm").total / 1e9, 1)}
    try:   # GPU-to-GPU links: NV# = NVLink, PIX/PXB/PHB/NODE/SYS = PCIe paths of increasing distance
        info["topology"] = subprocess.run(["nvidia-smi", "topo", "-m"], capture_output=True, text=True,
                                          timeout=30).stdout
    except Exception as e:
        info["topology"] = "nvidia-smi topo failed: %s" % e
    ad = os.environ.get("_CONDOR_MACHINE_AD")
    if ad and os.path.exists(ad):
        keep = ("GPUs_DeviceName", "TotalGpus", "TotalCpus", "TotalMemory", "CUDADriverVersion", "BackfillSlot")
        with open(ad) as f:
            info["machine_ad"] = {k.strip(): v.strip() for k, _, v in (l.partition(" = ") for l in f)
                                  if k.strip() in keep}
    return info


def timed(fn):
    for _ in range(WARMUP):
        fn()
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(ITERS):
        fn()
    torch.cuda.synchronize()
    return (time.time() - t0) / ITERS


def main():
    device = torch.device("cuda", local_rank)
    torch.cuda.set_device(device)
    say("start", **(machine_info() if rank == 0 else {}))
    dist.init_process_group("nccl", timeout=datetime.timedelta(seconds=TIMEOUT_S), device_id=device)

    # The start-up check recipe 2 uses: if this never prints, the GPUs couldn't reach each other.
    t0 = time.time()
    x = torch.ones(1, device=device)
    dist.all_reduce(x)
    torch.cuda.synchronize()
    say("check", ok=x.item() == world, seconds=round(time.time() - t0, 2))

    results = {}
    for mb in SIZES_MB:
        n = mb * 1024 * 1024 // 2                                # bf16 elements per GPU
        shard = torch.ones(n, dtype=torch.bfloat16, device=device)
        full = torch.empty(n * world, dtype=torch.bfloat16, device=device)
        # nccl-tests conventions: "bus bandwidth" makes numbers comparable across GPU counts.
        for op, fn, size, factor in [
            ("all_gather", lambda: dist.all_gather_into_tensor(full, shard), n * world * 2, (world - 1) / world),
            ("reduce_scatter", lambda: dist.reduce_scatter_tensor(shard, full), n * world * 2, (world - 1) / world),
            ("all_reduce", lambda: dist.all_reduce(shard), n * 2, 2 * (world - 1) / world),
        ]:
            s = timed(fn)
            busbw = size / s * factor / 1e9
            results[(op, mb)] = busbw
            say("bench", op=op, shard_mb=mb, seconds=round(s, 5), busbw_gb_s=round(busbw, 1))
        del shard, full
        torch.cuda.empty_cache()

    # What this means for one FSDP step of a 7B model (no overlap with compute assumed):
    # all-gather of bf16 weights in forward and again in backward, reduce-scatter of fp32 gradients.
    ag, rs = results[("all_gather", 1024)], results[("reduce_scatter", 1024)]
    moved_ag = 2 * MODEL_PARAMS * 2 * (world - 1) / world / 1e9
    moved_rs = MODEL_PARAMS * 4 * (world - 1) / world / 1e9
    say("fsdp_estimate", model_params=MODEL_PARAMS, gb_all_gather=round(moved_ag, 1),
        gb_reduce_scatter=round(moved_rs, 1), seconds_per_step=round(moved_ag / ag + moved_rs / rs, 2),
        note="communication per optimizer step, per micro-batch if gradients are synced every micro-batch; "
             "FSDP overlaps much of it with compute")
    dist.destroy_process_group()
    say("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
