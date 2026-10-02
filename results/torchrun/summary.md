# Probe results: torchrun

Generated 2026-10-02 12:44. Per-test details are in the per-site folders.

## chtc

### P7e-torchrun-vacate

_OPT-IN, needs pytorch.sif. When HTCondor sends SIGTERM to torchrun, do the workers receive it? If a worker's save takes 60 s, does torchrun wait for it, or kill the workers first (and after how long)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:12, Sys 0 00:00:02  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after killed (signal SIGTERM, no exit recorded): gap -86 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after killed (signal SIGTERM, no exit recorded): gap 172 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 0: gap -361 s, same host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 12:34:56.1 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 0.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=SIGTERM, exit=0
- torchrun rank 1: signal=SIGTERM, exit=0
- Wrapper said: WRAPPER run_torchrun.sh pid=14 about to exec torchrun | WRAPPER run_torchrun.sh pid=14 about to exec torchrun

### P7f-torchrun-exitcode

_OPT-IN, needs pytorch.sif. If every torchrun worker saves and exits 85, what exit code does HTCondor see from torchrun: 85 (restart) or something else (job completes or fails)?_

- Final job state: terminated ((1) Normal termination (return value 1); Usr 0 00:00:02, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap -30 s, same host, sandbox NEW, restored step None (saved by: None).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=85
- torchrun rank 1: signal=None, exit=85
- job.err shows an error (see 'job.err (last lines)' below): ============================================================
- Wrapper said: WRAPPER run_torchrun.sh pid=15 about to exec torchrun
