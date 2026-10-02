# P2d-default-vacate on ospool

**Question.** Baseline: a job with no SIGTERM handler dies on the signal. Does it restart from the last voluntary checkpoint (A)?

Job: `6588875.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2d-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 430 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:39:21.9 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 1.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| b4b92590 | 11:36:44.3 | a221.anvil.rcac.purdue.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.006)] | 85 |
| 7a082fd2 | 11:37:45.7 | a221.anvil.rcac.purdue.edu | True | 0 | 60 (voluntary) | SIGTERM | [] | none (killed?) |
| 202b2abd | 11:46:33.3 | mwt2-c047.campuscluster.illinois.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.008)] | 0 |

## HTCondor event log (AP clock)

- 11:35:40.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2d-default-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:36:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:40143?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector5#14599499%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:36:42.0 `040 file_transfer` Finished transferring input files 
- 11:36:43.0 `021 remote_error` Message from starter on slot1_57@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:36:43.0 `001 executing` Job executing on host: <<ip>:33881?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_57@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_YjcjOc/execute/dir_2085168/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:37:44.0 `040 file_transfer` Started transferring output files 
- 11:37:44.0 `040 file_transfer` Finished transferring output files 
- 11:39:23.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051439  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 11:41:02.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:33335?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14602104%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 11:46:30.0 `040 file_transfer` Finished transferring input files 
- 11:46:31.0 `021 remote_error` Message from starter on slot1_7@glidein_2288208_394956475@mwt2-c047.campuscluster.illinois.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:46:31.0 `001 executing` Job executing on host: <<ip>:43263?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_7@glidein_2288208_394956475@mwt2-c047.campuscluster.illinois.edu; CondorScratchDir = "/scratch.local/condor/execute/dir_2288193/glide_zsAgdL/execute/dir_2945180/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:52:34.0 `040 file_transfer` Started transferring output files 
- 11:52:34.0 `040 file_transfer` Finished transferring output files 
- 11:52:34.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 22239  -  Run Bytes Sent By Job; 287388349  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 693.0
CommittedSuspensionTime = 0
CommittedTime = 753
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959954
JobCurrentStartTransferOutputDate = 1790959954
LastRemoteHost = slot1_7@glidein_2288208_394956475@mwt2-c047.campuscluster.illinois.edu
LastRemoteWallClockTime = 693.0
LastVacateTime = 1790959163
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
RemoteWallClockTime = 862.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959954
TransferOutStarted = 1790959954
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1073678; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 22239; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:36:44.3 b4b92590 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b4b92590", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:36:44.3 b4b92590 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:36:44.3 b4b92590 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:36:44.3 b4b92590 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:37:44.4 b4b92590 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:37:44.4 b4b92590 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 60, "write_seconds": 0.006}
11:37:44.4 b4b92590 children_at_exit       {"alive": [], "exitcodes": []}
11:37:44.4 b4b92590 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:37:45.7 7a082fd2 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "b4b92590", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:37:45.7 7a082fd2 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:37:45.7 7a082fd2 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790959064.3603215, "saved_by_exec": "b4b92590", "saved_on_host": "a221.anvil.rcac.purdue.edu", "saved_reason": "voluntary", "step": 60}
11:37:45.8 7a082fd2 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:39:22.1 7a082fd2 signal                 {"first": true, "on_sigterm": "default", "received_at": 1790959162.0026264, "role": "parent", "signal": "SIGTERM", "step": 156}
11:39:22.0 7a082fd2 dying_by_signal        {"signal": "SIGTERM", "step": 157}
11:46:33.3 202b2abd start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "202b2abd", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:46:33.3 202b2abd history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:46:33.3 202b2abd restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790959064.3603215, "saved_by_exec": "b4b92590", "saved_on_host": "a221.anvil.rcac.purdue.edu", "saved_reason": "voluntary", "step": 60}
11:46:33.3 202b2abd loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:52:33.8 202b2abd save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:52:33.8 202b2abd save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.008, "step": 420, "write_seconds": 0.007}
11:52:33.9 202b2abd children_at_exit       {"alive": [], "exitcodes": []}
11:52:33.9 202b2abd exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:50.4 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2d-default-vacate/job.log", "trigger": "vacate"}
11:39:21.9 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790959003.0, "job": "6588875.0", "last_event": "file_transfer", "trigger": "vacate"}
11:39:21.9 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6588875.0"], "output": "Job 6588875.0 vacated\n", "rc": 0}
11:39:21.9 {"action": "done"}
```
