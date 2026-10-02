# P5a-bench on ospool

**Question.** How long does writing (with fsync) and renaming a 100 MB / 1 GB checkpoint take, as 1 file and as 64 files, on local scratch and on /staging?

Job: `6589683.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P5a-bench`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bench .: 100 MB in 1 file(s): write+fsync 0.13 s (796 MB/s), rename 0.000 s
- bench .: 100 MB in 64 file(s): write+fsync 0.10 s (704 MB/s), rename 0.000 s
- bench .: 1000 MB in 1 file(s): write+fsync 1.38 s (759 MB/s), rename 0.000 s
- bench .: 1000 MB in 64 file(s): write+fsync 1.29 s (778 MB/s), rename 0.000 s
- bench /staging/<user>/ckpt-probes/runs/6589683.0 None MB: ERROR [Errno 30] Read-only file system: '/staging'

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 9e887660 | 12:00:39.7 | c2023.swan.hcc.unl.edu | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:58:01.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P5a-bench"; JobBatchName = "probes.dag+6586482" ]
- 12:00:33.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:45609?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#14598670%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 12:00:39.0 `040 file_transfer` Finished transferring input files 
- 12:00:39.0 `021 remote_error` Message from starter on slot1@glidein_1627526_182790606@c2023.swan.hcc.unl.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 12:00:39.0 `001 executing` Job executing on host: <<ip>:34483?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f — SlotName: slot1@glidein_1627526_182790606@c2023.swan.hcc.unl.edu; CondorScratchDir = "/scratch/glide_hCa8Tx/execute/dir_1905909/scratch"; Cpus = 1; Disk = 36610688; GPUs = 0; Memory = 2000
- 12:00:43.0 `040 file_transfer` Started transferring output files 
- 12:00:43.0 `040 file_transfer` Finished transferring output files 
- 12:00:43.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 2449  -  Run Bytes Sent By Job; 286336878  - 

## condor_history (selected)

```
CommittedSlotTime = 11.0
CommittedSuspensionTime = 0
CommittedTime = 11
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790960443
JobCurrentStartTransferOutputDate = 1790960442
LastRemoteHost = slot1@glidein_1627526_182790606@c2023.swan.hcc.unl.edu
LastRemoteWallClockTime = 11.0
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
RemoteWallClockTime = 11.0
TransferOutFinished = 1790960443
TransferOutStarted = 1790960443
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 2449; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 2449; CedarFilesCountLastRun = 3 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
12:00:39.7 9e887660 start                  {"cwd": "/srv/scratch", "mode": "bench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "9e887660", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
12:00:39.9 9e887660 bench                  {"bytes": 104857600, "files": 1, "mb": 100, "mb_per_s": 795.8, "rename_seconds": 0.0, "target": ".", "write_seconds": 0.132}
12:00:39.0 9e887660 bench                  {"bytes": 67108864, "files": 64, "mb": 100, "mb_per_s": 703.6, "rename_seconds": 0.0, "target": ".", "write_seconds": 0.095}
12:00:41.4 9e887660 bench                  {"bytes": 1048576000, "files": 1, "mb": 1000, "mb_per_s": 759.4, "rename_seconds": 0.0, "target": ".", "write_seconds": 1.381}
12:00:42.7 9e887660 bench                  {"bytes": 1006632960, "files": 64, "mb": 1000, "mb_per_s": 778.0, "rename_seconds": 0.0, "target": ".", "write_seconds": 1.294}
12:00:42.8 9e887660 bench_error            {"error": "[Errno 30] Read-only file system: '/staging'", "target": "/staging/<user>/ckpt-probes/runs/6589683.0"}
12:00:42.8 9e887660 exit                   {"code": 0, "reason": "bench done"}
```
