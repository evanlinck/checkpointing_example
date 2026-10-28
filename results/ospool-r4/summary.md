# Probe results: ospool-r4

Generated 2026-10-26 09:58. Per-test details are in the per-site folders.

## chtc

### P11d-input-limit-ckpt-bare-vacate

_With max_transfer_input_mb = 50, a 100 MB spooled checkpoint, and a vacate that forces a restart in a new sandbox: is the restart held for exceeding the input limit (so a checkpoint counts as input), or does it resume? (OSPool access points such as ap40 set MAX_TRANSFER_INPUT_MB = 5000 and don't let users change it.) The container variant also shows whether the osdf:// container image counts._

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE)
- Held at 09:20:04.0: Error from slot1_15@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34491>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3508/0/cluster7093508.proc0.subproc0/ckpt/step_00000164/payload_000.bin: max total 
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Trigger vacate fired at 09:19:49.7 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.2 s after the signal.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-ckpt-ok-bare-vacate

_Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 12 s, DIFFERENT host, sandbox NEW, restored step 161 (saved by: signal).
- Trigger vacate fired at 09:19:49.3 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.6 s after the signal.
- Next execution restored step 161 (saved by: signal) -> the SIGTERM save (step 161) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-ckpt-ok-vacate

_Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:04  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 22 s, DIFFERENT host, sandbox NEW, restored step 151 (saved by: signal).
- Trigger vacate fired at 09:19:49.2 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.3 s after the signal.
- Next execution restored step 151 (saved by: signal) -> the SIGTERM save (step 151) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-ckpt-vacate

_With max_transfer_input_mb = 50, a 100 MB spooled checkpoint, and a vacate that forces a restart in a new sandbox: is the restart held for exceeding the input limit (so a checkpoint counts as input), or does it resume? (OSPool access points such as ap40 set MAX_TRANSFER_INPUT_MB = 5000 and don't let users change it.) The container variant also shows whether the osdf:// container image counts._

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE)
- Held at 09:20:12.0: Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Trigger vacate fired at 09:19:49.5 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 7.5 s after the signal.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-osdf-bare

_With max_transfer_input_mb = 50 and a 100 MB file listed as an osdf:// input (no container): is the job held for exceeding the input limit before it starts? Decides whether large base-model weights read through OSDF are affected by an access point's MAX_TRANSFER_INPUT_MB._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-osdf-ok-bare

_Control for P11d-input-limit-osdf: the same 100 MB osdf:// input with max_transfer_input_mb = 200. It should run normally._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-osdf-ok

_Control for P11d-input-limit-osdf: the same 100 MB osdf:// input with max_transfer_input_mb = 200. It should run normally._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-osdf

_With max_transfer_input_mb = 50 and a 100 MB file listed as an osdf:// input (no container): is the job held for exceeding the input limit before it starts? Decides whether large base-model weights read through OSDF are affected by an access point's MAX_TRANSFER_INPUT_MB._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

### P13-osdf-backup

_A directory listed in transfer_checkpoint_files and remapped to osdf:// with transfer_output_remaps: does HTCondor upload it at every exit 85 (a backup that outlives the job, OSPool's advised path for large outputs), only at the end, or not at all? Does the job still resume normally?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage;)
- Backup files on OSDF (/staging): state_00000030.json at 09:38:00.6, state_00000060.json at 09:38:00.6, state_00000090.json at 09:38:00.6; probe exits: 85 at 09:36:53.9, 85 at 09:37:25.8, 0 at 09:37:57.5.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## ospool

### P11d-input-limit-ckpt-ok-vacate

_Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 52 s, DIFFERENT host, sandbox NEW, restored step 153 (saved by: signal).
- Trigger vacate fired at 09:31:05.4 (AP clock).
- Evicted execution received SIGTERM 0.5 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 153 (saved by: signal) -> the SIGTERM save (step 153) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P11d-input-limit-ckpt-vacate

_With max_transfer_input_mb = 50, a 100 MB spooled checkpoint, and a vacate that forces a restart in a new sandbox: is the restart held for exceeding the input limit (so a checkpoint counts as input), or does it resume? (OSPool access points such as ap40 set MAX_TRANSFER_INPUT_MB = 5000 and don't let users change it.) The container variant also shows whether the osdf:// container image counts._

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE)
- Held at 09:27:26.0: Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Trigger vacate fired at 09:26:20.1 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.7 s after the signal.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P13-osdf-backup

_A directory listed in transfer_checkpoint_files and remapped to osdf:// with transfer_output_remaps: does HTCondor upload it at every exit 85 (a backup that outlives the job, OSPool's advised path for large outputs), only at the end, or not at all? Does the job still resume normally?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Backup files on OSDF (/staging): state_00000030.json at 09:25:36.7, state_00000060.json at 09:25:36.7, state_00000090.json at 09:25:36.7; probe exits: 85 at 09:24:22.3, 85 at 09:24:57.8, 0 at 09:25:33.5.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
