# P3a-grace-default-hold-release on ospool

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6589088.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P3a-grace-default-hold-release`

## Observations

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Trigger hold-release fired at 11:45:22.3 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 600.3 s after the signal = effective grace before SIGKILL.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 6e2679ad | 11:43:50.1 | gpu-node007 | False | 0 | None (None) |  | [(5, 'voluntary', 0.006)] | 85 |
| 511a13be | 11:43:56.5 | gpu-node007 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |

## HTCondor event log (AP clock)

- 11:43:40.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P3a-grace-default-hold-release"; JobBatchName = "probes.dag+6586482" ]
- 11:43:43.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:34269?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14602210%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:43:47.0 `040 file_transfer` Finished transferring input files 
- 11:43:49.0 `021 remote_error` Message from starter on slot1_2@glidein_274178_123184125@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:43:49.0 `001 executing` Job executing on host: <<ip>:44119?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274178_123184125@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_7p1DYF/execute/dir_1971139/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:43:55.0 `040 file_transfer` Started transferring output files 
- 11:43:55.0 `040 file_transfer` Finished transferring output files 
- 11:55:23.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051212  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :      0.00        1         1; Disk (KB)
- 11:55:23.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 11:55:57.0 `009 aborted` Job was aborted. — The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 5
ExitBySignal = true
ExitCode = 85
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959435
JobCurrentStartTransferOutputDate = 1790959435
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_2@glidein_274178_123184125@gpu-node007
LastRemoteWallClockTime = 701.0
LastVacateTime = 1790960123
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ UserRequest = 1 ]
NumInputTransferStarts = 1
NumJobCompletions = 0
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ UserRequest = 1 ]
RemoteWallClockTime = 701.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959435
TransferOutStarted = 1790959435
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1051212; CedarFilesCountTotal = 9; CedarSizeBytesLastRun = 1051212; CedarFilesCountLastRun = 9 ]
VacateReason = via condor_hold (by user <user>)
VacateReasonCode = 1
VacateReasonSubCode = 0
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:43:50.1 6e2679ad start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "6e2679ad", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:43:50.1 6e2679ad history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:43:50.1 6e2679ad restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:43:50.1 6e2679ad loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:43:55.1 6e2679ad save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:43:55.1 6e2679ad save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 5, "write_seconds": 0.005}
11:43:55.1 6e2679ad children_at_exit       {"alive": [], "exitcodes": []}
11:43:55.1 6e2679ad exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:43:56.5 511a13be start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "6e2679ad", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:43:56.5 511a13be history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:43:56.5 511a13be restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790959435.1209946, "saved_by_exec": "6e2679ad", "saved_on_host": "gpu-node007", "saved_reason": "voluntary", "step": 5}
11:43:56.5 511a13be loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:45:22.5 511a13be signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790959522.4414072, "role": "parent", "signal": "SIGTERM", "step": 90}
```

## Trigger log (AP clock)

```
11:13:50.4 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/ospool/ospool/P3a-grace-default-hold-release/job.log", "trigger": "hold-release"}
11:45:22.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790959429.0, "job": "6589088.0", "last_event": "file_transfer", "trigger": "hold-release"}
11:45:22.3 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6589088.0"], "output": "Job 6589088.0 held\n", "rc": 0}
11:55:37.0 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
11:56:08.0 {"action": "command", "cmd": ["/usr/bin/condor_release", "6589088.0"], "output": "\nJob 6589088.0 not found\n", "rc": 1}
11:56:08.0 {"action": "done"}
```
