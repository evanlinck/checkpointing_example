#!/bin/bash
# HTCondor tests for recipe 1. Run on the access point, in this directory.
#
# Short runs (3,000 steps with a 0.1 s pause after each, so at least ~5 minutes on any GPU) with a
# timed checkpoint every 2 minutes, so each test takes about 10-15 minutes of one GPU. The pause
# matters: without it a fast GPU (A100/H100) finishes 3,000 steps before the test interrupts it.
#
#   ./test_htcondor.sh job_chtc.sub timed          # timed exits only: each one resumes, and the run finishes
#   ./test_htcondor.sh job_chtc.sub vacate         # condor_vacate_job: resumes from the save made after SIGTERM
#   ./test_htcondor.sh job_chtc.sub hold           # condor_hold + condor_release: the same
#   ./test_htcondor.sh job_chtc.sub fast           # condor_vacate_job -fast: resumes from the last timed checkpoint
#   ./test_htcondor.sh job_chtc.sub inspect        # vacate + hold, copy out the kept checkpoint (condor_evicted_files)
#   ./test_htcondor.sh job_chtc_staging.sub vacate # checkpoints on /staging: the save after SIGTERM survives
#   ./test_htcondor.sh job_chtc_staging.sub fast   # /staging: resumes from the newest periodic save
#   ./test_htcondor.sh job_chtc_backup.sub backup  # condor_rm once a backup exists, resubmit: resumes from the backup
#   ./test_htcondor.sh job_ospool.sub timed        # (and vacate) on the OSPool
#   ./test_htcondor.sh job_chtc.sub reference      # no interruptions: the baseline for compare_runs.py
#
# Resume equivalence on a GPU: run `reference` twice and `vacate` once (in parallel is fine), then
#   python3 compare_runs.py --reference test_job_chtc_reference_<time>_<pid>.outputs \
#       --reference <the other reference's .outputs> --resumed test_job_chtc_vacate_<time>_<pid>.outputs
# (each test prints its directory names when it finishes; `ls -d test_*.outputs` lists them)
# Each spool test gets its own <test name>.checkpoints/ and <test name>.outputs/ here, so tests
# running at the same time don't overwrite each other's results.
#
# Your locations come from environment variables, so no personal path is stored in the repo:
#   export RECIPE1_IMAGE=osdf:///chtc/staging/<user>/<path>/recipe1.sif
#   export RECIPE1_DATA_DIR=/staging/<user>/tinystories      # where prepare_data.py wrote train.bin / val.bin
#   export RECIPE1_TEST_DIR=/staging/<user>/recipe1-tests     # scratch space for /staging and backup tests
#
# Like recipe 0's test, it only reads the job's own event log (no condor_q polling),
# sends one HTCondor command, waits for the job to finish, and checks its output.
set -euo pipefail
SUB=${1:?usage: $0 <submit file> <timed|vacate|hold|fast|inspect|backup|reference>}
MODE=${2:?usage: $0 <submit file> <timed|vacate|hold|fast|inspect|backup|reference>}
for v in RECIPE1_IMAGE RECIPE1_DATA_DIR RECIPE1_TEST_DIR; do
  if [ -z "${!v:-}" ]; then echo "ERROR: set $v first (see the top of this script)" >&2; exit 1; fi
done
if [ ! -d htcondor_ckpt ]; then
  echo "ERROR: htcondor_ckpt/ is not in this directory. Copy it here first:  cp -r ../../htcondor_ckpt ." >&2
  exit 1
fi
# The time plus this script's process id: tests started in the same second still get different names.
TAG="test_$(basename "$SUB" .sub)_${MODE}_$(date +%H%M%S)_$$"
RUN="$RECIPE1_TEST_DIR/$TAG"    # per-test directory on /staging (used by the staging and backup tests)

# The same command as the submit file, with test settings: 3,000 steps with a 0.1 s pause each
# (a minimum run time, whatever the GPU), a timed checkpoint every 120 s, fewer evaluations,
# no sample stories, and deterministic kernels so that test runs can be compared with each other.
# A reference run gets no timed checkpoint (a limit of a day: it never comes).
LIMIT=120; [ "$MODE" = reference ] && LIMIT=86400
CMD="export HOME=\$PWD; exec python3 train.py --config config.yaml --resume auto --set max_steps=3000 --set step_delay=0.1 --set max_runtime_seconds=$LIMIT --set eval_every_steps=500 --set sample_stories=false --set deterministic=true"
INPUTS="train.py, model.py, config.yaml, htcondor_ckpt, osdf:///chtc$RECIPE1_DATA_DIR/train.bin, osdf:///chtc$RECIPE1_DATA_DIR/val.bin"
DIRS=""     # spool tests: this test's own checkpoint and output directories (set in submit())
case "$SUB" in
  *staging*) CMD="$CMD --set data_dir=$RECIPE1_DATA_DIR --set ckpt_dir=$RUN/checkpoints --set out_dir=$RUN/outputs --set keep_checkpoints=2 --set save_every_minutes=1"
             INPUTS="train.py, model.py, config.yaml, htcondor_ckpt" ;;
  *backup*)  CMD="$CMD --set backup_dir=$RUN/backups --set backup_every_hours=0"; DIRS=spool ;;
  *)         DIRS=spool ;;
esac
# A reference run must not be interrupted, so keep it off backfill slots (where the GPU's owner can
# evict it): without +is_resumable it runs in the GPU Lab, which a 15-minute job fits easily.
NOBACKFILL=(); [ "$MODE" = reference ] && NOBACKFILL=(-a "+is_resumable = false")

