#!/bin/bash
# An alternative to the submit file's `shell` line (use: executable = run.sh).
# `exec` replaces this shell with Python, so Python is the process HTCondor
# signals. HTCondor sends SIGTERM only to the top process: without `exec`, bash
# would get it, and Python would never know it should save before the kill
# (measured; docs/environment.md §6).
exec python3 train.py "$@"
