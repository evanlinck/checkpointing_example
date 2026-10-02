# Probe results: core-chtc

Generated 2026-10-02 08:48. Per-test details are in the per-site folders.

## chtc

### P2a-save85-hold-release

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 111 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger hold-release fired at 13:46:49.8 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.0 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2a-save85-vacate-fast

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 43 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 13:46:49.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -6.3 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2a-save85-vacate

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 81 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:47:03.1 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.8 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 162) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Does condor_submit accept the combination, and is step B transferred on eviction?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 96 s, DIFFERENT host, sandbox NEW, restored step 162 (saved by: signal).
- Trigger vacate fired at 13:47:05.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 162 (saved by: signal) -> the SIGTERM save (step 162) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2c-save0-vacate

_Safety check: if a job saves and exits 0 in response to a vacate, does HTCondor wrongly treat the job as complete?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 0: gap 28 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:56:36.4 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 0, 0.5 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2d-default-vacate

_Baseline: a job with no SIGTERM handler dies on the signal. Does it restart from the last voluntary checkpoint (A)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 45 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:57:52.0 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 0.9 s after the signal = effective grace before SIGKILL.
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3a-grace-default-hold-release

_How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 70 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger hold-release fired at 14:07:24.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3a-grace-default-vacate

_How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 111 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:05:38.5 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 598.7 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3b-grace-jmvt60-vacate

_Is job_max_vacate_time = 60 honoured (grace about 60 s)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 7 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 66 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:19:55.3 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 60.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3c-grace-jmvt900-vacate

_If a job asks for job_max_vacate_time = 900, is it capped by the machine's MachineMaxVacateTime?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 171 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:21:25.4 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 899.2 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3d-killsig-usr1-vacate

_Is kill_sig honoured? The job asks for SIGUSR1; does it receive SIGUSR1 instead of SIGTERM?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGUSR1, no exit recorded): gap 58 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:21:25.5 (AP clock).
- Evicted execution received SIGUSR1 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.4 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P4a-staging-bare-vacate

_Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 19 s, DIFFERENT host, sandbox NEW, restored step 86 (saved by: signal).
- Trigger vacate fired at 13:58:09.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.1 s after the signal.
- Next execution restored step 86 (saved by: signal) -> the SIGTERM save (step 86) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P4a-staging-vacate

_Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 82 s, DIFFERENT host, sandbox NEW, restored step 112 (saved by: signal).
- Trigger vacate fired at 14:09:54.8 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.9 s after the signal.
- Next execution restored step 112 (saved by: signal) -> the SIGTERM save (step 112) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P4b-staging-midsave-kill-vacate-fast

_After a hard kill (condor_vacate_job -fast) in the middle of writing a 1 GB checkpoint to /staging, does the next start find a stale .tmp directory, and does it correctly resume from the previous complete checkpoint?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:55, Sys 0 00:07:35  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:56, Sys 0 00:07:45  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after ended without an exit record: gap 91 s, DIFFERENT host, sandbox NEW, restored step 8 (saved by: periodic), stale .tmp found: ['step_00000009.tmp'].
- Trigger vacate-fast fired at 13:55:39.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +5.7 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 8 (saved by: periodic).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
