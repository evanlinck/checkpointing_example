# P5c-spool-100mb on chtc

**Question.** How long is the gap between exit 85 and the restart when the checkpoint is 100 MB (transfer to the AP's spool)?

Job: `6574004.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P5c-spool-100mb`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 3009d067 | 08:58:34.1 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(30, 'voluntary', 0.113)] | 85 |
| 79a1888d | 08:59:05.7 | e2016.chtc.wisc.edu | True | 0 | 30 (voluntary) |  | [(60, 'final', 0.144)] | 0 |

## HTCondor event log (AP clock)

- 08:57:15.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P5c-spool-100mb"; JobBatchName = "probes.dag+6573176" ]
- 08:58:25.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_12_3486004_ed36_78593>
- 08:58:33.0 `040 file_transfer` Finished transferring input files 
- 08:58:33.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_12@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2210392/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:59:04.0 `040 file_transfer` Started transferring output files 
- 08:59:04.0 `040 file_transfer` Finished transferring output files 
- 08:59:36.0 `040 file_transfer` Started transferring output files 
- 08:59:36.0 `040 file_transfer` Finished transferring output files 
- 08:59:36.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 15357  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 32.0
CommittedSuspensionTime = 0
CommittedTime = 62
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949576
JobCurrentStartTransferOutputDate = 1790949576
LastRemoteHost = slot1_12@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 71.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 71.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949576
TransferOutStarted = 1790949576
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 15357; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 15357; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:58:34.1 3009d067 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2210392/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "3009d067", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch"}
08:58:34.1 3009d067 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch/ckpt", "store": "spool"}
08:58:34.2 3009d067 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:58:34.2 3009d067 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:59:04.2 3009d067 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
08:59:04.3 3009d067 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.113, "step": 30, "write_seconds": 0.112}
08:59:04.3 3009d067 children_at_exit       {"alive": [], "exitcodes": []}
08:59:04.3 3009d067 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
08:59:05.7 79a1888d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2210392/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "3009d067", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch"}
08:59:05.7 79a1888d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch/ckpt", "store": "spool"}
08:59:05.8 79a1888d restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210392/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790949544.3396506, "saved_by_exec": "3009d067", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
08:59:05.8 79a1888d loop_start             {"restored_step": 30, "step": 30, "total_steps": 60, "voluntary_exit_at": [30]}
08:59:35.8 79a1888d save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "final", "step": 60}
08:59:35.0 79a1888d save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "final", "seconds": 0.144, "step": 60, "write_seconds": 0.115}
08:59:35.0 79a1888d children_at_exit       {"alive": [], "exitcodes": []}
08:59:35.0 79a1888d exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
