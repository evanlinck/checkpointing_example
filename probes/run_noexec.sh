#!/bin/bash
# P7b: the common mistake. bash stays in charge and python is its child.
# The trap only logs; it does NOT forward the signal. While python runs in the
# foreground, bash defers the trap until python exits, so the log line will
# appear late (or never, if both are SIGKILLed).
echo "WRAPPER run_noexec.sh pid=$$ starting python3 as a child"
trap 'echo "WRAPPER bash received SIGTERM at $(date +%s.%N)"' TERM
python3 probe.py "$@"
rc=$?
echo "WRAPPER python exited with $rc at $(date +%s.%N); wrapper exiting with the same code"
exit $rc
