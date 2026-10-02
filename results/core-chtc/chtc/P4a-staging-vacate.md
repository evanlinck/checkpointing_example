# P4a-staging-vacate on chtc

**Question.** Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?

Job: `6527348.0`   Test dir: `runs/core-chtc/chtc/P4a-staging-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 82 s, DIFFERENT host, sandbox NEW, restored step 112 (saved by: signal).
- Trigger vacate fired at 14:09:54.8 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.9 s after the signal.
- Next execution restored step 112 (saved by: signal) -> the SIGTERM save (step 112) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 0932f248 | 14:07:19.4 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(30, 'periodic', 0.362), (60, 'voluntary', 0.55)] | 85 |
| a1c3a1ae | 14:08:43.6 | e2016.chtc.wisc.edu | True | 0 | 60 (voluntary) | SIGTERM | [(90, 'periodic', 0.739), (112, 'signal', 0.308)] | 85 |
| 180f598d | 14:11:17.6 | e2481 | False | 1 | 112 (signal) |  | [(120, 'periodic', 0.853), (150, 'periodic', 1.472), (180, 'periodic', 0.452), (210, 'periodic', 0.319), (240, 'periodic', 0.792), (270, 'periodic', 0.644), (300, 'periodic', 0.868), (330, 'periodic', 0.376), (360, 'periodic', 0.374), (390, 'periodic', 1.723), (420, 'periodic', 0.577), (420, 'final', 0.811)] | 0 |

## HTCondor event log (AP clock)

- 14:06:32.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P4a-staging-vacate"; JobBatchName = "probes.dag+6527287" ]
- 14:07:06.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76114>
- 14:07:16.0 `040 file_transfer` Finished transferring input files 
- 14:07:18.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4097410/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:08:42.0 `040 file_transfer` Started transferring output files 
- 14:08:42.0 `040 file_transfer` Finished transferring output files 
- 14:09:55.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :                 1         1; Disk (KB)            :   27
- 14:11:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_39_3564670_3d75_92238>
- 14:11:16.0 `040 file_transfer` Finished transferring input files 
- 14:11:16.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_39@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3456962/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:18:25.0 `040 file_transfer` Started transferring output files 
- 14:18:28.0 `040 file_transfer` Finished transferring output files 
- 14:18:28.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 20002  -  Run Bytes Sent By Job; 286336886  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 446.0
CommittedSuspensionTime = 0
CommittedTime = 529
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790882305
LastRemoteHost = slot1_39@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 446.0
LastVacateTime = 1790881795
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
RemoteWallClockTime = 616.0
SuccessCheckpointExitCode = 85
TransferOutFinished = 1790882308
TransferOutStarted = 1790882305
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 20006; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 20002; CedarFilesCountLastRun = 2 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:07:19.4 0932f248 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4097410/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "0932f248", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4097410/scratch"}
14:07:19.5 0932f248 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "store": "staging"}
14:07:19.6 0932f248 restore                {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:07:19.8 0932f248 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
14:07:59.8 0932f248 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 30}
14:08:00.2 0932f248 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.362, "step": 30, "write_seconds": 0.295}
14:08:41.7 0932f248 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
14:08:42.3 0932f248 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.55, "step": 60, "write_seconds": 0.15}
14:08:42.3 0932f248 children_at_exit       {"alive": [], "exitcodes": []}
14:08:42.4 0932f248 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
14:08:43.6 a1c3a1ae start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4097410/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "0932f248", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4097410/scratch"}
14:08:43.6 a1c3a1ae history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "store": "staging"}
14:08:43.7 a1c3a1ae restore                {"chosen": "step_00000060", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790881721.8725927, "saved_by_exec": "0932f248", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reason": "
14:08:43.7 a1c3a1ae loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
14:09:25.5 a1c3a1ae save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 90}
14:09:26.3 a1c3a1ae save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.739, "step": 90, "write_seconds": 0.359}
14:09:54.9 a1c3a1ae signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790881794.9093678, "role": "parent", "signal": "SIGTERM", "step": 111}
14:09:55.5 a1c3a1ae save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 112}
14:09:55.8 a1c3a1ae save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.308, "step": 112, "write_seconds": 0.214}
14:09:55.8 a1c3a1ae signal_save_finished   {"ok": true, "seconds_since_signal": 0.902}
14:09:55.8 a1c3a1ae children_at_exit       {"alive": [], "exitcodes": []}
14:09:55.8 a1c3a1ae exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 112}
14:11:17.6 180f598d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3456962/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "180f598d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3456962/scratch"}
14:11:18.2 180f598d history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "store": "staging"}
14:11:18.8 180f598d restore                {"chosen": "step_00000112", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527348.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000112", "nested_dir_ok": true, "saved_at": 1790881795.581727, "saved_by_exec": "a1c3a1ae", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reason": "s
14:11:18.8 180f598d loop_start             {"restored_step": 112, "step": 112, "total_steps": 420, "voluntary_exit_at": [60]}
14:11:30.0 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 120}
14:11:31.8 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.853, "step": 120, "write_seconds": 0.716}
14:12:14.0 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 150}
14:12:16.4 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.472, "step": 150, "write_seconds": 0.734}
14:13:01.3 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 180}
14:13:01.8 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.452, "step": 180, "write_seconds": 0.279}
14:13:40.2 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 210}
14:13:40.5 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.319, "step": 210, "write_seconds": 0.209}
14:14:21.2 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 240}
14:14:22.0 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.792, "step": 240, "write_seconds": 0.322}
14:15:09.5 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 270}
14:15:10.2 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.644, "step": 270, "write_seconds": 0.332}
14:15:49.5 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 300}
14:15:50.3 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.868, "step": 300, "write_seconds": 0.38}
14:16:29.2 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 330}
14:16:29.6 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.376, "step": 330, "write_seconds": 0.228}
14:17:07.1 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 360}
14:17:07.5 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.374, "step": 360, "write_seconds": 0.188}
14:17:42.2 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 390}
14:17:43.9 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.723, "step": 390, "write_seconds": 0.315}
14:18:22.1 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 420}
14:18:22.6 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.577, "step": 420, "write_seconds": 0.374}
14:18:22.7 180f598d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
14:18:23.5 180f598d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.811, "step": 420, "write_seconds": 0.204}
14:18:23.6 180f598d children_at_exit       {"alive": [], "exitcodes": []}
14:18:23.7 180f598d exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:23.2 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P4a-staging-vacate/job.log", "trigger": "vacate"}
14:09:54.8 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790881638.0, "job": "6527348.0", "last_event": "file_transfer", "trigger": "vacate"}
14:09:54.9 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527348.0"], "output": "Job 6527348.0 vacated\n", "rc": 0}
14:09:54.9 {"action": "done"}
```
