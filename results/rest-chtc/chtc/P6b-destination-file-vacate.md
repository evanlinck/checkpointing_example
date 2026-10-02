# P6b-destination-file-vacate on chtc

**Question.** Does checkpoint_destination = file:///staging/<user> work on CHTC execute points that mount /staging?

Job: `6574209.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P6b-destination-file-vacate`

## Observations

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1086 s, DIFFERENT host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 09:02:46.6 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| bb8b3d81 | 09:00:12.5 | e4022 | False | 0 | None (None) |  | [(60, 'voluntary', 0.008)] | 85 |
| 3b82e95d | 09:19:18.7 | e4017 | False | 1 | None (None) |  | [(60, 'voluntary', 0.008)] | 85 |

## HTCondor event log (AP clock)

- 08:59:45.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P6b-destination-file-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:00:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4022.chtc.wisc.edu&noUDP&sock=slot1_13_2697437_2353_118261>
- 09:00:11.0 `040 file_transfer` Finished transferring input files 
- 09:00:11.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_13@e4022.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_83907/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:01:13.0 `040 file_transfer` Started transferring output files 
- 09:18:43.0 `040 file_transfer` Finished transferring output files 
- 09:18:43.0 `021 remote_error` Error from starter on slot1_13@e4022.chtc.wisc.edu: — Starter failed to upload checkpoint; Code 36 Subcode -1
- 09:18:43.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            :   27
- 09:19:10.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4017.chtc.wisc.edu&noUDP&sock=slot1_96_3342259_9201_123520>
- 09:19:17.0 `040 file_transfer` Finished transferring input files 
- 09:19:17.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_96@e4017.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1043518/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:20:19.0 `040 file_transfer` Started transferring output files 
- 09:37:50.0 `040 file_transfer` Finished transferring output files 
- 09:37:50.0 `021 remote_error` Error from starter on slot1_96@e4017.chtc.wisc.edu: — Starter failed to upload checkpoint; Code 36 Subcode -1
- 09:38:00.0 `004 evicted` Job was evicted. Code 36 Subcode -1 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Error from slot1_96@e4017.chtc.wisc.edu: Starter failed to upload checkpoint; Cpus                 :  
- 09:38:00.0 `012 held` Job was held. — Error from slot1_96@e4017.chtc.wisc.edu: Starter failed to upload checkpoint; Code 36 Subcode -1
- 09:48:57.0 `009 aborted` Job was aborted. — The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE

## condor_history (selected)

```
CheckpointDestination = file:///staging/<user>/ckpt-probes/runs/6574209.0/ckptdest
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 0
ExitBySignal = false
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790950818
LastHoldReason = Error from slot1_96@e4017.chtc.wisc.edu: Starter failed to upload checkpoint
LastHoldReasonCode = 36
LastHoldReasonSubCode = -1
LastRemoteHost = slot1_96@e4017.chtc.wisc.edu
LastRemoteWallClockTime = 1130.0
LastVacateTime = 1790950723
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ FailedToCheckpoint = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 0
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 2
NumVacatesByReason = [ ScheddVacate = 1; FailedToCheckpoint = 1 ]
RemoteWallClockTime = 2251.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790951870
TransferOutStarted = 1790950819
TransferOutput = ckpt,out
TransferOutputStats = [ FILESizeBytesTotal = 0; CedarSizeBytesTotal = 1136; FILEFilesCountTotal = 10; CedarFilesCountTotal = 2; FILESizeBytesLastRun = 0; CedarSizeBytesLastRun = 568; FILEFilesCountLastRun = 5; CedarFilesCountLastRun = 1 ]
VacateReason = Error from slot1_96@e4017.chtc.wisc.edu: Starter failed to upload checkpoint
VacateReasonCode = 36
VacateReasonSubCode = -1
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:00:12.5 bb8b3d81 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_83907/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "bb8b3d81", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_83907/scratch"}
09:00:12.5 bb8b3d81 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_83907/scratch/ckpt", "store": "destination"}
09:00:12.5 bb8b3d81 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_83907/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:00:12.5 bb8b3d81 loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60]}
09:01:12.5 bb8b3d81 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:01:12.5 bb8b3d81 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.008, "step": 60, "write_seconds": 0.007}
09:01:12.5 bb8b3d81 children_at_exit       {"alive": [], "exitcodes": []}
09:01:12.5 bb8b3d81 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:19:18.7 3b82e95d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1043518/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "3b82e95d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1043518/scratch"}
09:19:18.7 3b82e95d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1043518/scratch/ckpt", "store": "destination"}
09:19:18.7 3b82e95d restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1043518/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:19:18.7 3b82e95d loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60]}
09:20:18.8 3b82e95d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:20:18.8 3b82e95d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.008, "step": 60, "write_seconds": 0.008}
09:20:18.8 3b82e95d children_at_exit       {"alive": [], "exitcodes": []}
09:20:18.8 3b82e95d exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
```

## Trigger log (AP clock)

```
08:49:30.8 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P6b-destination-file-vacate/job.log", "trigger": "vacate"}
09:02:46.6 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949611.0, "job": "6574209.0", "last_event": "file_transfer", "trigger": "vacate"}
09:02:46.6 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6574209.0"], "output": "Job 6574209.0 vacated\n", "rc": 0}
09:02:46.6 {"action": "done"}
```
