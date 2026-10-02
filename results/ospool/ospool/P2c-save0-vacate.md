# P2c-save0-vacate on ospool

**Question.** Safety check: if a job saves and exits 0 in response to a vacate, does HTCondor wrongly treat the job as complete?

Job: `6588772.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2c-save0-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 0: gap 49 s, same host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:36:51.7 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 0, 1.0 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 157) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 8130ba23 | 11:34:14.4 | gpu-node007 | False | 0 | None (None) |  | [(60, 'voluntary', 0.007)] | 85 |
| 66311ff1 | 11:35:15.7 | gpu-node007 | True | 0 | 60 (voluntary) | SIGTERM | [(157, 'signal', 0.006)] | 0 |
| 40a2d0bd | 11:37:41.6 | gpu-node007 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.006)] | 0 |

## HTCondor event log (AP clock)

- 11:33:50.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2c-save0-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:34:02.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:34827?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector5#14599430%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:34:12.0 `040 file_transfer` Finished transferring input files 
- 11:34:13.0 `021 remote_error` Message from starter on slot1_2@glidein_274178_123184125@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:34:13.0 `001 executing` Job executing on host: <<ip>:44119?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274178_123184125@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_7p1DYF/execute/dir_1957331/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:35:14.0 `040 file_transfer` Started transferring output files 
- 11:35:14.0 `040 file_transfer` Finished transferring output files 
- 11:36:53.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051207  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 11:37:29.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:40933?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector3#14595816%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:37:39.0 `040 file_transfer` Finished transferring input files 
- 11:37:40.0 `021 remote_error` Message from starter on slot1_2@glidein_274178_123184125@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:37:40.0 `001 executing` Job executing on host: <<ip>:44119?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274178_123184125@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_7p1DYF/execute/dir_1962528/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:43:42.0 `040 file_transfer` Started transferring output files 
- 11:43:42.0 `040 file_transfer` Finished transferring output files 
- 11:43:42.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19470  -  Run Bytes Sent By Job; 287388117  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 375.0
CommittedSuspensionTime = 0
CommittedTime = 435
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959422
JobCurrentStartTransferOutputDate = 1790959422
LastRemoteHost = slot1_2@glidein_274178_123184125@gpu-node007
LastRemoteWallClockTime = 375.0
LastVacateTime = 1790959013
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
RemoteWallClockTime = 547.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959422
TransferOutStarted = 1790959422
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1070677; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 19470; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:34:14.4 8130ba23 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "8130ba23", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:34:14.4 8130ba23 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:34:14.4 8130ba23 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:34:14.4 8130ba23 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:35:14.5 8130ba23 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:35:14.5 8130ba23 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 60, "write_seconds": 0.006}
11:35:14.5 8130ba23 children_at_exit       {"alive": [], "exitcodes": []}
11:35:14.5 8130ba23 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:35:15.7 66311ff1 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "8130ba23", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:35:15.7 66311ff1 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:35:15.7 66311ff1 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958914.4935615, "saved_by_exec": "8130ba23", "saved_on_host": "gpu-node007", "saved_reason": "voluntary", "step": 60}
11:35:15.7 66311ff1 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:36:51.9 66311ff1 signal                 {"first": true, "on_sigterm": "save0", "received_at": 1790959011.8601964, "role": "parent", "signal": "SIGTERM", "step": 156}
11:36:52.8 66311ff1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 157}
11:36:52.8 66311ff1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.006, "step": 157, "write_seconds": 0.005}
11:36:52.8 66311ff1 signal_save_finished   {"ok": true, "seconds_since_signal": 0.966}
11:36:52.8 66311ff1 children_at_exit       {"alive": [], "exitcodes": []}
11:36:52.8 66311ff1 exit                   {"code": 0, "reason": "signal SIGTERM, on_sigterm=save0", "step": 157}
11:37:41.6 40a2d0bd start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "40a2d0bd", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:37:41.6 40a2d0bd history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:37:41.6 40a2d0bd restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958914.4935615, "saved_by_exec": "8130ba23", "saved_on_host": "gpu-node007", "saved_reason": "voluntary", "step": 60}
11:37:41.6 40a2d0bd loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:43:42.1 40a2d0bd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:43:42.1 40a2d0bd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.006, "step": 420, "write_seconds": 0.005}
11:43:42.2 40a2d0bd children_at_exit       {"alive": [], "exitcodes": []}
11:43:42.2 40a2d0bd exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:50.4 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2c-save0-vacate/job.log", "trigger": "vacate"}
11:36:51.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958853.0, "job": "6588772.0", "last_event": "file_transfer", "trigger": "vacate"}
11:36:51.8 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6588772.0"], "output": "Job 6588772.0 vacated\n", "rc": 0}
11:36:51.8 {"action": "done"}
```
