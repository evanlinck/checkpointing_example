# P3a-grace-default-vacate on chtc_backfill

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6573298.0`   Test dir: `/home/<user>/probes/runs/backfill/chtc_backfill/P3a-grace-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 15 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 08:57:04.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f23747cb | 08:55:34.3 | cxiaogpu4000 | False | 0 | None (None) |  | [(5, 'voluntary', 0.009)] | 85 |
| 2db52ea8 | 08:55:42.1 | cxiaogpu4000 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| 638a5997 | 09:07:19.0 | gpu4000 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 08:49:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P3a-grace-default-vacate"; JobBatchName = "probes.dag+6573292" ]
- 08:51:52.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_8_1070907_9c35_79663>
- 08:55:33.0 `040 file_transfer` Finished transferring input files 
- 08:55:33.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_8@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_7aa67590 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3334851/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_7aa67590 = [ Id = "GPU-7aa67590"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 08:55:41.0 `040 file_transfer` Started transferring output files 
- 08:55:41.0 `040 file_transfer` Finished transferring output files 
- 09:07:04.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051227  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 09:07:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=gpu4000.chtc.wisc.edu&noUDP&sock=slot2_8_4130900_7fa7_70597>
- 09:07:18.0 `040 file_transfer` Finished transferring input files 
- 09:07:18.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_8@gpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_cdbf3fca }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1035772/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_cdbf3fca = [ Id = "GPU-cdbf3fca"; Capability = 8.9; DeviceName = "NVIDIA L40"; DeviceUuid = "cdbf3fca-8
- 09:07:19.0 `040 file_transfer` Started transferring output files 
- 09:07:19.0 `040 file_transfer` Finished transferring output files 
- 09:07:19.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052271  -  Run Bytes Sent By Job; 287388137 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 9.0
CommittedSuspensionTime = 0
CommittedTime = 16
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790950039
JobCurrentStartTransferOutputDate = 1790950039
LastRemoteHost = slot2_8@gpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 9.0
LastVacateTime = 1790950024
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
RemoteWallClockTime = 921.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950039
TransferOutStarted = 1790950039
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103498; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052271; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:55:34.3 f23747cb start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3334851/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f23747cb", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch"}
08:55:34.3 f23747cb history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch/ckpt", "store": "spool"}
08:55:34.7 f23747cb restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:55:34.7 f23747cb loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
08:55:41.4 f23747cb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
08:55:41.4 f23747cb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.009, "step": 5, "write_seconds": 0.008}
08:55:41.4 f23747cb children_at_exit       {"alive": [], "exitcodes": []}
08:55:41.4 f23747cb exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
08:55:42.1 2db52ea8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3334851/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "f23747cb", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch"}
08:55:42.1 2db52ea8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch/ckpt", "store": "spool"}
08:55:42.4 2db52ea8 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334851/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790949341.4465015, "saved_by_exec": "f23747cb", "saved_on_host": "cxiaogpu4000", "saved_reason": "vo
08:55:42.4 2db52ea8 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
08:57:04.7 2db52ea8 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790949424.6222708, "role": "parent", "signal": "SIGTERM", "step": 74}
09:07:19.0 638a5997 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1035772/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "638a5997", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot2/dir_1035772/scratch"}
09:07:19.0 638a5997 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot2/dir_1035772/scratch/ckpt", "store": "spool"}
09:07:19.0 638a5997 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot2/dir_1035772/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790949341.4465015, "saved_by_exec": "f23747cb", "saved_on_host": "cxiaogpu4000", "saved_reason": "vo
09:07:19.0 638a5997 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:49.2 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/backfill/chtc_backfill/P3a-grace-default-vacate/job.log", "trigger": "vacate"}
08:57:04.6 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949333.0, "job": "6573298.0", "last_event": "image_size", "trigger": "vacate"}
08:57:04.6 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6573298.0"], "output": "Job 6573298.0 vacated\n", "rc": 0}
08:57:04.6 {"action": "done"}
```
