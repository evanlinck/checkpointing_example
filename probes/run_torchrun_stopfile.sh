#!/bin/bash
# P7h: graceful shutdown that does not depend on any torchrun feature or version.
#
# HTCondor sends the soft-kill signal only to the top process (this script; see P7b/P7c).
# Instead of forwarding SIGTERM to torchrun (which would start torchrun's own kill timer,
# 30 s by default), we just create a STOP file. The workers check for it every step, save,
# append to the RESTART file, and exit. torchrun reports the workers' exit as a failure
# (exit 1), so this script turns "workers asked for a restart" back into exit 85.
STOP="$PWD/STOP_REQUESTED"
RESTART="$PWD/RESTART_REQUESTED"
rm -f "$STOP" "$RESTART"

echo "WRAPPER torch $(python3 -c 'import torch; print(torch.__version__)' 2>/dev/null)"
on_term() {
  echo "WRAPPER got SIGTERM at $(date +%s.%N); creating $STOP (not forwarding the signal)"
  touch "$STOP"
}
trap on_term TERM

torchrun --standalone --nproc_per_node=2 probe.py --stop-file "$STOP" --restart-file "$RESTART" "$@" &
pid=$!
# `wait` returns early whenever a trapped signal arrives, so keep waiting until torchrun is gone.
while true; do
  wait "$pid"; rc=$?
  kill -0 "$pid" 2>/dev/null || break
done
echo "WRAPPER torchrun exited with $rc at $(date +%s.%N)"

if [ -s "$RESTART" ]; then
  echo "WRAPPER workers saved and asked for a restart:"; cat "$RESTART"
  rm -f "$RESTART" "$STOP"
  exit 85
fi
exit "$rc"
