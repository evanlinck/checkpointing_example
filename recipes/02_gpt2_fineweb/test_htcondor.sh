#!/bin/bash
# HTCondor tests for recipe 2. Run on the access point, in this directory.
#
#   ./test_htcondor.sh <mode> [extra condor_submit arguments...]
#
#   ./test_htcondor.sh comm       # only check that the GPUs can communicate (~2 min): starts, trains 20 steps
#   ./test_htcondor.sh timed      # timed exits only: each one resumes, and the run finishes
#   ./test_htcondor.sh vacate     # condor_vacate_job: every rank stops at the same step, resumes from that save
#   ./test_htcondor.sh hold       # condor_hold + condor_release: the same
#   ./test_htcondor.sh fast       # condor_vacate_job -fast (no signal): resumes from the last periodic/timed save
#   ./test_htcondor.sh reference  # no interruptions (kept off backfill): the baseline for compare_runs.py
#
# Extra arguments go to condor_submit, e.g.
#   ./test_htcondor.sh vacate -a "NGPUS = 4"                        # 4 GPUs instead of the tests' 2
#   ./test_htcondor.sh comm -a "gpus_minimum_capability = 12.0"     # only Blackwell GPUs (RTX PRO 6000)
#   ./test_htcondor.sh vacate -a "requirements = (HasCHTCStaging =?= true) && (TARGET.BackfillSlot =?= true)"
#
# The tests use 2 GPUs (4-GPU machines are scarce), 300 steps with a 0.5 s pause after each (so a
# fast machine doesn't finish before the test interrupts it), a timed exit every 2 minutes, and
# in-place saves every minute. Each takes about 10-15 minutes, so about 0.3-0.5 GPU-hours with 2 GPUs.
#
# Tests can wait in the queue for a long time. To keep one running after you log out, start it
# with nohup and read its output file later (the last line is PASS or FAIL):
#   nohup ./test_htcondor.sh vacate > vacate_run.txt 2>&1 &
# If you stop a script part-way, its job stays in the queue: condor_rm it before testing again.
#
# Your locations come from environment variables, so no personal path is stored in the repo:
#   export RECIPE2_IMAGE=osdf:///chtc/staging/<user>/<path>/recipe1.sif
#   export RECIPE2_DATA_DIR=/staging/<user>/recipe2/fineweb10B     # where prepare_data.py wrote the shards
#   export RECIPE2_TEST_DIR=/staging/<user>/recipe2/tests          # each test gets its own directory here
#
# Like recipe 1's test, it only reads the job's own event log (no condor_q polling), sends one
# HTCondor command, waits for the job to finish, and checks its output.
set -euo pipefail
MODE=${1:?usage: $0 <comm|timed|vacate|hold|fast|reference> [extra condor_submit arguments...]}
shift
for v in RECIPE2_IMAGE RECIPE2_DATA_DIR RECIPE2_TEST_DIR; do
  if [ -z "${!v:-}" ]; then echo "ERROR: set $v first (see the top of this script)" >&2; exit 1; fi
done
if [ ! -d htcondor_ckpt ]; then
  echo "ERROR: htcondor_ckpt/ is not in this directory. Copy it here first:  cp -r ../../htcondor_ckpt ." >&2
  exit 1
fi
# The time plus this script's process id: tests started in the same second still get different names.
TAG="test_${MODE}_$(date +%H%M%S)_$$"
RUN="$RECIPE2_TEST_DIR/$TAG"    # this test's checkpoints and outputs, on /staging

# job.sub's own command (launch.py -> torchrun -> one process per GPU), with test settings passed
# through its EXTRA macro and this test's locations through DATA_DIR and RUN_DIR. So the tests
# exercise exactly the command a real run uses.
# max_runtime_seconds: a timed exit every 2 minutes (a reference run: never).
LIMIT=120; [ "$MODE" = reference ] && LIMIT=86400
SETTINGS="--set max_steps=300 --set step_delay=0.5 --set max_runtime_seconds=$LIMIT --set save_every_minutes=1 --set eval_every_steps=100"
[ "$MODE" = comm ] && SETTINGS="--set max_steps=20 --set eval_every_steps=0 --set save_every_minutes=0"
# A reference run must not be interrupted: keep it off backfill slots, where the GPU's owner can
# evict it. Without +is_resumable it runs in the GPU Lab, which a 15-minute job fits easily.
NOBACKFILL=(); [ "$MODE" = reference ] && NOBACKFILL=(-a "+is_resumable = false")

submit() {   # prints the job id. $1 = the run name (job.sub names its files job_<RUN>.*); the rest go to condor_submit
  local name=$1; shift
  condor_submit job.sub -a "NGPUS = 2" -a "RUN = $name" -a "DATA_DIR = $RECIPE2_DATA_DIR" -a "RUN_DIR = $RUN" \
    -a "EXTRA = $SETTINGS" -a "container_image = $RECIPE2_IMAGE" -a "stream_output = true" -a "stream_error = true" \
    ${NOBACKFILL[@]+"${NOBACKFILL[@]}"} "$@" \
    | awk '/submitted to cluster/ {print $NF}' | tr -d . | sed 's/$/.0/'
}

