# P2a-save85-vacate on chtc_backfill

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6586849.0`   Test dir: `/home/<user>/probes/runs/backfill2/chtc_backfill/P2a-save85-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 31 s, same host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:26:56.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.6 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 150) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| fb81d8d5 | 11:24:26.2 | txie-dsigpu4000 | False | 0 | None (None) |  | [(60, 'voluntary', 0.003)] | 85 |
| c8af01b3 | 11:25:26.0 | txie-dsigpu4000 | True | 0 | 60 (voluntary) | SIGTERM | [(150, 'signal', 0.01)] | 85 |
| cd5e7a24 | 11:27:28.0 | txie-dsigpu4000 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.01)] | 0 |

## HTCondor event log (AP clock)

- 11:17:36.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P2a-save85-vacate"; JobBatchName = "probes.dag+6586847" ]
- 11:22:00.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=txie-dsigpu4000.chtc.wisc.edu&noUDP&sock=backfill1_5_2080173_cf47_26349>
- 11:24:25.0 `040 file_transfer` Finished transferring input files 
- 11:24:25.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: backfill1_5@txie-dsigpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_aab08e20 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1356092/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_aab08e20 = [ Id = "GPU-aab08e20"; Capability = 9.0; DeviceName = "NVIDIA H100 80GB HBM3"; D
- 11:25:26.0 `040 file_transfer` Started transferring output files 
- 11:25:26.0 `040 file_transfer` Finished transferring output files 
- 11:26:57.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051350  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.03        1         1; Disk (KB)           
- 11:27:24.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=txie-dsigpu4000.chtc.wisc.edu&noUDP&sock=backfill1_5_2080173_cf47_26354>
- 11:27:27.0 `040 file_transfer` Finished transferring input files 
- 11:27:27.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: backfill1_5@txie-dsigpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_aab08e20 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1358051/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_aab08e20 = [ Id = "GPU-aab08e20"; Capability = 9.0; DeviceName = "NVIDIA H100 80GB HBM3"; D
- 11:33:28.0 `040 file_transfer` Started transferring output files 
- 11:33:28.0 `040 file_transfer` Finished transferring output files 
- 11:33:28.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 20324  -  Run Bytes Sent By Job; 287388260  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 364.0
CommittedSuspensionTime = 0
CommittedTime = 424
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958808
JobCurrentStartTransferOutputDate = 1790958808
LastRemoteHost = backfill1_5@txie-dsigpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 364.0
LastVacateTime = 1790958417
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
RemoteWallClockTime = 661.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958808
TransferOutStarted = 1790958808
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1071674; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 20324; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:24:26.2 fb81d8d5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1356092/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "fb81d8d5", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch"}
11:24:26.2 fb81d8d5 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch/ckpt", "store": "spool"}
11:24:26.2 fb81d8d5 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:24:26.2 fb81d8d5 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:25:26.3 fb81d8d5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:25:26.3 fb81d8d5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.003, "step": 60, "write_seconds": 0.003}
11:25:26.3 fb81d8d5 children_at_exit       {"alive": [], "exitcodes": []}
11:25:26.3 fb81d8d5 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:25:26.0 c8af01b3 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1356092/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "fb81d8d5", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch"}
11:25:26.0 c8af01b3 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch/ckpt", "store": "spool"}
11:25:26.0 c8af01b3 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1356092/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958326.2540026, "saved_by_exec": "fb81d8d5", "saved_on_host": "txie-dsigpu4000", "saved_reason": 
11:25:26.0 c8af01b3 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:26:56.6 c8af01b3 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790958416.4723241, "role": "parent", "signal": "SIGTERM", "step": 149}
11:26:57.1 c8af01b3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 150}
11:26:57.1 c8af01b3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.01, "step": 150, "write_seconds": 0.009}
11:26:57.1 c8af01b3 signal_save_finished   {"ok": true, "seconds_since_signal": 0.599}
11:26:57.1 c8af01b3 children_at_exit       {"alive": [], "exitcodes": []}
11:26:57.1 c8af01b3 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 150}
11:27:28.0 cd5e7a24 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1358051/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "cd5e7a24", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1358051/scratch"}
11:27:28.0 cd5e7a24 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1358051/scratch/ckpt", "store": "spool"}
11:27:28.0 cd5e7a24 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1358051/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958326.2540026, "saved_by_exec": "fb81d8d5", "saved_on_host": "txie-dsigpu4000", "saved_reason": 
11:27:28.0 cd5e7a24 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:33:28.3 cd5e7a24 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:33:28.4 cd5e7a24 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.01, "step": 420, "write_seconds": 0.01}
11:33:28.4 cd5e7a24 children_at_exit       {"alive": [], "exitcodes": []}
11:33:28.4 cd5e7a24 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:17:40.9 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill2/chtc_backfill/P2a-save85-vacate/job.log", "trigger": "vacate"}
11:26:56.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958265.0, "job": "6586849.0", "last_event": "file_transfer", "trigger": "vacate"}
11:26:56.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6586849.0"], "output": "Job 6586849.0 vacated\n", "rc": 0}
11:26:56.5 {"action": "done"}
```
