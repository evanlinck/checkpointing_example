# P3a-grace-default-vacate on chtc_backfill

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6586853.0`   Test dir: `/home/<user>/probes/runs/backfill2/chtc_backfill/P3a-grace-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 86 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:37:13.0 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 600.3 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 020bdca8 | 11:35:42.9 | txie-dsigpu4000 | False | 0 | None (None) |  | [(5, 'voluntary', 0.003)] | 85 |
| 89ee4d87 | 11:35:49.0 | txie-dsigpu4000 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| 46f7628a | 11:48:39.5 | lli-chtcgpu6000.chtc.wisc.edu | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:17:36.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P3a-grace-default-vacate"; JobBatchName = "probes.dag+6586847" ]
- 11:33:28.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=txie-dsigpu4000.chtc.wisc.edu&noUDP&sock=backfill1_5_2080173_cf47_26368>
- 11:35:42.0 `040 file_transfer` Finished transferring input files 
- 11:35:42.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: backfill1_5@txie-dsigpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_aab08e20 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1361405/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_aab08e20 = [ Id = "GPU-aab08e20"; Capability = 9.0; DeviceName = "NVIDIA H100 80GB HBM3"; D
- 11:35:48.0 `040 file_transfer` Started transferring output files 
- 11:35:48.0 `040 file_transfer` Finished transferring output files 
- 11:47:13.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051263  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 11:48:35.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=lli-chtcgpu6000.chtc.wisc.edu&noUDP&sock=backfill1_1_2844619_2bf5_8373>
- 11:48:38.0 `040 file_transfer` Finished transferring input files 
- 11:48:39.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias — SlotName: backfill1_1@lli-chtcgpu6000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_978250f0 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_417471/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_978250f0 = [ Id = "GPU-978250f0"; Capability = 12.0; DeviceName = "NVIDIA RTX PRO 6000 Black
- 11:48:39.0 `040 file_transfer` Started transferring output files 
- 11:48:39.0 `040 file_transfer` Finished transferring output files 
- 11:48:39.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052378  -  Run Bytes Sent By Job; 287388173 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 5.0
CommittedSuspensionTime = 0
CommittedTime = 10
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959719
JobCurrentStartTransferOutputDate = 1790959719
LastRemoteHost = backfill1_1@lli-chtcgpu6000.chtc.wisc.edu
LastRemoteWallClockTime = 5.0
LastVacateTime = 1790959633
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
RemoteWallClockTime = 830.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959719
TransferOutStarted = 1790959719
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103641; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052378; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:35:42.9 020bdca8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1361405/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "020bdca8", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch"}
11:35:42.9 020bdca8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch/ckpt", "store": "spool"}
11:35:42.9 020bdca8 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:35:42.0 020bdca8 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:35:48.3 020bdca8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:35:48.3 020bdca8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.003, "step": 5, "write_seconds": 0.003}
11:35:48.3 020bdca8 children_at_exit       {"alive": [], "exitcodes": []}
11:35:48.3 020bdca8 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:35:49.0 89ee4d87 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1361405/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "020bdca8", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch"}
11:35:49.0 89ee4d87 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch/ckpt", "store": "spool"}
11:35:49.0 89ee4d87 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1361405/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790958948.3387017, "saved_by_exec": "020bdca8", "saved_on_host": "txie-dsigpu4000", "saved_reason": 
11:35:49.0 89ee4d87 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:37:13.3 89ee4d87 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790959033.2180696, "role": "parent", "signal": "SIGTERM", "step": 84}
11:48:39.5 46f7628a start                  {"cwd": "/var/lib/condor/execute/slot1/dir_417471/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "46f7628a", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_417471/scratch"}
11:48:39.5 46f7628a history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_417471/scratch/ckpt", "store": "spool"}
11:48:39.5 46f7628a restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_417471/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790958948.3387017, "saved_by_exec": "020bdca8", "saved_on_host": "txie-dsigpu4000", "saved_reason": "
11:48:39.5 46f7628a exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:17:41.9 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/backfill2/chtc_backfill/P3a-grace-default-vacate/job.log", "trigger": "vacate"}
11:37:13.0 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958942.0, "job": "6586853.0", "last_event": "image_size", "trigger": "vacate"}
11:37:13.2 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6586853.0"], "output": "Job 6586853.0 vacated\n", "rc": 0}
11:37:13.2 {"action": "done"}
```
