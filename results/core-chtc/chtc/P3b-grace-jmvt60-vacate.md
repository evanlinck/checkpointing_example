# P3b-grace-jmvt60-vacate on chtc

**Question.** Is job_max_vacate_time = 60 honoured (grace about 60 s)?

Job: `6527362.0`   Test dir: `runs/core-chtc/chtc/P3b-grace-jmvt60-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 7 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 66 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:19:55.3 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 60.0 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f45a4301 | 14:18:13.7 | e2016.chtc.wisc.edu | False | 0 | None (None) |  | [(5, 'voluntary', 0.004)] | 85 |
| 358c6740 | 14:18:27.3 | e2016.chtc.wisc.edu | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| a6dc2fb5 | 14:22:01.7 | e2016.chtc.wisc.edu | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:17:38.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P3b-grace-jmvt60-vacate"; JobBatchName = "probes.dag+6527287" ]
- 14:18:06.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76139>
- 14:18:12.0 `040 file_transfer` Finished transferring input files 
- 14:18:12.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4100383/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:18:21.0 `040 file_transfer` Started transferring output files 
- 14:18:24.0 `040 file_transfer` Finished transferring output files 
- 14:20:55.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051306  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 14:21:55.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76141>
- 14:22:00.0 `040 file_transfer` Finished transferring input files 
- 14:22:00.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4100960/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:22:01.0 `040 file_transfer` Started transferring output files 
- 14:22:01.0 `040 file_transfer` Finished transferring output files 
- 14:22:02.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052392  -  Run Bytes Sent By Job; 287388216 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 7.0
CommittedSuspensionTime = 0
CommittedTime = 14
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790882521
JobCurrentStartTransferOutputDate = 1790882521
JobMaxVacateTime = 60
LastRemoteHost = slot1_25@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 7.0
LastVacateTime = 1790882455
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
RemoteWallClockTime = 176.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790882521
TransferOutStarted = 1790882521
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103698; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052392; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:18:13.7 f45a4301 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4100383/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f45a4301", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch"}
14:18:13.7 f45a4301 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch/ckpt", "store": "spool"}
14:18:13.7 f45a4301 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:18:13.9 f45a4301 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
14:18:20.7 f45a4301 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
14:18:20.7 f45a4301 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.004, "step": 5, "write_seconds": 0.003}
14:18:20.7 f45a4301 children_at_exit       {"alive": [], "exitcodes": []}
14:18:20.7 f45a4301 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
14:18:27.3 358c6740 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4100383/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "f45a4301", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch"}
14:18:27.3 358c6740 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch/ckpt", "store": "spool"}
14:18:27.3 358c6740 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100383/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882300.6731517, "saved_by_exec": "f45a4301", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
14:18:27.4 358c6740 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
14:19:55.4 358c6740 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790882395.354586, "role": "parent", "signal": "SIGTERM", "step": 70}
14:22:01.7 a6dc2fb5 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4100960/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a6dc2fb5", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4100960/scratch"}
14:22:01.7 a6dc2fb5 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100960/scratch/ckpt", "store": "spool"}
14:22:01.7 a6dc2fb5 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4100960/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790882300.6731517, "saved_by_exec": "f45a4301", "saved_on_host": "e2016.chtc.wisc.edu", "saved_reaso
14:22:01.7 a6dc2fb5 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
13:43:23.1 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P3b-grace-jmvt60-vacate/job.log", "trigger": "vacate"}
14:19:55.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790882292.0, "job": "6527362.0", "last_event": "image_size", "trigger": "vacate"}
14:19:55.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527362.0"], "output": "Job 6527362.0 vacated\n", "rc": 0}
14:19:55.3 {"action": "done"}
```
