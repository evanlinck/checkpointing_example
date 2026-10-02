# P7b-wrapper-noexec-bare-vacate on chtc

**Question.** When a shell wrapper runs python WITHOUT exec, who gets the signal: only bash, or python too? Is python killed before it finishes saving?

Job: `6576341.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7b-wrapper-noexec-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 0 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 0: gap 72 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:18:02.6 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +183.6 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_noexec.sh pid=3688363 starting python3 as a child | WRAPPER python exited with 85 at 1790950610.364302723; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=3689599 starting python3 as a child | WRAPPER bash received SIGTERM at 1790950866.143705933 | WRAPPER python exited with 0 at 1790950866.146206582; wrapper exiting with the same code | WRAPPER run_noexec.sh pid=138638 

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 87607f86 | 09:16:25.3 | e4035 | False | 0 | None (None) |  | [(5, 'voluntary', 20.05)] | 85 |
| cc05ee04 | 09:16:50.5 | e4035 | True | 0 | 5 (voluntary) |  | [(240, 'final', 20.075)] | 0 |
| aacdc359 | 09:22:17.9 | e2597 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:15:52.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7b-wrapper-noexec-bare-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:16:25.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4035.chtc.wisc.edu&noUDP&sock=slot1_29_626393_48d9_121495>
- 09:16:25.0 `040 file_transfer` Finished transferring input files 
- 09:16:25.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_29@e4035.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3688298/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:16:50.0 `040 file_transfer` Started transferring output files 
- 09:16:50.0 `040 file_transfer` Finished transferring output files 
- 09:21:06.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050603  -  Run Bytes Sent By Job; 31061  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            :   
- 09:22:12.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2597.chtc.wisc.edu&noUDP&sock=slot1_81_1158672_fe06_116032>
- 09:22:12.0 `040 file_transfer` Finished transferring input files 
- 09:22:17.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_81@e2597.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_137431/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:22:18.0 `040 file_transfer` Started transferring output files 
- 09:22:18.0 `040 file_transfer` Finished transferring output files 
- 09:22:18.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051662  -  Run Bytes Sent By Job; 1081696  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 6.0
CommittedSuspensionTime = 0
CommittedTime = 31
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790950938
LastRemoteHost = slot1_81@e2597.chtc.wisc.edu
LastRemoteWallClockTime = 6.0
LastVacateTime = 1790950866
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
RemoteWallClockTime = 288.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950938
TransferOutStarted = 1790950938
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102265; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051662; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:16:25.3 87607f86 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3688298/scratch", "mode": "run", "ppid": 3688363, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "87607f86", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch"}
09:16:25.3 87607f86 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch/ckpt", "store": "spool"}
09:16:25.3 87607f86 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:16:25.3 87607f86 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:16:30.3 87607f86 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:16:50.3 87607f86 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.05, "step": 5, "write_seconds": 0.013}
09:16:50.3 87607f86 children_at_exit       {"alive": [], "exitcodes": []}
09:16:50.3 87607f86 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:16:50.5 cc05ee04 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3688298/scratch", "mode": "run", "ppid": 3689599, "previous_starts_in_sandbox": 1, "python": "3.9.25", "sandbox_created_by": "87607f86", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch"}
09:16:50.5 cc05ee04 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch/ckpt", "store": "spool"}
09:16:50.5 cc05ee04 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3688298/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950590.302114, "saved_by_exec": "87607f86", "saved_on_host": "e4035", "saved_reason": "voluntary"
09:16:50.5 cc05ee04 loop_start             {"restored_step": 5, "step": 5, "total_steps": 240, "voluntary_exit_at": [5]}
09:20:45.0 cc05ee04 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 240}
09:21:06.0 cc05ee04 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 20.075, "step": 240, "write_seconds": 0.021}
09:21:06.1 cc05ee04 children_at_exit       {"alive": [], "exitcodes": []}
09:21:06.1 cc05ee04 exit                   {"code": 0, "reason": "finished 240 steps", "step": 240}
09:22:17.9 aacdc359 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_137431/scratch", "mode": "run", "ppid": 138638, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "aacdc359", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_137431/scratch"}
09:22:17.9 aacdc359 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_137431/scratch/ckpt", "store": "spool"}
09:22:17.9 aacdc359 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_137431/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950590.302114, "saved_by_exec": "87607f86", "saved_on_host": "e4035", "saved_reason": "voluntary",
09:22:17.9 aacdc359 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.9 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7b-wrapper-noexec-bare-vacate/job.log", "trigger": "vacate"}
09:18:02.6 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790950585.0, "job": "6576341.0", "last_event": "file_transfer", "trigger": "vacate"}
09:18:02.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6576341.0"], "output": "Job 6576341.0 vacated\n", "rc": 0}
09:18:02.7 {"action": "done"}
```
