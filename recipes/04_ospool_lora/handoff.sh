#!/bin/bash
# handoff.sh - the DAG's helper (recipe4.dag). It runs on the access point, before and after
# each training job, in this directory.
#
#   handoff.sh pre           before a job: make sure the directories the job lists exist
#   handoff.sh post <code>   after a job, with its exit code: decide what the DAG does next
#
# What the exit codes mean (train.py):
#    0  training finished                -> this script exits 0: the DAG is done
#   86  "continue in a new job": the job  -> move the job's checkpoints to resume/, where the
#       saved before the access point's      next job looks for them, and exit 1: the DAG's
#       limit on a job's total time          RETRY submits a new job
#   anything else: an error              -> exit 2: RETRY ... UNLESS-EXIT 2 stops retrying,
#                                           so a broken job isn't started again and again
set -u
case "${1:-}" in
  pre)
    mkdir -p resume checkpoints outputs
    exit 0
    ;;
  post)
    code="${2:-}"
    if [ "$code" = 0 ]; then
      echo "training finished"
      exit 0
    elif [ "$code" = 86 ]; then
      # The job's final output brought its checkpoints back here. They become the next job's
      # starting point (resume/), and checkpoints/ starts empty in the new job.
      if [ ! -d checkpoints ]; then
        echo "exit 86 but no checkpoints/ came back: not retrying (see job.err)"
        exit 2
      fi
      rm -rf resume.old
      [ -d resume ] && mv resume resume.old
      mv checkpoints resume && rm -rf resume.old
      echo "handed off: checkpoints/ -> resume/; asking the DAG for a new job"
      exit 1
    else
      echo "the job ended with exit code $code: an error, so no new job (see job.err)"
      exit 2
    fi
    ;;
  *)
    echo "usage: $0 pre | post <exit code>" >&2
    exit 2
    ;;
esac
