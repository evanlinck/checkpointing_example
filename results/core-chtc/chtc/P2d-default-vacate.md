# P2d-default-vacate on chtc

**Question.** Baseline: a job with no SIGTERM handler dies on the signal. Does it restart from the last voluntary checkpoint (A)?

Job: `6527327.0`   Test dir: `runs/core-chtc/chtc/P2d-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 45 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:57:52.0 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 0.9 s after the signal = effective grace before SIGKILL.
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 781ce6d2 | 13:55:17.6 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.007)] | 85 |
| a53355f9 | 13:56:18.6 | e2016.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [] | none (killed?) |
| 918313d9 | 13:58:37.6 | e2478 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.414)] | 0 |

## HTCondor event log (AP clock)

- 13:54:35.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2d-default-vacate"; JobBatchName = "probes.dag+6527287" ]
- 13:54:44.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76093>
- 13:55:16.0 `040 file_transfer` Finished transferring input files 
- 13:55:16.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4092681/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:56:17.0 `040 file_transfer` Started transferring output files 
- 13:56:17.0 `040 file_transfer` Finished transferring output files 
- 13:57:52.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051418  -  Run Bytes Sent By Job; 95496046  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)            
- 13:58:30.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2478.chtc.wisc.edu&noUDP&sock=slot1_43_254454_9ca4_88089>
- 13:58:36.0 `040 file_transfer` Finished transferring input files 
- 13:58:36.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_43@e2478.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2737576/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:04:39.0 `040 file_transfer` Started transferring output files 
- 14:04:39.0 `040 file_transfer` Finished transferring output files 
- 14:04:40.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19705  -  Run Bytes Sent By Job; 287388328  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 371.0
CommittedSuspensionTime = 0
CommittedTime = 431
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790881479
JobCurrentStartTransferOutputDate = 1790881479
LastRemoteHost = slot1_43@e2478.chtc.wisc.edu
LastRemoteWallClockTime = 371.0
LastVacateTime = 1790881072
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
RemoteWallClockTime = 560.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790881479
TransferOutStarted = 1790881479
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1071123; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 19705; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:55:17.6 781ce6d2 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4092681/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "781ce6d2", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch"}
13:55:17.6 781ce6d2 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch/ckpt", "store": "spool"}
13:55:17.6 781ce6d2 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:55:17.6 781ce6d2 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:56:17.7 781ce6d2 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:56:17.8 781ce6d2 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 60, "write_seconds": 0.006}
13:56:17.8 781ce6d2 children_at_exit       {"alive": [], "exitcodes": []}
13:56:17.8 781ce6d2 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:56:18.6 a53355f9 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4092681/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "781ce6d2", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch"}
13:56:18.6 a53355f9 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch/ckpt", "store": "spool"}
13:56:18.6 a53355f9 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4092681/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880977.7517097, "saved_by_exec": "781ce6d2", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
13:56:18.6 a53355f9 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:57:52.1 a53355f9 signal                 {"first": true, "on_sigterm": "default", "received_at": 1790881072.0362086, "role": "parent", "signal": "SIGTERM", "step": 153}
13:57:52.9 a53355f9 dying_by_signal        {"signal": "SIGTERM", "step": 154}
13:58:37.6 918313d9 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2737576/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "918313d9", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2737576/scratch"}
13:58:37.6 918313d9 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2737576/scratch/ckpt", "store": "spool"}
13:58:37.6 918313d9 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2737576/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880977.7517097, "saved_by_exec": "781ce6d2", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
13:58:37.6 918313d9 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
14:04:39.1 918313d9 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
14:04:39.5 918313d9 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.414, "step": 420, "write_seconds": 0.386}
14:04:39.5 918313d9 children_at_exit       {"alive": [], "exitcodes": []}
14:04:39.6 918313d9 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:21.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2d-default-vacate/job.log", "trigger": "vacate"}
13:57:52.0 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880916.0, "job": "6527327.0", "last_event": "file_transfer", "trigger": "vacate"}
13:57:52.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527327.0"], "output": "Job 6527327.0 vacated\n", "rc": 0}
13:57:52.0 {"action": "done"}
```
