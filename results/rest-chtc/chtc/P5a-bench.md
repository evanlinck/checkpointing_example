# P5a-bench on chtc

**Question.** How long does writing (with fsync) and renaming a 100 MB / 1 GB checkpoint take, as 1 file and as 64 files, on local scratch and on /staging?

Job: `6573183.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P5a-bench`

## Observations

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

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| bcc98832 | 08:50:09.7 | e4086.chtc.wisc.edu | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 08:49:24.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P5a-bench"; JobBatchName = "probes.dag+6573176" ]
- 08:50:04.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4086.chtc.wisc.edu&noUDP&sock=slot1_23_3546937_bcc4_128610>
- 08:50:08.0 `040 file_transfer` Finished transferring input files 
- 08:50:08.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_23@e4086.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_668794/scratch"; Cpus = 1; Disk = 4194304; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:50:54.0 `040 file_transfer` Started transferring output files 
- 08:50:54.0 `040 file_transfer` Finished transferring output files 
- 08:50:54.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:06  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 3515  -  Run Bytes Sent By Job; 286336878  - 

## condor_history (selected)

```
CommittedSlotTime = 51.0
CommittedSuspensionTime = 0
CommittedTime = 51
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949054
JobCurrentStartTransferOutputDate = 1790949054
LastRemoteHost = slot1_23@e4086.chtc.wisc.edu
LastRemoteWallClockTime = 51.0
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
RemoteWallClockTime = 51.0
TransferOutFinished = 1790949054
TransferOutStarted = 1790949054
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 3515; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 3515; CedarFilesCountLastRun = 3 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:50:09.7 bcc98832 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_668794/scratch", "mode": "bench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "bcc98832", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_668794/scratch"}
08:50:09.9 bcc98832 bench                  {"bytes": 104857600, "files": 1, "mb": 100, "mb_per_s": 466.9, "rename_seconds": 0.0, "target": ".", "write_seconds": 0.225}
08:50:10.2 bcc98832 bench                  {"bytes": 67108864, "files": 64, "mb": 100, "mb_per_s": 418.3, "rename_seconds": 0.0, "target": ".", "write_seconds": 0.16}
08:50:14.4 bcc98832 bench                  {"bytes": 1048576000, "files": 1, "mb": 1000, "mb_per_s": 371.6, "rename_seconds": 0.001, "target": ".", "write_seconds": 2.822}
08:50:17.0 bcc98832 bench                  {"bytes": 1006632960, "files": 64, "mb": 1000, "mb_per_s": 582.7, "rename_seconds": 0.0, "target": ".", "write_seconds": 1.728}
08:50:20.2 bcc98832 bench                  {"bytes": 104857600, "files": 1, "mb": 100, "mb_per_s": 94.6, "rename_seconds": 0.018, "target": "/staging/<user>/ckpt-probes/runs/6573183.0", "write_seconds": 1.108}
08:50:26.5 bcc98832 bench                  {"bytes": 67108864, "files": 64, "mb": 100, "mb_per_s": 10.8, "rename_seconds": 0.011, "target": "/staging/<user>/ckpt-probes/runs/6573183.0", "write_seconds": 6.218}
08:50:29.3 bcc98832 bench                  {"bytes": 1048576000, "files": 1, "mb": 1000, "mb_per_s": 409.0, "rename_seconds": 0.013, "target": "/staging/<user>/ckpt-probes/runs/6573183.0", "write_seconds": 2.564}
08:50:53.4 bcc98832 bench                  {"bytes": 1006632960, "files": 64, "mb": 1000, "mb_per_s": 42.3, "rename_seconds": 0.026, "target": "/staging/<user>/ckpt-probes/runs/6573183.0", "write_seconds": 23.816}
08:50:53.0 bcc98832 exit                   {"code": 0, "reason": "bench done"}
```
