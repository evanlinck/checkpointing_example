# P0-fingerprint on chtc_backfill

**Question.** What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks.

Job: `6573293.0`   Test dir: `/home/<user>/probes/runs/backfill/chtc_backfill/P0-fingerprint`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 1.8 GB.
- Machine ad: CUDADeviceName=GPUs_DeviceName, CUDADriverVersion=GPUs_DriverVersion, CUDAMaxSupportedVersion=GPUs_MaxSupportedVersion, CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, GPUs_DriverVersion=12.8, GPUs_MaxSupportedVersion=12080, HasChtcStaging=HasRaddusHtcCephFS, JavaSpecificationVersion=17, JavaVersion=17.0.20, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6573293.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| a4dfbf66 | 08:53:22.2 | gpu4000 | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 08:49:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P0-fingerprint"; JobBatchName = "probes.dag+6573292" ]
- 08:49:52.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=gpu4000.chtc.wisc.edu&noUDP&sock=slot2_8_4130900_7fa7_70562>
- 08:53:21.0 `040 file_transfer` Finished transferring input files 
- 08:53:21.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_8@gpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_cdbf3fca }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1001781/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_cdbf3fca = [ Id = "GPU-cdbf3fca"; Capability = 8.9; DeviceName = "NVIDIA L40"; DeviceUuid = "cdbf3fca-8
- 08:53:22.0 `040 file_transfer` Started transferring output files 
- 08:53:22.0 `040 file_transfer` Finished transferring output files 
- 08:53:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 38988  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CommittedSlotTime = 210.0
CommittedSuspensionTime = 0
CommittedTime = 210
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790949202
LastRemoteHost = slot2_8@gpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 210.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 210.0
TransferOutFinished = 1790949202
TransferOutStarted = 1790949202
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 38988; CedarFilesCountTotal = 6; CedarSizeBytesLastRun = 38988; CedarFilesCountLastRun = 6 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:53:22.2 a4dfbf66 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1001781/scratch", "mode": "fingerprint", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a4dfbf66", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot2/dir_1001781/scratch"}
08:53:22.5 a4dfbf66 fingerprint            {"container": {"apptainer_env": true, "dockerenv": false, "singularity_d": true}, "cwd": "/var/lib/condor/execute/slot2/dir_1001781/scratch", "internet": {"https://github.com": {"ok": true, "seconds": 0.06, "status": 200}, "https://huggingface.co/api/models?limit=1": {"ok": true, "seconds": 0.05, "s
08:53:22.5 a4dfbf66 exit                   {"code": 0, "reason": "fingerprint done"}
```
