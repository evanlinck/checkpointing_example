# Probe results: p7-rerun

Generated 2026-10-02 11:26. Per-test details are in the per-site folders.

## chtc

### P7a-wrapper-exec-bare-vacate

_When the executable is a shell script that execs python, does python receive the soft-kill signal?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 43 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:16:17.8 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.2 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 80) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=2830497 about to exec python3 | WRAPPER run_exec.sh pid=2830967 about to exec python3 | WRAPPER run_exec.sh pid=1483384 about to exec python3

### P7a-wrapper-exec-vacate

_When the executable is a shell script that execs python, does python receive the soft-kill signal?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 43 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:16:17.7 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.7 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 78) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=45 about to exec python3 | WRAPPER run_exec.sh pid=14 about to exec python3 | WRAPPER run_exec.sh pid=139 about to exec python3

### P7e-torchrun-vacate

_OPT-IN, needs pytorch.sif. Does torchrun forward the signal to its workers, and how long does it wait before killing them? Does a worker's exit 85 reach HTCondor as 85?_

- Final job state: terminated ((1) Normal termination (return value 1); Usr 0 00:00:04, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:04, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after ended without an exit record: gap -25 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Trigger did not fire: job ended before the trigger fired.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=None
- torchrun rank 1: signal=None, exit=None
- Wrapper said: WRAPPER run_torchrun.sh pid=141 about to exec torchrun
