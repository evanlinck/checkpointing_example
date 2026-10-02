# P2b-evict-transfer-vacate-fast on chtc

**Question.** Same as P2a, plus when_to_transfer_output = ON_EXIT_OR_EVICT. Is step B transferred on eviction? After a hard kill (-fast), where nothing can be transferred, does the job still restart from the spooled voluntary checkpoint A, or from scratch?

Job: `6573179.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-vacate-fast`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 96 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 08:52:29.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -8.8 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| eea802a6 | 08:49:56.7 | e2590 | False | 0 | None (None) |  | [(60, 'voluntary', 0.037)] | 85 |
| 765192c6 | 08:50:58.0 | e2590 | True | 0 | 60 (voluntary) |  | [] | none (killed?) |
| 072c75e2 | 08:53:56.9 | e4022 | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.02)] | 0 |

## HTCondor event log (AP clock)

- 08:49:24.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P2b-evict-transfer-vacate-fast"; JobBatchName = "probes.dag+6573176" ]
- 08:49:49.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2590.chtc.wisc.edu&noUDP&sock=slot1_69_1848655_6f40_113880>
- 08:49:55.0 `040 file_transfer` Finished transferring input files 
- 08:49:55.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_69@e2590.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1060140/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:50:57.0 `040 file_transfer` Started transferring output files 
- 08:50:57.0 `040 file_transfer` Finished transferring output files 
- 08:52:29.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051391  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            
- 08:53:51.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4022.chtc.wisc.edu&noUDP&sock=slot1_13_2697437_2353_118231>
- 08:53:55.0 `040 file_transfer` Finished transferring input files 
- 08:53:55.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_13@e4022.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_33172/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:59:57.0 `040 file_transfer` Started transferring output files 
- 08:59:57.0 `040 file_transfer` Finished transferring output files 
- 09:00:02.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 20711  -  Run Bytes Sent By Job; 287388301  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 372.0
CommittedSuspensionTime = 0
CommittedTime = 433
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790949597
LastRemoteHost = slot1_13@e4022.chtc.wisc.edu
LastRemoteWallClockTime = 372.0
LastVacateTime = 1790949149
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
RemoteWallClockTime = 532.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790949597
TransferOutStarted = 1790949597
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1072102; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 20711; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
08:49:56.7 eea802a6 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1060140/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "eea802a6", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch"}
08:49:56.7 eea802a6 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch/ckpt", "store": "spool"}
08:49:56.7 eea802a6 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:49:56.7 eea802a6 loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
08:50:57.0 eea802a6 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
08:50:57.1 eea802a6 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.037, "step": 60, "write_seconds": 0.035}
08:50:57.1 eea802a6 children_at_exit       {"alive": [], "exitcodes": []}
08:50:57.1 eea802a6 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
08:50:58.0 765192c6 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1060140/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "eea802a6", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch"}
08:50:58.0 765192c6 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch/ckpt", "store": "spool"}
08:50:58.0 765192c6 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1060140/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949057.0581794, "saved_by_exec": "eea802a6", "saved_on_host": "e2590", "saved_reason": "voluntary
08:50:59.0 765192c6 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:53:56.9 072c75e2 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_33172/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "072c75e2", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_33172/scratch"}
08:53:56.9 072c75e2 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_33172/scratch/ckpt", "store": "spool"}
08:53:56.9 072c75e2 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_33172/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790949057.0581794, "saved_by_exec": "eea802a6", "saved_on_host": "e2590", "saved_reason": "voluntary",
08:53:56.9 072c75e2 loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
08:59:57.3 072c75e2 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
08:59:57.4 072c75e2 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.02, "step": 420, "write_seconds": 0.013}
08:59:57.4 072c75e2 children_at_exit       {"alive": [], "exitcodes": []}
08:59:57.4 072c75e2 exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
08:49:29.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P2b-evict-transfer-vacate-fast/job.log", "trigger": "vacate-fast"}
08:52:29.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790948995.0, "job": "6573179.0", "last_event": "file_transfer", "trigger": "vacate-fast"}
08:52:29.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "-fast", "6573179.0"], "output": "Job 6573179.0 fast-vacated\n", "rc": 0}
08:52:29.3 {"action": "done"}
```
