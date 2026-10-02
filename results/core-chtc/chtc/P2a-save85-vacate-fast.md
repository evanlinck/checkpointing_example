# P2a-save85-vacate-fast on chtc

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6527290.0`   Test dir: `runs/core-chtc/chtc/P2a-save85-vacate-fast`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 43 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 13:46:49.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -6.3 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 33c2b967 | 13:44:20.8 | e2473 | False | 0 | None (None) |  | [(60, 'voluntary', 0.012)] | 85 |
| b71df791 | 13:45:21.9 | e2473 | True | 0 | 60 (voluntary) |  | [] | none (killed?) |
| 53eda9b1 | 13:47:26.5 | e2481 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.015)] | 0 |

## HTCondor event log (AP clock)

- 13:43:12.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2a-save85-vacate-fast"; JobBatchName = "probes.dag+6527287" ]
- 13:44:14.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2473.chtc.wisc.edu&noUDP&sock=slot1_65_342642_0927_91238>
- 13:44:19.0 `040 file_transfer` Finished transferring input files 
- 13:44:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_65@e2473.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3242335/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:45:21.0 `040 file_transfer` Started transferring output files 
- 13:45:21.0 `040 file_transfer` Finished transferring output files 
- 13:46:49.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051271  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 13:46:51.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_9_3564670_3d75_92165>
- 13:47:25.0 `040 file_transfer` Finished transferring input files 
- 13:47:25.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_9@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3358243/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:53:27.0 `040 file_transfer` Started transferring output files 
- 13:53:27.0 `040 file_transfer` Finished transferring output files 
- 13:53:27.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19731  -  Run Bytes Sent By Job; 96547349  - 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 396.0
CommittedSuspensionTime = 0
CommittedTime = 456
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790880807
JobCurrentStartTransferOutputDate = 1790880807
LastRemoteHost = slot1_9@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 396.0
LastVacateTime = 1790880409
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
RemoteWallClockTime = 552.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790880807
TransferOutStarted = 1790880807
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1071002; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 19731; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:44:20.8 33c2b967 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3242335/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "33c2b967", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch"}
13:44:20.8 33c2b967 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch/ckpt", "store": "spool"}
13:44:20.8 33c2b967 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:44:20.8 33c2b967 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:45:21.1 33c2b967 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:45:21.1 33c2b967 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.012, "step": 60, "write_seconds": 0.01}
13:45:21.1 33c2b967 children_at_exit       {"alive": [], "exitcodes": []}
13:45:21.1 33c2b967 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:45:21.9 b71df791 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3242335/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "33c2b967", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch"}
13:45:21.9 b71df791 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch/ckpt", "store": "spool"}
13:45:21.9 b71df791 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3242335/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880321.1098452, "saved_by_exec": "33c2b967", "saved_on_host": "e2473", "saved_reason": "voluntary
13:45:21.9 b71df791 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:47:26.5 53eda9b1 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3358243/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "53eda9b1", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3358243/scratch"}
13:47:26.5 53eda9b1 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3358243/scratch/ckpt", "store": "spool"}
13:47:26.5 53eda9b1 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3358243/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790880321.1098452, "saved_by_exec": "33c2b967", "saved_on_host": "e2473", "saved_reason": "voluntary
13:47:26.5 53eda9b1 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:53:27.2 53eda9b1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
13:53:27.2 53eda9b1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.015, "step": 420, "write_seconds": 0.014}
13:53:27.2 53eda9b1 children_at_exit       {"alive": [], "exitcodes": []}
13:53:27.2 53eda9b1 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:19.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P2a-save85-vacate-fast/job.log", "trigger": "vacate-fast"}
13:46:49.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880259.0, "job": "6527290.0", "last_event": "file_transfer", "trigger": "vacate-fast"}
13:46:49.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "-fast", "6527290.0"], "output": "Job 6527290.0 fast-vacated\n", "rc": 0}
13:46:49.3 {"action": "done"}
```
