#!/bin/bash
# Run the same probe DAG several times, spaced out, to see how much a measurement varies
# (/staging is shared with other users, so one run per number isn't enough). Run on the access
# point, in this directory, and leave it running:
#   nohup ./run_rounds.sh pstaging 3 6 --sites chtc,chtc_gpu --tests P15a --maxjobs 2 > rounds_run.txt 2>&1 &
# = 3 rounds of P15a on CHTC CPU and GPU machines, starting 6 h after the previous round FINISHED.
# Each round is an ordinary make_dag.py run tagged <tag>-r1, -r2, ...: results/<tag>-rN/summary.md.
set -euo pipefail
cd "$(dirname "$0")"
TAG=${1:?usage: $0 <tag> <rounds> <hours between rounds> <make_dag.py arguments...>}
ROUNDS=${2:?rounds}
HOURS=${3:?hours between rounds}
shift 3
for i in $(seq 1 "$ROUNDS"); do
  t="$TAG-r$i"
  python3 make_dag.py --tag "$t" --check "$@"
  condor_submit_dag "runs/$t/probes.dag"
  echo "$(date): round $i submitted ($t); waiting for it to finish"
  # DAGMan writes this line when the DAG is done. Checking a local file: no condor_q polling.
  until grep -q "EXITING WITH STATUS" "runs/$t/probes.dag.dagman.out" 2>/dev/null; do sleep 120; done
  echo "$(date): round $i done: results/$t/summary.md"
  [ "$i" -lt "$ROUNDS" ] && sleep $((HOURS * 3600))
done
echo "$(date): all $ROUNDS rounds done"
