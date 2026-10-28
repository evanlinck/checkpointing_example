#!/bin/bash
# spool_check.sh - a tiny self-checkpointing job, so ap_survey.sh --job can look at a real job's spool.
# Each execution adds 1 MB to ckpt/ and exits 85 ("saved, restart me"); the 10th exits 0.
# Every execution sleeps 60 s, so the job stays in the queue for ~10-15 minutes.
set -eu
mkdir -p ckpt
n=$(cat ckpt/count 2>/dev/null || echo 0)
n=$((n + 1))
echo "execution $n on $(hostname) at $(date -u +%H:%M:%S)"
sleep 60
head -c 1048576 /dev/urandom > "ckpt/part_$n.bin"
echo "$n" > ckpt/count
[ "$n" -ge 10 ] && exit 0
exit 85
