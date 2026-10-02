# P3d-killsig-usr1-vacate on chtc

**Question.** Is kill_sig honoured? The job asks for SIGUSR1; does it receive SIGUSR1 instead of SIGTERM?

Job: `6527365.0`   Test dir: `runs/core-chtc/chtc/P3d-killsig-usr1-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGUSR1, no exit recorded): gap 58 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:21:25.5 (AP clock).
- Evicted execution received SIGUSR1 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.4 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4d159160 | 14:19:45.4 | e2482 | False | 0 | None (None) |  | [(5, 'voluntary', 0.018)] | 85 |
| e0d2775e | 14:19:53.6 | e2482 | True | 0 | 5 (voluntary) | SIGUSR1 | [] | none (killed?) |
| cbe1898e | 14:32:23.3 | e2481 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:18:43.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P3d-killsig-usr1-vacate"; JobBatchName = "probes.dag+6527287" ]
- 14:19:39.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2482.chtc.wisc.edu&noUDP&sock=slot1_34_2310106_68ad_91457>
- 14:19:44.0 `040 file_transfer` Finished transferring input files 
- 14:19:44.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_34@e2482.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_994580/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:19:52.0 `040 file_transfer` Started transferring output files 
- 14:19:52.0 `040 file_transfer` Finished transferring output files 
- 14:31:25.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051121  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 14:32:17.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_17_3564670_3d75_92288>
- 14:32:22.0 `040 file_transfer` Finished transferring input files 
- 14:32:22.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_17@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3521454/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:32:23.0 `040 file_transfer` Started transferring output files 
- 14:32:23.0 `040 file_transfer` Finished transferring output files 
- 14:32:23.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052150  -  Run Bytes Sent By Job; 287388031 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 6.0
CommittedSuspensionTime = 0
CommittedTime = 13
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790883143
JobCurrentStartTransferOutputDate = 1790883143
KillSig = SIGUSR1
LastRemoteHost = slot1_17@e2481.chtc.wisc.edu
LastRemoteWallClockTime = 6.0
LastVacateTime = 1790883085
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
RemoteWallClockTime = 712.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790883143
TransferOutStarted = 1790883143
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103271; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052150; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:19:45.4 4d159160 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_994580/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4d159160", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch"}
14:19:45.4 4d159160 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch/ckpt", "store": "spool"}
14:19:45.4 4d159160 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:19:45.5 4d159160 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
14:19:52.2 4d159160 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
14:19:52.3 4d159160 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.018, "step": 5, "write_seconds": 0.018}
14:19:52.3 4d159160 children_at_exit       {"alive": [], "exitcodes": []}
14:19:52.3 4d159160 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
14:19:53.6 e0d2775e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_994580/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4d159160", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch"}
14:19:53.6 e0d2775e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch/ckpt", "store": "spool"}
14:19:53.6 e0d2775e restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_994580/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882392.263711, "saved_by_exec": "4d159160", "saved_on_host": "e2482", "saved_reason": "voluntary",
14:19:53.6 e0d2775e loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
14:21:25.6 e0d2775e signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790882485.6064947, "role": "parent", "signal": "SIGUSR1", "step": 71}
14:32:23.3 cbe1898e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3521454/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "cbe1898e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3521454/scratch"}
14:32:23.3 cbe1898e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3521454/scratch/ckpt", "store": "spool"}
14:32:23.3 cbe1898e restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3521454/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882392.263711, "saved_by_exec": "4d159160", "saved_on_host": "e2482", "saved_reason": "voluntary"
14:32:23.3 cbe1898e exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
13:43:23.2 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P3d-killsig-usr1-vacate/job.log", "trigger": "vacate"}
14:21:25.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790882384.0, "job": "6527365.0", "last_event": "image_size", "trigger": "vacate"}
14:21:25.6 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527365.0"], "output": "Job 6527365.0 vacated\n", "rc": 0}
14:21:25.6 {"action": "done"}
```
