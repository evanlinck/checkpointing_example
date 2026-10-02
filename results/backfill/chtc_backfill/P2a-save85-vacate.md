# P2a-save85-vacate on chtc_backfill

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6573294.0`   Test dir: `/home/<user>/probes/runs/backfill/chtc_backfill/P2a-save85-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 49 s, same host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 08:53:48.7 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.4 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 7d11cf86 | 08:51:15.6 | cxiaogpu4000 | False | 0 | None (None) |  | [(60, 'voluntary', 0.331)] | 85 |
| e83c8bdd | 08:52:17.9 | cxiaogpu4000 | True | 0 | 60 (voluntary) | SIGTERM | [(149, 'signal', 1.699)] | 85 |
| 93a6e8ee | 08:54:40.6 | cxiaogpu4000 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.047)] | 0 |

## HTCondor event log (AP clock)

- 08:49:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P2a-save85-vacate"; JobBatchName = "probes.dag+6573292" ]
- 08:51:08.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_6_1070907_9c35_79662>
- 08:51:14.0 `040 file_transfer` Finished transferring input files 
- 08:51:14.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_6@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_a0c0169f }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3334610/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_a0c0169f = [ Id = "GPU-a0c0169f"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 08:52:17.0 `040 file_transfer` Started transferring output files 
- 08:52:17.0 `040 file_transfer` Finished transferring output files 
- 08:53:51.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051306  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 08:54:30.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_6_1070907_9c35_79669>
- 08:54:39.0 `040 file_transfer` Finished transferring input files 
- 08:54:39.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_6@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_a0c0169f }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3339879/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_a0c0169f = [ Id = "GPU-a0c0169f"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 09:00:47.0 `040 file_transfer` Started transferring output files 
- 09:00:47.0 `040 file_transfer` Finished transferring output files 
- 09:00:47.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19986  -  Run Bytes Sent By Job; 287388216  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 377.0
CommittedSuspensionTime = 0
CommittedTime = 438
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949647
JobCurrentStartTransferOutputDate = 1790949647
LastRemoteHost = backfill1_6@cxiaogpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 378.0
LastVacateTime = 1790949231
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
RemoteWallClockTime = 541.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949647
TransferOutStarted = 1790949647
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1071292; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 19986; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:51:15.6 7d11cf86 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3334610/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "7d11cf86", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch"}
08:51:15.6 7d11cf86 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch/ckpt", "store": "spool"}
08:51:15.9 7d11cf86 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:51:15.9 7d11cf86 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:52:16.8 7d11cf86 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:52:17.1 7d11cf86 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.331, "step": 60, "write_seconds": 0.33}
08:52:17.1 7d11cf86 children_at_exit       {"alive": [], "exitcodes": []}
08:52:17.1 7d11cf86 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:52:17.9 e83c8bdd start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3334610/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "7d11cf86", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch"}
08:52:17.9 e83c8bdd history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch/ckpt", "store": "spool"}
08:52:18.2 e83c8bdd restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3334610/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949137.103197, "saved_by_exec": "7d11cf86", "saved_on_host": "cxiaogpu4000", "saved_reason": "vol
08:52:18.2 e83c8bdd loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:53:48.8 e83c8bdd signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949228.746531, "role": "parent", "signal": "SIGTERM", "step": 148}
08:53:49.5 e83c8bdd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 149}
08:53:51.2 e83c8bdd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 1.699, "step": 149, "write_seconds": 1.697}
08:53:51.2 e83c8bdd signal_save_finished   {"ok": true, "seconds_since_signal": 2.436}
08:53:51.2 e83c8bdd children_at_exit       {"alive": [], "exitcodes": []}
08:53:51.2 e83c8bdd exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 149}
08:54:40.6 93a6e8ee start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3339879/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "93a6e8ee", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3339879/scratch"}
08:54:40.6 93a6e8ee history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3339879/scratch/ckpt", "store": "spool"}
08:54:40.0 93a6e8ee restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3339879/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949137.103197, "saved_by_exec": "7d11cf86", "saved_on_host": "cxiaogpu4000", "saved_reason": "vol
08:54:40.0 93a6e8ee loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
09:00:47.5 93a6e8ee save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
09:00:47.6 93a6e8ee save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.047, "step": 420, "write_seconds": 0.046}
09:00:47.6 93a6e8ee children_at_exit       {"alive": [], "exitcodes": []}
09:00:47.6 93a6e8ee exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:48.4 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill/chtc_backfill/P2a-save85-vacate/job.log", "trigger": "vacate"}
08:53:48.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949074.0, "job": "6573294.0", "last_event": "file_transfer", "trigger": "vacate"}
08:53:48.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6573294.0"], "output": "Job 6573294.0 vacated\n", "rc": 0}
08:53:48.7 {"action": "done"}
```
