#!/bin/bash
# P7a: the recommended wrapper. `exec` REPLACES bash with python, so python is
# the process HTCondor started and it receives the soft-kill signal directly.
echo "WRAPPER run_exec.sh pid=$$ about to exec python3"
exec python3 probe.py "$@"
