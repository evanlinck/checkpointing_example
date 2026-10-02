# P2a-save85-hold-release on ospool

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6586718.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2a-save85-hold-release`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 149 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger hold-release fired at 11:20:46.5 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 151) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 13fb7929 | 11:18:14.8 | gpu-node006 | False | 0 | None (None) |  | [(60, 'voluntary', 0.007)] | 85 |
| 55060f9d | 11:19:16.3 | gpu-node006 | True | 0 | 60 (voluntary) | SIGTERM | [(151, 'signal', 0.15)] | 85 |
| 531a25db | 11:23:16.6 | a221.anvil.rcac.purdue.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.007)] | 0 |

## HTCondor event log (AP clock)

- 11:15:59.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2a-save85-hold-release"; JobBatchName = "probes.dag+6586482" ]
- 11:17:26.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:33217?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#14601970%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:18:13.0 `040 file_transfer` Finished transferring input files 
- 11:18:14.0 `021 remote_error` Message from starter on slot1_2@glidein_2078512_412968555@gpu-node006: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:18:14.0 `001 executing` Job executing on host: <<ip>:36569?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_2078512_412968555@gpu-node006; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_qXOG6B/execute/dir_1753438/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:19:15.0 `040 file_transfer` Started transferring output files 
- 11:19:15.0 `040 file_transfer` Finished transferring output files 
- 11:20:47.0 `004 evicted` Job was evicted. Code 1 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051294  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: via condor_hold (by user <user>); Cpus                 :      0.00        1         1; Disk (KB)
- 11:20:47.0 `012 held` Job was held. — via condor_hold (by user <user>); Code 1 Subcode 0
- 11:21:31.0 `013 released` Job was released. — via condor_release (by user <user>)
- 11:23:12.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:36917?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#14602213%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:23:15.0 `040 file_transfer` Finished transferring input files 
- 11:23:15.0 `021 remote_error` Message from starter on slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:23:15.0 `001 executing` Job executing on host: <<ip>:33881?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_YjcjOc/execute/dir_2056245/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:29:17.0 `040 file_transfer` Started transferring output files 
- 11:29:17.0 `040 file_transfer` Finished transferring output files 
- 11:29:17.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 21503  -  Run Bytes Sent By Job; 287388204  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 366.0
CommittedSuspensionTime = 0
CommittedTime = 426
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958557
JobCurrentStartTransferOutputDate = 1790958557
LastHoldReason = via condor_hold (by user <user>)
LastHoldReasonCode = 1
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu
LastRemoteWallClockTime = 367.0
LastVacateTime = 1790958047
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
RemoteWallClockTime = 569.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958557
TransferOutStarted = 1790958557
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1072797; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 21503; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:18:14.8 13fb7929 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "13fb7929", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:18:14.8 13fb7929 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:18:14.8 13fb7929 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:18:14.8 13fb7929 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:19:14.9 13fb7929 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:19:14.9 13fb7929 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 60, "write_seconds": 0.006}
11:19:14.9 13fb7929 children_at_exit       {"alive": [], "exitcodes": []}
11:19:14.9 13fb7929 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:19:16.3 55060f9d start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "13fb7929", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:19:16.3 55060f9d history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:19:16.3 55060f9d restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790957954.917789, "saved_by_exec": "13fb7929", "saved_on_host": "gpu-node006", "saved_reason": "voluntary", "step": 60}
11:19:16.3 55060f9d loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:20:47.0 55060f9d signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790958046.9605153, "role": "parent", "signal": "SIGTERM", "step": 150}
11:20:47.5 55060f9d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 151}
11:20:47.6 55060f9d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.15, "step": 151, "write_seconds": 0.101}
11:20:47.6 55060f9d signal_save_finished   {"ok": true, "seconds_since_signal": 0.678}
11:20:47.7 55060f9d children_at_exit       {"alive": [], "exitcodes": []}
11:20:47.7 55060f9d exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 151}
11:23:16.6 531a25db start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "531a25db", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:23:16.6 531a25db history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:23:16.6 531a25db restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790957954.917789, "saved_by_exec": "13fb7929", "saved_on_host": "gpu-node006", "saved_reason": "voluntary", "step": 60}
11:23:16.6 531a25db loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:29:17.3 531a25db save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:29:17.3 531a25db save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.007, "step": 420, "write_seconds": 0.006}
11:29:17.3 531a25db children_at_exit       {"alive": [], "exitcodes": []}
11:29:17.3 531a25db exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:46.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2a-save85-hold-release/job.log", "trigger": "hold-release"}
11:20:46.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790957894.0, "job": "6586718.0", "last_event": "file_transfer", "trigger": "hold-release"}
11:20:46.5 {"action": "command", "cmd": ["/usr/bin/condor_hold", "6586718.0"], "output": "Job 6586718.0 held\n", "rc": 0}
11:21:01.6 {"action": "saw_held", "held_body": ["via condor_hold (by user <user>)", "Code 1 Subcode 0"], "held_text": "Job was held."}
11:21:31.6 {"action": "command", "cmd": ["/usr/bin/condor_release", "6586718.0"], "output": "Job 6586718.0 released\n", "rc": 0}
11:21:31.6 {"action": "done"}
```
