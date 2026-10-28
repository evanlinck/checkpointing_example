# Probe results: handoff

Generated 2026-10-27 09:23. Per-test details are in the per-site folders.

## chtc

### P13b-osdf-handoff-exit86

_Same as P13, but the job ends with exit 86 instead of 0 (a planned hand-off: "continue in a new job", since exit 0 should mean training is finished). Does the remapped directory still reach OSDF, and does the job leave the queue normally (return value 86, not a hold or a requeue)?_

- Final job state: terminated ((1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Backup files on OSDF (/staging): state_00000030.json at 09:22:06.1, state_00000060.json at 09:22:06.1, state_00000090.json at 09:22:06.1; probe exits: 85 at 09:20:56.7, 85 at 09:21:28.9, 86 at 09:22:00.0.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## ospool

### P13b-osdf-handoff-exit86

_Same as P13, but the job ends with exit 86 instead of 0 (a planned hand-off: "continue in a new job", since exit 0 should mean training is finished). Does the remapped directory still reach OSDF, and does the job leave the queue normally (return value 86, not a hold or a requeue)?_

- Final job state: terminated ((1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Backup files on OSDF (/staging): state_00000030.json at 09:23:39.5, state_00000060.json at 09:23:36.0, state_00000090.json at 09:23:39.5; probe exits: 85 at 09:22:21.2, 85 at 09:22:55.9, 86 at 09:23:31.1.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
