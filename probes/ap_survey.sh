#!/bin/bash
# ap_survey.sh - read-only survey of an access point (AP) and its pool, for OSPool checkpointing advice.
#
# Answers, without submitting any jobs:
#   spool.txt           where SPOOL is, how big and full, transfer limits, what holds/removes jobs
#   transfer_queue.txt  the schedd's file-transfer queue (are uploads throttled?)
#   held_ckpt_jobs.txt  self-checkpointing jobs on hold now: how many days held, by hold code
#   glideins.txt        glidein policy, hours left before glideins retire/die, sites that preempt
#   gpus.txt            the pool's GPUs: type, count per slot, memory, compute capability
#   history.txt         one line per finished job (no owners, no job ids), for ap_survey_summary.py
#   holds.txt           most common hold reasons among self-checkpointing jobs
#   job.txt             (--job only) checkpoint/spool attributes of one of your own jobs
#
# Run it on the AP, from this directory (it needs redact.py next to it):
#   nohup ./ap_survey.sh > ap_survey_run.txt 2>&1 &
#   nohup ./ap_survey.sh --job 1234.0 --history-days 7 > ap_survey_run.txt 2>&1 &
# Then:  python3 ap_survey_summary.py results/ap-survey/<ap>
#
# Options:
#   --out DIR           output directory (default: results/ap-survey/<short host name>)
#   --job ID            also look at one of your own running self-checkpointing jobs
#   --history-days N    days of job history to read (default 30; 0 skips history.txt and holds.txt)
#
# Load: one condor_q (with a constraint), a few condor_status queries of the collector,
# and condor_history, which reads the AP's local history files (no schedd queries). On a busy AP
# 30 days of history can take several minutes, hence nohup.
#
# Privacy: no command prints Owner or job ids. Every file except history.txt (numbers only) goes
# through redact.py (user names, home and /ospool data paths, IPs, execute host names), and also
# loses user@ names.
# Check the files before sharing them.

set -uo pipefail   # no -e: a failing block is recorded and the survey moves on

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/results/ap-survey/$(hostname -s)"
JOB=""
DAYS=30
while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    --job) JOB="$2"; shift 2 ;;
    --history-days) DAYS="$2"; shift 2 ;;
    -h|--help) sed -n '2,32p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
mkdir -p "$OUT"

# Hold reasons and config can name users as user@host; redact.py only knows the current user.
redact() { sed -E 's/[A-Za-z0-9_.-]+@([A-Za-z0-9.-]+)/<user>@\1/g' | python3 "$HERE/redact.py" -; }

# block NAME [raw]: run the commands in the function NAME_cmds, save redacted output to NAME.txt.
# "raw" skips redaction: only for history.txt, which holds nothing but numbers and counts and can be
# too large to redact in memory.
block() {
  local name="$1" filter=redact t0=$SECONDS
  [ "${2:-}" = raw ] && filter=cat
  echo "== $name"
  { echo "# $name, $(date -u +%Y-%m-%dT%H:%M:%SZ), $(hostname -f)"; "${name}_cmds" 2>&1; } | $filter > "$OUT/$name.txt"
  echo "   $OUT/$name.txt ($((SECONDS - t0)) s, $(wc -l < "$OUT/$name.txt") lines)"
}
# show CMD...: print the command, then run it; a failure is noted, not fatal.
show() { echo; echo "\$ $*"; "$@" || echo "(exit code $?)"; }

SPOOL_DIR="$(condor_config_val SPOOL 2>/dev/null)"

spool_cmds() {
  show condor_version
  show condor_config_val SPOOL
  show df -h "$SPOOL_DIR"
  show ls -ld "$SPOOL_DIR"
  # Values from the running schedd (what it actually uses), then everything related in the config.
  # Undefined knobs print "Not defined"; that is an answer too (no limit).
  for k in MAX_TRANSFER_OUTPUT_MB MAX_TRANSFER_INPUT_MB MAX_CONCURRENT_UPLOADS MAX_CONCURRENT_DOWNLOADS \
           SYSTEM_PERIODIC_HOLD SYSTEM_PERIODIC_REMOVE SYSTEM_PERIODIC_RELEASE; do
    echo; echo "\$ condor_config_val -schedd $k"
    condor_config_val -schedd "$k" 2>&1 || true
  done
  # -dump only shows the first line of multi-line values; print the ones that matter in full.
  for k in JOB_TRANSFORM_JobDuration JOB_TRANSFORM_DurationIn CKPT_JOB_DURATION JOB_TRANSFORM_ReleaseLimit \
           MAX_TRANSFER_LIFETIME MAX_TRANSFER_QUEUE_AGE CHECKPOINT_DESTINATION_MAPFILE; do
    echo; echo "\$ condor_config_val $k"
    condor_config_val "$k" 2>&1 || true
  done
  local mapfile; mapfile="$(condor_config_val CHECKPOINT_DESTINATION_MAPFILE 2>/dev/null)"
  [ -n "$mapfile" ] && show cat "$mapfile"
  echo; echo "\$ condor_config_val -dump | grep -iE 'SPOOL|CHECKPOINT|TRANSFER|PERIODIC|JOB_TRANSFORM|SUBMIT_REQUIREMENT'"
  condor_config_val -dump 2>&1 | grep -iE 'SPOOL|CHECKPOINT|TRANSFER|PERIODIC|JOB_TRANSFORM|SUBMIT_REQUIREMENT'
}

