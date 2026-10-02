# P8b-rapid-exits on chtc

**Question.** What happens when a job exits 85 every 5 seconds, 12 times? Throttling, a hold after N restarts, or nothing?

Job: `6574310.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P8b-rapid-exits`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 13; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 17 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 15 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 20 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 25 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 35 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 40 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 45 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 50 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 55 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 13 of 13 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4dbd7480 | 09:00:19.5 | e4086.chtc.wisc.edu | False | 0 | None (None) |  | [(5, 'voluntary', 0.01)] | 85 |
| b4a34adb | 09:00:25.6 | e4086.chtc.wisc.edu | True | 0 | 5 (voluntary) |  | [(10, 'voluntary', 0.053)] | 85 |
| a0b5a219 | 09:00:47.6 | e4086.chtc.wisc.edu | True | 0 | 10 (voluntary) |  | [(15, 'voluntary', 0.136)] | 85 |
| 368dc524 | 09:00:53.8 | e4086.chtc.wisc.edu | True | 0 | 15 (voluntary) |  | [(20, 'voluntary', 0.143)] | 85 |
| 49615003 | 09:01:00.1 | e4086.chtc.wisc.edu | True | 0 | 20 (voluntary) |  | [(25, 'voluntary', 0.143)] | 85 |
| 3a878edf | 09:01:06.4 | e4086.chtc.wisc.edu | True | 0 | 25 (voluntary) |  | [(30, 'voluntary', 0.117)] | 85 |
| 3fa3ce62 | 09:01:12.6 | e4086.chtc.wisc.edu | True | 0 | 30 (voluntary) |  | [(35, 'voluntary', 0.106)] | 85 |
| 4596b78d | 09:01:18.8 | e4086.chtc.wisc.edu | True | 0 | 35 (voluntary) |  | [(40, 'voluntary', 0.118)] | 85 |
| 443cf892 | 09:01:25.0 | e4086.chtc.wisc.edu | True | 0 | 40 (voluntary) |  | [(45, 'voluntary', 0.135)] | 85 |
| 6fe70e60 | 09:01:31.2 | e4086.chtc.wisc.edu | True | 0 | 45 (voluntary) |  | [(50, 'voluntary', 0.108)] | 85 |
| 5c5733fa | 09:01:37.4 | e4086.chtc.wisc.edu | True | 0 | 50 (voluntary) |  | [(55, 'voluntary', 0.105)] | 85 |
| e9ee68d7 | 09:01:43.5 | e4086.chtc.wisc.edu | True | 0 | 55 (voluntary) |  | [(60, 'voluntary', 0.131)] | 85 |
| 5145d764 | 09:01:49.8 | e4086.chtc.wisc.edu | True | 0 | 60 (voluntary) |  | [(70, 'final', 0.122)] | 0 |

## HTCondor event log (AP clock)

