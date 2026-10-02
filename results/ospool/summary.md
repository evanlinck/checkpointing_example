# Probe results: ospool

Generated 2026-10-02 12:11. Per-test details are in the per-site folders.

## ospool

### P0-fingerprint

_What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 2836.4 GB.
- Machine ad: CondorVersion=$CondorVersion: 25.14.1 2026-09-23 BuildID: 958323 PackageID: 25.14.1-1 GitSHA: 6ee23ffa $, GLIDEIN_Site=MI-HORUS, GLIDEIN_SiteWMS=SLURM, GLIDEIN_SiteWMS_JobId=2606077, GLIDEIN_SiteWMS_Queue=Unknown, GLIDEIN_SiteWMS_Slot=Unknown, GLIDEIN_ToRetire=1790969519, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=ifthenelse((JobUniverse != 13 && DiskUsage =!= undefined && DiskUsage > Disk),-1,ifthenelse((JobUniverse != 13 && MemoryUsage =!= undefined && MemoryUsage > Memory),-1,ifthenelse(((JobUniverse != 1 && (JobUniverse != 13 && DiskUsage =!= undefined && DiskUsage > Disk)) || (JobUniverse != 1 && (JobUniverse != 13 && MemoryUsage =!= undefined && MemoryUsage > Memory)) || ((false) || (false) || (false) || (false))) =!= true,ifthenelse((SiteWMS_WN_Preempt =?= true),1200,10000000),0))), OSPool=true, OpSysAndVer=CentOS8, PelicanPluginVersion=7.26.0, RetirementTimeRemaining=0, S
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": false, "isdir": false}, "/staging/<user>/ckpt-probes/runs/6586483.0": {"exists": false, "isdir": false}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

### P1-voluntary-exit

_After exit 85, does the job restart in the same sandbox on the same host? Does a file outside transfer_checkpoint_files survive? Do nested directories transfer? How long is the exit-to-restart gap? Is stdout appended or truncated across restarts? Does an exit-85 restart write a new "executing" event? Does the final exit 0 complete normally?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

### P2a-save85-hold-release

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 149 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger hold-release fired at 11:20:46.5 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 151) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2a-save85-vacate-fast

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 28 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 11:18:44.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -0.8 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2a-save85-vacate

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 24 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:20:43.8 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.1 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 154) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-hold-release

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 92 s, DIFFERENT host, sandbox NEW, restored step 153 (saved by: signal).
- Trigger hold-release fired at 11:33:21.5 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.1 s after the signal.
- Next execution restored step 153 (saved by: signal) -> the SIGTERM save (step 153) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate-fast

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 73 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 11:28:20.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -1.5 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 34 s, DIFFERENT host, sandbox NEW, restored step 61 (saved by: signal).
- Trigger vacate fired at 11:23:47.0 (AP clock).
- Evicted execution received SIGTERM 4.9 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.7 s after the signal.
- Next execution restored step 61 (saved by: signal) -> the SIGTERM save (step 61) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2c-save0-vacate

_Safety check: if a job saves and exits 0 in response to a vacate, does HTCondor wrongly treat the job as complete?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 0: gap 49 s, same host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:36:51.7 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 0, 1.0 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 157) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2d-default-vacate

_Baseline: a job with no SIGTERM handler dies on the signal. Does it restart from the last voluntary checkpoint (A)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 430 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:39:21.9 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 1.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3a-grace-default-hold-release

_How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?_

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Trigger hold-release fired at 11:45:22.3 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 600.3 s after the signal = effective grace before SIGKILL.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P3a-grace-default-vacate

_How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 259 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:43:37.2 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.8 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3b-grace-jmvt60-vacate

_Is job_max_vacate_time = 60 honoured (grace about 60 s)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 184 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:47:22.4 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 59.4 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3c-grace-jmvt900-vacate

_If a job asks for job_max_vacate_time = 900, is it capped by the machine's MachineMaxVacateTime?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 89 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:55:07.9 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 899.6 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3d-killsig-usr1-vacate

_Is kill_sig honoured? The job asks for SIGUSR1; does it receive SIGUSR1 instead of SIGTERM?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGUSR1, no exit recorded): gap 78 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:58:38.2 (AP clock).
- Evicted execution received SIGUSR1 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P5a-bench

_How long does writing (with fsync) and renaming a 100 MB / 1 GB checkpoint take, as 1 file and as 64 files, on local scratch and on /staging?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bench .: 100 MB in 1 file(s): write+fsync 0.13 s (796 MB/s), rename 0.000 s
- bench .: 100 MB in 64 file(s): write+fsync 0.10 s (704 MB/s), rename 0.000 s
- bench .: 1000 MB in 1 file(s): write+fsync 1.38 s (759 MB/s), rename 0.000 s
- bench .: 1000 MB in 64 file(s): write+fsync 1.29 s (778 MB/s), rename 0.000 s
- bench /staging/<user>/ckpt-probes/runs/6589683.0 None MB: ERROR [Errno 30] Read-only file system: '/staging'

### P5c-spool-100mb

_How long is the gap between exit 85 and the restart when the checkpoint is 100 MB (transfer to the AP's spool)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P5d-spool-1gb

_How long is the gap between exit 85 and the restart when the checkpoint is 1000 MB (transfer to the AP's spool)?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 7 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

### P6a-destination-osdf-vacate

_Does checkpoint_destination = osdf://... (our /staging namespace) work, from CHTC and from the OSPool? After a vacate, does the restart get the checkpoint back from there?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 14 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 54 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:37:36.9 (AP clock).
- Evicted execution received SIGTERM 0.3 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 137) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P8b-rapid-exits

_What happens when a job exits 85 every 5 seconds, 12 times? Throttling, a hold after N restarts, or nothing?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 13; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 15 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 20 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 25 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 35 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 40 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 45 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 50 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 55 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
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
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
