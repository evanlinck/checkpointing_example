#!/bin/bash
# setup.sh - one-time preparation for the probes.
#
# REQUIRED first:  export PROBE_STAGING_DIR=/staging/<username>   (your /staging directory)
#
#   bash setup.sh dirs                 on ap2002: create the /staging directories
#   bash setup.sh build [--with-torch] inside an interactive build job (see build.sub):
#                                      build the container image(s) into /staging
#
# CHTC asks that images be built in an interactive build job, not on the access point:
#   condor_submit -i build.sub      then, once it starts:   bash setup.sh build
set -euo pipefail
if [ -z "${PROBE_STAGING_DIR:-}" ]; then
  echo "ERROR: PROBE_STAGING_DIR is not set." >&2
  echo "       Run:  export PROBE_STAGING_DIR=/staging/<username>" >&2
  echo "       (add that line to ~/.bashrc on the access point so it is always set)" >&2
  exit 1
fi
STAGING="$PROBE_STAGING_DIR/ckpt-probes"

case "${1:-}" in
  dirs)
    mkdir -p "$STAGING/images" "$STAGING/runs"
    echo "Created $STAGING/{images,runs}"
    ;;
  build)
    mkdir -p "$STAGING/images"
    # A plain Python image: probe.py needs nothing beyond the standard library.
    if [ ! -f "$STAGING/images/python312.sif" ]; then
      apptainer build python312.sif docker://python:3.12-slim
      mv python312.sif "$STAGING/images/"
    fi
    if [ "${2:-}" = "--with-torch" ] && [ ! -f "$STAGING/images/pytorch.sif" ]; then
      # Only for the opt-in torchrun test (P7e). CPU-only wheels keep it small.
      apptainer build pytorch.sif pytorch-cpu.def
      mv pytorch.sif "$STAGING/images/"
    fi
    ls -lh "$STAGING/images"
    ;;
  *)
    sed -n '2,10p' "$0"; exit 1 ;;
esac
