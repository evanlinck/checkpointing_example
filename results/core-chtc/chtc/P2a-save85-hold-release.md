# P2a-save85-hold-release on chtc

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6527292.0`   Test dir: `runs/core-chtc/chtc/P2a-save85-hold-release`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 111 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger hold-release fired at 13:46:49.8 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.0 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 149) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| c50aaab8 | 13:44:20.6 | e2481 | False | 0 | None (None) |  | [(60, 'voluntary', 0.197)] | 85 |
| 3c2198b8 | 13:45:21.7 | e2481 | True | 0 | 60 (voluntary) | SIGTERM | [(149, 'signal', 0.01)] | 85 |
| 65af625d | 13:48:41.9 | e2016.chtc.wisc.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.004)] | 0 |

## HTCondor event log (AP clock)

- 13:43:12.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2a-save85-hold-release"; JobBatchName = "probes.dag+6527287" ]
- 13:44:14.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_9_3564670_3d75_92158>
- 13:44:19.0 `040 file_transfer` Finished transferring input files 
- 13:44:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_9@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3350135/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:45:21.0 `040 file_transfer` Started transferring output files 
- 13:45:21.0 `040 file_transfer` Finished transferring output files 
- 13:46:51.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051287  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :        0        1         1; Disk (KB) 
- 13:46:51.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 13:47:35.0 `013 released` Job was released. — via condor_release (by user <user>)
- 13:48:18.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76073>
- 13:48:41.0 `040 file_transfer` Finished transferring input files 
- 13:48:41.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4089292/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:54:42.0 `040 file_transfer` Started transferring output files 
- 13:54:42.0 `040 file_transfer` Finished transferring output files 
- 13:54:43.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 21031  -  Run Bytes Sent By Job; 96547365  - 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 386.0
CommittedSuspensionTime = 0
CommittedTime = 446
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790880882
JobCurrentStartTransferOutputDate = 1790880882
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_25@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 386.0
LastVacateTime = 1790880411
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ UserRequest = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ UserRequest = 1 ]
RemoteWallClockTime = 543.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790880882
TransferOutStarted = 1790880882
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1072318; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 21031; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:44:20.6 c50aaab8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3350135/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "c50aaab8", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch"}
13:44:20.6 c50aaab8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch/ckpt", "store": "spool"}
13:44:20.6 c50aaab8 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:44:20.6 c50aaab8 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:45:20.7 c50aaab8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:45:20.9 c50aaab8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.197, "step": 60, "write_seconds": 0.138}
13:45:20.9 c50aaab8 children_at_exit       {"alive": [], "exitcodes": []}
13:45:20.9 c50aaab8 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:45:21.7 3c2198b8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3350135/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "c50aaab8", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch"}
13:45:21.7 3c2198b8 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch/ckpt", "store": "spool"}
13:45:21.8 3c2198b8 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3350135/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880320.7733293, "saved_by_exec": "c50aaab8", "saved_on_host": "e2481", "saved_reason": "voluntary
13:45:21.8 3c2198b8 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:46:50.1 3c2198b8 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790880409.966744, "role": "parent", "signal": "SIGTERM", "step": 148}
13:46:50.0 3c2198b8 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 149}
13:46:50.0 3c2198b8 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.01, "step": 149, "write_seconds": 0.009}
13:46:50.0 3c2198b8 signal_save_finished   {"ok": true, "seconds_since_signal": 1.0}
13:46:50.0 3c2198b8 children_at_exit       {"alive": [], "exitcodes": []}
13:46:50.0 3c2198b8 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 149}
13:48:41.9 65af625d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4089292/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "65af625d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4089292/scratch"}
13:48:41.9 65af625d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4089292/scratch/ckpt", "store": "spool"}
13:48:41.9 65af625d restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4089292/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880320.7733293, "saved_by_exec": "c50aaab8", "saved_on_host": "e2481", "saved_reason": "voluntary
13:48:41.9 65af625d loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:54:42.9 65af625d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
13:54:42.9 65af625d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.004, "step": 420, "write_seconds": 0.003}
13:54:42.9 65af625d children_at_exit       {"alive": [], "exitcodes": []}
13:54:42.9 65af625d exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:19.6 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2a-save85-hold-release/job.log", "trigger": "hold-release"}
13:46:49.8 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880259.0, "job": "6527292.0", "last_event": "file_transfer", "trigger": "hold-release"}
13:46:49.0 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6527292.0"], "output": "Job 6527292.0 held\n", "rc": 0}
13:47:04.0 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
13:47:35.0 {"action": "command", "cmd": ["/usr/bin/condor_release", "6527292.0"], "output": "Job 6527292.0 released\n", "rc": 0}
13:47:35.0 {"action": "done"}
```
