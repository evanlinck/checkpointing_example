# P4a-staging-bare-vacate on chtc

**Question.** Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?

Job: `6527328.0`   Test dir: `runs/core-chtc/chtc/P4a-staging-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 19 s, DIFFERENT host, sandbox NEW, restored step 86 (saved by: signal).
- Trigger vacate fired at 13:58:09.4 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.1 s after the signal.
- Next execution restored step 86 (saved by: signal) -> the SIGTERM save (step 86) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 24b652b5 | 13:55:30.7 | e2478 | False | 0 | None (None) |  | [(30, 'periodic', 2.396), (60, 'voluntary', 0.706)] | 85 |
| 193d8470 | 13:57:22.7 | e2478 | True | 0 | 60 (voluntary) | SIGTERM | [(86, 'signal', 0.717)] | 85 |
| 0251fec5 | 13:58:30.9 | e2016.chtc.wisc.edu | False | 1 | 86 (signal) |  | [(90, 'periodic', 1.406), (120, 'periodic', 1.951), (150, 'periodic', 0.326), (180, 'periodic', 1.512), (210, 'periodic', 0.719), (240, 'periodic', 1.389), (270, 'periodic', 1.725), (300, 'periodic', 1.279), (330, 'periodic', 0.478), (360, 'periodic', 0.721), (390, 'periodic', 0.642), (420, 'periodic', 0.899), (420, 'final', 0.961)] | 0 |

## HTCondor event log (AP clock)

- 13:54:50.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P4a-staging-bare-vacate"; JobBatchName = "probes.dag+6527287" ]
- 13:55:25.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2478.chtc.wisc.edu&noUDP&sock=slot1_43_254454_9ca4_88075>
- 13:55:25.0 `040 file_transfer` Finished transferring input files 
- 13:55:30.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_43@e2478.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2717987/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:57:22.0 `040 file_transfer` Started transferring output files 
- 13:57:22.0 `040 file_transfer` Finished transferring output files 
- 13:58:11.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 30512  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :     0.00        1         1; Disk (KB)            :    60   
- 13:58:30.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76098>
- 13:58:30.0 `040 file_transfer` Finished transferring input files 
- 13:58:30.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4093967/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:06:25.0 `040 file_transfer` Started transferring output files 
- 14:06:25.0 `040 file_transfer` Finished transferring output files 
- 14:06:26.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 22130  -  Run Bytes Sent By Job; 30520  -  Ru

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 476.0
CommittedSuspensionTime = 0
CommittedTime = 587
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790881585
JobCurrentStartTransferOutputDate = 1790881585
LastRemoteHost = slot1_25@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 476.0
LastVacateTime = 1790881091
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
RemoteWallClockTime = 642.0
SuccessCheckpointExitCode = 85
TransferOutFinished = 1790881585
TransferOutStarted = 1790881585
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 22134; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 22130; CedarFilesCountLastRun = 2 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:55:30.7 24b652b5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2717987/scratch", "mode": "run", "ppid": 2717987, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "24b652b5", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2717987/scratch"}
13:55:31.0 24b652b5 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "store": "staging"}
13:55:31.2 24b652b5 restore                {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:55:32.6 24b652b5 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
13:56:30.7 24b652b5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 30}
13:56:33.1 24b652b5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 2.396, "step": 30, "write_seconds": 0.409}
13:57:21.8 24b652b5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:57:22.5 24b652b5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.706, "step": 60, "write_seconds": 0.483}
13:57:22.6 24b652b5 children_at_exit       {"alive": [], "exitcodes": []}
13:57:22.6 24b652b5 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:57:22.7 193d8470 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2717987/scratch", "mode": "run", "ppid": 2717987, "previous_starts_in_sandbox": 1, "python": "3.9.25", "sandbox_created_by": "24b652b5", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2717987/scratch"}
13:57:22.7 193d8470 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "store": "staging"}
13:57:23.7 193d8470 restore                {"chosen": "step_00000060", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790881042.024297, "saved_by_exec": "24b652b5", "saved_on_host": "e2478", "saved_reason": "voluntary", "st
13:57:23.7 193d8470 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
13:58:09.5 193d8470 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790881089.4281454, "role": "parent", "signal": "SIGTERM", "step": 85}
13:58:10.3 193d8470 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 86}
13:58:11.0 193d8470 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.717, "step": 86, "write_seconds": 0.325}
13:58:11.1 193d8470 signal_save_finished   {"ok": true, "seconds_since_signal": 1.673}
13:58:11.2 193d8470 children_at_exit       {"alive": [], "exitcodes": []}
13:58:11.5 193d8470 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 86}
13:58:30.9 0251fec5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4093967/scratch", "mode": "run", "ppid": 4093967, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "0251fec5", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4093967/scratch"}
13:58:30.0 0251fec5 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "store": "staging"}
13:58:31.2 0251fec5 restore                {"chosen": "step_00000086", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527328.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000086", "nested_dir_ok": true, "saved_at": 1790881090.5678852, "saved_by_exec": "193d8470", "saved_on_host": "e2478", "saved_reason": "signal", "step
13:58:31.3 0251fec5 loop_start             {"restored_step": 86, "step": 86, "total_steps": 420, "voluntary_exit_at": [60]}
13:58:35.6 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 90}
13:58:37.0 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.406, "step": 90, "write_seconds": 0.465}
13:59:27.6 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 120}
13:59:29.5 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.951, "step": 120, "write_seconds": 0.468}
14:00:16.3 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 150}
14:00:16.7 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.326, "step": 150, "write_seconds": 0.158}
14:00:55.6 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 180}
14:00:57.1 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.512, "step": 180, "write_seconds": 0.739}
14:01:41.4 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 210}
14:01:42.1 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.719, "step": 210, "write_seconds": 0.433}
14:02:18.9 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 240}
14:02:20.3 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.389, "step": 240, "write_seconds": 0.441}
14:03:01.0 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 270}
14:03:02.8 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.725, "step": 270, "write_seconds": 0.539}
14:03:40.5 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 300}
14:03:41.8 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 1.279, "step": 300, "write_seconds": 0.502}
14:04:20.7 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 330}
14:04:21.1 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.478, "step": 330, "write_seconds": 0.285}
14:05:01.9 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 360}
14:05:02.6 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.721, "step": 360, "write_seconds": 0.336}
14:05:40.2 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 390}
14:05:40.9 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.642, "step": 390, "write_seconds": 0.325}
14:06:23.2 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 420}
14:06:24.1 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.899, "step": 420, "write_seconds": 0.289}
14:06:24.2 0251fec5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
14:06:25.1 0251fec5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.961, "step": 420, "write_seconds": 0.703}
14:06:25.3 0251fec5 children_at_exit       {"alive": [], "exitcodes": []}
14:06:25.4 0251fec5 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
13:43:23.5 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P4a-staging-bare-vacate/job.log", "trigger": "vacate"}
13:58:09.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880930.0, "job": "6527328.0", "last_event": "file_transfer", "trigger": "vacate"}
13:58:09.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527328.0"], "output": "Job 6527328.0 vacated\n", "rc": 0}
13:58:09.4 {"action": "done"}
```
