# P1-voluntary-exit on ospool

**Question.** After exit 85, does the job restart in the same sandbox on the same host? Does a file outside transfer_checkpoint_files survive? Do nested directories transfer? How long is the exit-to-restart gap? Is stdout appended or truncated across restarts? Does an exit-85 restart write a new "executing" event? Does the final exit 0 complete normally?

Job: `6586484.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P1-voluntary-exit`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 1fab0719 | 11:15:55.0 | chpc-compute007 | False | 0 | None (None) |  | [(60, 'voluntary', 0.002)] | 85 |
| 34aa3188 | 11:16:57.1 | chpc-compute007 | True | 0 | 60 (voluntary) |  | [(120, 'voluntary', 0.003)] | 85 |
| ad611bb8 | 11:17:58.7 | chpc-compute007 | True | 0 | 120 (voluntary) |  | [(180, 'voluntary', 0.004)] | 85 |
| 81e7e44b | 11:19:00.9 | chpc-compute007 | True | 0 | 180 (voluntary) |  | [(240, 'final', 0.003)] | 0 |

## HTCondor event log (AP clock)

- 11:13:37.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P1-voluntary-exit"; JobBatchName = "probes.dag+6586482" ]
- 11:15:44.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37329?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#14601770%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:15:53.0 `040 file_transfer` Finished transferring input files 
- 11:15:53.0 `021 remote_error` Message from starter on slot1_10@glidein_2302659_69688800@chpc-compute007.cm.cluster: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:15:54.0 `001 executing` Job executing on host: <<ip>:36261?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_10@glidein_2302659_69688800@chpc-compute007.cm.cluster; CondorScratchDir = "/tmp/glide_hU01Au/execute/dir_336390/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:16:55.0 `040 file_transfer` Started transferring output files 
- 11:16:55.0 `040 file_transfer` Finished transferring output files 
- 11:17:57.0 `040 file_transfer` Started transferring output files 
- 11:17:57.0 `040 file_transfer` Finished transferring output files 
- 11:18:59.0 `040 file_transfer` Started transferring output files 
- 11:18:59.0 `040 file_transfer` Finished transferring output files 
- 11:20:01.0 `040 file_transfer` Started transferring output files 
- 11:20:01.0 `040 file_transfer` Finished transferring output files 
- 11:20:01.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 36220  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 2
CommittedSlotTime = 63.0
CommittedSuspensionTime = 0
CommittedTime = 243
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958001
JobCurrentStartTransferOutputDate = 1790958001
LastRemoteHost = slot1_10@glidein_2302659_69688800@chpc-compute007.cm.cluster
LastRemoteWallClockTime = 259.0
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
RemoteWallClockTime = 259.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958001
TransferOutStarted = 1790958001
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 36220; CedarFilesCountTotal = 17; CedarSizeBytesLastRun = 36220; CedarFilesCountLastRun = 17 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:15:55.0 1fab0719 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "1fab0719", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:15:55.0 1fab0719 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:15:55.0 1fab0719 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:15:55.0 1fab0719 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
11:16:55.1 1fab0719 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:16:55.1 1fab0719 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.002, "step": 60, "write_seconds": 0.002}
11:16:55.1 1fab0719 children_at_exit       {"alive": [], "exitcodes": []}
11:16:55.1 1fab0719 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:16:57.1 34aa3188 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "1fab0719", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:16:57.1 34aa3188 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:16:57.1 34aa3188 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790957815.0775757, "saved_by_exec": "1fab0719", "saved_on_host": "chpc-compute007", "saved_reason": "voluntary", "step": 60}
11:16:57.1 34aa3188 loop_start             {"restored_step": 60, "step": 60, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
11:17:57.1 34aa3188 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 120}
11:17:57.1 34aa3188 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.003, "step": 120, "write_seconds": 0.002}
11:17:57.1 34aa3188 children_at_exit       {"alive": [], "exitcodes": []}
11:17:57.1 34aa3188 exit                   {"code": 85, "reason": "voluntary exit at step 120", "step": 120}
11:17:58.7 ad611bb8 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "1fab0719", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:17:58.7 ad611bb8 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:17:58.7 ad611bb8 restore                {"chosen": "step_00000120", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000120", "nested_dir_ok": true, "saved_at": 1790957877.1299903, "saved_by_exec": "34aa3188", "saved_on_host": "chpc-compute007", "saved_reason": "voluntary", "step": 120}
11:17:58.7 ad611bb8 loop_start             {"restored_step": 120, "step": 120, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
11:18:58.8 ad611bb8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 180}
11:18:58.8 ad611bb8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.004, "step": 180, "write_seconds": 0.002}
11:18:58.8 ad611bb8 children_at_exit       {"alive": [], "exitcodes": []}
11:18:58.8 ad611bb8 exit                   {"code": 85, "reason": "voluntary exit at step 180", "step": 180}
11:19:00.9 81e7e44b start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "1fab0719", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:19:00.9 81e7e44b history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:19:00.9 81e7e44b restore                {"chosen": "step_00000180", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000180", "nested_dir_ok": true, "saved_at": 1790957938.782074, "saved_by_exec": "ad611bb8", "saved_on_host": "chpc-compute007", "saved_reason": "voluntary", "step": 180}
11:19:00.9 81e7e44b loop_start             {"restored_step": 180, "step": 180, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
11:20:00.9 81e7e44b save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 240}
11:20:00.9 81e7e44b save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.003, "step": 240, "write_seconds": 0.002}
11:20:00.9 81e7e44b children_at_exit       {"alive": [], "exitcodes": []}
11:20:00.9 81e7e44b exit                   {"code": 0, "reason": "finished 240 steps", "step": 240}
```
