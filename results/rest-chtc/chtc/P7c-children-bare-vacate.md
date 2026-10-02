# P7c-children-bare-vacate on chtc

**Question.** Do child processes (like DataLoader workers) receive the signal directly? Does a child that does not handle it die while the parent is still saving?

Job: `6574514.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7c-children-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 85 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:05:01.8 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 21.1 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 77) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Children that received a signal directly: none; child exits seen by parent: none.

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 231d3642 | 09:03:25.4 | e4087.chtc.wisc.edu | False | 0 | None (None) |  | [(5, 'voluntary', 20.053)] | 85 |
| f1609fe8 | 09:03:50.7 | e4087.chtc.wisc.edu | True | 0 | 5 (voluntary) | SIGTERM | [(77, 'signal', 20.061)] | 85 |
| 1f081db0 | 09:06:47.5 | e2481 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:02:10.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7c-children-bare-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:03:25.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4087.chtc.wisc.edu&noUDP&sock=slot1_155_3567653_088f_116698>
- 09:03:25.0 `040 file_transfer` Finished transferring input files 
- 09:03:25.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_155@e4087.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1610644/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:03:50.0 `040 file_transfer` Started transferring output files 
- 09:03:50.0 `040 file_transfer` Finished transferring output files 
- 09:05:22.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050704  -  Run Bytes Sent By Job; 30512  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :     0.03        1         1; Disk (KB)            :  2
- 09:06:47.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_9_3564670_3d75_95296>
- 09:06:47.0 `040 file_transfer` Finished transferring input files 
- 09:06:47.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_9@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_647353/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:06:47.0 `040 file_transfer` Started transferring output files 
- 09:06:47.0 `040 file_transfer` Finished transferring output files 
- 09:06:47.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051761  -  Run Bytes Sent By Job; 1081248  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 0.0
CommittedSuspensionTime = 0
CommittedTime = 25
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790950007
JobCurrentStartTransferOutputDate = 1790950007
LastRemoteHost = slot1_9@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 0.0
LastVacateTime = 1790949922
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
RemoteWallClockTime = 118.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950007
TransferOutStarted = 1790950007
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102465; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051761; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:03:25.4 231d3642 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1610644/scratch", "mode": "run", "ppid": 1610644, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "231d3642", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch"}
09:03:25.4 231d3642 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch/ckpt", "store": "spool"}
09:03:25.4 231d3642 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:03:25.4 231d3642 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:03:25.4 231d3642-c0 child_start            {"behavior": "ignore", "child": 0, "ppid": 1610663}
09:03:25.4 231d3642-c1 child_start            {"behavior": "die", "child": 1, "ppid": 1610663}
09:03:30.4 231d3642 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:03:50.4 231d3642 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.053, "step": 5, "write_seconds": 0.009}
09:03:50.4 231d3642 children_at_exit       {"alive": [true, true], "exitcodes": [null, null]}
09:03:50.5 231d3642 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:03:50.7 f1609fe8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1610644/scratch", "mode": "run", "ppid": 1610644, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "231d3642", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch"}
09:03:50.7 f1609fe8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch/ckpt", "store": "spool"}
09:03:50.7 f1609fe8 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1610644/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790949810.3945649, "saved_by_exec": "231d3642", "saved_on_host": "e4087.chtc.wisc.edu", "saved_reaso
09:03:50.7 f1609fe8-c0 child_start            {"behavior": "ignore", "child": 0, "ppid": 1610932}
09:03:50.7 f1609fe8 loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
09:03:50.7 f1609fe8-c1 child_start            {"behavior": "die", "child": 1, "ppid": 1610932}
09:05:01.9 f1609fe8 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949901.835755, "role": "parent", "signal": "SIGTERM", "step": 76}
09:05:02.8 f1609fe8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 77}
09:05:22.9 f1609fe8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 20.061, "step": 77, "write_seconds": 0.015}
09:05:22.9 f1609fe8 signal_save_finished   {"ok": true, "seconds_since_signal": 21.025}
09:05:22.9 f1609fe8 children_at_exit       {"alive": [true, true], "exitcodes": [null, null]}
09:05:22.9 f1609fe8 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 77}
09:06:47.5 1f081db0 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_647353/scratch", "mode": "run", "ppid": 647353, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "1f081db0", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_647353/scratch"}
09:06:47.5 1f081db0 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_647353/scratch/ckpt", "store": "spool"}
09:06:47.5 1f081db0 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_647353/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790949810.3945649, "saved_by_exec": "231d3642", "saved_on_host": "e4087.chtc.wisc.edu", "saved_reason
09:06:47.5 1f081db0 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.9 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7c-children-bare-vacate/job.log", "trigger": "vacate"}
09:05:01.8 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949805.0, "job": "6574514.0", "last_event": "file_transfer", "trigger": "vacate"}
09:05:01.8 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6574514.0"], "output": "Job 6574514.0 vacated\n", "rc": 0}
09:05:01.8 {"action": "done"}
```
