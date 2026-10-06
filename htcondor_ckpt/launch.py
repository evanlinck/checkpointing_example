#!/usr/bin/env python3
"""
launch.py: run a multi-process launcher (torchrun, accelerate, deepspeed, mpirun...)
so that HTCondor's stop signal and exit code 85 still work.

Why this is needed (measured on CHTC, docs/environment.md section 6):
  - HTCondor sends SIGTERM only to the job's top process.
  - torchrun, given SIGTERM, passes it to its workers but kills them ~30 s later:
    a longer save is cut off.
  - torchrun turns a worker's exit 85 ("restart me") into exit 1, so HTCondor
    thinks the job finished (or failed).

What this wrapper does instead (it relies on no launcher feature or version):
  1. Starts the launcher in its own process group, with two environment variables:
       HTCONDOR_CKPT_STOP_FILE     the workers watch for this file
       HTCONDOR_CKPT_RESTART_FILE  the workers write here when they exit to be restarted
     (stop.StopPolicy reads both automatically.)
  2. On SIGTERM it creates the stop file. It does NOT forward the signal, so the
     launcher never starts its kill timer. The workers see the file at their next
     step, save, and exit.
  3. When the launcher exits: if any worker asked for a restart, exit 85; otherwise
     pass the launcher's exit code through.

Use it in the submit file (keep the `exec`, so this wrapper is the top process):
    shell = exec python3 launch.py -- torchrun --standalone --nproc_per_node=4 train.py --resume auto

Standalone: standard library only, no imports from the other htcondor_ckpt modules.
"""

import os
import signal
import subprocess
import sys

EXIT_RESTART = 85
STOP_FILE_ENV = "HTCONDOR_CKPT_STOP_FILE"
RESTART_FILE_ENV = "HTCONDOR_CKPT_RESTART_FILE"


def main(argv):
    if "--" not in argv or argv.index("--") == len(argv) - 1:
        print("usage: launch.py [--stop-file PATH] [--restart-file PATH] -- <launcher command ...>",
              file=sys.stderr)
        return 2
    opts, command = argv[:argv.index("--")], argv[argv.index("--") + 1:]
    stop_file = os.path.abspath("STOP_REQUESTED")
    restart_file = os.path.abspath("RESTART_REQUESTED")
    for i, opt in enumerate(opts):
        if opt == "--stop-file":
            stop_file = os.path.abspath(opts[i + 1])
        elif opt == "--restart-file":
            restart_file = os.path.abspath(opts[i + 1])
    for path in (stop_file, restart_file):  # leftovers from an earlier run in this sandbox
        if os.path.exists(path):
            os.remove(path)

    def on_signal(signum, frame):
        # Don't forward the signal: that would start the launcher's own kill timer.
        print("launch.py: received %s; created %s (signal not forwarded)"
              % (signal.Signals(signum).name, stop_file), flush=True)
        open(stop_file, "a").close()

    signal.signal(signal.SIGTERM, on_signal)

    env = dict(os.environ, **{STOP_FILE_ENV: stop_file, RESTART_FILE_ENV: restart_file})
    # start_new_session: the launcher gets its own process group, so a signal sent to
    # our whole group (some schedulers do that) still reaches only this wrapper.
    child = subprocess.Popen(command, env=env, start_new_session=True)
    while True:
        try:
            code = child.wait()
            break
        except KeyboardInterrupt:  # Ctrl-C when testing by hand: treat like SIGTERM
            on_signal(signal.SIGINT, None)

    restart = os.path.exists(restart_file) and os.path.getsize(restart_file) > 0
    if restart:
        with open(restart_file) as f:
            print("launch.py: launcher exited %d; workers asked for a restart:\n%s"
                  % (code, f.read().rstrip()), flush=True)
        os.remove(restart_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        return EXIT_RESTART
    print("launch.py: launcher exited %d" % code, flush=True)
    return code if code >= 0 else 128 - code  # killed by signal N -> 128 + N, like a shell


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
