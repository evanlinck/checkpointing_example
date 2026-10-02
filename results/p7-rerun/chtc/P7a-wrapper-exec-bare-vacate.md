# P7a-wrapper-exec-bare-vacate on chtc

**Question.** When the executable is a shell script that execs python, does python receive the soft-kill signal?

Job: `6586478.0`   Test dir: `/home/<user>/probes/runs/p7-rerun/chtc/P7a-wrapper-exec-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 43 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:16:17.8 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.2 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 80) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=2830497 about to exec python3 | WRAPPER run_exec.sh pid=2830967 about to exec python3 | WRAPPER run_exec.sh pid=1483384 about to exec python3

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 87c0a78b | 11:14:37.8 | e2606 | False | 0 | None (None) |  | [(5, 'voluntary', 20.082)] | 85 |
| b137cf3a | 11:15:03.2 | e2606 | True | 0 | 5 (voluntary) | SIGTERM | [(80, 'signal', 20.067)] | 85 |
| 38a0aa55 | 11:17:21.6 | e4019 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:13:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7a-wrapper-exec-bare-vacate"; JobBatchName = "probes.dag+6586475" ]
- 11:14:32.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2606.chtc.wisc.edu&noUDP&sock=slot1_114_530692_45c5_129956>
- 11:14:32.0 `040 file_transfer` Finished transferring input files 
- 11:14:37.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_114@e2606.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2829538/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 11:15:02.0 `040 file_transfer` Started transferring output files 
- 11:15:03.0 `040 file_transfer` Finished transferring output files 
- 11:16:38.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050591  -  Run Bytes Sent By Job; 30764  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :     0.00        1         1; Disk (KB)            :  2
- 11:17:16.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4019.chtc.wisc.edu&noUDP&sock=slot1_36_4092665_7b74_115280>
- 11:17:16.0 `040 file_transfer` Finished transferring input files 
- 11:17:21.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_36@e4019.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1482517/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 11:17:21.0 `040 file_transfer` Started transferring output files 
- 11:17:21.0 `040 file_transfer` Finished transferring output files 
- 11:17:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051651  -  Run Bytes Sent By Job; 1081387  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 7.0
CommittedSuspensionTime = 0
CommittedTime = 32
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790957841
JobCurrentStartTransferOutputDate = 1790957841
LastRemoteHost = slot1_36@e4019.chtc.wisc.edu
LastRemoteWallClockTime = 7.0
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
RemoteWallClockTime = 133.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790957841
TransferOutStarted = 1790957841
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102242; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051651; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:14:37.8 87c0a78b start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2829538/scratch", "mode": "run", "ppid": 2829538, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "87c0a78b", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch"}
11:14:37.8 87c0a78b history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch/ckpt", "store": "spool"}
11:14:37.9 87c0a78b restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:14:37.9 87c0a78b loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
11:14:42.9 87c0a78b save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:15:02.0 87c0a78b save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.082, "step": 5, "write_seconds": 0.033}
11:15:02.0 87c0a78b children_at_exit       {"alive": [], "exitcodes": []}
11:15:02.0 87c0a78b exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:15:03.2 b137cf3a start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2829538/scratch", "mode": "run", "ppid": 2829538, "previous_starts_in_sandbox": 1, "python": "3.9.25", "sandbox_created_by": "87c0a78b", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch"}
11:15:03.2 b137cf3a history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch/ckpt", "store": "spool"}
11:15:03.2 b137cf3a restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2829538/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790957682.9027202, "saved_by_exec": "87c0a78b", "saved_on_host": "e2606", "saved_reason": "voluntary
11:15:03.2 b137cf3a loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
11:16:18.5 b137cf3a signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790957778.4103189, "role": "parent", "signal": "SIGTERM", "step": 79}
11:16:18.5 b137cf3a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 80}
11:16:38.6 b137cf3a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 20.067, "step": 80, "write_seconds": 0.014}
11:16:38.6 b137cf3a signal_save_finished   {"ok": true, "seconds_since_signal": 20.174}
11:16:38.6 b137cf3a children_at_exit       {"alive": [], "exitcodes": []}
11:16:38.6 b137cf3a exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 80}
11:17:21.6 38a0aa55 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1482517/scratch", "mode": "run", "ppid": 1482517, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "38a0aa55", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1482517/scratch"}
11:17:21.6 38a0aa55 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1482517/scratch/ckpt", "store": "spool"}
11:17:21.6 38a0aa55 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1482517/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790957682.9027202, "saved_by_exec": "87c0a78b", "saved_on_host": "e2606", "saved_reason": "voluntary
11:17:21.6 38a0aa55 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:32.6 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/p7-rerun/chtc/P7a-wrapper-exec-bare-vacate/job.log", "trigger": "vacate"}
11:16:17.8 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790957677.0, "job": "6586478.0", "last_event": "file_transfer", "trigger": "vacate"}
11:16:18.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6586478.0"], "output": "Job 6586478.0 vacated\n", "rc": 0}
11:16:18.4 {"action": "done"}
```
