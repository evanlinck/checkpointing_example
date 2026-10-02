# Probe results: torchrun3

Generated 2026-10-02 13:29. Per-test details are in the per-site folders.

## chtc

### P7h-torchrun-stopfile-vacate

_OPT-IN, needs pytorch.sif. If a wrapper turns SIGTERM into a STOP file instead of forwarding it, do the torchrun workers finish a 60 s save (no 30 s kill)? Does the wrapper's mapping make a voluntary exit 85 restart the job in place, and does the SIGTERM save survive eviction?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:21, Sys 0 00:00:06  -  Total Remote Usage;)
- Executions seen by the probe: 6; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -70 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 12 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap -134 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 47 s, DIFFERENT host, sandbox NEW, restored step 84 (saved by: signal).
- Restart after exit 0: gap 0 s, same host, sandbox NEW, restored step 84 (saved by: signal).
- Trigger vacate fired at 13:27:21.4 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +60.9 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 84 (saved by: signal) -> the SIGTERM save (step 84) SURVIVED.
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=0
- torchrun rank 1: signal=None, exit=0
- job.err shows an error (see 'job.err (last lines)' below):   cpu = _conversion_method_template(device=torch.device("cpu"))
- Wrapper said: WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 1 at 1790965556.171341573 | WRAPPER workers saved and asked for a restart: | WRAPPER torch 2.14.1+cpu | WRAPPER got SIGTERM at 1790965641.396042193; creating /var/lib/condor/execute/slot1/dir_3898946/scratch/STOP_REQUESTED (not forwarding the signal) | WRAPPER torchrun exited with 1 at 1790965702.968469630 | WRAPPER workers saved and asked fo