transfer_queue_cmds() {
  # The schedd's ad can be named after an alias (e.g. ap40...) rather than hostname -f, so list the
  # schedds first, then read this AP's ad from the file the schedd writes, or from the collector.
  show condor_status -schedd -af Name Machine
  local ad_file; ad_file="$(condor_config_val SCHEDD_DAEMON_AD_FILE 2>/dev/null)"
  echo; echo "\$ grep TransferQueue/FileTransfer $ad_file"
  if [ -r "$ad_file" ]; then
    grep -iE 'TransferQueue|FileTransfer.*(Upload|Download)' "$ad_file" | sort
  else
    echo "(not readable; trying the collector)"
    local short; short="$(hostname -s)"
    condor_status -schedd -const "regexp(\"$short\", Machine) || regexp(\"$short\", Name)" -l 2>&1 \
      | grep -iE 'TransferQueue|FileTransfer.*(Upload|Download)' | sort
  fi
}

held_ckpt_jobs_cmds() {
  echo "# count, days on hold, HoldReasonCode, HoldReasonSubCode (self-checkpointing jobs only)"
  echo "\$ condor_q -allusers -const 'JobStatus == 5 && SuccessCheckpointExitCode =!= undefined' -af ..."
  condor_q -allusers -const 'JobStatus == 5 && SuccessCheckpointExitCode =!= undefined' \
    -af 'int((time() - EnteredCurrentStatus) / 86400)' HoldReasonCode HoldReasonSubCode 2>&1 \
    | sort -n | uniq -c
  echo; echo "# distinct submitters among those held jobs (a count only, no names)"
  condor_q -allusers -const 'JobStatus == 5 && SuccessCheckpointExitCode =!= undefined' -af Owner 2>/dev/null \
    | sort -u | wc -l
  echo; echo "# all self-checkpointing jobs in the queue, by JobStatus (1 idle, 2 running, 5 held)"
  condor_q -allusers -const 'SuccessCheckpointExitCode =!= undefined' -af JobStatus 2>&1 | sort | uniq -c
}

glideins_cmds() {
  echo "# One slot's policy attributes (which GLIDEIN_* deadlines exist?)"
  condor_status -limit 1 -l 2>&1 \
    | grep -iE '^(GLIDEIN_(ToRetire|ToDie|Max_Walltime|Retire_Time|Max_Idle|Site|SiteWMS)|SiteWMS_WN_Preempt|MaxJobRetirementTime|MachineMaxVacateTime|Disk|Memory|TotalDisk|TotalMemory|PREEMPT|WANT_HOLD|KILL|CondorVersion) '
  echo; echo "# count, site, hours until GLIDEIN_ToRetire, hours until GLIDEIN_ToDie (all slots now)"
  condor_status -const 'GLIDEIN_ToRetire =!= undefined' \
    -af GLIDEIN_Site 'int((GLIDEIN_ToRetire - time()) / 3600)' 'int((GLIDEIN_ToDie - time()) / 3600)' 2>&1 \
    | sort | uniq -c | sort -k2,2 -k3,3n
  echo; echo "# count, SiteWMS_WN_Preempt, site"
  condor_status -af SiteWMS_WN_Preempt GLIDEIN_Site 2>&1 | sort | uniq -c | sort -rn
}

gpus_cmds() {
  echo "# count, GPU name, GPUs in the slot, memory (MB), compute capability"
  condor_status -const 'TotalGPUs > 0' \
    -af GPUs_DeviceName TotalGPUs GPUs_GlobalMemoryMb GPUs_Capability 2>&1 \
    | sort | uniq -c | sort -rn
}

# Tab-separated, one line per job; read by ap_survey_summary.py (column names in the header).
HIST_ATTRS=(JobStatus RequestGPUs NumJobStarts NumShadowStarts NumHolds RemoteWallClockTime CommittedTime
            SuccessCheckpointExitCode NumVacatesByReason NumHoldsByReason MachineAttrGLIDEIN_Site0)
history_cmds() {
  local since=$(( $(date +%s) - DAYS * 86400 ))
  echo "# columns: ${HIST_ATTRS[*]}"
  condor_history -completedsince "$since" -af:t "${HIST_ATTRS[@]}" 2>&1
}

holds_cmds() {
  echo "# count, HoldReasonCode, HoldReasonSubCode, HoldReason (first 150 characters); last hold of"
  echo "# finished self-checkpointing jobs that were ever held, newest 20000"
  condor_history -limit 20000 -const 'SuccessCheckpointExitCode =!= undefined && NumHolds > 0' \
    -af:t HoldReasonCode HoldReasonSubCode HoldReason 2>&1 \
    | awk -F'\t' 'BEGIN { OFS = "\t" } { gsub(/[0-9][0-9][0-9]+/, "N", $3); print }' \
    | cut -c1-150 | sort | uniq -c | sort -rn | head -40
}

job_cmds() {
  echo "\$ condor_q $JOB -l | grep -iE 'checkpoint|spool|TransferOut|TransferCheckpoint|DiskUsage|PeriodicRemove|PeriodicHold'"
  condor_q "$JOB" -l 2>&1 | grep -iE 'checkpoint|spool|TransferOut|TransferCheckpoint|DiskUsage|PeriodicRemove|PeriodicHold' | sort
  # HTCondor keeps job C.P's spooled files in $SPOOL/<C mod 10000>/<P>/clusterC.procP.subproc0*
  local c="${JOB%%.*}" p="${JOB#*.}"
  [ "$p" = "$JOB" ] && p=0
  show ls -la "$SPOOL_DIR/$((c % 10000))/$p/"
  show du -sb "$SPOOL_DIR/$((c % 10000))/$p/"
}

block spool
block transfer_queue
block held_ckpt_jobs
block glideins
block gpus
[ -n "$JOB" ] && block job
if [ "$DAYS" -gt 0 ]; then
  block history raw
  block holds
fi
echo "Done. Next: python3 $HERE/ap_survey_summary.py $OUT"
