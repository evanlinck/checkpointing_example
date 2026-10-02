# P7a-wrapper-exec-vacate on chtc

**Question.** When the executable is a shell script that execs python, does python receive the soft-kill signal?

Job: `6586476.0`   Test dir: `/home/<user>/probes/runs/p7-rerun/chtc/P7a-wrapper-exec-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 43 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:16:17.7 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.7 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 78) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=45 about to exec python3 | WRAPPER run_exec.sh pid=14 about to exec python3 | WRAPPER run_exec.sh pid=139 about to exec python3

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4e2bede5 | 11:14:39.4 | e2471 | False | 0 | None (None) |  | [(5, 'voluntary', 20.036)] | 85 |
| 41ccca3a | 11:15:05.3 | e2471 | True | 0 | 5 (voluntary) | SIGTERM | [(78, 'signal', 20.04)] | 85 |
| b6a93528 | 11:17:21.3 | e2620 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:13:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7a-wrapper-exec-vacate"; JobBatchName = "probes.dag+6586475" ]
- 11:14:32.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2471.chtc.wisc.edu&noUDP&sock=slot1_34_3046204_0a5a_104642>
- 11:14:38.0 `040 file_transfer` Finished transferring input files 
- 11:14:38.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_34@e2471.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_690478/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 11:15:04.0 `040 file_transfer` Started transferring output files 
- 11:15:04.0 `040 file_transfer` Finished transferring output files 
- 11:16:38.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050511  -  Run Bytes Sent By Job; 286337130  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 11:17:15.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2620.chtc.wisc.edu&noUDP&sock=slot1_125_2492080_8dd5_125924>
- 11:17:20.0 `040 file_transfer` Finished transferring input files 
- 11:17:20.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_125@e2620.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2624818/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 11:17:21.0 `040 file_transfer` Started transferring output files 
- 11:17:21.0 `040 file_transfer` Finished transferring output files 
- 11:17:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051543  -  Run Bytes Sent By Job; 287387673 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 8.0
CommittedSuspensionTime = 0
CommittedTime = 33
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790957841
LastRemoteHost = slot1_125@e2620.chtc.wisc.edu
LastRemoteWallClockTime = 8.0
LastVacateTime = 1790957798
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
RemoteWallClockTime = 134.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790957841
TransferOutStarted = 1790957841
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102054; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051543; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:14:39.4 4e2bede5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_690478/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4e2bede5", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch"}
11:14:39.4 4e2bede5 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch/ckpt", "store": "spool"}
11:14:39.4 4e2bede5 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:14:39.4 4e2bede5 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
11:14:44.4 4e2bede5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:15:04.5 4e2bede5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.036, "step": 5, "write_seconds": 0.009}
11:15:04.5 4e2bede5 children_at_exit       {"alive": [], "exitcodes": []}
11:15:04.5 4e2bede5 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:15:05.3 41ccca3a start                  {"cwd": "/var/lib/condor/execute/slot1/dir_690478/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4e2bede5", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch"}
11:15:05.3 41ccca3a history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch/ckpt", "store": "spool"}
11:15:05.3 41ccca3a restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_690478/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790957684.4537652, "saved_by_exec": "4e2bede5", "saved_on_host": "e2471", "saved_reason": "voluntary"
11:15:05.3 41ccca3a loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
11:16:17.8 41ccca3a signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790957777.739317, "role": "parent", "signal": "SIGTERM", "step": 77}
11:16:18.4 41ccca3a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 78}
11:16:38.4 41ccca3a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 20.04, "step": 78, "write_seconds": 0.013}
11:16:38.4 41ccca3a signal_save_finished   {"ok": true, "seconds_since_signal": 20.69}
11:16:38.4 41ccca3a children_at_exit       {"alive": [], "exitcodes": []}
11:16:38.4 41ccca3a exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 78}
11:17:21.3 b6a93528 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2624818/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b6a93528", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2624818/scratch"}
11:17:21.3 b6a93528 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2624818/scratch/ckpt", "store": "spool"}
11:17:21.3 b6a93528 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2624818/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790957684.4537652, "saved_by_exec": "4e2bede5", "saved_on_host": "e2471", "saved_reason": "voluntary
11:17:21.3 b6a93528 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:32.5 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/p7-rerun/chtc/P7a-wrapper-exec-vacate/job.log", "trigger": "vacate"}
11:16:17.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790957678.0, "job": "6586476.0", "last_event": "file_transfer", "trigger": "vacate"}
11:16:17.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6586476.0"], "output": "Job 6586476.0 vacated\n", "rc": 0}
11:16:17.7 {"action": "done"}
```
