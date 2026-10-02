# P2b-evict-transfer-vacate on chtc_backfill

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6586851.0`   Test dir: `/home/<user>/probes/runs/backfill2/chtc_backfill/P2b-evict-transfer-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 201 s, same host, sandbox NEW, restored step 157 (saved by: signal).
- Trigger vacate fired at 11:30:57.7 (AP clock).
- Evicted execution received SIGTERM 0.3 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.9 s after the signal.
- Next execution restored step 157 (saved by: signal) -> the SIGTERM save (step 157) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 03c995ac | 11:28:19.7 | cxiaogpu4000 | False | 0 | None (None) |  | [(60, 'voluntary', 0.362)] | 85 |
| dda53e58 | 11:29:20.8 | cxiaogpu4000 | True | 0 | 60 (voluntary) | SIGTERM | [(157, 'signal', 0.007)] | 85 |
| 929b7f80 | 11:34:19.7 | cxiaogpu4000 | False | 1 | 157 (signal) |  | [(420, 'final', 0.008)] | 0 |

## HTCondor event log (AP clock)

- 11:17:36.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P2b-evict-transfer-vacate"; JobBatchName = "probes.dag+6586847" ]
- 11:28:04.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_7_1070907_9c35_79970>
- 11:28:18.0 `040 file_transfer` Finished transferring input files 
- 11:28:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_7@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_abbef2b2 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3411888/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_abbef2b2 = [ Id = "GPU-abbef2b2"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 11:29:20.0 `040 file_transfer` Started transferring output files 
- 11:29:20.0 `040 file_transfer` Finished transferring output files 
- 11:30:58.0 `040 file_transfer` Started transferring output files 
- 11:30:58.0 `040 file_transfer` Finished transferring output files 
- 11:30:59.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2104183  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :                 1         1; Disk (KB)            
- 11:31:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_7_1070907_9c35_79976>
- 11:34:18.0 `040 file_transfer` Finished transferring input files 
- 11:34:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_7@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_abbef2b2 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3414584/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_abbef2b2 = [ Id = "GPU-abbef2b2"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 11:38:43.0 `040 file_transfer` Started transferring output files 
- 11:38:43.0 `040 file_transfer` Finished transferring output files 
- 11:38:43.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 26051  -  Run Bytes Sent By Job; 288441125  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 427.0
CommittedSuspensionTime = 0
CommittedTime = 487
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959123
JobCurrentStartTransferOutputDate = 1790959123
LastRemoteHost = backfill1_7@cxiaogpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 427.0
LastVacateTime = 1790958659
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
RemoteWallClockTime = 603.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959123
TransferOutStarted = 1790959123
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2130234; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 26051; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
11:28:19.7 03c995ac start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3411888/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "03c995ac", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch"}
11:28:19.7 03c995ac history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch/ckpt", "store": "spool"}
11:28:19.7 03c995ac restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:28:19.7 03c995ac loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:29:19.8 03c995ac save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:29:20.2 03c995ac save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.362, "step": 60, "write_seconds": 0.36}
11:29:20.2 03c995ac children_at_exit       {"alive": [], "exitcodes": []}
11:29:20.2 03c995ac exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:29:20.8 dda53e58 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3411888/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "03c995ac", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch"}
11:29:20.8 dda53e58 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch/ckpt", "store": "spool"}
11:29:20.8 dda53e58 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3411888/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958560.1557846, "saved_by_exec": "03c995ac", "saved_on_host": "cxiaogpu4000", "saved_reason": "vo
11:29:20.8 dda53e58 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:30:58.0 dda53e58 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790958657.9838316, "role": "parent", "signal": "SIGTERM", "step": 156}
11:30:58.9 dda53e58 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 157}
11:30:58.9 dda53e58 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.007, "step": 157, "write_seconds": 0.007}
11:30:58.9 dda53e58 signal_save_finished   {"ok": true, "seconds_since_signal": 0.928}
11:30:58.9 dda53e58 children_at_exit       {"alive": [], "exitcodes": []}
11:30:58.9 dda53e58 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 157}
11:34:19.7 929b7f80 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3414584/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "929b7f80", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3414584/scratch"}
11:34:19.7 929b7f80 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3414584/scratch/ckpt", "store": "spool"}
11:34:19.7 929b7f80 restore                {"chosen": "step_00000157", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3414584/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000157", "nested_dir_ok": true, "saved_at": 1790958658.9106207, "saved_by_exec": "dda53e58", "saved_on_host": "cxiaogpu4000", "saved_reason": "si
11:34:19.7 929b7f80 loop_start             {"restored_step": 157, "step": 157, "total_steps": 420, "voluntary_exit_at": [60]}
11:38:43.1 929b7f80 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:38:43.1 929b7f80 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.008, "step": 420, "write_seconds": 0.007}
11:38:43.1 929b7f80 children_at_exit       {"alive": [], "exitcodes": []}
11:38:43.1 929b7f80 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:17:41.9 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill2/chtc_backfill/P2b-evict-transfer-vacate/job.log", "trigger": "vacate"}
11:30:57.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958499.0, "job": "6586851.0", "last_event": "file_transfer", "trigger": "vacate"}
11:30:57.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6586851.0"], "output": "Job 6586851.0 vacated\n", "rc": 0}
11:30:57.0 {"action": "done"}
```
