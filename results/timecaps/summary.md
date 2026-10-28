# Probe results: timecaps

Generated 2026-10-27 09:43. Per-test details are in the per-site folders.

## chtc

### P14a-execute-limit

_OSPool access points cap each execution (ap40: AllowedExecuteDuration = 20 h, then a hold). Here allowed_execute_duration = 150 s and the probe exits 85 every 60 s (restarting in place). Does the job finish (each exit-85 restart starts a new execution, so a timed checkpoint keeps a job under the cap), or is it held ~150 s after it first started?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:06  -  Total Remote Usage;)
- First start 09:24:50.1; never held; job ad at first start: {'AllowedExecuteDuration': '150', 'JobStartDate': '1793111075'}.
- Executions seen by the probe: 6; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 240 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 300 (saved by: voluntary).
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).

### P14b-job-limit

_OSPool access points cap a self-checkpointing job's total time (ap40: AllowedJobDuration = 14 days, then a hold). Here allowed_job_duration = 240 s and the probe exits 85 every 60 s. When is the job held: 240 s after it first started (wall clock, across restarts), or after 240 s of running? With what message? Can the job compute its own deadline from JobStartDate + AllowedJobDuration in its job ad?_

- Final job state: aborted (via condor_rm (by user <user>))
- First start 09:24:49.4; held 240 s later; job ad at first start: {'AllowedExecuteDuration': '259200', 'AllowedJobDuration': '240', 'JobStartDate': '1793111075'} -> deadline the job could compute: 09:28:35.0.
- Held at 09:28:49.0: The job exceeded allowed job duration of 04:00; Code 46 Subcode 0
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 8 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## ospool

### P14a-execute-limit

_OSPool access points cap each execution (ap40: AllowedExecuteDuration = 20 h, then a hold). Here allowed_execute_duration = 150 s and the probe exits 85 every 60 s (restarting in place). Does the job finish (each exit-85 restart starts a new execution, so a timed checkpoint keeps a job under the cap), or is it held ~150 s after it first started?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- First start 09:30:24.3; never held; job ad at first start: {'AllowedExecuteDuration': '150', 'JobStartDate': '1793111054'}.
- Executions seen by the probe: 6; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 240 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 300 (saved by: voluntary).
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).
