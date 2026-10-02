# P4a-staging-vacate on chtc_backfill

**Question.** Is a SIGTERM save to /staging durable and found after the job is rescheduled (possibly on another host)? Do directory rename, fsync, and an atomic 'latest' pointer work on /staging? Is /staging visible inside the container?

Job: `6587308.0`   Test dir: `/home/<user>/probes/runs/backfill2/chtc_backfill/P4a-staging-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 22 s, same host, sandbox NEW, restored step 131 (saved by: signal).
- Trigger vacate fired at 11:44:28.7 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.6 s after the signal.
- Next execution restored step 131 (saved by: signal) -> the SIGTERM save (step 131) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 5fc8a1b0 | 11:41:50.3 | cxiaogpu4000 | False | 0 | None (None) |  | [(30, 'periodic', 0.359), (60, 'voluntary', 0.752)] | 85 |
| c42dd8cd | 11:43:04.8 | cxiaogpu4000 | True | 0 | 60 (voluntary) | SIGTERM | [(90, 'periodic', 0.594), (120, 'periodic', 0.321), (131, 'signal', 0.438)] | 85 |
| 40c49b2f | 11:44:51.0 | cxiaogpu4000 | False | 1 | 131 (signal) |  | [(150, 'periodic', 0.405), (180, 'periodic', 0.804), (210, 'periodic', 0.533), (240, 'periodic', 0.647), (270, 'periodic', 0.361), (300, 'periodic', 0.335), (330, 'periodic', 0.351), (360, 'periodic', 0.346), (390, 'periodic', 0.295), (420, 'periodic', 0.685), (420, 'final', 0.473)] | 0 |

## HTCondor event log (AP clock)

- 11:22:07.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_backfill__P4a-staging-vacate"; JobBatchName = "probes.dag+6586847" ]
- 11:38:43.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_7_1070907_9c35_79991>
- 11:41:49.0 `040 file_transfer` Finished transferring input files 
- 11:41:49.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_7@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_abbef2b2 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3417883/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_abbef2b2 = [ Id = "GPU-abbef2b2"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 11:43:03.0 `040 file_transfer` Started transferring output files 
- 11:43:04.0 `040 file_transfer` Finished transferring output files 
- 11:44:30.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)            : 279
- 11:44:48.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cxiaogpu4000.chtc.wisc.edu&noUDP&sock=backfill1_7_1070907_9c35_79999>
- 11:44:51.0 `040 file_transfer` Finished transferring input files 
- 11:44:51.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=cx — SlotName: backfill1_7@cxiaogpu4000.chtc.wisc.edu; AvailableGPUs = { GPUs_GPU_abbef2b2 }; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3420063/scratch"; Cpus = 1; Disk = 2097152; GPUs = 1; GPUs_GPU_abbef2b2 = [ Id = "GPU-abbef2b2"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; Devi
- 11:50:51.0 `040 file_transfer` Started transferring output files 
- 11:50:51.0 `040 file_transfer` Finished transferring output files 
- 11:50:51.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19257  -  Run Bytes Sent By Job; 286336886  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 364.0
CommittedSuspensionTime = 0
CommittedTime = 437
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790959851
LastRemoteHost = backfill1_7@cxiaogpu4000.chtc.wisc.edu
LastRemoteWallClockTime = 364.0
LastVacateTime = 1790959470
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
RemoteWallClockTime = 711.0
SuccessCheckpointExitCode = 85
TransferOutFinished = 1790959851
TransferOutStarted = 1790959851
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 19261; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 19257; CedarFilesCountLastRun = 2 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:41:50.3 5fc8a1b0 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3417883/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "5fc8a1b0", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3417883/scratch"}
11:41:50.3 5fc8a1b0 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "store": "staging"}
11:41:50.4 5fc8a1b0 restore                {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:41:50.4 5fc8a1b0 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:42:25.6 5fc8a1b0 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 30}
11:42:25.9 5fc8a1b0 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.359, "step": 30, "write_seconds": 0.33}
11:43:02.4 5fc8a1b0 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:43:03.2 5fc8a1b0 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.752, "step": 60, "write_seconds": 0.299}
11:43:03.2 5fc8a1b0 children_at_exit       {"alive": [], "exitcodes": []}
11:43:03.2 5fc8a1b0 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:43:04.8 c42dd8cd start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3417883/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "5fc8a1b0", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3417883/scratch"}
11:43:04.8 c42dd8cd history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "store": "staging"}
11:43:04.8 c42dd8cd restore                {"chosen": "step_00000060", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790959382.7043703, "saved_by_exec": "5fc8a1b0", "saved_on_host": "cxiaogpu4000", "saved_reason": "volunta
11:43:04.9 c42dd8cd loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:43:39.9 c42dd8cd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 90}
11:43:40.5 c42dd8cd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.594, "step": 90, "write_seconds": 0.495}
11:44:16.5 c42dd8cd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 120}
11:44:16.8 c42dd8cd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.321, "step": 120, "write_seconds": 0.151}
11:44:28.8 c42dd8cd signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790959468.7337089, "role": "parent", "signal": "SIGTERM", "step": 130}
11:44:29.8 c42dd8cd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 131}
11:44:30.3 c42dd8cd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.438, "step": 131, "write_seconds": 0.25}
11:44:30.3 c42dd8cd signal_save_finished   {"ok": true, "seconds_since_signal": 1.535}
11:44:30.3 c42dd8cd children_at_exit       {"alive": [], "exitcodes": []}
11:44:30.3 c42dd8cd exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 131}
11:44:51.0 40c49b2f start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3420063/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "40c49b2f", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3420063/scratch"}
11:44:51.0 40c49b2f history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "store": "staging"}
11:44:58.6 40c49b2f restore                {"chosen": "step_00000131", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6587308.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000131", "nested_dir_ok": true, "saved_at": 1790959470.0655181, "saved_by_exec": "c42dd8cd", "saved_on_host": "cxiaogpu4000", "saved_reason": "signal"
11:44:59.3 40c49b2f loop_start             {"restored_step": 131, "step": 131, "total_steps": 420, "voluntary_exit_at": [60]}
11:45:25.0 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 150}
11:45:26.4 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.405, "step": 150, "write_seconds": 0.322}
11:46:01.6 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 180}
11:46:02.4 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.804, "step": 180, "write_seconds": 0.39}
11:46:39.2 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 210}
11:46:39.7 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.533, "step": 210, "write_seconds": 0.388}
11:47:15.3 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 240}
11:47:15.9 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.647, "step": 240, "write_seconds": 0.301}
11:47:51.1 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 270}
11:47:51.5 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.361, "step": 270, "write_seconds": 0.193}
11:48:25.7 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 300}
11:48:26.0 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.335, "step": 300, "write_seconds": 0.247}
11:49:02.1 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 330}
11:49:02.4 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.351, "step": 330, "write_seconds": 0.183}
11:49:38.1 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 360}
11:49:38.5 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.346, "step": 360, "write_seconds": 0.096}
11:50:14.0 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 390}
11:50:14.3 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.295, "step": 390, "write_seconds": 0.18}
11:50:49.9 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "periodic", "step": 420}
11:50:50.6 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "periodic", "seconds": 0.685, "step": 420, "write_seconds": 0.383}
11:50:50.6 40c49b2f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:50:51.1 40c49b2f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.473, "step": 420, "write_seconds": 0.284}
11:50:51.2 40c49b2f children_at_exit       {"alive": [], "exitcodes": []}
11:50:51.2 40c49b2f exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:17:42.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/backfill2/chtc_backfill/P4a-staging-vacate/job.log", "trigger": "vacate"}
11:44:28.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790959309.0, "job": "6587308.0", "last_event": "file_transfer", "trigger": "vacate"}
11:44:28.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6587308.0"], "output": "Job 6587308.0 vacated\n", "rc": 0}
11:44:28.7 {"action": "done"}
```
