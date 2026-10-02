# P5d-spool-1gb on chtc

**Question.** How long is the gap between exit 85 and the restart when the checkpoint is 1000 MB (transfer to the AP's spool)?

Job: `6574005.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P5d-spool-1gb`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:05  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:05  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| a67dd1bc | 08:58:45.0 | e4086.chtc.wisc.edu | False | 0 | None (None) |  | [(30, 'voluntary', 4.443)] | 85 |
| 678f1fbd | 08:59:25.8 | e4086.chtc.wisc.edu | True | 0 | 30 (voluntary) |  | [(60, 'final', 13.649)] | 0 |

## HTCondor event log (AP clock)

- 08:57:15.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P5d-spool-1gb"; JobBatchName = "probes.dag+6573176" ]
- 08:58:40.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4086.chtc.wisc.edu&noUDP&sock=slot1_73_3546937_bcc4_128637>
- 08:58:44.0 `040 file_transfer` Finished transferring input files 
- 08:58:44.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_73@e4086.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_700187/scratch"; Cpus = 1; Disk = 4194304; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:59:20.0 `040 file_transfer` Started transferring output files 
- 08:59:24.0 `040 file_transfer` Finished transferring output files 
- 09:00:10.0 `040 file_transfer` Started transferring output files 
- 09:00:10.0 `040 file_transfer` Finished transferring output files 
- 09:00:11.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:05  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:05  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 15296  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 51.0
CommittedSuspensionTime = 0
CommittedTime = 86
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949610
JobCurrentStartTransferOutputDate = 1790949610
LastRemoteHost = slot1_73@e4086.chtc.wisc.edu
LastRemoteWallClockTime = 92.0
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
RemoteWallClockTime = 92.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949610
TransferOutStarted = 1790949610
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 15296; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 15296; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:58:45.0 a67dd1bc start                  {"cwd": "/var/lib/condor/execute/slot1/dir_700187/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a67dd1bc", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch"}
08:58:45.0 a67dd1bc history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch/ckpt", "store": "spool"}
08:58:45.0 a67dd1bc restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:58:45.0 a67dd1bc loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:59:16.0 a67dd1bc save_start             {"ckpt_files": 1, "ckpt_mb": 1000, "reason": "voluntary", "step": 30}
08:59:20.5 a67dd1bc save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 4.443, "step": 30, "write_seconds": 4.442}
08:59:20.5 a67dd1bc children_at_exit       {"alive": [], "exitcodes": []}
08:59:20.5 a67dd1bc exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
08:59:25.8 678f1fbd start                  {"cwd": "/var/lib/condor/execute/slot1/dir_700187/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "a67dd1bc", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch"}
08:59:25.8 678f1fbd history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch/ckpt", "store": "spool"}
08:59:25.8 678f1fbd restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_700187/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790949560.489951, "saved_by_exec": "a67dd1bc", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason"
08:59:25.8 678f1fbd loop_start             {"restored_step": 30, "step": 30, "total_steps": 60, "voluntary_exit_at": [30]}
08:59:55.9 678f1fbd save_start             {"ckpt_files": 1, "ckpt_mb": 1000, "reason": "final", "step": 60}
09:00:09.5 678f1fbd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "final", "seconds": 13.649, "step": 60, "write_seconds": 12.928}
09:00:10.3 678f1fbd children_at_exit       {"alive": [], "exitcodes": []}
09:00:10.3 678f1fbd exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
