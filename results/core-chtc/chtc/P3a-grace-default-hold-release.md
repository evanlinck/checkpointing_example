# P3a-grace-default-hold-release on chtc

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6527340.0`   Test dir: `runs/core-chtc/chtc/P3a-grace-default-hold-release`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 70 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger hold-release fired at 14:07:24.6 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 3f85ae72 | 14:05:41.1 | e2481 | False | 0 | None (None) |  | [(5, 'voluntary', 0.012)] | 85 |
| 188b7ee0 | 14:05:49.4 | e2481 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| b5879daa | 14:18:33.8 | e2481 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:04:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P3a-grace-default-hold-release"; JobBatchName = "probes.dag+6527287" ]
- 14:05:31.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_30_3564670_3d75_92220>
- 14:05:40.0 `040 file_transfer` Finished transferring input files 
- 14:05:40.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_30@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3440670/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:05:48.0 `040 file_transfer` Started transferring output files 
- 14:05:48.0 `040 file_transfer` Finished transferring output files 
- 14:17:28.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051209  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :      0.00        1         1; Disk (KB)
- 14:17:28.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 14:18:10.0 `013 released` Job was released. — via condor_release (by user <user>)
- 14:18:28.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_39_3564670_3d75_92258>
- 14:18:33.0 `040 file_transfer` Finished transferring input files 
- 14:18:33.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_39@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3479566/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:18:33.0 `040 file_transfer` Started transferring output files 
- 14:18:33.0 `040 file_transfer` Finished transferring output files 
- 14:18:34.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052260  -  Run Bytes Sent By Job; 287388119 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 6.0
CommittedSuspensionTime = 0
CommittedTime = 13
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790882313
JobCurrentStartTransferOutputDate = 1790882313
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_39@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 6.0
LastVacateTime = 1790882248
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
RemoteWallClockTime = 723.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790882313
TransferOutStarted = 1790882313
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103469; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052260; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:05:41.1 3f85ae72 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3440670/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "3f85ae72", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch"}
14:05:41.1 3f85ae72 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch/ckpt", "store": "spool"}
14:05:41.1 3f85ae72 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:05:41.2 3f85ae72 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
14:05:48.7 3f85ae72 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
14:05:48.7 3f85ae72 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.012, "step": 5, "write_seconds": 0.011}
14:05:48.7 3f85ae72 children_at_exit       {"alive": [], "exitcodes": []}
14:05:48.7 3f85ae72 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
14:05:49.4 188b7ee0 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3440670/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "3f85ae72", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch"}
14:05:49.4 188b7ee0 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch/ckpt", "store": "spool"}
14:05:49.4 188b7ee0 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3440670/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790881548.7129638, "saved_by_exec": "3f85ae72", "saved_on_host": "e2481", "saved_reason": "voluntary
14:05:49.4 188b7ee0 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
14:07:24.7 188b7ee0 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790881644.6013854, "role": "parent", "signal": "SIGTERM", "step": 76}
14:18:33.8 b5879daa start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3479566/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b5879daa", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3479566/scratch"}
14:18:33.8 b5879daa history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3479566/scratch/ckpt", "store": "spool"}
14:18:33.8 b5879daa restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3479566/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790881548.7129638, "saved_by_exec": "3f85ae72", "saved_on_host": "e2481", "saved_reason": "voluntary
14:18:33.8 b5879daa exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
13:43:23.1 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P3a-grace-default-hold-release/job.log", "trigger": "hold-release"}
14:07:24.6 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790881540.0, "job": "6527340.0", "last_event": "image_size", "trigger": "hold-release"}
14:07:24.6 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6527340.0"], "output": "Job 6527340.0 held\n", "rc": 0}
14:17:40.2 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
14:18:10.3 {"action": "command", "cmd": ["/usr/bin/condor_release", "6527340.0"], "output": "Job 6527340.0 released\n", "rc": 0}
14:18:10.3 {"action": "done"}
```
