# P3c-grace-jmvt900-vacate on chtc

**Question.** If a job asks for job_max_vacate_time = 900, is it capped by the machine's MachineMaxVacateTime?

Job: `6527364.0`   Test dir: `runs/core-chtc/chtc/P3c-grace-jmvt900-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 171 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:21:25.4 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 899.2 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| ea218c58 | 14:19:45.6 | e2473 | False | 0 | None (None) |  | [(5, 'voluntary', 0.015)] | 85 |
| d5087dd7 | 14:19:53.7 | e2473 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| f4e7eaac | 14:39:15.9 | e2018.chtc.wisc.edu | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:18:38.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P3c-grace-jmvt900-vacate"; JobBatchName = "probes.dag+6527287" ]
- 14:19:39.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2473.chtc.wisc.edu&noUDP&sock=slot1_34_342642_0927_91343>
- 14:19:44.0 `040 file_transfer` Finished transferring input files 
- 14:19:44.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_34@e2473.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_754245/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:19:52.0 `040 file_transfer` Started transferring output files 
- 14:19:52.0 `040 file_transfer` Finished transferring output files 
- 14:36:25.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051133  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 14:39:01.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2018.chtc.wisc.edu&noUDP&sock=slot1_29_1076884_f288_9288>
- 14:39:15.0 `040 file_transfer` Finished transferring input files 
- 14:39:15.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_29@e2018.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_890066/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:39:15.0 `040 file_transfer` Started transferring output files 
- 14:39:15.0 `040 file_transfer` Finished transferring output files 
- 14:39:16.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052206  -  Run Bytes Sent By Job; 287388043 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 15.0
CommittedSuspensionTime = 0
CommittedTime = 22
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790883555
JobCurrentStartTransferOutputDate = 1790883555
JobMaxVacateTime = 900
LastRemoteHost = slot1_29@e2018.chtc.wisc.edu
LastRemoteWallClockTime = 15.0
LastVacateTime = 1790883385
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
RemoteWallClockTime = 1021.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790883555
TransferOutStarted = 1790883555
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103339; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052206; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:19:45.6 ea218c58 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_754245/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "ea218c58", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch"}
14:19:45.6 ea218c58 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch/ckpt", "store": "spool"}
14:19:45.6 ea218c58 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:19:45.6 ea218c58 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
14:19:52.3 ea218c58 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
14:19:52.3 ea218c58 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.015, "step": 5, "write_seconds": 0.014}
14:19:52.3 ea218c58 children_at_exit       {"alive": [], "exitcodes": []}
14:19:52.3 ea218c58 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
14:19:53.7 d5087dd7 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_754245/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "ea218c58", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch"}
14:19:53.7 d5087dd7 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch/ckpt", "store": "spool"}
14:19:53.7 d5087dd7 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_754245/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882392.2651129, "saved_by_exec": "ea218c58", "saved_on_host": "e2473", "saved_reason": "voluntary"
14:19:53.7 d5087dd7 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
14:21:25.6 d5087dd7 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790882485.6230245, "role": "parent", "signal": "SIGTERM", "step": 71}
14:39:15.9 f4e7eaac start                  {"cwd": "/var/lib/condor/execute/slot1/dir_890066/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f4e7eaac", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_890066/scratch"}
14:39:15.9 f4e7eaac history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_890066/scratch/ckpt", "store": "spool"}
14:39:15.9 f4e7eaac restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_890066/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882392.2651129, "saved_by_exec": "ea218c58", "saved_on_host": "e2473", "saved_reason": "voluntary"
14:39:15.9 f4e7eaac exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
13:43:23.1 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P3c-grace-jmvt900-vacate/job.log", "trigger": "vacate"}
14:21:25.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790882384.0, "job": "6527364.0", "last_event": "image_size", "trigger": "vacate"}
14:21:25.6 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527364.0"], "output": "Job 6527364.0 vacated\n", "rc": 0}
14:21:25.6 {"action": "done"}
```
