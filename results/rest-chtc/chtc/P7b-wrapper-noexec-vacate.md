# P7b-wrapper-noexec-vacate on chtc

**Question.** When a shell wrapper runs python WITHOUT exec, who gets the signal: only bash, or python too? Is python killed before it finishes saving?

Job: `6575720.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7b-wrapper-noexec-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 0: gap 48 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:14:47.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +181.5 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_noexec.sh pid=14 starting python3 as a child | WRAPPER python exited with 85 at 1790950412.701157790; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=14 starting python3 as a child | WRAPPER bash received SIGTERM at 1790950668.860492951 | WRAPPER python exited with 0 at 1790950668.865047461; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=14 starting pytho

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 04e6966d | 09:13:07.2 | e2470 | False | 0 | None (None) |  | [(5, 'voluntary', 20.035)] | 85 |
| 0eee56e6 | 09:13:33.4 | e2470 | True | 0 | 5 (voluntary) |  | [(240, 'final', 20.043)] | 0 |
| 4180afa3 | 09:18:37.3 | e2470 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:12:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7b-wrapper-noexec-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:12:59.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2470.chtc.wisc.edu&noUDP&sock=slot1_35_1971642_e6e9_94230>
- 09:13:06.0 `040 file_transfer` Finished transferring input files 
- 09:13:06.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_35@e2470.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1200832/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:13:32.0 `040 file_transfer` Started transferring output files 
- 09:13:32.0 `040 file_transfer` Finished transferring output files 
- 09:17:49.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050527  -  Run Bytes Sent By Job; 286337427  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 09:18:30.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2470.chtc.wisc.edu&noUDP&sock=slot1_35_1971642_e6e9_94236>
- 09:18:36.0 `040 file_transfer` Finished transferring input files 
- 09:18:36.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_35@e2470.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1207633/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:18:37.0 `040 file_transfer` Started transferring output files 
- 09:18:38.0 `040 file_transfer` Finished transferring output files 
- 09:18:38.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051561  -  Run Bytes Sent By Job; 287387986 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 8.0
CommittedSuspensionTime = 0
CommittedTime = 33
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790950717
LastRemoteHost = slot1_35@e2470.chtc.wisc.edu
LastRemoteWallClockTime = 8.0
LastVacateTime = 1790950669
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
RemoteWallClockTime = 299.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950718
TransferOutStarted = 1790950717
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102088; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051561; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:13:07.2 04e6966d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1200832/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "04e6966d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch"}
09:13:07.2 04e6966d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch/ckpt", "store": "spool"}
09:13:07.2 04e6966d restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:13:07.2 04e6966d loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:13:12.6 04e6966d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:13:32.7 04e6966d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.035, "step": 5, "write_seconds": 0.011}
09:13:32.7 04e6966d children_at_exit       {"alive": [], "exitcodes": []}
09:13:32.7 04e6966d exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:13:33.4 0eee56e6 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1200832/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "04e6966d", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch"}
09:13:33.4 0eee56e6 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch/ckpt", "store": "spool"}
09:13:33.4 0eee56e6 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1200832/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950392.6553385, "saved_by_exec": "04e6966d", "saved_on_host": "e2470", "saved_reason": "voluntary
09:13:33.4 0eee56e6 loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
09:17:28.8 0eee56e6 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 240}
09:17:48.8 0eee56e6 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 20.043, "step": 240, "write_seconds": 0.011}
09:17:48.8 0eee56e6 children_at_exit       {"alive": [], "exitcodes": []}
09:17:48.8 0eee56e6 exit                   {"code": 0, "reason": "finished 240 steps", "step": 240}
09:18:37.3 4180afa3 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1207633/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4180afa3", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1207633/scratch"}
09:18:37.3 4180afa3 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1207633/scratch/ckpt", "store": "spool"}
09:18:37.3 4180afa3 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1207633/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950392.6553385, "saved_by_exec": "04e6966d", "saved_on_host": "e2470", "saved_reason": "voluntary
09:18:37.3 4180afa3 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.8 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7b-wrapper-noexec-vacate/job.log", "trigger": "vacate"}
09:14:47.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790950386.0, "job": "6575720.0", "last_event": "file_transfer", "trigger": "vacate"}
09:14:47.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6575720.0"], "output": "Job 6575720.0 vacated\n", "rc": 0}
09:14:47.4 {"action": "done"}
```
