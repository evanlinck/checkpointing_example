# Probe results: smoke

Generated 2026-10-01 13:33. Per-test details are in the per-site folders.

## chtc

### P0-fingerprint-bare

_What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1; NumJobStarts=?, NumShadowStarts=? (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.9.25; container: {'apptainer_env': False, 'dockerenv': False, 'singularity_d': False}; scratch free 373.2 GB.
- Machine ad: CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, HasChtcStaging=HasRaddusHtcCephFS, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6527260.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: /usr/libexec/condor/condor_chirp; chirp test: 0
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

### P0-fingerprint

_What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1; NumJobStarts=?, NumShadowStarts=? (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 282.4 GB.
- Machine ad: CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, HasChtcStaging=HasRaddusHtcCephFS, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6527259.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

### P1-voluntary-exit

_After exit 85, does the job restart in the same sandbox on the same host? Does a file outside transfer_checkpoint_files survive? Do nested directories transfer? How long is the exit-to-restart gap? Is stdout appended or truncated across restarts? Does an exit-85 restart write a new "executing" event? Does the final exit 0 complete normally?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1; NumJobStarts=?, NumShadowStarts=? (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
