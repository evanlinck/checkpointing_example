# P14a-execute-limit on chtc

**Question.** OSPool access points cap each execution (ap40: AllowedExecuteDuration = 20 h, then a hold). Here allowed_execute_duration = 150 s and the probe exits 85 every 60 s (restarting in place). Does the job finish (each exit-85 restart starts a new execution, so a timed checkpoint keeps a job under the cap), or is it held ~150 s after it first started?

Job: `7195167.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/timecaps/chtc/P14a-execute-limit`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:06  -  Total Remote Usage;)
- First start 09:24:50.1; never held; job ad at first start: {'AllowedExecuteDuration': '150', 'JobStartDate': '1793111075'}.
- Executions seen by the probe: 6; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 240 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 300 (saved by: voluntary).
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d16a10ed | 09:24:50.1 | <host-1> | False | 0 | None (None) |  | [(60, 'voluntary', 0.012)] | 85 |
| a92e50e8 | 09:25:52.4 | <host-1> | True | 0 | 60 (voluntary) |  | [(120, 'voluntary', 0.029)] | 85 |
| 7cc2b900 | 09:26:54.9 | <host-1> | True | 0 | 120 (voluntary) |  | [(180, 'voluntary', 0.036)] | 85 |
| e2ed421c | 09:27:59.1 | <host-1> | True | 0 | 180 (voluntary) |  | [(240, 'voluntary', 0.039)] | 85 |
| 8edf6d09 | 09:29:02.1 | <host-1> | True | 0 | 240 (voluntary) |  | [(300, 'voluntary', 0.041)] | 85 |
| f3373030 | 09:30:04.8 | <host-1> | True | 0 | 300 (voluntary) |  | [(360, 'final', 0.053)] | 0 |

## HTCondor event log (AP clock)

- 09:24:08.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P14a-execute-limit"; JobBatchName = "probes.dag+7195166" ]
- 09:24:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_39_2733766_3479_90092>
- 09:24:47.0 `040 file_transfer` Finished transferring input files 
- 09:24:47.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_39@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1753490/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:25:50.0 `040 file_transfer` Started transferring output files 
- 09:25:50.0 `040 file_transfer` Finished transferring output files 
- 09:26:52.0 `040 file_transfer` Started transferring output files 
- 09:26:52.0 `040 file_transfer` Finished transferring output files 
- 09:27:55.0 `040 file_transfer` Started transferring output files 
- 09:27:55.0 `040 file_transfer` Finished transferring output files 
- 09:28:59.0 `040 file_transfer` Started transferring output files 
- 09:28:59.0 `040 file_transfer` Finished transferring output files 
- 09:30:02.0 `040 file_transfer` Started transferring output files 
- 09:30:02.0 `040 file_transfer` Finished transferring output files 
- 09:31:05.0 `040 file_transfer` Started transferring output files 
- 09:31:05.0 `040 file_transfer` Finished transferring output files 
- 09:31:06.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:06  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 32615  -  Run Bytes Sent By Job; 286339495  -

## condor_history (selected)

