# P2c-save0-vacate on chtc

**Question.** Safety check: if a job saves and exits 0 in response to a vacate, does HTCondor wrongly treat the job as complete?

Job: `6527326.0`   Test dir: `runs/core-chtc/chtc/P2c-save0-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 0: gap 28 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:56:36.4 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 0, 0.5 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 74bc2391 | 13:54:02.8 | e2475 | False | 0 | None (None) |  | [(60, 'voluntary', 0.019)] | 85 |
| 68422c97 | 13:55:06.5 | e2475 | True | 0 | 60 (voluntary) | SIGTERM | [(149, 'signal', 0.085)] | 0 |
| 2438ff7c | 13:57:05.4 | e2464.chtc.wisc.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.007)] | 0 |

## HTCondor event log (AP clock)

- 13:53:35.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2c-save0-vacate"; JobBatchName = "probes.dag+6527287" ]
- 13:53:54.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2475.chtc.wisc.edu&noUDP&sock=slot1_20_1013765_e6e2_99036>
- 13:54:01.0 `040 file_transfer` Finished transferring input files 
- 13:54:01.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_20@e2475.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3242418/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:55:05.0 `040 file_transfer` Started transferring output files 
- 13:55:05.0 `040 file_transfer` Finished transferring output files 
- 13:56:37.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051194  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 13:56:59.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_44_1734380_5bf9_11152>
- 13:57:04.0 `040 file_transfer` Finished transferring input files 
- 13:57:04.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_44@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_747838/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:03:06.0 `040 file_transfer` Started transferring output files 
- 14:03:06.0 `040 file_transfer` Finished transferring output files 
- 14:03:06.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 20260  -  Run Bytes Sent By Job; 287388104  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 367.0
CommittedSuspensionTime = 0
CommittedTime = 427
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790881386
LastRemoteHost = slot1_44@e2464.chtc.wisc.edu
LastRemoteWallClockTime = 367.0
LastVacateTime = 1790880997
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
RemoteWallClockTime = 530.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790881386
TransferOutStarted = 1790881386
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1071454; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 20260; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:54:02.8 74bc2391 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3242418/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "74bc2391", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch"}
13:54:02.8 74bc2391 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch/ckpt", "store": "spool"}
13:54:02.8 74bc2391 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:54:02.8 74bc2391 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:55:02.0 74bc2391 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:55:02.0 74bc2391 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.019, "step": 60, "write_seconds": 0.018}
13:55:02.0 74bc2391 children_at_exit       {"alive": [], "exitcodes": []}
13:55:02.0 74bc2391 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:55:06.5 68422c97 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3242418/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "74bc2391", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch"}
13:55:06.5 68422c97 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch/ckpt", "store": "spool"}
13:55:06.5 68422c97 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242418/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880902.992075, "saved_by_exec": "74bc2391", "saved_on_host": "e2475", "saved_reason": "voluntary"
13:55:06.5 68422c97 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:56:36.5 68422c97 signal                 {"first": true, "on_sigterm": "save0", "received_at": 1790880996.4879675, "role": "parent", "signal": "SIGTERM", "step": 148}
13:56:36.9 68422c97 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 149}
13:56:36.0 68422c97 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.085, "step": 149, "write_seconds": 0.081}
13:56:36.0 68422c97 signal_save_finished   {"ok": true, "seconds_since_signal": 0.49}
13:56:36.0 68422c97 children_at_exit       {"alive": [], "exitcodes": []}
13:56:36.0 68422c97 exit                   {"code": 0, "reason": "signal SIGTERM, on_sigterm=save0", "step": 149}
13:57:05.4 2438ff7c start                  {"cwd": "/var/lib/condor/execute/slot1/dir_747838/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "2438ff7c", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_747838/scratch"}
13:57:05.4 2438ff7c history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_747838/scratch/ckpt", "store": "spool"}
13:57:05.4 2438ff7c restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_747838/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880902.992075, "saved_by_exec": "74bc2391", "saved_on_host": "e2475", "saved_reason": "voluntary",
13:57:05.4 2438ff7c loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
14:03:06.2 2438ff7c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
14:03:06.2 2438ff7c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.007, "step": 420, "write_seconds": 0.005}
14:03:06.2 2438ff7c children_at_exit       {"alive": [], "exitcodes": []}
14:03:06.2 2438ff7c exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:20.6 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2c-save0-vacate/job.log", "trigger": "vacate"}
13:56:36.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880841.0, "job": "6527326.0", "last_event": "file_transfer", "trigger": "vacate"}
13:56:36.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527326.0"], "output": "Job 6527326.0 vacated\n", "rc": 0}
13:56:36.5 {"action": "done"}
```
