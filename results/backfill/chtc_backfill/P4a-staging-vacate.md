# P4a-staging-vacate on chtc_backfill

**Question.** Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?

Job: `6573603.0`   Test dir: `/home/<user>/probes/runs/backfill/chtc_backfill/P4a-staging-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 47 s, same host, sandbox NEW, restored step 155 (saved by: signal).
- Trigger vacate fired at 08:56:19.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.4 s after the signal.
- Next execution restored step 155 (saved by: signal) -> the SIGTERM save (step 155) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| fbe3c49c | 08:53:40.8 | gpu4000 | False | 0 | None (None) |  | [(30, 'periodic', 0.137), (60, 'voluntary', 0.211)] | 85 |
| 4f6c30a1 | 08:54:43.1 | gpu4000 | True | 0 | 60 (voluntary) | SIGTERM | [(90, 'periodic', 0.34), (120, 'periodic', 0.236), (150, 'periodic', 0.204), (155, 'signal', 0.318)] | 85 |
| b2163ed3 | 08:57:08.5 | gpu4000 | False | 1 | 155 (signal) |  | [(180, 'periodic', 0.482), (210, 'periodic', 0.438), (240, 'periodic', 0.259), (270, 'periodic', 0.389), (300, 'periodic', 0.166), (330, 'periodic', 0.247), (360, 'periodic', 0.199), (390, 'periodic', 0.394), (420, 'periodic', 0.52), (420, 'final', 0.292)] | 0 |

## HTCondor event log (AP clock)

- 08:53:31.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P4a-staging-vacate"; JobBatchName = "probes.dag+6573292" ]
- 08:53:37.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=gpu4000.chtc.wisc.edu&noUDP&sock=slot2_8_4130900_7fa7_70576>
- 08:53:40.0 `040 file_transfer` Finished transferring input files 
- 08:53:40.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_8@gpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_cdbf3fca }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1003516/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_cdbf3fca = [ Id = "GPU-cdbf3fca"; Capability = 8.9; DeviceName = "NVIDIA L40"; DeviceUuid = "cdbf3fca-8
- 08:54:42.0 `040 file_transfer` Started transferring output files 
- 08:54:42.0 `040 file_transfer` Finished transferring output files 
- 08:56:21.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)            : 279
- 08:57:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=gpu4000.chtc.wisc.edu&noUDP&sock=slot2_8_4130900_7fa7_70578>
- 08:57:07.0 `040 file_transfer` Finished transferring input files 
- 08:57:07.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_8@gpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_cdbf3fca }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1018268/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_cdbf3fca = [ Id = "GPU-cdbf3fca"; Capability = 8.9; DeviceName = "NVIDIA L40"; DeviceUuid = "cdbf3fca-8
- 09:01:44.0 `040 file_transfer` Started transferring output files 
- 09:01:44.0 `040 file_transfer` Finished transferring output files 
- 09:01:45.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 18016  -  Run Bytes Sent By Job; 286336886  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 282.0
CommittedSuspensionTime = 0
CommittedTime = 344
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949704
JobCurrentStartTransferOutputDate = 1790949704
LastRemoteHost = slot2_8@gpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 282.0
LastVacateTime = 1790949380
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 446.0
SuccessCheckpointExitCode = 85
TransferOutFinished = 1790949704
TransferOutStarted = 1790949704
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 18020; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 18016; CedarFilesCountLastRun = 2 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:53:40.8 fbe3c49c start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1003516/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "fbe3c49c", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot2/dir_1003516/scratch"}
08:53:40.8 fbe3c49c history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "store": "staging"}
08:53:40.9 fbe3c49c restore                {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:53:40.9 fbe3c49c loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:54:11.5 fbe3c49c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 30}
08:54:11.6 fbe3c49c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.137, "step": 30, "write_seconds": 0.118}
08:54:42.3 fbe3c49c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:54:42.5 fbe3c49c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.211, "step": 60, "write_seconds": 0.069}
08:54:42.5 fbe3c49c children_at_exit       {"alive": [], "exitcodes": []}
08:54:42.5 fbe3c49c exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:54:43.1 4f6c30a1 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1003516/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "fbe3c49c", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot2/dir_1003516/scratch"}
08:54:43.1 4f6c30a1 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "store": "staging"}
08:54:43.2 4f6c30a1 restore                {"chosen": "step_00000060", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949282.3169518, "saved_by_exec": "fbe3c49c", "saved_on_host": "gpu4000", "saved_reason": "voluntary", 
08:54:43.2 4f6c30a1 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:55:13.6 4f6c30a1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 90}
08:55:13.0 4f6c30a1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.34, "step": 90, "write_seconds": 0.275}
08:55:44.5 4f6c30a1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 120}
08:55:44.7 4f6c30a1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.236, "step": 120, "write_seconds": 0.139}
08:56:15.3 4f6c30a1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 150}
08:56:15.5 4f6c30a1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.204, "step": 150, "write_seconds": 0.141}
08:56:19.7 4f6c30a1 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949379.6145895, "role": "parent", "signal": "SIGTERM", "step": 154}
08:56:20.6 4f6c30a1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 155}
08:56:20.9 4f6c30a1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.318, "step": 155, "write_seconds": 0.238}
08:56:20.9 4f6c30a1 signal_save_finished   {"ok": true, "seconds_since_signal": 1.32}
08:56:20.0 4f6c30a1 children_at_exit       {"alive": [], "exitcodes": []}
08:56:20.0 4f6c30a1 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 155}
08:57:08.5 b2163ed3 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1018268/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b2163ed3", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot2/dir_1018268/scratch"}
08:57:08.5 b2163ed3 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "store": "staging"}
08:57:08.5 b2163ed3 restore                {"chosen": "step_00000155", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6573603.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000155", "nested_dir_ok": true, "saved_at": 1790949380.7440884, "saved_by_exec": "4f6c30a1", "saved_on_host": "gpu4000", "saved_reason": "signal", "st
08:57:08.5 b2163ed3 loop_start             {"restored_step": 155, "step": 155, "total_steps": 420, "voluntary_exit_at": [60]}
08:57:34.1 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 180}
08:57:34.5 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.482, "step": 180, "write_seconds": 0.417}
08:58:05.0 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 210}
08:58:05.5 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.438, "step": 210, "write_seconds": 0.258}
08:58:36.7 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 240}
08:58:36.0 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.259, "step": 240, "write_seconds": 0.136}
08:59:08.0 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 270}
08:59:08.4 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.389, "step": 270, "write_seconds": 0.207}
08:59:39.2 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 300}
08:59:39.4 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.166, "step": 300, "write_seconds": 0.108}
09:00:10.3 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 330}
09:00:10.5 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.247, "step": 330, "write_seconds": 0.162}
09:00:41.5 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 360}
09:00:41.7 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.199, "step": 360, "write_seconds": 0.093}
09:01:12.5 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 390}
09:01:12.9 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.394, "step": 390, "write_seconds": 0.119}
09:01:44.0 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 420}
09:01:44.6 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.52, "step": 420, "write_seconds": 0.219}
09:01:44.6 b2163ed3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
09:01:44.9 b2163ed3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.292, "step": 420, "write_seconds": 0.206}
09:01:44.9 b2163ed3 children_at_exit       {"alive": [], "exitcodes": []}
09:01:44.9 b2163ed3 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:49.2 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill/chtc_backfill/P4a-staging-vacate/job.log", "trigger": "vacate"}
08:56:19.6 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949220.0, "job": "6573603.0", "last_event": "file_transfer", "trigger": "vacate"}
08:56:19.6 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6573603.0"], "output": "Job 6573603.0 vacated\n", "rc": 0}
08:56:19.6 {"action": "done"}
```
