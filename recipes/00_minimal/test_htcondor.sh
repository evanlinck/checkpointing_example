#!/bin/bash
# HTCondor tests for recipe 0. Run on the access point, in this directory.
#
#   ./test_htcondor.sh job_chtc.sub vacate    # condor_vacate_job: SIGTERM -> save -> exit 85 -> resume from that save
#   ./test_htcondor.sh job_chtc.sub hold      # condor_hold + condor_release: same as a vacate
#   ./test_htcondor.sh job_chtc.sub fast      # condor_vacate_job -fast: hard kill -> resume from the last timed checkpoint
#   ./test_htcondor.sh job_ospool.sub timed   # no interruption: timed exits every 60 s until done
#   ./test_htcondor.sh job_chtc.sub inspect   # vacate, hold, and copy out the checkpoint HTCondor kept
#                                             # (condor_evicted_files), then release and check the resume
#
# To run several at once, start them in the background (each writes its own files):
#   for m in hold fast; do nohup ./test_htcondor.sh job_chtc.sub $m > result_chtc_$m.txt 2>&1 & done
#   for m in timed vacate; do nohup ./test_htcondor.sh job_ospool.sub $m > result_ospool_$m.txt 2>&1 & done
#   wait; tail -n 1 result_*.txt
#
# Each test takes about 10 minutes. The script only reads the job's own event log
# (no condor_q polling), sends one HTCondor command, waits for the job to finish,
# and checks job output for the expected resume.
set -euo pipefail
SUB=${1:?usage: $0 <submit file> <vacate|hold|fast|timed|inspect>}
MODE=${2:?usage: $0 <submit file> <vacate|hold|fast|timed|inspect>}
TAG="test_$(basename "$SUB" .sub)_${MODE}_$(date +%H%M%S)"   # e.g. test_job_chtc_vacate_161818

# A shorter checkpoint interval (60 s) and ~6 minutes of training in total.
# (Replaces the submit file's `shell` line; keep the `exec`: see job_chtc.sub.)
CMD="exec python3 train.py --epochs 10 --step-delay 0.12 --max-runtime-seconds 60"
# Your container image. Set RECIPE0_IMAGE instead of editing the submit file, so your
# /staging path never ends up in the repository:
#   export RECIPE0_IMAGE=osdf:///chtc/staging/<user>/<path>/recipe0.sif
IMAGE=()
if [ -n "${RECIPE0_IMAGE:-}" ]; then
  IMAGE=(-a "container_image = $RECIPE0_IMAGE")
elif grep -q "^container_image.*<user>" "$SUB"; then
  echo "ERROR: $SUB still has the <user> placeholder in container_image." >&2
  echo "       Run:  export RECIPE0_IMAGE=osdf:///chtc/staging/<user>/<path>/recipe0.sif" >&2
  exit 1
fi

# stream_output: so the evicted run's own lines (its save after SIGTERM) reach $TAG.out even if
# it is killed before its output could be transferred.
cluster=$(condor_submit "$SUB" -a "shell = $CMD" -a "log = $TAG.log" -a "output = $TAG.out" \
          -a "error = $TAG.err" -a "stream_output = true" -a "stream_error = true" "${IMAGE[@]}" \
          | awk '/submitted to cluster/ {print $NF}' | tr -d .)
job="$cluster.0"
echo "submitted $job ($MODE); event log: $TAG.log"

until grep -q "^001 " "$TAG.log" 2>/dev/null; do sleep 15; done
echo "running since $(date +%T); waiting 100 s so a timed checkpoint exists first"
sleep 100

case "$MODE" in
  vacate) condor_vacate_job "$job" ;;
  fast)   condor_vacate_job -fast "$job" ;;
  hold)   condor_hold "$job"
          until grep -q "^012 " "$TAG.log"; do sleep 15; done   # held (after the job saved and exited)
          sleep 20
          condor_release "$job" ;;
  timed)  ;;
  inspect)
    # The debugging workflow from the HTCondor manual ("Debugging Self-Checkpointing Jobs"):
    # evict the job, hold it at once so it can't restart and overwrite what HTCondor kept,
    # copy the kept checkpoint out with condor_evicted_files, look at it, then release.
    condor_vacate_job "$job"
    condor_hold "$job"
    until grep -q "^012 " "$TAG.log"; do sleep 15; done
    mkdir -p "$TAG.evicted"
    echo "--- condor_evicted_files get $job (run inside $TAG.evicted/) ---"
    (cd "$TAG.evicted" && condor_evicted_files get "$job") || echo "condor_evicted_files failed (exit $?)"
    echo "--- files HTCondor kept for $job ---"
    (cd "$TAG.evicted" && find . -type f -exec ls -l {} \;) | tee "$TAG.evicted.txt"
    condor_release "$job" ;;
  *)      echo "unknown mode $MODE"; exit 2 ;;
esac
echo "$MODE at $(date +%T); waiting for the job to finish (condor_wait reads the event log)"
condor_wait "$TAG.log" "$job" >/dev/null

echo "--- what the job reported ($TAG.out) ---"
grep -E "^(STARTING|RESUMED|SAVED|EXIT|DONE|SIGTERM)" "$TAG.out" || true

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; exit 1; }
grep -q "^DONE" "$TAG.out" || fail "the job did not finish"
case "$MODE" in
  inspect)
    grep -q "checkpoint.pt$" "$TAG.evicted.txt" && pass "condor_evicted_files returned the checkpoint (see $TAG.evicted/)" \
      || fail "condor_evicted_files did not return checkpoints/checkpoint.pt (see $TAG.evicted.txt)"
    grep -q "saved because: signal" "$TAG.out" && pass "and the released job resumed from the save made after SIGTERM" \
      || fail "the released job did not resume from the save made after SIGTERM" ;;
  vacate|hold)
    grep -q "reason: signal" "$TAG.out" || fail "no save after SIGTERM"
    grep -q "saved because: signal" "$TAG.out" && pass "resumed from the save made after SIGTERM" \
      || fail "the save made after SIGTERM was not restored (is when_to_transfer_output = ON_EXIT_OR_EVICT set?)" ;;
  # (if "no save after SIGTERM" fails: Python never received the signal; check the `exec` in the shell line)
  fast)
    grep -q "reason: signal" "$TAG.out" && fail "unexpected: a save after a signal (-fast sends none)"
    grep -q "saved because: timed" "$TAG.out" && pass "resumed from the last timed checkpoint after the hard kill" \
      || fail "never resumed from a timed checkpoint" ;;
  timed)
    n=$(grep -c "reason: timed" "$TAG.out")
    [ "$n" -ge 2 ] && pass "$n timed checkpoints, each resumed, and the job finished" || fail "only $n timed checkpoints" ;;
esac
