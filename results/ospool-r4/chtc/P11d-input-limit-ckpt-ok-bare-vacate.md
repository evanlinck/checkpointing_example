# P11d-input-limit-ckpt-ok-bare-vacate on chtc

**Question.** Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit.

Job: `7093504.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-ok-bare-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 12 s, DIFFERENT host, sandbox NEW, restored step 161 (saved by: signal).
- Trigger vacate fired at 09:19:49.3 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 2.6 s after the signal.
- Next execution restored step 161 (saved by: signal) -> the SIGTERM save (step 161) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d50c8a01 | 09:17:06.5 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 1.602)] | 85 |
| 82373b05 | 09:17:38.8 | <host-1> | True | 0 | 30 (voluntary) | SIGTERM | [(161, 'signal', 1.848)] | 85 |
| 3c9ab416 | 09:20:04.5 | <host-2> | False | 1 | 161 (signal) |  | [(300, 'final', 0.167)] | 0 |

## HTCondor event log (AP clock)

- 09:16:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P11d-input-limit-ckpt-ok-bare-vacate"; JobBatchName = "probes.dag+7093501" ]
- 09:17:06.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_45_2701374_1c54_87899>
- 09:17:06.0 `040 file_transfer` Finished transferring input files 
- 09:17:06.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_45@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2853483/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:17:38.0 `040 file_transfer` Started transferring output files 
- 09:17:38.0 `040 file_transfer` Finished transferring output files 
- 09:19:52.0 `040 file_transfer` Started transferring output files 
- 09:19:52.0 `040 file_transfer` Finished transferring output files 
- 09:19:52.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 104864936  -  Run Bytes Sent By Job; 32888  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.01        1         1; Disk (KB)            :
- 09:20:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-2>&noUDP&sock=slot1_19_2980341_9944_67819>
- 09:20:04.0 `040 file_transfer` Finished transferring input files 
- 09:20:04.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_19@<host-2>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3762893/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:22:24.0 `040 file_transfer` Started transferring output files 
- 09:22:24.0 `040 file_transfer` Finished transferring output files 
- 09:22:24.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 23456  -  Run Bytes Sent By Job; 104897864  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 141.0
CommittedSuspensionTime = 0
CommittedTime = 172
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024544
JobCurrentStartTransferOutputDate = 1793024544
LastRemoteHost = slot1_19@<host-2>
LastRemoteWallClockTime = 141.0
LastVacateTime = 1793024392
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
RemoteWallClockTime = 308.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793024544
TransferOutStarted = 1793024544
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 104888392; CedarFilesCountTotal = 20; CedarSizeBytesLastRun = 23456; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:06.5 d50c8a01 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2853483/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 2853483, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "d50c8a01", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/exe
09:17:06.5 d50c8a01 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2853483/scratch/ckpt", "store": "spool"}
09:17:06.5 d50c8a01 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2853483/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:06.5 d50c8a01 loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
09:17:36.5 d50c8a01 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
09:17:38.1 d50c8a01 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 1.602, "step": 30, "write_seconds": 1.602}
09:17:38.1 d50c8a01 children_at_exit       {"alive": [], "exitcodes": []}
09:17:38.1 d50c8a01 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:17:38.8 82373b05 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2853483/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 2853483, "previous_starts_in_sandbox": 1, "python": "3.9.25", "sandbox_created_by": "d50c8a01", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/exec
09:17:38.8 82373b05 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2853483/scratch/ckpt", "store": "spool"}
09:17:38.8 82373b05 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2853483/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024258.1408234, "saved_by_exec": "d50c8a01", "saved_on_host": "<host-1>", "saved_reason": "voluntary
09:17:38.8 82373b05 loop_start             {"restored_step": 30, "step": 30, "total_steps": 300, "voluntary_exit_at": [30]}
09:19:49.5 82373b05 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793024389.52299, "role": "parent", "signal": "SIGTERM", "step": 160}
09:19:50.3 82373b05 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "signal", "step": 161}
09:19:52.1 82373b05 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "signal", "seconds": 1.848, "step": 161, "write_seconds": 1.785}
09:19:52.1 82373b05 signal_save_finished   {"ok": true, "seconds_since_signal": 2.589}
09:19:52.1 82373b05 children_at_exit       {"alive": [], "exitcodes": []}
09:19:52.1 82373b05 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 161}
09:20:04.5 3c9ab416 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3762893/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 3762893, "previous_starts_in_sandbox": 0, "python": "3.12.15", "sandbox_created_by": "3c9ab416", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/ex
09:20:04.5 3c9ab416 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3762893/scratch/ckpt", "store": "spool"}
09:20:04.5 3c9ab416 restore                {"chosen": "step_00000161", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3762893/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000161", "nested_dir_ok": true, "saved_at": 1793024392.040483, "saved_by_exec": "82373b05", "saved_on_host": "<host-1>", "saved_reason": "signal", "
09:20:04.5 3c9ab416 loop_start             {"restored_step": 161, "step": 161, "total_steps": 300, "voluntary_exit_at": [30]}
09:22:23.9 3c9ab416 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "final", "step": 300}
09:22:24.0 3c9ab416 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "final", "seconds": 0.167, "step": 300, "write_seconds": 0.123}
09:22:24.1 3c9ab416 children_at_exit       {"alive": [], "exitcodes": []}
09:22:24.1 3c9ab416 exit                   {"code": 0, "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
09:16:19.1 {"action": "waiting", "after": 150.0, "log": "/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-ok-bare-vacate/job.log", "trigger": "vacate"}
09:19:49.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1793024226.0, "job": "7093504.0", "last_event": "file_transfer", "trigger": "vacate"}
09:19:49.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "7093504.0"], "output": "Job 7093504.0 vacated\n", "rc": 0}
09:19:49.5 {"action": "done"}
```
