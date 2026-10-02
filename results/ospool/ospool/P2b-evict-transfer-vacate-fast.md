# P2b-evict-transfer-vacate-fast on ospool

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6587656.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-vacate-fast`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 73 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 11:28:20.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -1.5 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d28e86d7 | 11:25:46.1 | a213.anvil.rcac.purdue.edu | False | 0 | None (None) |  | [(60, 'voluntary', 0.006)] | 85 |
| 4de99b31 | 11:26:47.6 | a213.anvil.rcac.purdue.edu | True | 0 | 60 (voluntary) |  | [] | none (killed?) |
| cbdcabef | 11:29:31.7 | a221.anvil.rcac.purdue.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.008)] | 0 |

## HTCondor event log (AP clock)

- 11:25:19.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2b-evict-transfer-vacate-fast"; JobBatchName = "probes.dag+6586482" ]
- 11:25:40.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:39773?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#14599807%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:25:44.0 `040 file_transfer` Finished transferring input files 
- 11:25:45.0 `021 remote_error` Message from starter on slot1_38@glidein_79141_540569430@a213.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:25:45.0 `001 executing` Job executing on host: <<ip>:38025?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_38@glidein_79141_540569430@a213.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_Y7BbYf/execute/dir_2309935/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:26:46.0 `040 file_transfer` Started transferring output files 
- 11:26:46.0 `040 file_transfer` Finished transferring output files 
- 11:28:20.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051596  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :                 1         1; Disk (KB)            
- 11:29:18.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42079?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector2#14601980%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:29:30.0 `040 file_transfer` Finished transferring input files 
- 11:29:30.0 `021 remote_error` Message from starter on slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:29:30.0 `001 executing` Job executing on host: <<ip>:33881?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_YjcjOc/execute/dir_2072273/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:35:32.0 `040 file_transfer` Started transferring output files 
- 11:35:32.0 `040 file_transfer` Finished transferring output files 
- 11:35:32.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 22705  -  Run Bytes Sent By Job; 287388506  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 374.0
CommittedSuspensionTime = 0
CommittedTime = 434
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958932
JobCurrentStartTransferOutputDate = 1790958932
LastRemoteHost = slot1_93@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu
LastRemoteWallClockTime = 374.0
LastVacateTime = 1790958500
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
RemoteWallClockTime = 537.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958932
TransferOutStarted = 1790958932
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1074301; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 22705; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
11:25:46.1 d28e86d7 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d28e86d7", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:25:46.1 d28e86d7 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:25:46.1 d28e86d7 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:25:46.1 d28e86d7 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:26:46.1 d28e86d7 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:26:46.1 d28e86d7 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 60, "write_seconds": 0.005}
11:26:46.1 d28e86d7 children_at_exit       {"alive": [], "exitcodes": []}
11:26:46.1 d28e86d7 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:26:47.6 4de99b31 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "d28e86d7", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:26:47.6 4de99b31 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:26:47.6 4de99b31 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958406.1386194, "saved_by_exec": "d28e86d7", "saved_on_host": "a213.anvil.rcac.purdue.edu", "saved_reason": "voluntary", "step": 60}
11:26:47.6 4de99b31 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:29:31.7 cbdcabef start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "cbdcabef", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:29:31.7 cbdcabef history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:29:31.7 cbdcabef restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958406.1386194, "saved_by_exec": "d28e86d7", "saved_on_host": "a213.anvil.rcac.purdue.edu", "saved_reason": "voluntary", "step": 60}
11:29:31.7 cbdcabef loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:35:32.2 cbdcabef save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:35:32.2 cbdcabef save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.008, "step": 420, "write_seconds": 0.007}
11:35:32.2 cbdcabef children_at_exit       {"alive": [], "exitcodes": []}
11:35:32.2 cbdcabef exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:49.4 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2b-evict-transfer-vacate-fast/job.log", "trigger": "vacate-fast"}
11:28:20.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958345.0, "job": "6587656.0", "last_event": "file_transfer", "trigger": "vacate-fast"}
11:28:20.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "-fast", "6587656.0"], "output": "Job 6587656.0 fast-vacated\n", "rc": 0}
11:28:20.3 {"action": "done"}
```