# Interrupt only while the job is training. With a timed exit every 2 minutes the job restarts often,
# and a vacate or hold sent while it is saving for a timed exit, or in the seconds between two
# executions, finds nothing to save: the job resumes from an earlier save and the test fails for no
# real reason. The job's output is streamed back (stream_output), so wait for one of the first few
# training-step lines after a (re)start: then the next timed exit is a minute or more away.
wait_training() {   # $1 = how many step lines after a (re)start still count as "early"
  echo "waiting until the job is early in an execution, training (not saving or restarting)..."
  for _ in $(seq 240); do
    local lines; lines=$(grep -E "^(step [0-9]+|SAVED|RESUMED|STARTING|launch.py|DONE)" "$TAG.out" 2>/dev/null || true)
    local since; since=$(echo "$lines" | awk '/^(RESUMED|STARTING)/ {n = 0; started = 1; next} /^step / {n++; next} {n = -1} END {print (started ? n : -1)}')
    if [ "$since" -ge 1 ] && [ "$since" -le "$1" ]; then return 0; fi
    if grep -q "^005 " "$TAG.log"; then return 0; fi    # the job ended: the check below reports it
    sleep 5
  done
  echo "(never saw an early training step; interrupting anyway)"
}

job=$(submit "$TAG" "$@")
TAG="job_$TAG"    # from here on: the job's files, as job.sub names them
echo "submitted $job ($MODE); event log: $TAG.log; run directory: $RUN"
until grep -q "^001 " "$TAG.log" 2>/dev/null; do sleep 15; done
echo "running since $(date +%T) on $(grep -A1 '^001 ' "$TAG.log" | grep -o 'alias=[^&]*' | head -1 | cut -d= -f2)"

if [ "$MODE" != comm ] && [ "$MODE" != reference ] && [ "$MODE" != timed ]; then
  echo "waiting 240 s, so the run is training and has saved at least once"
  sleep 240
  # If the job already ended (e.g. it crashed on start-up), say so instead of failing on "job not found".
  if grep -q "^005 " "$TAG.log"; then
    echo "FAIL: the job ended before the test could interrupt it:"
    grep -A1 "^005 " "$TAG.log" | tail -1
    echo "--- end of $TAG.out ---"; tail -5 "$TAG.out"
    echo "--- end of $TAG.err ---"; tail -5 "$TAG.err"
    exit 1
  fi
  wait_training 2      # rank 0 prints a step line every 10 steps (~20 s on 2 GPUs)
fi

case "$MODE" in
  comm|timed|reference) ;;
  vacate) condor_vacate_job "$job" ;;
  fast)   condor_vacate_job -fast "$job" ;;
  hold)   condor_hold "$job"
          until grep -q "^012 " "$TAG.log"; do sleep 15; done
          sleep 20
          condor_release "$job" ;;
  *)      echo "unknown mode $MODE"; exit 2 ;;
esac
echo "$MODE at $(date +%T); waiting for the job to finish (condor_wait reads the event log)"
condor_wait "$TAG.log" "$job" >/dev/null

echo "--- what the job reported ($TAG.out) ---"
grep -E "^(\[rank [0-9]+\] )?(STARTING|RESUMED|SAVED|DONE|stop:|save finished|first step|communication|checking|WARNING|\(the stop)|^launch.py|could NOT" "$TAG.out" || true

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; echo "--- end of $TAG.err ---"; tail -15 "$TAG.err"; exit 1; }
grep -q "communication OK" "$TAG.out" || fail "the GPUs never confirmed they can communicate (see $TAG.err)"
grep -q "^DONE" "$TAG.out" || fail "the job did not finish"

# Every rank must have stopped at the same step at every stop (the "[rank N] stop: ..." lines).
# (Ranks' lines are matched anywhere on a line: output from two processes can run together.)
same_stop_step() {
  local steps; steps=$(grep -oE "\[rank [0-9]+\] stop: [^[]*(stopping at step|reached at step) [0-9]+" "$TAG.out" | grep -oE "[0-9]+$" | sort -u)
  local per_stop; per_stop=$(grep -oE "\[rank 0\] stop:" "$TAG.out" | grep -c . || true)
  [ "$(echo "$steps" | grep -c .)" -eq "$per_stop" ]
}
case "$MODE" in
  comm)
    pass "the GPUs communicate and the job trained (GPUs: $(grep -oE 'on NVIDIA [^,]*' "$TAG.out" | sort -u | tr '\n' ' '))" ;;
  reference)
    grep -q "^RESUMED" "$TAG.out" && fail "the reference run was interrupted (see $TAG.log); run it again"
    pass "uninterrupted run finished; metrics in $RUN/outputs/metrics.jsonl" ;;
  timed)
    n=$(grep -c "reason: timed" "$TAG.out" || true)
    [ "$n" -ge 2 ] || fail "only $n timed checkpoints"
    same_stop_step || fail "the ranks did not all stop at the same step"
    pass "$n timed checkpoints, all ranks stopping at the same step each time, and the run finished" ;;
  vacate|hold)
    grep -q "reason: stop_file" "$TAG.out" || fail "no save after the SIGTERM (via launch.py's stop file)"
    same_stop_step || fail "the ranks did not all stop at the same step"
    grep -q "saved because: stop_file" "$TAG.out" || fail "the save made after the SIGTERM was not restored"
    pass "all ranks stopped at the same step, rank 0 saved, and the job resumed from that save" ;;
  fast)
    grep -q "reason: stop_file" "$TAG.out" && fail "unexpected: a save after a signal (-fast sends none)"
    grep -qE "saved because: (timed|periodic)" "$TAG.out" || fail "never resumed from a timed or periodic save"
    pass "resumed from the last timed/periodic save after the hard kill" ;;
esac
echo "(this test's files on /staging: $RUN; remove them when done)"
