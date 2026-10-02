# P2b-evict-transfer-hold-release on ospool

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6588467.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-hold-release`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 92 s, DIFFERENT host, sandbox NEW, restored step 153 (saved by: signal).
- Trigger hold-release fired at 11:33:21.5 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.1 s after the signal.
- Next execution restored step 153 (saved by: signal) -> the SIGTERM save (step 153) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 8adce357 | 11:30:47.5 | gpu-node007 | False | 0 | None (None) |  | [(60, 'voluntary', 0.007)] | 85 |
| 36d6d439 | 11:31:49.1 | gpu-node007 | True | 0 | 60 (voluntary) | SIGTERM | [(153, 'signal', 0.006)] | 85 |
| f02efcce | 11:34:53.0 | a213.anvil.rcac.purdue.edu | False | 1 | 153 (signal) |  | [(420, 'final', 0.007)] | 0 |

## HTCondor event log (AP clock)

- 11:30:30.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2b-evict-transfer-hold-release"; JobBatchName = "probes.dag+6586482" ]
- 11:30:40.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:44387?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14601818%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:30:45.0 `040 file_transfer` Finished transferring input files 
- 11:30:46.0 `021 remote_error` Message from starter on slot1_2@glidein_274178_123184125@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:30:46.0 `001 executing` Job executing on host: <<ip>:44119?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274178_123184125@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_7p1DYF/execute/dir_1952987/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:31:47.0 `040 file_transfer` Started transferring output files 
- 11:31:48.0 `040 file_transfer` Finished transferring output files 
- 11:33:22.0 `040 file_transfer` Started transferring output files 
- 11:33:22.0 `040 file_transfer` Finished transferring output files 
- 11:33:22.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2104188  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :        0        1         1; Disk (KB) 
- 11:33:22.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 11:34:06.0 `013 released` Job was released. — via condor_release (by user <user>)
- 11:34:48.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:39399?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector5#14599462%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:34:51.0 `040 file_transfer` Finished transferring input files 
- 11:34:52.0 `021 remote_error` Message from starter on slot1_38@glidein_79141_540569430@a213.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:34:52.0 `001 executing` Job executing on host: <<ip>:38025?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_38@glidein_79141_540569430@a213.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_Y7BbYf/execute/dir_2327211/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:39:21.0 `040 file_transfer` Started transferring output files 
- 11:39:21.0 `040 file_transfer` Finished transferring output files 
- 11:39:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 27254  -  Run Bytes Sent By Job; 288441130  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 275.0
CommittedSuspensionTime = 0
CommittedTime = 335
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959161
JobCurrentStartTransferOutputDate = 1790959161
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_38@glidein_79141_540569430@a213.anvil.rcac.purdue.edu
LastRemoteWallClockTime = 275.0
LastVacateTime = 1790958802
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ UserRequest = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ UserRequest = 1 ]
RemoteWallClockTime = 438.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959161
TransferOutStarted = 1790959161
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2131442; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 27254; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
11:30:47.5 8adce357 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "8adce357", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:30:47.5 8adce357 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:30:47.5 8adce357 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:30:47.6 8adce357 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:31:47.7 8adce357 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:31:47.7 8adce357 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 60, "write_seconds": 0.005}
11:31:47.7 8adce357 children_at_exit       {"alive": [], "exitcodes": []}
11:31:47.7 8adce357 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:31:49.1 36d6d439 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "8adce357", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:31:49.1 36d6d439 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:31:49.1 36d6d439 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958707.6625397, "saved_by_exec": "8adce357", "saved_on_host": "gpu-node007", "saved_reason": "voluntary", "step": 60}
11:31:49.1 36d6d439 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:33:22.1 36d6d439 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790958802.05154, "role": "parent", "signal": "SIGTERM", "step": 152}
11:33:22.2 36d6d439 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 153}
11:33:22.2 36d6d439 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.006, "step": 153, "write_seconds": 0.005}
11:33:22.2 36d6d439 signal_save_finished   {"ok": true, "seconds_since_signal": 0.144}
11:33:22.2 36d6d439 children_at_exit       {"alive": [], "exitcodes": []}
11:33:22.2 36d6d439 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 153}
11:34:53.0 f02efcce start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f02efcce", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:34:53.0 f02efcce history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:34:53.0 f02efcce restore                {"chosen": "step_00000153", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000153", "nested_dir_ok": true, "saved_at": 1790958802.193609, "saved_by_exec": "36d6d439", "saved_on_host": "gpu-node007", "saved_reason": "signal", "step": 153}
11:34:53.0 f02efcce loop_start             {"restored_step": 153, "step": 153, "total_steps": 420, "voluntary_exit_at": [60]}
11:39:21.3 f02efcce save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:39:21.3 f02efcce save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.007, "step": 420, "write_seconds": 0.006}
11:39:21.3 f02efcce children_at_exit       {"alive": [], "exitcodes": []}
11:39:21.3 f02efcce exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:50.3 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-hold-release/job.log", "trigger": "hold-release"}
11:33:21.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958646.0, "job": "6588467.0", "last_event": "file_transfer", "trigger": "hold-release"}
11:33:21.5 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6588467.0"], "output": "Job 6588467.0 held\n", "rc": 0}
11:33:36.5 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
11:34:06.5 {"action": "command", "cmd": ["/usr/bin/condor_release", "6588467.0"], "output": "Job 6588467.0 released\n", "rc": 0}
11:34:06.5 {"action": "done"}
```
