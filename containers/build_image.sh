#!/bin/bash
# Build the shared image and copy it to OUT_DIR (on /staging). Run by build_image.sub on a CHTC
# build node, or by hand inside an interactive build job:  bash build_image.sh /staging/<user>/images
set -euo pipefail
OUT_DIR=${1:?usage: build_image.sh <output directory on /staging> [image name]}
NAME=${2:-ckpt-recipes-v1.sif}
if [ -e "$OUT_DIR/$NAME" ]; then
  echo "ERROR: $OUT_DIR/$NAME already exists. OSDF caches by name: pick a new name (e.g. -v2)." >&2
  exit 1
fi
# Apptainer's temporary files go to the job's scratch directory, not the node's small /tmp.
export APPTAINER_TMPDIR=$PWD/apptainer_tmp APPTAINER_CACHEDIR=$PWD/apptainer_cache
mkdir -p "$APPTAINER_TMPDIR" "$APPTAINER_CACHEDIR"
echo "building $NAME at $(date)"
apptainer build "$NAME" recipes.def          # also runs the %test section
apptainer exec "$NAME" cat /opt/versions.txt > versions.txt
mkdir -p "$OUT_DIR"
cp "$NAME" "$OUT_DIR/$NAME.tmp" && mv "$OUT_DIR/$NAME.tmp" "$OUT_DIR/$NAME"
cp versions.txt "$OUT_DIR/${NAME%.sif}.versions.txt"
ls -lh "$OUT_DIR/$NAME"
echo "done at $(date). Use:  container_image = osdf:///chtc${OUT_DIR}/$NAME"
