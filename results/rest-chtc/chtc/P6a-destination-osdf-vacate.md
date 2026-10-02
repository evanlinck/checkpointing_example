# P6a-destination-osdf-vacate on chtc

**Question.** Does checkpoint_destination = osdf://... (our /staging namespace) work, from CHTC and from the OSPool? After a vacate, does the restart get the checkpoint back from there?

Job: `6574208.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P6a-destination-osdf-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 292 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 09:02:16.5 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.6 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 147) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| dcc97d0a | 08:59:46.4 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.006)] | 85 |
| 67792d74 | 09:00:49.9 | e2016.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [(147, 'signal', 0.004)] | 85 |
| 92c98848 | 09:07:08.7 | e4049 | False | 1 | 60 (voluntary) |  | [(360, 'final', 0.008)] | 0 |

## HTCondor event log (AP clock)

- 08:59:25.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P6a-destination-osdf-vacate"; JobBatchName = "probes.dag+6573176" ]
- 08:59:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_12_3486004_ed36_78594>
- 08:59:45.0 `040 file_transfer` Finished transferring input files 
- 08:59:45.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_12@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2210659/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:00:48.0 `040 file_transfer` Started transferring output files 
- 09:00:48.0 `040 file_transfer` Finished transferring output files 
- 09:02:17.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1052110  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 09:03:24.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4049.chtc.wisc.edu&noUDP&sock=slot1_34_2613859_e04d_133276>
- 09:07:07.0 `040 file_transfer` Finished transferring input files 
- 09:07:07.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_34@e4049.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3946891/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:12:09.0 `040 file_transfer` Started transferring output files 
- 09:12:09.0 `040 file_transfer` Finished transferring output files 
- 09:12:09.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 18806  -  Run Bytes Sent By Job; 287389678  -

## condor_history (selected)

```
CheckpointDestination = osdf:///chtc/staging/<user>/ckpt-probes/ckptdest/6574208.0
CheckpointNumber = 0
CommittedSlotTime = 525.0
CommittedSuspensionTime = 0
CommittedTime = 585
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790950329
JobCurrentStartTransferOutputDate = 1790950329
LastRemoteHost = slot1_34@e4049.chtc.wisc.edu
LastRemoteWallClockTime = 525.0
LastVacateTime = 1790949737
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
RemoteWallClockTime = 686.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950329
TransferOutStarted = 1790950329
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 19374; CedarFilesCountTotal = 16; CedarSizeBytesLastRun = 18806; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:59:46.4 dcc97d0a start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2210659/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "dcc97d0a", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch"}
08:59:46.4 dcc97d0a history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch/ckpt", "store": "destination"}
08:59:46.4 dcc97d0a restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:59:46.4 dcc97d0a loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60]}
09:00:46.5 dcc97d0a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:00:46.5 dcc97d0a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 60, "write_seconds": 0.004}
09:00:46.5 dcc97d0a children_at_exit       {"alive": [], "exitcodes": []}
09:00:46.5 dcc97d0a exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:00:49.9 67792d74 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2210659/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "dcc97d0a", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch"}
09:00:49.9 67792d74 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch/ckpt", "store": "destination"}
09:00:49.9 67792d74 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2210659/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949646.5403752, "saved_by_exec": "dcc97d0a", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
09:00:49.9 67792d74 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60]}
09:02:16.6 67792d74 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790949736.545754, "role": "parent", "signal": "SIGTERM", "step": 146}
09:02:17.2 67792d74 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 147}
09:02:17.2 67792d74 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.004, "step": 147, "write_seconds": 0.004}
09:02:17.2 67792d74 signal_save_finished   {"ok": true, "seconds_since_signal": 0.641}
09:02:17.2 67792d74 children_at_exit       {"alive": [], "exitcodes": []}
09:02:17.2 67792d74 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 147}
09:07:08.7 92c98848 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3946891/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "92c98848", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3946891/scratch"}
09:07:08.7 92c98848 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3946891/scratch/ckpt", "store": "destination"}
09:07:08.7 92c98848 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3946891/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949646.5403752, "saved_by_exec": "dcc97d0a", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
09:07:08.7 92c98848 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60]}
09:12:09.1 92c98848 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 360}
09:12:09.1 92c98848 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.008, "step": 360, "write_seconds": 0.003}
09:12:09.1 92c98848 children_at_exit       {"alive": [], "exitcodes": []}
09:12:09.1 92c98848 exit                   {"code": 0, "reason": "finished 360 steps", "step": 360}
```

## Trigger log (AP clock)

```
08:49:30.7 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P6a-destination-osdf-vacate/job.log", "trigger": "vacate"}
09:02:16.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790949585.0, "job": "6574208.0", "last_event": "file_transfer", "trigger": "vacate"}
09:02:16.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6574208.0"], "output": "Job 6574208.0 vacated\n", "rc": 0}
09:02:16.5 {"action": "done"}
```
