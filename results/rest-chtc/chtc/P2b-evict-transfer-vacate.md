# P2b-evict-transfer-vacate on chtc

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6573177.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 11 s, DIFFERENT host, sandbox NEW, restored step 150 (saved by: signal).
- Trigger vacate fired at 08:52:26.0 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 150 (saved by: signal) -> the SIGTERM save (step 150) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4184bddb | 08:49:56.5 | e4022 | False | 0 | None (None) |  | [(60, 'voluntary', 0.022)] | 85 |
| 99942d37 | 08:50:57.6 | e4022 | True | 0 | 60 (voluntary) | SIGTERM | [(150, 'signal', 0.013)] | 85 |
| 59540f8e | 08:52:38.2 | e2464.chtc.wisc.edu | False | 1 | 150 (signal) |  | [(420, 'final', 0.011)] | 0 |

## HTCondor event log (AP clock)

- 08:49:24.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2b-evict-transfer-vacate"; JobBatchName = "probes.dag+6573176" ]
- 08:49:50.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4022.chtc.wisc.edu&noUDP&sock=slot1_11_2697437_2353_118225>
- 08:49:55.0 `040 file_transfer` Finished transferring input files 
- 08:49:55.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_11@e4022.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_14927/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:50:56.0 `040 file_transfer` Started transferring output files 
- 08:50:56.0 `040 file_transfer` Finished transferring output files 
- 08:52:27.0 `040 file_transfer` Started transferring output files 
- 08:52:27.0 `040 file_transfer` Finished transferring output files 
- 08:52:27.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2103802  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 08:52:32.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_13_1734380_5bf9_13915>
- 08:52:37.0 `040 file_transfer` Finished transferring input files 
- 08:52:37.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_13@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3616788/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:57:08.0 `040 file_transfer` Started transferring output files 
- 08:57:08.0 `040 file_transfer` Finished transferring output files 
- 08:57:09.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 25779  -  Run Bytes Sent By Job; 288440744  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 279.0
CommittedSuspensionTime = 0
CommittedTime = 339
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790949428
JobCurrentStartTransferOutputDate = 1790949428
LastRemoteHost = slot1_13@e2464.chtc.wisc.edu
LastRemoteWallClockTime = 279.0
LastVacateTime = 1790949147
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
RemoteWallClockTime = 437.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949428
TransferOutStarted = 1790949428
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2129581; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 25779; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
08:49:56.5 4184bddb start                  {"cwd": "/var/lib/condor/execute/slot1/dir_14927/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4184bddb", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch"}
08:49:56.5 4184bddb history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch/ckpt", "store": "spool"}
08:49:56.5 4184bddb restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:49:56.5 4184bddb loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:50:56.6 4184bddb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:50:56.6 4184bddb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.022, "step": 60, "write_seconds": 0.022}
08:50:56.6 4184bddb children_at_exit       {"alive": [], "exitcodes": []}
08:50:56.6 4184bddb exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:50:57.6 99942d37 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_14927/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4184bddb", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch"}
08:50:57.6 99942d37 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch/ckpt", "store": "spool"}
08:50:57.6 99942d37 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_14927/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949056.6265607, "saved_by_exec": "4184bddb", "saved_on_host": "e4022", "saved_reason": "voluntary",
08:50:57.6 99942d37 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:52:27.1 99942d37 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949147.0657077, "role": "parent", "signal": "SIGTERM", "step": 149}
08:52:27.7 99942d37 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 150}
08:52:27.7 99942d37 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.013, "step": 150, "write_seconds": 0.008}
08:52:27.7 99942d37 signal_save_finished   {"ok": true, "seconds_since_signal": 0.659}
08:52:27.7 99942d37 children_at_exit       {"alive": [], "exitcodes": []}
08:52:27.7 99942d37 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 150}
08:52:38.2 59540f8e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3616788/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "59540f8e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3616788/scratch"}
08:52:38.2 59540f8e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3616788/scratch/ckpt", "store": "spool"}
08:52:38.2 59540f8e restore                {"chosen": "step_00000150", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3616788/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000150", "nested_dir_ok": true, "saved_at": 1790949147.7183847, "saved_by_exec": "99942d37", "saved_on_host": "e4022", "saved_reason": "signal", 
08:52:38.2 59540f8e loop_start             {"restored_step": 150, "step": 150, "total_steps": 420, "voluntary_exit_at": [60]}
08:57:08.9 59540f8e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
08:57:08.9 59540f8e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.011, "step": 420, "write_seconds": 0.005}
08:57:08.9 59540f8e children_at_exit       {"alive": [], "exitcodes": []}
08:57:08.9 59540f8e exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:26.8 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-vacate/job.log", "trigger": "vacate"}
08:52:26.0 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790948995.0, "job": "6573177.0", "last_event": "file_transfer", "trigger": "vacate"}
08:52:27.1 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6573177.0"], "output": "Job 6573177.0 vacated\n", "rc": 0}
08:52:27.1 {"action": "done"}
```
