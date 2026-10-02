# P8d-empty-ckpt-dir on chtc

**Question.** What happens when the job exits 85 and the checkpoint directory exists but is empty? (The probe stops after 3 such exits in one sandbox.)

Job: `6573402.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P8d-empty-ckpt-dir`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| cc13f3f6 | 08:54:33.5 | e2481 | False | 0 | None (None) |  | [] | 85 |
| dfe308c1 | 08:55:04.4 | e2481 | True | 0 | None (None) |  | [] | 85 |
| 4ec15535 | 08:55:35.2 | e2481 | True | 0 | None (None) |  | [] | 85 |
| 08f99767 | 08:56:06.3 | e2481 | True | 0 | None (None) |  | [(60, 'final', 0.012)] | 0 |

## HTCondor event log (AP clock)

- 08:51:00.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P8d-empty-ckpt-dir"; JobBatchName = "probes.dag+6573176" ]
- 08:51:12.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_9_3564670_3d75_95265>
- 08:54:32.0 `040 file_transfer` Finished transferring input files 
- 08:54:32.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_9@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_566305/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:55:03.0 `040 file_transfer` Started transferring output files 
- 08:55:03.0 `040 file_transfer` Finished transferring output files 
- 08:55:34.0 `040 file_transfer` Started transferring output files 
- 08:55:34.0 `040 file_transfer` Finished transferring output files 
- 08:56:05.0 `040 file_transfer` Started transferring output files 
- 08:56:05.0 `040 file_transfer` Finished transferring output files 
- 08:57:06.0 `040 file_transfer` Started transferring output files 
- 08:57:06.0 `040 file_transfer` Finished transferring output files 
- 08:57:06.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 27464  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 2
CommittedSlotTime = 61.0
CommittedSuspensionTime = 0
CommittedTime = 151
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949426
JobCurrentStartTransferOutputDate = 1790949426
LastRemoteHost = slot1_9@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 354.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 4
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 354.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949426
TransferOutStarted = 1790949426
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 27464; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 27464; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:54:33.5 cc13f3f6 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_566305/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "cc13f3f6", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch"}
08:54:33.5 cc13f3f6 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "store": "spool"}
08:54:33.5 cc13f3f6 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:54:33.5 cc13f3f6 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:55:03.6 cc13f3f6 emptied_checkpoint_dir {"step": 30}
08:55:03.6 cc13f3f6 children_at_exit       {"alive": [], "exitcodes": []}
08:55:03.6 cc13f3f6 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
08:55:04.4 dfe308c1 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_566305/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "cc13f3f6", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch"}
08:55:04.4 dfe308c1 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "store": "spool"}
08:55:04.4 dfe308c1 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:55:04.4 dfe308c1 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:55:34.5 dfe308c1 emptied_checkpoint_dir {"step": 30}
08:55:34.5 dfe308c1 children_at_exit       {"alive": [], "exitcodes": []}
08:55:34.5 dfe308c1 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
08:55:35.2 4ec15535 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_566305/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "cc13f3f6", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch"}
08:55:35.2 4ec15535 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "store": "spool"}
08:55:35.2 4ec15535 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:55:35.2 4ec15535 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:56:05.3 4ec15535 emptied_checkpoint_dir {"step": 30}
08:56:05.3 4ec15535 children_at_exit       {"alive": [], "exitcodes": []}
08:56:05.3 4ec15535 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
08:56:06.3 08f99767 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_566305/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "cc13f3f6", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch"}
08:56:06.3 08f99767 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "store": "spool"}
08:56:06.3 08f99767 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_566305/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:56:06.3 08f99767 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:56:36.4 08f99767 voluntary_exit_skipped {"reason": "max_voluntary_exits reached in this sandbox", "step": 30}
08:57:06.4 08f99767 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 60}
08:57:06.4 08f99767 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.012, "step": 60, "write_seconds": 0.011}
08:57:06.4 08f99767 children_at_exit       {"alive": [], "exitcodes": []}
08:57:06.4 08f99767 exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
