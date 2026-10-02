# P2b-evict-transfer-vacate on chtc

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Does condor_submit accept the combination, and is step B transferred on eviction?

Job: `6527294.0`   Test dir: `runs/core-chtc/chtc/P2b-evict-transfer-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 96 s, DIFFERENT host, sandbox NEW, restored step 162 (saved by: signal).
- Trigger vacate fired at 13:47:05.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 162 (saved by: signal) -> the SIGTERM save (step 162) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d3c65c35 | 13:44:22.7 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.006)] | 85 |
| 00b761d1 | 13:45:23.8 | e2016.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [(162, 'signal', 0.004)] | 85 |
| 03383a44 | 13:48:41.9 | e2475 | False | 1 | 162 (signal) |  | [(420, 'final', 3.072)] | 0 |

## HTCondor event log (AP clock)

- 13:43:13.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2b-evict-transfer-vacate"; JobBatchName = "probes.dag+6527287" ]
- 13:44:15.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76068>
- 13:44:21.0 `040 file_transfer` Finished transferring input files 
- 13:44:21.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4088023/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:45:22.0 `040 file_transfer` Started transferring output files 
- 13:45:23.0 `040 file_transfer` Finished transferring output files 
- 13:47:06.0 `040 file_transfer` Started transferring output files 
- 13:47:06.0 `040 file_transfer` Finished transferring output files 
- 13:47:06.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2104596  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 13:48:17.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2475.chtc.wisc.edu&noUDP&sock=slot1_20_1013765_e6e2_99020>
- 13:48:41.0 `040 file_transfer` Finished transferring input files 
- 13:48:41.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_20@e2475.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3223201/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:53:04.0 `040 file_transfer` Started transferring output files 
- 13:53:04.0 `040 file_transfer` Finished transferring output files 
- 13:53:05.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 26085  -  Run Bytes Sent By Job; 97600706  - 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 288.0
CommittedSuspensionTime = 0
CommittedTime = 348
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790880784
JobCurrentStartTransferOutputDate = 1790880784
LastRemoteHost = slot1_20@e2475.chtc.wisc.edu
LastRemoteWallClockTime = 288.0
LastVacateTime = 1790880426
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
RemoteWallClockTime = 459.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790880784
TransferOutStarted = 1790880784
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2130681; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 26085; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
13:44:22.7 d3c65c35 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4088023/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d3c65c35", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch"}
13:44:22.7 d3c65c35 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch/ckpt", "store": "spool"}
13:44:22.7 d3c65c35 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:44:22.7 d3c65c35 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:45:22.8 d3c65c35 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:45:22.8 d3c65c35 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 60, "write_seconds": 0.005}
13:45:22.8 d3c65c35 children_at_exit       {"alive": [], "exitcodes": []}
13:45:22.8 d3c65c35 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:45:23.8 00b761d1 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4088023/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "d3c65c35", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch"}
13:45:23.8 00b761d1 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch/ckpt", "store": "spool"}
13:45:23.8 00b761d1 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4088023/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880322.8324018, "saved_by_exec": "d3c65c35", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
13:45:23.9 00b761d1 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:47:05.5 00b761d1 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790880425.4003515, "role": "parent", "signal": "SIGTERM", "step": 161}
13:47:06.1 00b761d1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 162}
13:47:06.1 00b761d1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.004, "step": 162, "write_seconds": 0.003}
13:47:06.1 00b761d1 signal_save_finished   {"ok": true, "seconds_since_signal": 0.695}
13:47:06.1 00b761d1 children_at_exit       {"alive": [], "exitcodes": []}
13:47:06.1 00b761d1 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 162}
13:48:41.9 03383a44 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3223201/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "03383a44", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3223201/scratch"}
13:48:41.9 03383a44 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3223201/scratch/ckpt", "store": "spool"}
13:48:41.0 03383a44 restore                {"chosen": "step_00000162", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3223201/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000162", "nested_dir_ok": true, "saved_at": 1790880426.0937886, "saved_by_exec": "00b761d1", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
13:48:41.0 03383a44 loop_start             {"restored_step": 162, "step": 162, "total_steps": 420, "voluntary_exit_at": [60]}
13:53:00.4 03383a44 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
13:53:03.5 03383a44 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 3.072, "step": 420, "write_seconds": 2.805}
13:53:03.6 03383a44 children_at_exit       {"alive": [], "exitcodes": []}
13:53:04.1 03383a44 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:20.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2b-evict-transfer-vacate/job.log", "trigger": "vacate"}
13:47:05.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880261.0, "job": "6527294.0", "last_event": "file_transfer", "trigger": "vacate"}
13:47:05.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527294.0"], "output": "Job 6527294.0 vacated\n", "rc": 0}
13:47:05.4 {"action": "done"}
```
