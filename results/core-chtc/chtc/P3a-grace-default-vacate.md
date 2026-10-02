# P3a-grace-default-vacate on chtc

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6527336.0`   Test dir: `runs/core-chtc/chtc/P3a-grace-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 111 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 14:05:38.5 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 598.7 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 8ecc843f | 14:04:04.1 | e2464.chtc.wisc.edu | False | 0 | None (None) |  | [(5, 'voluntary', 0.012)] | 85 |
| 7e4f7065 | 14:04:11.9 | e2464.chtc.wisc.edu | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| 58ebbb9b | 14:17:28.4 | e2016.chtc.wisc.edu | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:03:16.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P3a-grace-default-vacate"; JobBatchName = "probes.dag+6527287" ]
- 14:03:58.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_44_1734380_5bf9_11158>
- 14:04:03.0 `040 file_transfer` Finished transferring input files 
- 14:04:03.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_44@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_750650/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:04:10.0 `040 file_transfer` Started transferring output files 
- 14:04:10.0 `040 file_transfer` Finished transferring output files 
- 14:15:38.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051315  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 14:16:53.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_25_3486004_ed36_76134>
- 14:16:59.0 `040 file_transfer` Finished transferring input files 
- 14:17:27.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_25@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_4099844/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:17:28.0 `040 file_transfer` Started transferring output files 
- 14:17:28.0 `040 file_transfer` Finished transferring output files 
- 14:17:29.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052404  -  Run Bytes Sent By Job; 287388225 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 36.0
CommittedSuspensionTime = 0
CommittedTime = 42
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790882248
LastRemoteHost = slot1_25@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 36.0
LastVacateTime = 1790882138
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
RemoteWallClockTime = 737.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790882248
TransferOutStarted = 1790882248
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103719; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052404; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:04:04.1 8ecc843f start                  {"cwd": "/var/lib/condor/execute/slot1/dir_750650/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "8ecc843f", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch"}
14:04:04.1 8ecc843f history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch/ckpt", "store": "spool"}
14:04:04.1 8ecc843f restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
14:04:04.2 8ecc843f loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
14:04:09.9 8ecc843f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
14:04:09.9 8ecc843f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.012, "step": 5, "write_seconds": 0.012}
14:04:09.9 8ecc843f children_at_exit       {"alive": [], "exitcodes": []}
14:04:09.9 8ecc843f exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
14:04:11.9 7e4f7065 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_750650/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "8ecc843f", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch"}
14:04:11.9 7e4f7065 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch/ckpt", "store": "spool"}
14:04:11.9 7e4f7065 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_750650/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790881449.8645725, "saved_by_exec": "8ecc843f", "saved_on_host": "e2464.chtc.wisc.edu", "saved_reason
14:04:11.9 7e4f7065 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
14:05:38.6 7e4f7065 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790881538.5189478, "role": "parent", "signal": "SIGTERM", "step": 70}
14:17:28.4 58ebbb9b start                  {"cwd": "/var/lib/condor/execute/slot1/dir_4099844/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "58ebbb9b", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_4099844/scratch"}
14:17:28.4 58ebbb9b history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_4099844/scratch/ckpt", "store": "spool"}
14:17:28.4 58ebbb9b restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_4099844/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790881449.8645725, "saved_by_exec": "8ecc843f", "saved_on_host": "e2464.chtc.wisc.edu", "saved_reaso
14:17:28.4 58ebbb9b exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
13:43:22.2 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P3a-grace-default-vacate/job.log", "trigger": "vacate"}
14:05:38.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790881443.0, "job": "6527336.0", "last_event": "image_size", "trigger": "vacate"}
14:05:38.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6527336.0"], "output": "Job 6527336.0 vacated\n", "rc": 0}
14:05:38.5 {"action": "done"}
```
