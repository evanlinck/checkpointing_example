# P11d-input-limit-ckpt-ok-vacate on chtc

**Question.** Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit.

Job: `7093502.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-ok-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:04  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 22 s, DIFFERENT host, sandbox NEW, restored step 151 (saved by: signal).
- Trigger vacate fired at 09:19:49.2 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.3 s after the signal.
- Next execution restored step 151 (saved by: signal) -> the SIGTERM save (step 151) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 5d7b31d1 | 09:17:14.8 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 0.848)] | 85 |
| 4cbd38f7 | 09:17:47.0 | <host-1> | True | 0 | 30 (voluntary) | SIGTERM | [(151, 'signal', 1.04)] | 85 |
| 92f61555 | 09:20:13.2 | <host-2> | False | 1 | 151 (signal) |  | [(300, 'final', 2.113)] | 0 |

## HTCondor event log (AP clock)

- 09:16:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P11d-input-limit-ckpt-ok-vacate"; JobBatchName = "probes.dag+7093501" ]
- 09:17:06.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_23_2711711_7658_95195>
- 09:17:13.0 `040 file_transfer` Finished transferring input files 
- 09:17:13.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_23@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1862916/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:17:46.0 `040 file_transfer` Started transferring output files 
- 09:17:46.0 `040 file_transfer` Finished transferring output files 
- 09:19:50.0 `040 file_transfer` Started transferring output files 
- 09:19:51.0 `040 file_transfer` Finished transferring output files 
- 09:19:51.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 104864952  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.02        1         1; Disk (KB)         
- 09:20:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-2>&noUDP&sock=slot1_45_2701374_1c54_87903>
- 09:20:11.0 `040 file_transfer` Finished transferring input files 
- 09:20:11.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_45@<host-2>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2863105/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:22:44.0 `040 file_transfer` Started transferring output files 
- 09:22:44.0 `040 file_transfer` Finished transferring output files 
- 09:22:45.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:04  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 22885  -  Run Bytes Sent By Job; 391204246  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 162.0
CommittedSuspensionTime = 0
CommittedTime = 193
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024564
JobCurrentStartTransferOutputDate = 1793024564
LastRemoteHost = slot1_45@<host-2>
LastRemoteWallClockTime = 162.0
LastVacateTime = 1793024391
MaxTransferInputMB = 200
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
RemoteWallClockTime = 328.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793024564
TransferOutStarted = 1793024564
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 104887837; CedarFilesCountTotal = 20; CedarSizeBytesLastRun = 22885; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:14.8 5d7b31d1 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1862916/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "5d7b31d1", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:17:14.8 5d7b31d1 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1862916/scratch/ckpt", "store": "spool"}
09:17:14.8 5d7b31d1 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1862916/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:14.8 5d7b31d1 loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
09:17:44.9 5d7b31d1 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
09:17:45.8 5d7b31d1 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.848, "step": 30, "write_seconds": 0.847}
09:17:45.8 5d7b31d1 children_at_exit       {"alive": [], "exitcodes": []}
09:17:45.8 5d7b31d1 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:17:47.0 4cbd38f7 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1862916/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "5d7b31d1", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:17:47.0 4cbd38f7 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1862916/scratch/ckpt", "store": "spool"}
09:17:47.0 4cbd38f7 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_1862916/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024265.7908835, "saved_by_exec": "5d7b31d1", "saved_on_host": "<host-1>", "saved_reaso
09:17:47.0 4cbd38f7 loop_start             {"restored_step": 30, "step": 30, "total_steps": 300, "voluntary_exit_at": [30]}
09:19:49.5 4cbd38f7 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793024389.3961143, "role": "parent", "signal": "SIGTERM", "step": 150}
09:19:49.7 4cbd38f7 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "signal", "step": 151}
09:19:50.7 4cbd38f7 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "signal", "seconds": 1.04, "step": 151, "write_seconds": 0.958}
09:19:50.7 4cbd38f7 signal_save_finished   {"ok": true, "seconds_since_signal": 1.345}
09:19:50.7 4cbd38f7 children_at_exit       {"alive": [], "exitcodes": []}
09:19:50.7 4cbd38f7 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 151}
09:20:13.2 92f61555 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2863105/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "92f61555", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:20:13.2 92f61555 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2863105/scratch/ckpt", "store": "spool"}
09:20:13.2 92f61555 restore                {"chosen": "step_00000151", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2863105/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000151", "nested_dir_ok": true, "saved_at": 1793024390.655635, "saved_by_exec": "4cbd38f7", "saved_on_host": "<host-1>", "saved_reason
09:20:13.2 92f61555 loop_start             {"restored_step": 151, "step": 151, "total_steps": 300, "voluntary_exit_at": [30]}
09:22:42.7 92f61555 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "final", "step": 300}
09:22:44.8 92f61555 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "final", "seconds": 2.113, "step": 300, "write_seconds": 2.043}
09:22:44.8 92f61555 children_at_exit       {"alive": [], "exitcodes": []}
09:22:44.8 92f61555 exit                   {"code": 0, "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
09:16:19.0 {"action": "waiting", "after": 150.0, "log": "/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-ok-vacate/job.log", "trigger": "vacate"}
09:19:49.2 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1793024233.0, "job": "7093502.0", "last_event": "file_transfer", "trigger": "vacate"}
09:19:49.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "7093502.0"], "output": "Job 7093502.0 vacated\n", "rc": 0}
09:19:49.3 {"action": "done"}
```
