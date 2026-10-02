# P0-fingerprint on chtc_backfill

**Question.** What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks.

Job: `6586848.0`   Test dir: `/home/<user>/probes/runs/backfill2/chtc_backfill/P0-fingerprint`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 28893.8 GB.
- Machine ad: BackfillSlot=true, CUDADeviceName=GPUs_DeviceName, CUDADriverVersion=GPUs_DriverVersion, CUDAMaxSupportedVersion=GPUs_MaxSupportedVersion, CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, GPUs_DriverVersion=12.8, GPUs_MaxSupportedVersion=12080, HasChtcStaging=HasRaddusHtcCephFS, JavaSpecificationVersion=17, JavaVersion=17.0.20, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6586848.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 753aaa4d | 11:22:00.2 | txie-dsigpu4000 | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:17:36.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P0-fingerprint"; JobBatchName = "probes.dag+6586847" ]
- 11:21:56.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=txie-dsigpu4000.chtc.wisc.edu&noUDP&sock=backfill1_5_2080173_cf47_26348>
- 11:21:59.0 `040 file_transfer` Finished transferring input files 
- 11:21:59.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: backfill1_5@txie-dsigpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_aab08e20 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1355525/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_aab08e20 = [ Id = "GPU-aab08e20"; Capability = 9.0; DeviceName = "NVIDIA H100 80GB HBM3"; D
- 11:22:00.0 `040 file_transfer` Started transferring output files 
- 11:22:00.0 `040 file_transfer` Finished transferring output files 
- 11:22:00.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 38844  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CommittedSlotTime = 4.0
CommittedSuspensionTime = 0
CommittedTime = 4
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958120
JobCurrentStartTransferOutputDate = 1790958120
LastRemoteHost = backfill1_5@txie-dsigpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 4.0
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
RemoteWallClockTime = 4.0
TransferOutFinished = 1790958120
TransferOutStarted = 1790958120
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 38844; CedarFilesCountTotal = 6; CedarSizeBytesLastRun = 38844; CedarFilesCountLastRun = 6 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:22:00.2 753aaa4d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1355525/scratch", "mode": "fingerprint", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "753aaa4d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1355525/scratch"}
11:22:00.5 753aaa4d fingerprint            {"container": {"apptainer_env": true, "dockerenv": false, "singularity_d": true}, "cwd": "/var/lib/condor/execute/slot1/dir_1355525/scratch", "internet": {"https://github.com": {"ok": true, "seconds": 0.06, "status": 200}, "https://huggingface.co/api/models?limit=1": {"ok": true, "seconds": 0.06, "s
11:22:00.5 753aaa4d exit                   {"code": 0, "reason": "fingerprint done"}
```
