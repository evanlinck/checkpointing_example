# GPU communication benchmark

From `probes/gpu_comm/` (8 jobs). Bus bandwidth in GB/s at 1 GB per-GPU shards (bf16). "FSDP s/step": estimated communication time per step for a 7.3B model (2 all-gathers of bf16 weights + 1 reduce-scatter of fp32 gradients), before any overlap with compute.

| GPU | GPUs | links | NCCL_P2P_LEVEL | start-up check | NCCL transport | all-gather | reduce-scatter | FSDP s/step | /dev/shm GB | NCCL | GPUs visible / used |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA H100 80GB HBM3 | 2 | ? | (default) | OK | P2P/CUMEM | 278.7 | 266.5 | 0.11 | 1082.1 | 2.27.3 | 4 / 2 |
| NVIDIA H100 80GB HBM3 | 2 | ? | (default) | OK | P2P/CUMEM | 282.3 | 272.9 | 0.11 | 1082.1 | 2.27.3 | 4 / 2 |
| NVIDIA H100 80GB HBM3 | 2 | NVLink | NVL | OK | P2P/CUMEM | 280.6 | 271.7 | 0.11 | 1082.1 | 2.27.3 | 4 / 2 |
| NVIDIA H100 80GB HBM3 | 2 | NVLink | NVL | OK | P2P/CUMEM | 277.7 | 265.1 | 0.11 | 1082.1 | 2.27.3 | 4 / 2 |
| NVIDIA H100 80GB HBM3 | 4 | ? | (default) | OK | P2P/CUMEM | 341.0 | 342.8 | 0.13 | 1082.1 | 2.27.3 | 4 / 4 |
| NVIDIA H100 80GB HBM3 | 4 | ? | (default) | OK | P2P/CUMEM | 338.4 | 341.2 | 0.13 | 1082.1 | 2.27.3 | 4 / 4 |
| NVIDIA H100 80GB HBM3 | 4 | NVLink | NVL | OK | P2P/CUMEM | 336.6 | 339.0 | 0.13 | 1082.1 | 2.27.3 | 4 / 4 |
| NVIDIA H100 80GB HBM3 | 4 | NVLink | NVL | OK | P2P/CUMEM | 342.3 | 344.6 | 0.13 | 1082.1 | 2.27.3 | 4 / 4 |
