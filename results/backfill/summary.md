# Probe results: backfill

Generated 2026-10-02 09:07. Per-test details are in the per-site folders.

## chtc_backfill

### P0-fingerprint

_What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 1.8 GB.
- Machine ad: CUDADeviceName=GPUs_DeviceName, CUDADriverVersion=GPUs_DriverVersion, CUDAMaxSupportedVersion=GPUs_MaxSupportedVersion, CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, GPUs_DriverVersion=12.8, GPUs_MaxSupportedVersion=12080, HasChtcStaging=HasRaddusHtcCephFS, JavaSpecificationVersion=17, JavaVersion=17.0.20, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6573293.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

### P2a-save85-vacate

_KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 49 s, same host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 08:53:48.7 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.4 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P2b-evict-transfer-vacate

_Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 30 s, DIFFERENT host, sandbox NEW, restored step 162 (saved by: signal).
- Trigger vacate fired at 08:54:34.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.2 s after the signal.
- Next execution restored step 162 (saved by: signal) -> the SIGTERM save (step 162) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P3a-grace-default-vacate

_How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 15 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 08:57:04.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

### P4a-staging-vacate

_Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 47 s, same host, sandbox NEW, restored step 155 (saved by: signal).
- Trigger vacate fired at 08:56:19.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.4 s after the signal.
- Next execution restored step 155 (saved by: signal) -> the SIGTERM save (step 155) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