submit() {   # submit $SUB with the test settings; prints the job id. $1 = name for this job's files
  local cmd=$CMD extra=()
  if [ -n "$DIRS" ]; then   # spool: <name>.checkpoints and <name>.outputs, in the job and back here
    cmd="$CMD --set ckpt_dir=$1.checkpoints --set out_dir=$1.outputs"
    extra=(-a "transfer_checkpoint_files = $1.checkpoints, $1.outputs" -a "transfer_output_files = $1.checkpoints, $1.outputs")
  fi
  condor_submit "$SUB" -a "shell = $cmd" -a "transfer_input_files = $INPUTS" -a "container_image = $RECIPE1_IMAGE" \
    ${extra[@]+"${extra[@]}"} ${NOBACKFILL[@]+"${NOBACKFILL[@]}"} \
    -a "log = $1.log" -a "output = $1.out" -a "error = $1.err" -a "stream_output = true" -a "stream_error = true" \
    | awk '/submitted to cluster/ {print $NF}' | tr -d . | sed 's/$/.0/'
}
wait_running() { until grep -q "^001 " "$1.log" 2>/dev/null; do sleep 15; done; }

job=$(submit "$TAG")
echo "submitted $job ($MODE); event log: $TAG.log"
wait_running "$TAG"
echo "running since $(date +%T) on $(grep -A1 '^001 ' "$TAG.log" | grep -o 'alias=[^&]*' | head -1 | cut -d= -f2); waiting 200 s so a timed checkpoint exists first"
sleep 200

# If the job already ended (e.g. it crashed on start-up), say so instead of failing on "job not found".
if grep -q "^005 " "$TAG.log"; then
  echo "FAIL: the job ended before the test could interrupt it:"
  grep -A1 "^005 " "$TAG.log" | tail -1
  echo "--- end of $TAG.err ---"; tail -5 "$TAG.err"
  exit 1
fi

case "$MODE" in
  timed|reference) ;;
  vacate) condor_vacate_job "$job" ;;
  fast)   condor_vacate_job -fast "$job" ;;
  hold)   condor_hold "$job"
          until grep -q "^012 " "$TAG.log"; do sleep 15; done
          sleep 20
          condor_release "$job" ;;
  inspect)
          condor_vacate_job "$job"
          condor_hold "$job"
          until grep -q "^012 " "$TAG.log"; do sleep 15; done
          mkdir -p "$TAG.evicted"
          (cd "$TAG.evicted" && condor_evicted_files get "$job") || echo "condor_evicted_files failed"
          (cd "$TAG.evicted" && find . -type f -exec ls -l {} \;) | tee "$TAG.evicted.txt"
          condor_release "$job" ;;
  backup)
          echo "waiting for a backup in $RUN/backups ..."
          until ls -d "$RUN"/backups/step_* >/dev/null 2>&1; do sleep 15; done
          echo "backup exists: $(ls -d "$RUN"/backups/step_*); removing the job (its spooled checkpoint goes with it)"
          condor_rm "$job"
          until grep -q "^009 " "$TAG.log"; do sleep 15; done
          TAG="${TAG}_resubmitted"
          job=$(submit "$TAG")
          echo "resubmitted as $job; event log: $TAG.log" ;;
  *)      echo "unknown mode $MODE"; exit 2 ;;
esac
echo "$MODE at $(date +%T); waiting for the job to finish (condor_wait reads the event log)"
condor_wait "$TAG.log" "$job" >/dev/null

echo "--- what the job reported ($TAG.out) ---"
grep -E "^(STARTING|RESUMED|SAVED|BACKUP|EXIT|DONE|stop:|save finished|first step|WARNING)" "$TAG.out" || true

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; exit 1; }
grep -q "^DONE" "$TAG.out" || fail "the job did not finish"
case "$MODE" in
  reference)
    grep -q "^RESUMED" "$TAG.out" && fail "the reference run was interrupted (see $TAG.log); run it again"
    pass "uninterrupted run finished; metrics in $TAG.outputs/metrics.jsonl" ;;
  timed)
    n=$(grep -c "reason: timed" "$TAG.out" || true)
    [ "$n" -ge 2 ] && pass "$n timed checkpoints, each resumed, and the run finished" || fail "only $n timed checkpoints" ;;
  vacate|hold)
    grep -q "reason: signal" "$TAG.out" || fail "no save after SIGTERM"
    grep -q "saved because: signal" "$TAG.out" && pass "resumed from the save made after SIGTERM" \
      || fail "the save made after SIGTERM was not restored" ;;
  fast)
    grep -q "reason: signal" "$TAG.out" && fail "unexpected: a save after a signal (-fast sends none)"
    grep -qE "saved because: (timed|periodic)" "$TAG.out" && pass "resumed from the last timed/periodic checkpoint after the hard kill" \
      || fail "never resumed from a timed or periodic checkpoint" ;;
  inspect)
    grep -q "state.pt$" "$TAG.evicted.txt" && pass "condor_evicted_files returned the checkpoint (see $TAG.evicted/)" \
      || fail "condor_evicted_files did not return a checkpoint (see $TAG.evicted.txt)"
    grep -q "saved because: signal" "$TAG.out" && pass "and the released job resumed from the save made after SIGTERM" \
      || fail "the released job did not resume from the save made after SIGTERM" ;;
  backup)
    grep -q "RESUMED .* from $RUN/backups" "$TAG.out" && pass "the resubmitted job resumed from the /staging backup" \
      || fail "the resubmitted job did not resume from the backup" ;;
esac
[ -n "$DIRS" ] && echo "(this test's checkpoints and outputs: $TAG.checkpoints/, $TAG.outputs/)"
echo "(test files on /staging, if any: $RUN; remove them when done)"