```
CheckpointNumber = 4
CommittedSlotTime = 64.0
CommittedSuspensionTime = 0
CommittedTime = 369
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793111465
JobCurrentStartTransferOutputDate = 1793111465
LastRemoteHost = slot1_39@<host-1>
LastRemoteWallClockTime = 391.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 6
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 391.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793111465
TransferOutStarted = 1793111465
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 32615; CedarFilesCountTotal = 16; CedarSizeBytesLastRun = 32615; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:24:50.1 d16a10ed start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:24:50.1 d16a10ed history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:24:50.1 d16a10ed restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:24:50.1 d16a10ed loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:25:50.3 d16a10ed save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:25:50.3 d16a10ed save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.012, "step": 60, "write_seconds": 0.011}
09:25:50.3 d16a10ed children_at_exit       {"alive": [], "exitcodes": []}
09:25:50.3 d16a10ed exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:25:52.4 a92e50e8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:25:52.4 a92e50e8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:25:52.4 a92e50e8 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793111150.2827072, "saved_by_exec": "d16a10ed", "saved_on_host": "<host-1>", "saved_reason": "voluntary
09:25:52.4 a92e50e8 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:26:52.8 a92e50e8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 120}
09:26:52.8 a92e50e8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.029, "step": 120, "write_seconds": 0.027}
09:26:52.8 a92e50e8 children_at_exit       {"alive": [], "exitcodes": []}
09:26:52.8 a92e50e8 exit                   {"code": 85, "reason": "voluntary exit at step 120", "step": 120}
09:26:54.9 7cc2b900 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:26:54.9 7cc2b900 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:26:54.9 7cc2b900 restore                {"chosen": "step_00000120", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000120", "nested_dir_ok": true, "saved_at": 1793111212.7966597, "saved_by_exec": "a92e50e8", "saved_on_host": "<host-1>", "saved_reason": "voluntary
09:26:54.0 7cc2b900 loop_start             {"restored_step": 120, "step": 120, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:27:55.2 7cc2b900 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 180}
09:27:55.3 7cc2b900 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.036, "step": 180, "write_seconds": 0.014}
09:27:55.3 7cc2b900 children_at_exit       {"alive": [], "exitcodes": []}
09:27:55.3 7cc2b900 exit                   {"code": 85, "reason": "voluntary exit at step 180", "step": 180}
09:27:59.1 e2ed421c start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:27:59.1 e2ed421c history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:27:59.1 e2ed421c restore                {"chosen": "step_00000180", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000180", "nested_dir_ok": true, "saved_at": 1793111275.228617, "saved_by_exec": "7cc2b900", "saved_on_host": "<host-1>", "saved_reason": "voluntary"
09:27:59.1 e2ed421c loop_start             {"restored_step": 180, "step": 180, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:28:59.4 e2ed421c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 240}
09:28:59.4 e2ed421c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.039, "step": 240, "write_seconds": 0.022}
09:28:59.4 e2ed421c children_at_exit       {"alive": [], "exitcodes": []}
09:28:59.4 e2ed421c exit                   {"code": 85, "reason": "voluntary exit at step 240", "step": 240}
09:29:02.1 8edf6d09 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 4, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:29:02.1 8edf6d09 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:29:02.1 8edf6d09 restore                {"chosen": "step_00000240", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000240", "nested_dir_ok": true, "saved_at": 1793111339.397619, "saved_by_exec": "e2ed421c", "saved_on_host": "<host-1>", "saved_reason": "voluntary"
09:29:02.1 8edf6d09 loop_start             {"restored_step": 240, "step": 240, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:30:02.3 8edf6d09 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 300}
09:30:02.4 8edf6d09 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.041, "step": 300, "write_seconds": 0.018}
09:30:02.4 8edf6d09 children_at_exit       {"alive": [], "exitcodes": []}
09:30:02.4 8edf6d09 exit                   {"code": 85, "reason": "voluntary exit at step 300", "step": 300}
09:30:04.8 f3373030 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1753490/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 5, "python": "3.12.14", "sandbox_created_by": "d16a10ed", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:30:04.8 f3373030 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "store": "spool"}
09:30:04.8 f3373030 restore                {"chosen": "step_00000300", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1753490/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000300", "nested_dir_ok": true, "saved_at": 1793111402.330288, "saved_by_exec": "8edf6d09", "saved_on_host": "<host-1>", "saved_reason": "voluntary"
09:30:04.8 f3373030 loop_start             {"restored_step": 300, "step": 300, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:31:05.2 f3373030 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 360}
09:31:05.2 f3373030 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.053, "step": 360, "write_seconds": 0.01}
09:31:05.3 f3373030 children_at_exit       {"alive": [], "exitcodes": []}
09:31:05.3 f3373030 exit                   {"code": 0, "reason": "finished 360 steps", "step": 360}
```
