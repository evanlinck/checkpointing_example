# P0-fingerprint on ospool

**Question.** What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks.

Job: `6586483.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P0-fingerprint`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 2836.4 GB.
- Machine ad: CondorVersion=$CondorVersion: 25.14.1 2026-09-23 BuildID: 958323 PackageID: 25.14.1-1 GitSHA: 6ee23ffa $, GLIDEIN_Site=MI-HORUS, GLIDEIN_SiteWMS=SLURM, GLIDEIN_SiteWMS_JobId=2606077, GLIDEIN_SiteWMS_Queue=Unknown, GLIDEIN_SiteWMS_Slot=Unknown, GLIDEIN_ToRetire=1790969519, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=ifthenelse((JobUniverse != 13 && DiskUsage =!= undefined && DiskUsage > Disk),-1,ifthenelse((JobUniverse != 13 && MemoryUsage =!= undefined && MemoryUsage > Memory),-1,ifthenelse(((JobUniverse != 1 && (JobUniverse != 13 && DiskUsage =!= undefined && DiskUsage > Disk)) || (JobUniverse != 1 && (JobUniverse != 13 && MemoryUsage =!= undefined && MemoryUsage > Memory)) || ((false) || (false) || (false) || (false))) =!= true,ifthenelse((SiteWMS_WN_Preempt =?= true),1200,10000000),0))), OSPool=true, OpSysAndVer=CentOS8, PelicanPluginVersion=7.26.0, RetirementTimeRemaining=0, S
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": false, "isdir": false}, "/staging/<user>/ckpt-probes/runs/6586483.0": {"exists": false, "isdir": false}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 23769844 | 11:15:50.5 | wsu-lc02.osris.org | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:13:37.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P0-fingerprint"; JobBatchName = "probes.dag+6586482" ]
- 11:15:45.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:46463?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14601177%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:15:48.0 `040 file_transfer` Finished transferring input files 
- 11:15:49.0 `021 remote_error` Message from starter on slot1@glidein_865012_304242041@wsu-lc02.osris.org: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:15:49.0 `001 executing` Job executing on host: <<ip>:40059?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1@glidein_865012_304242041@wsu-lc02.osris.org; CondorScratchDir = "/scratch/glide_D5wKd8/execute/dir_1900683/scratch"; Cpus = 1; Disk = 25637737; GPUs = 0; Memory = 2048
- 11:15:51.0 `040 file_transfer` Started transferring output files 
- 11:15:51.0 `040 file_transfer` Finished transferring output files 
- 11:15:51.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 55386  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CommittedSlotTime = 8.0
CommittedSuspensionTime = 0
CommittedTime = 8
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790957751
JobCurrentStartTransferOutputDate = 1790957751
LastRemoteHost = slot1@glidein_865012_304242041@wsu-lc02.osris.org
LastRemoteWallClockTime = 8.0
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
RemoteWallClockTime = 8.0
TransferOutFinished = 1790957751
TransferOutStarted = 1790957751
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 55386; CedarFilesCountTotal = 6; CedarSizeBytesLastRun = 55386; CedarFilesCountLastRun = 6 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:15:50.5 23769844 start                  {"cwd": "/srv/scratch", "mode": "fingerprint", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "23769844", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:15:50.9 23769844 fingerprint            {"container": {"apptainer_env": true, "dockerenv": false, "singularity_d": true}, "cwd": "/srv/scratch", "internet": {"https://github.com": {"ok": true, "seconds": 0.1, "status": 200}, "https://huggingface.co/api/models?limit=1": {"ok": true, "seconds": 0.1, "status": 200}, "https://pypi.org/simple/
11:15:50.9 23769844 exit                   {"code": 0, "reason": "fingerprint done"}
```
