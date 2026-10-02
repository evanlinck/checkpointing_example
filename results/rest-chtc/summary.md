# Probe results: rest-chtc

Generated 2026-10-02 09:49. Per-test details are in the per-site folders.

## chtc

### P2b-evict-transfer-hold-release

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 88 s, DIFFERENT host, sandbox NEW, restored step 154 (saved by: signal).
- Trigger hold-release fired at 08:52:30.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.5 s after the signal.
- Next execution restored step 154 (saved by: signal) -> the SIGTERM save (step 154) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate-fast

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 96 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 08:52:29.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -8.8 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 11 s, DIFFERENT host, sandbox NEW, restored step 150 (saved by: signal).
- Trigger vacate fired at 08:52:26.0 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 150 (saved by: signal) -> the SIGTERM save (step 150) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P5a-bench

_How long does writing (with fsync) and renaming a 100 MB / 1 GB checkpoint take, as 1 file and as 64 files, on local scratch and on /staging?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:06  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bench .: 100 MB in 1 file(s): write+fsync 0.23 s (467 MB/s), rename 0.000 s
- bench .: 100 MB in 64 file(s): write+fsync 0.16 s (418 MB/s), rename 0.000 s
- bench .: 1000 MB in 1 file(s): write+fsync 2.82 s (372 MB/s), rename 0.001 s
- bench .: 1000 MB in 64 file(s): write+fsync 1.73 s (583 MB/s), rename 0.000 s
- bench /staging/<user>/ckpt-probes/runs/6573183.0: 100 MB in 1 file(s): write+fsync 1.11 s (95 MB/s), rename 0.018 s
- bench /staging/<user>/ckpt-probes/runs/6573183.0: 100 MB in 64 file(s): write+fsync 6.22 s (11 MB/s), rename 0.011 s
- bench /staging/<user>/ckpt-probes/runs/6573183.0: 1000 MB in 1 file(s): write+fsync 2.56 s (409 MB/s), rename 0.013 s
- bench /staging/<user>/ckpt-probes/runs/6573183.0: 1000 MB in 64 file(s): write+fsync 23.82 s (42 MB/s), rename 0.026 s

### P5c-spool-100mb

_How long is the gap between exit 85 and the restart when the checkpoint is 100 MB (transfer to the AP's spool)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P5d-spool-1gb

_How long is the gap between exit 85 and the restart when the checkpoint is 1000 MB (transfer to the AP's spool)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:05  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:05  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P6a-destination-osdf-vacate

_Does checkpoint_destination = osdf://... (our /staging namespace) work, from CHTC and from the OSPool? After a vacate, does the restart get the checkpoint back from there?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 292 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 09:02:16.5 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.6 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 147) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P6b-destination-file-vacate

_Does checkpoint_destination = file:///staging/<user> work on CHTC execute points that mount /staging?_

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1086 s, DIFFERENT host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 09:02:46.6 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P7a-wrapper-exec-bare-vacate

_When the executable is a shell script that execs python, does python receive the soft-kill signal?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 95 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:13:47.3 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.8 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 73) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=3986726 about to exec python3 | WRAPPER run_exec.sh pid=3987008 about to exec python3 | WRAPPER run_exec.sh pid=3418696 about to exec python3

### P7a-wrapper-exec-vacate

_When the executable is a shell script that execs python, does python receive the soft-kill signal?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=3 (condor_history).
- Restart after exit 85: gap 374 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:09:16.0 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=142 about to exec python3 | WRAPPER run_exec.sh pid=76 about to exec python3

### P7b-wrapper-noexec-bare-vacate

_When a shell wrapper runs python WITHOUT exec, who gets the signal: only bash, or python too? Is python killed before it finishes saving?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 0: gap 72 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:18:02.6 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +183.6 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_noexec.sh pid=3688363 starting python3 as a child | WRAPPER python exited with 85 at 1790950610.364302723; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=3689599 starting python3 as a child | WRAPPER bash received SIGTERM at 1790950866.143705933 | WRAPPER python exited with 0 at 1790950866.146206582; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=138638 

### P7b-wrapper-noexec-vacate

_When a shell wrapper runs python WITHOUT exec, who gets the signal: only bash, or python too? Is python killed before it finishes saving?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 0: gap 48 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:14:47.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +181.5 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_noexec.sh pid=14 starting python3 as a child | WRAPPER python exited with 85 at 1790950412.701157790; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=14 starting python3 as a child | WRAPPER bash received SIGTERM at 1790950668.860492951 | WRAPPER python exited with 0 at 1790950668.865047461; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=14 starting pytho

### P7c-children-bare-vacate

_Do child processes (like DataLoader workers) receive the signal directly? Does a child that does not handle it die while the parent is still saving?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 85 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:05:01.8 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 21.1 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 77) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Children that received a signal directly: none; child exits seen by parent: none.

### P7c-children-vacate

_Do child processes (like DataLoader workers) receive the signal directly? Does a child that does not handle it die while the parent is still saving?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 40 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:21:17.8 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.2 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 69) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Children that received a signal directly: none; child exits seen by parent: none.

### P8a-missing-ckpt-file

_What happens when the job exits 85 but a path listed in transfer_checkpoint_files does not exist? (Hold? Error? Ignored?)_

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 0; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).

### P8b-rapid-exits

_What happens when a job exits 85 every 5 seconds, 12 times? Throttling, a hold after N restarts, or nothing?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 13; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 17 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 15 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 20 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 25 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 35 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 40 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 45 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 50 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 55 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 13 of 13 executions (tells whether stdout is kept across restarts).

### P8c-no-ckpt-code

_Sanity check: without checkpoint_exit_code, is exit 85 simply treated as the job finishing (with return value 85)?_

- Final job state: terminated ((1) Normal termination (return value 85); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

### P8d-empty-ckpt-dir

_What happens when the job exits 85 and the checkpoint directory exists but is empty? (The probe stops after 3 such exits in one sandbox.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
