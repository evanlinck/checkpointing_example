# P2b-evict-transfer-vacate on chtc_backfill

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6573296.0`   Test dir: `/home/<user>/probes/runs/backfill/chtc_backfill/P2b-evict-transfer-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 30 s, DIFFERENT host, sandbox NEW, restored step 162 (saved by: signal).
- Trigger vacate fired at 08:54:34.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.2 s after the signal.
- Next execution restored step 162 (saved by: signal) -> the SIGTERM save (step 162) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 3f58c9ba | 08:51:52.4 | jcaicedogpu0003 | False | 0 | None (None) |  | [(60, 'voluntary', 0.009)] | 85 |
| 54d85619 | 08:52:53.1 | jcaicedogpu0003 | True | 0 | 60 (voluntary) | SIGTERM | [(162, 'signal', 0.33)] | 85 |
| b25c8854 | 08:55:05.4 | vetsigian0001 | False | 1 | 162 (signal) |  | [(420, 'final', 0.132)] | 0 |

## HTCondor event log (AP clock)

- 08:49:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P2b-evict-transfer-vacate"; JobBatchName = "probes.dag+6573292" ]
- 08:51:48.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=jcaicedogpu0003.chtc.wisc.edu&noUDP&sock=backfill1_5_2133144_abd1_79477>
- 08:51:51.0 `040 file_transfer` Finished transferring input files 
- 08:51:51.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — SlotName: backfill1_5@jcaicedogpu0003.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_76cc646a }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3213705/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_76cc646a = [ Id = "GPU-76cc646a"; Capability = 8.9; DeviceName = "NVIDIA L40S"; DeviceUuid 
- 08:52:52.0 `040 file_transfer` Started transferring output files 
- 08:52:52.0 `040 file_transfer` Finished transferring output files 
- 08:54:35.0 `040 file_transfer` Started transferring output files 
- 08:54:35.0 `040 file_transfer` Finished transferring output files 
- 08:54:35.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2104450  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 08:54:58.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=vetsigian0001.chtc.wisc.edu&noUDP&sock=slot2_3_1468762_7308_26076>
- 08:55:04.0 `040 file_transfer` Finished transferring input files 
- 08:55:04.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_3@vetsigian0001.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_a2d98c30 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_3503045/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_a2d98c30 = [ Id = "GPU-a2d98c30"; Capability = 7.5; DeviceName = "NVIDIA GeForce RTX 2080 Ti"; De
- 08:59:24.0 `040 file_transfer` Started transferring output files 
- 08:59:24.0 `040 file_transfer` Finished transferring output files 
- 08:59:25.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 26325  -  Run Bytes Sent By Job; 288441392  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 267.0
CommittedSuspensionTime = 0
CommittedTime = 327
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949564
JobCurrentStartTransferOutputDate = 1790949564
LastRemoteHost = slot2_3@vetsigian0001.chtc.wisc.edu
LastRemoteWallClockTime = 267.0
LastVacateTime = 1790949275
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 434.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949564
TransferOutStarted = 1790949564
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2130775; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 26325; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
08:51:52.4 3f58c9ba start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3213705/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "3f58c9ba", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch"}
08:51:52.4 3f58c9ba history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch/ckpt", "store": "spool"}
08:51:52.4 3f58c9ba restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:51:52.4 3f58c9ba loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:52:52.5 3f58c9ba save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:52:52.5 3f58c9ba save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.009, "step": 60, "write_seconds": 0.003}
08:52:52.5 3f58c9ba children_at_exit       {"alive": [], "exitcodes": []}
08:52:52.5 3f58c9ba exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:52:53.1 54d85619 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3213705/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "3f58c9ba", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch"}
08:52:53.1 54d85619 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch/ckpt", "store": "spool"}
08:52:53.1 54d85619 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3213705/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949172.5033288, "saved_by_exec": "3f58c9ba", "saved_on_host": "jcaicedogpu0003", "saved_reason": 
08:52:53.1 54d85619 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:54:34.4 54d85619 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949274.4352858, "role": "parent", "signal": "SIGTERM", "step": 161}
08:54:35.2 54d85619 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 162}
08:54:35.6 54d85619 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.33, "step": 162, "write_seconds": 0.325}
08:54:35.6 54d85619 signal_save_finished   {"ok": true, "seconds_since_signal": 1.143}
08:54:35.6 54d85619 children_at_exit       {"alive": [], "exitcodes": []}
08:54:35.6 54d85619 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 162}
08:55:05.4 b25c8854 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_3503045/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b25c8854", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot2/dir_3503045/scratch"}
08:55:05.4 b25c8854 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot2/dir_3503045/scratch/ckpt", "store": "spool"}
08:55:05.4 b25c8854 restore                {"chosen": "step_00000162", "ckpt_dir": "/var/lib/condor/execute/slot2/dir_3503045/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000162", "nested_dir_ok": true, "saved_at": 1790949275.5673728, "saved_by_exec": "54d85619", "saved_on_host": "jcaicedogpu0003", "saved_reason": 
08:55:05.5 b25c8854 loop_start             {"restored_step": 162, "step": 162, "total_steps": 420, "voluntary_exit_at": [60]}
08:59:24.5 b25c8854 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
08:59:24.6 b25c8854 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.132, "step": 420, "write_seconds": 0.08}
08:59:24.7 b25c8854 children_at_exit       {"alive": [], "exitcodes": []}
08:59:24.7 b25c8854 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:49.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill/chtc_backfill/P2b-evict-transfer-vacate/job.log", "trigger": "vacate"}
08:54:34.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949111.0, "job": "6573296.0", "last_event": "file_transfer", "trigger": "vacate"}
08:54:34.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6573296.0"], "output": "Job 6573296.0 vacated\n", "rc": 0}
08:54:34.4 {"action": "done"}
```
