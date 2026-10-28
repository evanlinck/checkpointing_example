#!/bin/bash
# HTCondor tests for recipe 4. Run on the access point, in this directory, after
# settings.sub is set up (its three lines) and data/ exists (prepare.sub).
#
#   ./test_htcondor.sh timed       # timed checkpoints only: each one resumes, and the run finishes
#   ./test_htcondor.sh vacate      # condor_vacate_job: resumes from the save made after SIGTERM
#   ./test_htcondor.sh hold        # condor_hold + condor_release: the same
#   ./test_htcondor.sh fast        # condor_vacate_job -fast (no warning): resumes from the last timed checkpoint
#   ./test_htcondor.sh handoff     # the DAG: the job hands over to a new job (exit 86), which finishes
#   ./test_htcondor.sh reference   # no interruptions: a baseline to compare losses with
#
# Each test is a short run (900 steps with a 0.1 s pause after each) with a timed checkpoint
# every 2 minutes, so it can be interrupted several times: about 10-20 minutes of one GPU.
# The handoff test sets allowed_job_duration = 420 s: the access point's limit on a job's
# total time (14 days on ap40), shrunk to 7 minutes.
#
# Each test runs in its own directory (test_<mode>_<time>/), with copies of the files, so
# tests don't share checkpoints. To keep a test running after you log out:
#   nohup ./test_htcondor.sh vacate > vacate_run.txt 2>&1 &
# Like recipes 0 and 1, it reads only the job's event log (no condor_q polling).
set -euo pipefail
MODE=${1:?usage: $0 <timed|vacate|hold|fast|handoff|reference>}
[ -d htcondor_ckpt ] || { echo "ERROR: copy the shared modules here first:  cp -r ../../htcondor_ckpt ." >&2; exit 1; }
[ -d data ] || { echo "ERROR: data/ is missing: run prepare.sub first" >&2; exit 1; }
grep -qE "^DATA_URL.*<user>" settings.sub && { echo "ERROR: settings.sub still says <user>: edit its three lines first" >&2; exit 1; }
# An older copy of htcondor_ckpt/ lacks what recipe 4 needs (our first test run failed this way).
grep -q "def job_time_left" htcondor_ckpt/stop.py || { echo "ERROR: htcondor_ckpt/ here is older than recipe 4:
       update the repository's htcondor_ckpt/, then:  rm -rf htcondor_ckpt && cp -r ../../htcondor_ckpt ." >&2; exit 1; }

TAG="test_${MODE}_$(date +%H%M%S)"
mkdir "$TAG"
cp -r train.py config.yaml settings.sub htcondor_ckpt data handoff.sh recipe4.dag "$TAG"/
mkdir -p "$TAG/resume"

# The submit file, with test settings added before its `queue` line.
LIMIT=120; [ "$MODE" = reference ] && LIMIT=86400
SETS="--set max_steps=900 --set step_delay=0.1 --set max_runtime_seconds=$LIMIT --set limit_margin_seconds=60"
SETS="$SETS --set eval_every_steps=300 --set deterministic=true"
{
  grep -v '^queue' job_ospool.sub
  echo "# ----- added by test_htcondor.sh -----"
  echo 'shell = export HOME=$PWD; mkdir -p checkpoints outputs; exec python3 train.py --config config.yaml --set model_dir=$(MODEL) '"$SETS"
  echo "stream_output = true"                     # see training steps live in job.out
  echo "stream_error  = true"
  [ "$MODE" = handoff ] && echo "allowed_job_duration = 420"
  echo "queue"
} > "$TAG/job_ospool.sub"
cd "$TAG"

if [ "$MODE" = handoff ]; then
  condor_submit_dag recipe4.dag
  echo "DAG submitted in $TAG/; waiting for it to finish (it reads recipe4.dag.dagman.out)"
  until grep -q "EXITING WITH STATUS" recipe4.dag.dagman.out 2>/dev/null; do sleep 30; done
else
  job=$(condor_submit job_ospool.sub | awk '/submitted to cluster/ {print $NF}' | tr -d . | sed 's/$/.0/')
  echo "submitted $job ($MODE) in $TAG/"
  until grep -q "^001 " job.log 2>/dev/null; do sleep 15; done
  echo "running since $(date +%T); waiting 200 s so a timed checkpoint exists first"
  sleep 200
  if [ "$MODE" = vacate ] || [ "$MODE" = hold ] || [ "$MODE" = fast ]; then
    # Interrupt while training, not while saving: wait for a step line soon after a (re)start.
    for _ in $(seq 120); do
      since=$( (grep -E "^(step [0-9]+|SAVED|RESUMED|STARTING|DONE)" job.out 2>/dev/null || true) | awk '/^(RESUMED|STARTING)/ {n = 0; s = 1; next} /^step / {n++; next} {n = -1} END {print (s ? n : -1)}')
      { [ "$since" -ge 1 ] && [ "$since" -le 5 ]; } && break
      grep -q "^005 " job.log && break
      sleep 5
    done
  fi
  case "$MODE" in
    vacate) condor_vacate_job "$job" ;;
    fast)   condor_vacate_job -fast "$job" ;;
    hold)   condor_hold "$job"
            until grep -q "^012 " job.log; do sleep 15; done
            sleep 20
            condor_release "$job" ;;
  esac
  echo "$MODE at $(date +%T); waiting for the job to finish"
  condor_wait job.log "$job" >/dev/null
fi

echo "--- what the job reported ($TAG/job.out) ---"
grep -E "^(TIME LIMIT|STARTING|RESUMED|SAVED|RESOURCES|EXIT|DONE|stop:|first step|WARNING)" job.out || true

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; exit 1; }
grep -q "^DONE" job.out || fail "the run did not finish"
case "$MODE" in
  reference)
    grep -q "^RESUMED" job.out && fail "the reference run was interrupted (see job.log); run it again"
    pass "an uninterrupted run finished; its log is $TAG/checkpoints/metrics.jsonl" ;;
  timed)
    n=$(grep -c "reason: timed" job.out || true)
    [ "$n" -ge 2 ] && pass "$n timed checkpoints, each resumed, and the run finished" || fail "only $n timed checkpoints" ;;
  vacate|hold)
    grep -q "reason: signal" job.out || fail "no save after SIGTERM"
    grep -q "saved because: signal" job.out && pass "resumed from the save made after SIGTERM" \
      || fail "the save made after SIGTERM was not restored" ;;
  fast)
    grep -q "reason: signal" job.out && fail "unexpected: a save after a signal (-fast sends none)"
    grep -q "saved because: timed" job.out && pass "resumed from the last timed checkpoint after the hard kill" \
      || fail "never resumed from a timed checkpoint" ;;
  handoff)
    grep -q "^EXIT 86" job.out || fail "the job never handed off (exit 86)"
    grep -qE "RESUMED .*saved because: handoff\) from resume" job.out \
      && pass "the job handed off (exit 86), and a new job continued from resume/ and finished" \
      || fail "no new job resumed from resume/ (see recipe4.dag.dagman.out)" ;;
esac
echo "(this test's files: $TAG/)"
