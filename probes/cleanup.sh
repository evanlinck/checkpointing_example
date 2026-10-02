#!/bin/bash
# cleanup.sh - delete probe data from /staging (keeps the container images).
# REQUIRED first:  export PROBE_STAGING_DIR=/staging/<username>   (your /staging directory)
#   bash cleanup.sh          show what would be deleted
#   bash cleanup.sh --yes    delete it
set -euo pipefail
if [ -z "${PROBE_STAGING_DIR:-}" ]; then
  echo "ERROR: PROBE_STAGING_DIR is not set." >&2
  echo "       Run:  export PROBE_STAGING_DIR=/staging/<username>" >&2
  echo "       (add that line to ~/.bashrc on the access point so it is always set)" >&2
  exit 1
fi
STAGING="$PROBE_STAGING_DIR/ckpt-probes"
du -sh "$STAGING"/runs "$STAGING"/ckptdest 2>/dev/null || true
if [ "${1:-}" = "--yes" ]; then
  rm -rf "$STAGING"/runs/* "$STAGING"/ckptdest
  echo "Deleted probe runs from $STAGING (images kept)."
else
  echo "Dry run. Re-run with --yes to delete the above."
fi
