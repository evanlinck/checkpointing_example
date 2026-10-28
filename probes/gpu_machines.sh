#!/bin/bash
# Which machines could run recipe 3, and how often are their GPUs free? Read-only: no jobs,
# one condor_status query of the collector per snapshot. Run on the access point, and leave it:
#   nohup ./gpu_machines.sh > gpu_machines_run.txt 2>&1 &                 # 48 snapshots, every 30 min (24 h)
#   nohup ./gpu_machines.sh 12 60 > gpu_machines_run.txt 2>&1 &           # 12 snapshots, every 60 min
# Snapshots (with machine names) go to runs/gpu-machines/<tag>/ (git-ignored); the summary, without
# machine names, to results/gpu-machines/<tag>/summary.md. It is rewritten after every snapshot,
# so you can read it while the script is still running.
set -euo pipefail
cd "$(dirname "$0")"
N=${1:-48}
EVERY_MIN=${2:-30}
TAG=${TAG:-$(date +%Y%m%d-%H%M)}
RAW=runs/gpu-machines/$TAG
mkdir -p "$RAW"
# One line per partitionable GPU slot (a machine's GPU Lab slot and its backfill slot are separate).
# Gpus / Cpus / Memory on a partitionable slot are what is still free on it.
ATTRS="Name Machine TotalGpus Gpus GPUs_DeviceName GPUs_GlobalMemoryMb GPUs_Capability TotalCpus Cpus TotalMemory Memory BackfillSlot HasCHTCStaging CUDADriverVersion"
for i in $(seq 1 "$N"); do
  out="$RAW/snap_$(date +%Y%m%d-%H%M%S).tsv"
  echo "# $ATTRS" > "$out"
  condor_status -constraint 'PartitionableSlot =?= true && TotalGpus > 0' -af:t $ATTRS >> "$out" || echo "condor_status failed at $(date)"
  echo "$(date): snapshot $i of $N, $(($(wc -l < "$out") - 1)) GPU slots"
  python3 gpu_machines_summary.py "$RAW" "results/gpu-machines/$TAG" > /dev/null
  [ "$i" -lt "$N" ] && sleep $((EVERY_MIN * 60))
done
echo "done: results/gpu-machines/$TAG/summary.md"
