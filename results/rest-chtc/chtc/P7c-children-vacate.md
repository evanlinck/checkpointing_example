# P7c-children-vacate on chtc

**Question.** Do child processes (like DataLoader workers) receive the signal directly? Does a child that does not handle it die while the parent is still saving?

Job: `6576123.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7c-children-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 40 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:21:17.8 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.2 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 69) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Children that received a signal directly: none; child exits seen by parent: none.

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 56b4df82 | 09:19:47.6 | e2010.chtc.wisc.edu | False | 0 | None (None) |  | [(5, 'voluntary', 20.063)] | 85 |
| 50e9e9a5 | 09:20:13.7 | e2010.chtc.wisc.edu | True | 0 | 5 (voluntary) | SIGTERM | [(69, 'signal', 20.047)] | 85 |
| b01ad3b9 | 09:22:18.1 | e2483 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:14:22.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7c-children-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:15:43.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2010.chtc.wisc.edu&noUDP&sock=slot1_13_1630143_f68a_65336>
- 09:19:46.0 `040 file_transfer` Finished transferring input files 
- 09:19:46.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_13@e2010.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1012179/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:20:12.0 `040 file_transfer` Started transferring output files 
- 09:20:12.0 `040 file_transfer` Finished transferring output files 
- 09:21:38.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050626  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.06        1         1; Disk (KB)           
- 09:22:12.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2483.chtc.wisc.edu&noUDP&sock=slot1_39_2337346_7400_103856>
- 09:22:17.0 `040 file_transfer` Finished transferring input files 
- 09:22:17.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_39@e2483.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3396815/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:22:18.0 `040 file_transfer` Started transferring output files 
- 09:22:18.0 `040 file_transfer` Finished transferring output files 
- 09:22:18.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051654  -  Run Bytes Sent By Job; 287387536 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 6.0
CommittedSuspensionTime = 0
CommittedTime = 31
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790950938
LastRemoteHost = slot1_39@e2483.chtc.wisc.edu
LastRemoteWallClockTime = 6.0
LastVacateTime = 1790950898
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
RemoteWallClockTime = 361.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950938
TransferOutStarted = 1790950938
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102280; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051654; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:19:47.6 56b4df82 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1012179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "56b4df82", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch"}
09:19:47.6 56b4df82 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch/ckpt", "store": "spool"}
09:19:47.6 56b4df82 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:19:47.6 56b4df82-c0 child_start            {"behavior": "ignore", "child": 0, "ppid": 14}
09:19:47.6 56b4df82 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:19:47.6 56b4df82-c1 child_start            {"behavior": "die", "child": 1, "ppid": 14}
09:19:52.7 56b4df82 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:20:12.7 56b4df82 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.063, "step": 5, "write_seconds": 0.004}
09:20:12.7 56b4df82 children_at_exit       {"alive": [true, true], "exitcodes": [null, null]}
09:20:12.8 56b4df82 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:20:13.7 50e9e9a5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1012179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "56b4df82", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch"}
09:20:13.7 50e9e9a5 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch/ckpt", "store": "spool"}
09:20:13.7 50e9e9a5 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1012179/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950792.6617517, "saved_by_exec": "56b4df82", "saved_on_host": "e2010.chtc.wisc.edu", "saved_reaso
09:20:13.7 50e9e9a5-c0 child_start            {"behavior": "ignore", "child": 0, "ppid": 15}
09:20:13.7 50e9e9a5 loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
09:20:13.7 50e9e9a5-c1 child_start            {"behavior": "die", "child": 1, "ppid": 15}
09:21:17.8 50e9e9a5 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790950877.782279, "role": "parent", "signal": "SIGTERM", "step": 68}
09:21:17.9 50e9e9a5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 69}
09:21:37.9 50e9e9a5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 20.047, "step": 69, "write_seconds": 0.004}
09:21:37.9 50e9e9a5 signal_save_finished   {"ok": true, "seconds_since_signal": 20.149}
09:21:37.9 50e9e9a5 children_at_exit       {"alive": [true, true], "exitcodes": [null, null]}
09:21:37.0 50e9e9a5 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 69}
09:22:18.1 b01ad3b9 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3396815/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b01ad3b9", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3396815/scratch"}
09:22:18.1 b01ad3b9 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396815/scratch/ckpt", "store": "spool"}
09:22:18.1 b01ad3b9 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396815/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950792.6617517, "saved_by_exec": "56b4df82", "saved_on_host": "e2010.chtc.wisc.edu", "saved_reaso
09:22:18.1 b01ad3b9 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.9 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7c-children-vacate/job.log", "trigger": "vacate"}
09:21:17.8 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790950786.0, "job": "6576123.0", "last_event": "file_transfer", "trigger": "vacate"}
09:21:17.8 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6576123.0"], "output": "Job 6576123.0 vacated\n", "rc": 0}
09:21:17.8 {"action": "done"}
```
