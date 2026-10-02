# P2a-save85-vacate on chtc

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6527288.0`   Test dir: `runs/core-chtc/chtc/P2a-save85-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 81 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 13:47:03.1 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.8 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 162) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4e0ad34e | 13:44:20.8 | e2010.chtc.wisc.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.005)] | 85 |
| c77e3801 | 13:45:21.8 | e2010.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [(162, 'signal', 0.006)] | 85 |
| 5fba4b18 | 13:48:24.8 | e2464.chtc.wisc.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.01)] | 0 |

## HTCondor event log (AP clock)

- 13:43:12.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2a-save85-vacate"; JobBatchName = "probes.dag+6527287" ]
- 13:44:15.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2010.chtc.wisc.edu&noUDP&sock=slot1_29_1630143_f68a_62977>
- 13:44:19.0 `040 file_transfer` Finished transferring input files 
- 13:44:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_29@e2010.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1895954/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:45:20.0 `040 file_transfer` Started transferring output files 
- 13:45:21.0 `040 file_transfer` Finished transferring output files 
- 13:47:04.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051405  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.05        1         1; Disk (KB)           
- 13:48:17.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_25_1734380_5bf9_11131>
- 13:48:24.0 `040 file_transfer` Finished transferring input files 
- 13:48:24.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_25@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_745303/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:54:26.0 `040 file_transfer` Started transferring output files 
- 13:54:26.0 `040 file_transfer` Finished transferring output files 
- 13:54:26.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 20771  -  Run Bytes Sent By Job; 287388315  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 369.0
CommittedSuspensionTime = 0
CommittedTime = 429
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790880866
LastRemoteHost = slot1_25@e2464.chtc.wisc.edu
LastRemoteWallClockTime = 370.0
LastVacateTime = 1790880424
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
RemoteWallClockTime = 540.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790880866
TransferOutStarted = 1790880866
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1072176; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 20771; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:44:20.8 4e0ad34e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1895954/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4e0ad34e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch"}
13:44:20.8 4e0ad34e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch/ckpt", "store": "spool"}
13:44:20.8 4e0ad34e restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:44:20.8 4e0ad34e loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:45:20.9 4e0ad34e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:45:20.9 4e0ad34e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.005, "step": 60, "write_seconds": 0.004}
13:45:20.9 4e0ad34e children_at_exit       {"alive": [], "exitcodes": []}
13:45:20.9 4e0ad34e exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:45:21.8 c77e3801 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1895954/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4e0ad34e", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch"}
13:45:21.8 c77e3801 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch/ckpt", "store": "spool"}
13:45:21.8 c77e3801 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1895954/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880320.896464, "saved_by_exec": "4e0ad34e", "saved_on_host": "e2010.chtc.wisc.edu", "saved_reason
13:45:21.8 c77e3801 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:47:03.3 c77e3801 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790880423.261256, "role": "parent", "signal": "SIGTERM", "step": 161}
13:47:04.0 c77e3801 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 162}
13:47:04.0 c77e3801 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.006, "step": 162, "write_seconds": 0.006}
13:47:04.0 c77e3801 signal_save_finished   {"ok": true, "seconds_since_signal": 0.788}
13:47:04.0 c77e3801 children_at_exit       {"alive": [], "exitcodes": []}
13:47:04.0 c77e3801 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 162}
13:48:24.8 5fba4b18 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_745303/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "5fba4b18", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_745303/scratch"}
13:48:24.8 5fba4b18 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_745303/scratch/ckpt", "store": "spool"}
13:48:24.8 5fba4b18 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_745303/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880320.896464, "saved_by_exec": "4e0ad34e", "saved_on_host": "e2010.chtc.wisc.edu", "saved_reason"
13:48:24.8 5fba4b18 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:54:25.8 5fba4b18 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
13:54:25.8 5fba4b18 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.01, "step": 420, "write_seconds": 0.004}
13:54:25.8 5fba4b18 children_at_exit       {"alive": [], "exitcodes": []}
13:54:25.8 5fba4b18 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:17.8 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2a-save85-vacate/job.log", "trigger": "vacate"}
13:47:03.1 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880259.0, "job": "6527288.0", "last_event": "file_transfer", "trigger": "vacate"}
13:47:03.2 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527288.0"], "output": "Job 6527288.0 vacated\n", "rc": 0}
13:47:03.2 {"action": "done"}
```
