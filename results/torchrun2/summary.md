# Probe results: torchrun2

Generated 2026-10-02 13:17. Per-test details are in the per-site folders.

## chtc

### P7g-torchrun-shutdown-timeout-vacate

_OPT-IN, needs pytorch.sif. With TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120, does torchrun let the workers finish a 60 s save after SIGTERM (P7e showed it kills them after ~30 s by default)? Does the installed torch support the setting at all?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:09, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:18, Sys 0 00:00:04  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -139 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 37 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 0: gap -361 s, same host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 13:09:48.7 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 60.9 s after the signal.
- Next execution restored step None (saved by: None) -> the SIGTERM save (step 79) was LOST.
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=SIGTERM, exit=0
- torchrun rank 1: signal=SIGTERM, exit=0
- Wrapper said: WRAPPER torch 2.14.1+cpu; torchrun --shutdown-timeout supported: yes; TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120 | WRAPPER run_torchrun.sh pid=76 about to exec torchrun | WRAPPER torch 2.14.1+cpu; torchrun --shutdown-timeout supported: yes; TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120 | WRAPPER run_torchrun.sh pid=14 about to exec torchrun

### P7h-torchrun-stopfile-vacate

_OPT-IN, needs pytorch.sif. If a wrapper turns SIGTERM into a STOP file instead of forwarding it, do the torchrun workers finish a 60 s save (no 30 s kill)? Does the wrapper's mapping make a voluntary exit 85 restart the job in place, and does the SIGTERM save survive eviction?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:06, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:22, Sys 0 00:00:05  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -90 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 80 s, DIFFERENT host, sandbox NEW, restored step 30 (saved by: voluntary).
- Restart after exit 0: gap 0 s, same host, sandbox NEW, restored step 30 (saved by: voluntary).
- Trigger vacate fired at 13:10:03.7 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=0
- torchrun rank 1: signal=None, exit=0
- job.err shows an error (see 'job.err (last lines)' below):   cpu = _conversion_method_template(device=torch.device("cpu"))
- Wrapper said: WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 1 at 1790964602.467652729 | WRAPPER workers saved and asked for a restart: | WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 0 at 1790964682.857533974
