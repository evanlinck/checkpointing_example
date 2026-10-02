# P2b-evict-transfer-hold-release on chtc

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6573181.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-hold-release`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 88 s, DIFFERENT host, sandbox NEW, restored step 154 (saved by: signal).
- Trigger hold-release fired at 08:52:30.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.5 s after the signal.
- Next execution restored step 154 (saved by: signal) -> the SIGTERM save (step 154) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 1ed3a8c4 | 08:49:55.0 | e2464.chtc.wisc.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.004)] | 85 |
| a34b0ce0 | 08:50:56.7 | e2464.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [(154, 'signal', 0.007)] | 85 |
| 5a69e9a4 | 08:53:58.4 | e2016.chtc.wisc.edu | False | 1 | 154 (signal) |  | [(420, 'final', 0.005)] | 0 |

## HTCondor event log (AP clock)

- 08:49:24.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2b-evict-transfer-hold-release"; JobBatchName = "probes.dag+6573176" ]
- 08:49:49.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_13_1734380_5bf9_13908>
- 08:49:55.0 `040 file_transfer` Finished transferring input files 
- 08:49:55.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_13@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3601124/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:50:56.0 `040 file_transfer` Started transferring output files 
- 08:50:56.0 `040 file_transfer` Finished transferring output files 
- 08:52:30.0 `040 file_transfer` Started transferring output files 
- 08:52:30.0 `040 file_transfer` Finished transferring output files 
- 08:52:30.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2104613  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :      0.00        1         1; Disk (KB)
- 08:52:30.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 08:53:15.0 `013 released` Job was released. — via condor_release (by user <user>)
- 08:53:51.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_12_3486004_ed36_78587>
- 08:53:57.0 `040 file_transfer` Finished transferring input files 
- 08:53:57.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_12@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2190057/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:58:25.0 `040 file_transfer` Started transferring output files 
- 08:58:25.0 `040 file_transfer` Finished transferring output files 
- 08:58:25.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 27774  -  Run Bytes Sent By Job; 288441555  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 275.0
CommittedSuspensionTime = 0
CommittedTime = 335
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949505
JobCurrentStartTransferOutputDate = 1790949505
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_12@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 275.0
LastVacateTime = 1790949150
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ UserRequest = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ UserRequest = 1 ]
RemoteWallClockTime = 436.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949505
TransferOutStarted = 1790949505
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2132387; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 27774; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
08:49:55.0 1ed3a8c4 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3601124/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "1ed3a8c4", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch"}
08:49:55.0 1ed3a8c4 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch/ckpt", "store": "spool"}
08:49:55.0 1ed3a8c4 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:49:55.0 1ed3a8c4 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:50:56.1 1ed3a8c4 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:50:56.1 1ed3a8c4 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.004, "step": 60, "write_seconds": 0.004}
08:50:56.1 1ed3a8c4 children_at_exit       {"alive": [], "exitcodes": []}
08:50:56.1 1ed3a8c4 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:50:56.7 a34b0ce0 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3601124/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "1ed3a8c4", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch"}
08:50:56.7 a34b0ce0 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch/ckpt", "store": "spool"}
08:50:56.7 a34b0ce0 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3601124/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949056.119187, "saved_by_exec": "1ed3a8c4", "saved_on_host": "e2464.chtc.wisc.edu", "saved_reason
08:50:56.7 a34b0ce0 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:52:30.4 a34b0ce0 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949150.3822312, "role": "parent", "signal": "SIGTERM", "step": 153}
08:52:30.9 a34b0ce0 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 154}
08:52:30.9 a34b0ce0 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.007, "step": 154, "write_seconds": 0.004}
08:52:30.9 a34b0ce0 signal_save_finished   {"ok": true, "seconds_since_signal": 0.528}
08:52:30.9 a34b0ce0 children_at_exit       {"alive": [], "exitcodes": []}
08:52:30.9 a34b0ce0 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 154}
08:53:58.4 5a69e9a4 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2190057/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "5a69e9a4", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2190057/scratch"}
08:53:58.4 5a69e9a4 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2190057/scratch/ckpt", "store": "spool"}
08:53:58.4 5a69e9a4 restore                {"chosen": "step_00000154", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2190057/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000154", "nested_dir_ok": true, "saved_at": 1790949150.9067755, "saved_by_exec": "a34b0ce0", "saved_on_host": "e2464.chtc.wisc.edu", "saved_reaso
08:53:58.4 5a69e9a4 loop_start             {"restored_step": 154, "step": 154, "total_steps": 420, "voluntary_exit_at": [60]}
08:58:25.3 5a69e9a4 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
08:58:25.3 5a69e9a4 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.005, "step": 420, "write_seconds": 0.003}
08:58:25.3 5a69e9a4 children_at_exit       {"alive": [], "exitcodes": []}
08:58:25.3 5a69e9a4 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:30.2 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-hold-release/job.log", "trigger": "hold-release"}
08:52:30.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790948995.0, "job": "6573181.0", "last_event": "file_transfer", "trigger": "hold-release"}
08:52:30.4 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6573181.0"], "output": "Job 6573181.0 held\n", "rc": 0}
08:52:45.4 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
08:53:15.5 {"action": "command", "cmd": ["/usr/bin/condor_release", "6573181.0"], "output": "Job 6573181.0 released\n", "rc": 0}
08:53:15.5 {"action": "done"}
```
