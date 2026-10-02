# P7a-wrapper-exec-bare-vacate on chtc

**Question.** When the executable is a shell script that execs python, does python receive the soft-kill signal?

Job: `6575719.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7a-wrapper-exec-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 95 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:13:47.3 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 20.8 s after the signal.
- Next execution restored step 5 (saved by: voluntary) -> the SIGTERM save (step 73) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=3986726 about to exec python3 | WRAPPER run_exec.sh pid=3987008 about to exec python3 | WRAPPER run_exec.sh pid=3418696 about to exec python3

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f9f84b39 | 09:12:14.9 | e4049 | False | 0 | None (None) |  | [(5, 'voluntary', 20.04)] | 85 |
| cfcb57ca | 09:12:40.2 | e4049 | True | 0 | 5 (voluntary) | SIGTERM | [(73, 'signal', 20.217)] | 85 |
| 667e8912 | 09:15:43.0 | e2015.chtc.wisc.edu | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:12:07.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7a-wrapper-exec-bare-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:12:09.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4049.chtc.wisc.edu&noUDP&sock=slot1_34_2613859_e04d_133301>
- 09:12:09.0 `040 file_transfer` Finished transferring input files 
- 09:12:14.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_34@e4049.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3986564/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:12:40.0 `040 file_transfer` Started transferring output files 
- 09:12:40.0 `040 file_transfer` Finished transferring output files 
- 09:14:08.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050592  -  Run Bytes Sent By Job; 30764  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            :   
- 09:15:43.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2015.chtc.wisc.edu&noUDP&sock=slot1_17_1669604_ceaf_60160>
- 09:15:43.0 `040 file_transfer` Finished transferring input files 
- 09:15:43.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_17@e2015.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3418678/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:15:43.0 `040 file_transfer` Started transferring output files 
- 09:15:44.0 `040 file_transfer` Finished transferring output files 
- 09:15:44.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051694  -  Run Bytes Sent By Job; 1081388  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 1.0
CommittedSuspensionTime = 0
CommittedTime = 26
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790950544
JobCurrentStartTransferOutputDate = 1790950543
LastRemoteHost = slot1_17@e2015.chtc.wisc.edu
LastRemoteWallClockTime = 1.0
LastVacateTime = 1790950448
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
RemoteWallClockTime = 120.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950544
TransferOutStarted = 1790950543
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102286; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051694; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:12:14.9 f9f84b39 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3986564/scratch", "mode": "run", "ppid": 3986564, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "f9f84b39", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch"}
09:12:14.9 f9f84b39 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch/ckpt", "store": "spool"}
09:12:14.9 f9f84b39 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:12:14.9 f9f84b39 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:12:19.9 f9f84b39 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:12:39.0 f9f84b39 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.04, "step": 5, "write_seconds": 0.003}
09:12:39.0 f9f84b39 children_at_exit       {"alive": [], "exitcodes": []}
09:12:39.0 f9f84b39 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:12:40.2 cfcb57ca start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3986564/scratch", "mode": "run", "ppid": 3986564, "previous_starts_in_sandbox": 1, "python": "3.9.25", "sandbox_created_by": "f9f84b39", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch"}
09:12:40.2 cfcb57ca history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch/ckpt", "store": "spool"}
09:12:40.2 cfcb57ca restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3986564/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950339.9487054, "saved_by_exec": "f9f84b39", "saved_on_host": "e4049", "saved_reason": "voluntary
09:12:40.2 cfcb57ca loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
09:13:47.7 cfcb57ca signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790950427.684513, "role": "parent", "signal": "SIGTERM", "step": 72}
09:13:48.3 cfcb57ca save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 73}
09:14:08.5 cfcb57ca save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 20.217, "step": 73, "write_seconds": 0.181}
09:14:08.5 cfcb57ca signal_save_finished   {"ok": true, "seconds_since_signal": 20.825}
09:14:08.5 cfcb57ca children_at_exit       {"alive": [], "exitcodes": []}
09:14:08.5 cfcb57ca exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 73}
09:15:43.0 667e8912 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3418678/scratch", "mode": "run", "ppid": 3418678, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "667e8912", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3418678/scratch"}
09:15:43.0 667e8912 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3418678/scratch/ckpt", "store": "spool"}
09:15:43.0 667e8912 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3418678/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950339.9487054, "saved_by_exec": "f9f84b39", "saved_on_host": "e4049", "saved_reason": "voluntary
09:15:43.0 667e8912 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.8 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7a-wrapper-exec-bare-vacate/job.log", "trigger": "vacate"}
09:13:47.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790950334.0, "job": "6575719.0", "last_event": "file_transfer", "trigger": "vacate"}
09:13:47.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6575719.0"], "output": "Job 6575719.0 vacated\n", "rc": 0}
09:13:47.7 {"action": "done"}
```
