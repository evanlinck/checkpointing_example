# P2b-evict-transfer-vacate on ospool

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6587094.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 34 s, DIFFERENT host, sandbox NEW, restored step 61 (saved by: signal).
- Trigger vacate fired at 11:23:47.0 (AP clock).
- Evicted execution received SIGTERM 4.9 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.7 s after the signal.
- Next execution restored step 61 (saved by: signal) -> the SIGTERM save (step 61) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d1740687 | 11:21:11.2 | dwarf36 | False | 0 | None (None) |  | [(60, 'voluntary', 4.531)] | 85 |
| 8313c2c7 | 11:22:36.3 | dwarf36 | True | 0 | 60 (voluntary) | SIGTERM | [(61, 'signal', 0.142)] | 85 |
| af06565a | 11:24:28.2 | warlock21 | False | 1 | 61 (signal) |  | [(420, 'final', 0.139)] | 0 |

## HTCondor event log (AP clock)

- 11:20:09.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2b-evict-transfer-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:20:41.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:40277?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector10#14592694%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26a
- 11:21:08.0 `040 file_transfer` Finished transferring input files 
- 11:21:09.0 `021 remote_error` Message from starter on slot1_4@glidein_57289_959564904@dwarf36.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:21:09.0 `001 executing` Job executing on host: <<ip>:32899?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_4@glidein_57289_959564904@dwarf36.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_8QvUEy/execute/dir_1972913/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:22:34.0 `040 file_transfer` Started transferring output files 
- 11:22:34.0 `040 file_transfer` Finished transferring output files 
- 11:23:54.0 `040 file_transfer` Started transferring output files 
- 11:23:54.0 `040 file_transfer` Finished transferring output files 
- 11:23:54.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2102586  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 11:23:59.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:43593?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#14597542%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:24:25.0 `040 file_transfer` Finished transferring input files 
- 11:24:26.0 `021 remote_error` Message from starter on slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:24:26.0 `001 executing` Job executing on host: <<ip>:37419?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_e7SCVy/execute/dir_3349214/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:31:27.0 `040 file_transfer` Started transferring output files 
- 11:31:27.0 `040 file_transfer` Finished transferring output files 
- 11:31:28.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 26371  -  Run Bytes Sent By Job; 288439528  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 450.0
CommittedSuspensionTime = 0
CommittedTime = 534
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958687
JobCurrentStartTransferOutputDate = 1790958687
LastRemoteHost = slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu
LastRemoteWallClockTime = 450.0
LastVacateTime = 1790958234
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 644.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958687
TransferOutStarted = 1790958687
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2128957; CedarFilesCountTotal = 31; CedarSizeBytesLastRun = 26371; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
11:21:11.2 d1740687 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d1740687", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:21:11.2 d1740687 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:21:11.2 d1740687 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:21:11.2 d1740687 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:22:29.9 d1740687 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:22:34.4 d1740687 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 4.531, "step": 60, "write_seconds": 4.473}
11:22:34.5 d1740687 children_at_exit       {"alive": [], "exitcodes": []}
11:22:34.5 d1740687 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:22:36.3 8313c2c7 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "d1740687", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:22:36.3 8313c2c7 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:23:25.2 8313c2c7 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958154.3688688, "saved_by_exec": "d1740687", "saved_on_host": "dwarf36", "saved_reason": "voluntary", "step": 60}
11:23:52.8 8313c2c7 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:23:53.4 8313c2c7 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790958232.8152888, "role": "parent", "signal": "SIGTERM", "step": 60}
11:23:54.3 8313c2c7 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 61}
11:23:54.5 8313c2c7 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.142, "step": 61, "write_seconds": 0.117}
11:23:54.5 8313c2c7 signal_save_finished   {"ok": true, "seconds_since_signal": 1.653}
11:23:54.5 8313c2c7 children_at_exit       {"alive": [], "exitcodes": []}
11:23:54.5 8313c2c7 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 61}
11:24:28.2 af06565a start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "af06565a", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:24:28.2 af06565a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:24:28.3 af06565a restore                {"chosen": "step_00000061", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000061", "nested_dir_ok": true, "saved_at": 1790958234.3682823, "saved_by_exec": "8313c2c7", "saved_on_host": "dwarf36", "saved_reason": "signal", "step": 61}
11:24:28.3 af06565a loop_start             {"restored_step": 61, "step": 61, "total_steps": 420, "voluntary_exit_at": [60]}
11:31:27.5 af06565a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:31:27.6 af06565a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.139, "step": 420, "write_seconds": 0.097}
11:31:27.7 af06565a children_at_exit       {"alive": [], "exitcodes": []}
11:31:27.7 af06565a exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:47.4 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-vacate/job.log", "trigger": "vacate"}
11:23:47.0 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958069.0, "job": "6587094.0", "last_event": "file_transfer", "trigger": "vacate"}
11:23:47.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6587094.0"], "output": "Job 6587094.0 vacated\n", "rc": 0}
11:23:47.0 {"action": "done"}
```
