#!/bin/bash
# Run the GPU communication benchmark on several machines and summarize. Run on the access point,
# in this directory, and leave it running:
#   export RECIPES_IMAGE=osdf:///chtc/staging/<user>/images/ckpt-recipes-v1.sif
#   nohup ./run_comm_bench.sh > comm_run.txt 2>&1 &
# (recipe 1's image works too: it has the same PyTorch 2.8 with CUDA.)
#
# Submits, for 4 and 2 GPUs, with NCCL's default and with NCCL_P2P_LEVEL=NVL, COPIES jobs each
# (default 2), so 8 jobs of ~5 minutes: about 2-3 GPU-hours in all. Extra arguments go to
# condor_submit, e.g. -a "require_gpus = DeviceName == \"NVIDIA L40S\"" to test one GPU type.
# Results: results/gpu-comm/<tag>/summary.md (the .out and .err files are in runs/gpu-comm/<tag>/).
set -euo pipefail
cd "$(dirname "$0")"
: "${RECIPES_IMAGE:?set RECIPES_IMAGE first (see the top of this script)}"
COPIES=${COPIES:-2}
TAG=${TAG:-$(date +%Y%m%d-%H%M)}
RUN_DIR=$PWD/../runs/gpu-comm/$TAG
mkdir -p "$RUN_DIR"
for n in 4 2; do
  for p2p in "" NVL; do
    condor_submit comm_bench.sub -a "IMAGE = $RECIPES_IMAGE" -a "NGPUS = $n" -a "P2P = $p2p" \
      -a "RUN_DIR = $RUN_DIR" -a "COPIES = $COPIES" "$@"
  done
done
echo "submitted at $(date); waiting for all jobs to leave the queue (reads $RUN_DIR/comm.log only)"
# condor_wait follows the event log: no condor_q polling.
condor_wait "$RUN_DIR/comm.log" || true
python3 summarize_comm.py "$RUN_DIR" "$PWD/../results/gpu-comm/$TAG"