- 09:00:10.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P8b-rapid-exits"; JobBatchName = "probes.dag+6573176" ]
- 09:00:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4086.chtc.wisc.edu&noUDP&sock=slot1_73_3546937_bcc4_128639>
- 09:00:18.0 `040 file_transfer` Finished transferring input files 
- 09:00:18.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_73@e4086.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_713400/scratch"; Cpus = 1; Disk = 4194304; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:00:24.0 `040 file_transfer` Started transferring output files 
- 09:00:24.0 `040 file_transfer` Finished transferring output files 
- 09:00:30.0 `040 file_transfer` Started transferring output files 
- 09:00:30.0 `040 file_transfer` Finished transferring output files 
- 09:00:52.0 `040 file_transfer` Started transferring output files 
- 09:00:52.0 `040 file_transfer` Finished transferring output files 
- 09:00:59.0 `040 file_transfer` Started transferring output files 
- 09:00:59.0 `040 file_transfer` Finished transferring output files 
- 09:01:05.0 `040 file_transfer` Started transferring output files 
- 09:01:05.0 `040 file_transfer` Finished transferring output files 
- 09:01:11.0 `040 file_transfer` Started transferring output files 
- 09:01:11.0 `040 file_transfer` Finished transferring output files 
- 09:01:17.0 `040 file_transfer` Started transferring output files 
- 09:01:17.0 `040 file_transfer` Finished transferring output files 
- 09:01:24.0 `040 file_transfer` Started transferring output files 
- 09:01:24.0 `040 file_transfer` Finished transferring output files 
- 09:01:30.0 `040 file_transfer` Started transferring output files 
- 09:01:30.0 `040 file_transfer` Finished transferring output files 
- 09:01:36.0 `040 file_transfer` Started transferring output files 
- 09:01:36.0 `040 file_transfer` Finished transferring output files 
- 09:01:42.0 `040 file_transfer` Started transferring output files 
- 09:01:42.0 `040 file_transfer` Finished transferring output files 
- 09:01:48.0 `040 file_transfer` Started transferring output files 
- 09:01:48.0 `040 file_transfer` Finished transferring output files 
- 09:02:00.0 `040 file_transfer` Started transferring output files 
- 09:02:00.0 `040 file_transfer` Finished transferring output files 
- 09:02:01.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 94611  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 11
CommittedSlotTime = 13.0
CommittedSuspensionTime = 0
CommittedTime = 73
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949720
JobCurrentStartTransferOutputDate = 1790949720
LastRemoteHost = slot1_73@e4086.chtc.wisc.edu
LastRemoteWallClockTime = 110.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 13
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 110.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949720
TransferOutStarted = 1790949720
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 94611; CedarFilesCountTotal = 17; CedarSizeBytesLastRun = 94611; CedarFilesCountLastRun = 17 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:00:19.5 4dbd7480 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:00:19.5 4dbd7480 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:00:19.5 4dbd7480 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:00:19.5 4dbd7480 loop_start             {"restored_step": 0, "step": 0, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:00:24.5 4dbd7480 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:00:24.5 4dbd7480 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.01, "step": 5, "write_seconds": 0.009}
09:00:24.5 4dbd7480 children_at_exit       {"alive": [], "exitcodes": []}
09:00:24.5 4dbd7480 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:00:25.6 b4a34adb start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:00:25.6 b4a34adb history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:00:25.6 b4a34adb restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790949624.5155947, "saved_by_exec": "4dbd7480", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:00:25.6 b4a34adb loop_start             {"restored_step": 5, "step": 5, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:00:30.6 b4a34adb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 10}
09:00:30.7 b4a34adb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.053, "step": 10, "write_seconds": 0.032}
09:00:30.7 b4a34adb children_at_exit       {"alive": [], "exitcodes": []}
09:00:30.7 b4a34adb exit                   {"code": 85, "reason": "voluntary exit at step 10", "step": 10}
09:00:47.6 a0b5a219 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:00:47.6 a0b5a219 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:00:47.6 a0b5a219 restore                {"chosen": "step_00000010", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000010", "nested_dir_ok": true, "saved_at": 1790949630.6560674, "saved_by_exec": "b4a34adb", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:00:47.6 a0b5a219 loop_start             {"restored_step": 10, "step": 10, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:00:52.6 a0b5a219 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 15}
09:00:52.7 a0b5a219 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.136, "step": 15, "write_seconds": 0.004}
09:00:52.7 a0b5a219 children_at_exit       {"alive": [], "exitcodes": []}
09:00:52.8 a0b5a219 exit                   {"code": 85, "reason": "voluntary exit at step 15", "step": 15}
09:00:53.8 368dc524 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:00:53.8 368dc524 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:00:53.9 368dc524 restore                {"chosen": "step_00000015", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000015", "nested_dir_ok": true, "saved_at": 1790949652.6072764, "saved_by_exec": "a0b5a219", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:00:53.9 368dc524 loop_start             {"restored_step": 15, "step": 15, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:00:58.9 368dc524 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 20}
09:00:59.0 368dc524 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.143, "step": 20, "write_seconds": 0.004}
09:00:59.0 368dc524 children_at_exit       {"alive": [], "exitcodes": []}
09:00:59.0 368dc524 exit                   {"code": 85, "reason": "voluntary exit at step 20", "step": 20}
09:01:00.1 49615003 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 4, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:00.1 49615003 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:00.1 49615003 restore                {"chosen": "step_00000020", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000020", "nested_dir_ok": true, "saved_at": 1790949658.866644, "saved_by_exec": "368dc524", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason"
09:01:00.1 49615003 loop_start             {"restored_step": 20, "step": 20, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:05.1 49615003 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 25}
09:01:05.2 49615003 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.143, "step": 25, "write_seconds": 0.006}
09:01:05.2 49615003 children_at_exit       {"alive": [], "exitcodes": []}
09:01:05.2 49615003 exit                   {"code": 85, "reason": "voluntary exit at step 25", "step": 25}
09:01:06.4 3a878edf start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 5, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:06.4 3a878edf history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:06.4 3a878edf restore                {"chosen": "step_00000025", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000025", "nested_dir_ok": true, "saved_at": 1790949665.0854886, "saved_by_exec": "49615003", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:01:06.4 3a878edf loop_start             {"restored_step": 25, "step": 25, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:11.4 3a878edf save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
09:01:11.5 3a878edf save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.117, "step": 30, "write_seconds": 0.007}
09:01:11.5 3a878edf children_at_exit       {"alive": [], "exitcodes": []}
09:01:11.5 3a878edf exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:01:12.6 3fa3ce62 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 6, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:12.6 3fa3ce62 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:12.6 3fa3ce62 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790949671.408797, "saved_by_exec": "3a878edf", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason"
09:01:12.6 3fa3ce62 loop_start             {"restored_step": 30, "step": 30, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:17.6 3fa3ce62 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 35}
09:01:17.7 3fa3ce62 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.106, "step": 35, "write_seconds": 0.004}
09:01:17.7 3fa3ce62 children_at_exit       {"alive": [], "exitcodes": []}
09:01:17.8 3fa3ce62 exit                   {"code": 85, "reason": "voluntary exit at step 35", "step": 35}
09:01:18.8 4596b78d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 7, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:18.8 4596b78d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:18.8 4596b78d restore                {"chosen": "step_00000035", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000035", "nested_dir_ok": true, "saved_at": 1790949677.637791, "saved_by_exec": "3fa3ce62", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason"
09:01:18.8 4596b78d loop_start             {"restored_step": 35, "step": 35, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:23.8 4596b78d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 40}
09:01:23.0 4596b78d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.118, "step": 40, "write_seconds": 0.004}
09:01:23.0 4596b78d children_at_exit       {"alive": [], "exitcodes": []}
09:01:23.0 4596b78d exit                   {"code": 85, "reason": "voluntary exit at step 40", "step": 40}
09:01:25.0 443cf892 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 8, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:25.0 443cf892 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:25.0 443cf892 restore                {"chosen": "step_00000040", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000040", "nested_dir_ok": true, "saved_at": 1790949683.8538058, "saved_by_exec": "4596b78d", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:01:25.0 443cf892 loop_start             {"restored_step": 40, "step": 40, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:30.0 443cf892 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 45}
09:01:30.2 443cf892 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.135, "step": 45, "write_seconds": 0.004}
09:01:30.2 443cf892 children_at_exit       {"alive": [], "exitcodes": []}
09:01:30.2 443cf892 exit                   {"code": 85, "reason": "voluntary exit at step 45", "step": 45}
09:01:31.2 6fe70e60 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 9, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:31.2 6fe70e60 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:31.2 6fe70e60 restore                {"chosen": "step_00000045", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000045", "nested_dir_ok": true, "saved_at": 1790949690.0301754, "saved_by_exec": "443cf892", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:01:31.2 6fe70e60 loop_start             {"restored_step": 45, "step": 45, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:36.2 6fe70e60 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 50}
09:01:36.3 6fe70e60 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.108, "step": 50, "write_seconds": 0.005}
09:01:36.3 6fe70e60 children_at_exit       {"alive": [], "exitcodes": []}
09:01:36.3 6fe70e60 exit                   {"code": 85, "reason": "voluntary exit at step 50", "step": 50}
09:01:37.4 5c5733fa start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 10, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:37.4 5c5733fa history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:37.4 5c5733fa restore                {"chosen": "step_00000050", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000050", "nested_dir_ok": true, "saved_at": 1790949696.2204444, "saved_by_exec": "6fe70e60", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:01:37.4 5c5733fa loop_start             {"restored_step": 50, "step": 50, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:42.4 5c5733fa save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 55}
09:01:42.5 5c5733fa save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.105, "step": 55, "write_seconds": 0.004}
09:01:42.5 5c5733fa children_at_exit       {"alive": [], "exitcodes": []}
09:01:42.5 5c5733fa exit                   {"code": 85, "reason": "voluntary exit at step 55", "step": 55}
09:01:43.5 e9ee68d7 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 11, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:43.6 e9ee68d7 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:43.6 e9ee68d7 restore                {"chosen": "step_00000055", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000055", "nested_dir_ok": true, "saved_at": 1790949702.3931496, "saved_by_exec": "5c5733fa", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason
09:01:43.6 e9ee68d7 loop_start             {"restored_step": 55, "step": 55, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:48.6 e9ee68d7 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:01:48.7 e9ee68d7 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.131, "step": 60, "write_seconds": 0.009}
09:01:48.7 e9ee68d7 children_at_exit       {"alive": [], "exitcodes": []}
09:01:48.7 e9ee68d7 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:01:49.8 5145d764 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_713400/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 12, "python": "3.12.14", "sandbox_created_by": "4dbd7480", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch"}
09:01:49.8 5145d764 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "store": "spool"}
09:01:49.8 5145d764 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_713400/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949708.569094, "saved_by_exec": "e9ee68d7", "saved_on_host": "e4086.chtc.wisc.edu", "saved_reason"
09:01:49.8 5145d764 loop_start             {"restored_step": 60, "step": 60, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
09:01:59.8 5145d764 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 70}
09:01:59.9 5145d764 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.122, "step": 70, "write_seconds": 0.004}
09:01:59.9 5145d764 children_at_exit       {"alive": [], "exitcodes": []}
09:01:59.9 5145d764 exit                   {"code": 0, "reason": "finished 70 steps", "step": 70}
```
