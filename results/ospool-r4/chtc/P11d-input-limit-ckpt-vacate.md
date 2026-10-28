# P11d-input-limit-ckpt-vacate on chtc

**Question.** With max_transfer_input_mb = 50, a 100 MB spooled checkpoint, and a vacate that forces a restart in a new sandbox: is the restart held for exceeding the input limit (so a checkpoint counts as input), or does it resume? (OSPool access points such as ap40 set MAX_TRANSFER_INPUT_MB = 5000 and don't let users change it.) The container variant also shows whether the osdf:// container image counts.

Job: `7093506.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-vacate`

## Observations

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE)
- Held at 09:20:12.0: Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Trigger vacate fired at 09:19:49.5 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 7.5 s after the signal.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 2bd93e67 | 09:17:19.0 | <host-2> | False | 0 | None (None) |  | [(30, 'voluntary', 2.836)] | 85 |
| fba2f085 | 09:17:53.9 | <host-2> | True | 0 | 30 (voluntary) | SIGTERM | [(146, 'signal', 6.841)] | 85 |

## HTCondor event log (AP clock)

- 09:16:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P11d-input-limit-ckpt-vacate"; JobBatchName = "probes.dag+7093501" ]
- 09:17:06.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-2>&noUDP&sock=slot1_33_3879489_b497_87929>
- 09:17:17.0 `040 file_transfer` Finished transferring input files 
- 09:17:17.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_33@<host-2>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2664838/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:17:52.0 `040 file_transfer` Started transferring output files 
- 09:17:52.0 `040 file_transfer` Finished transferring output files 
- 09:19:57.0 `040 file_transfer` Started transferring output files 
- 09:19:57.0 `040 file_transfer` Finished transferring output files 
- 09:19:57.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:01, Sys 0 00:00:05  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 104864220  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.05        1         1; Disk (KB)         
- 09:20:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_23_2711711_7658_95200>
- 09:20:11.0 `040 file_transfer` Finished transferring input files 
- 09:20:11.0 `021 remote_error` Error from starter on slot1_23@<host-1>: — Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this f
- 09:20:12.0 `004 evicted` Job was evicted. Code 32 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 0  -  Run Bytes Received By Job; Reason: Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send fil
- 09:20:12.0 `012 held` Job was held. — Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total
- 09:51:01.0 `009 aborted` Job was aborted. — The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 34
ExitBySignal = false
ExitCode = 85
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024397
JobCurrentStartTransferOutputDate = 1793024397
LastHoldReason = Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this file=100 MB); STARTER failed to receive file(s) from <<ip>:9618>
LastHoldReasonCode = 32
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_23@<host-1>
LastRemoteWallClockTime = 9.0
LastVacateTime = 1793024397
MaxTransferInputMB = 50
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ MaxTransferInputSizeExceeded = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 0
NumJobMatches = 2
NumJobStarts = 1
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 2
NumVacatesByReason = [ ScheddVacate = 1; MaxTransferInputSizeExceeded = 1 ]
NumVacatesByReasonPreExecution = [ MaxTransferInputSizeExceeded = 1 ]
NumVacatesPreExecution = 1
RemoteWallClockTime = 181.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793024397
TransferOutStarted = 1793024397
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 104864220; CedarFilesCountTotal = 10; CedarSizeBytesLastRun = 104864220; CedarFilesCountLastRun = 10 ]
VacateReason = Error from slot1_23@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:34105>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3506/0/cluster7093506.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this file=100 MB); STARTER failed to receive file(s) from <<ip>:9618>
VacateReasonCode = 32
VacateReasonSubCode = 0
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:19.0 2bd93e67 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2664838/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "2bd93e67", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:17:19.0 2bd93e67 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2664838/scratch/ckpt", "store": "spool"}
09:17:19.0 2bd93e67 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2664838/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:19.0 2bd93e67 loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
09:17:49.1 2bd93e67 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
09:17:51.0 2bd93e67 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 2.836, "step": 30, "write_seconds": 2.833}
09:17:51.0 2bd93e67 children_at_exit       {"alive": [], "exitcodes": []}
09:17:51.0 2bd93e67 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:17:53.9 fba2f085 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2664838/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "2bd93e67", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:17:53.9 fba2f085 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2664838/scratch/ckpt", "store": "spool"}
09:17:53.9 fba2f085 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2664838/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024271.9464293, "saved_by_exec": "2bd93e67", "saved_on_host": "<host-2>", "saved_reason": "voluntary
09:17:53.9 fba2f085 loop_start             {"restored_step": 30, "step": 30, "total_steps": 300, "voluntary_exit_at": [30]}
09:19:49.8 fba2f085 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793024389.7080882, "role": "parent", "signal": "SIGTERM", "step": 145}
09:19:50.4 fba2f085 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "signal", "step": 146}
09:19:57.2 fba2f085 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "signal", "seconds": 6.841, "step": 146, "write_seconds": 6.766}
09:19:57.2 fba2f085 signal_save_finished   {"ok": true, "seconds_since_signal": 7.499}
09:19:57.2 fba2f085 children_at_exit       {"alive": [], "exitcodes": []}
09:19:57.2 fba2f085 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 146}
```

## Trigger log (AP clock)

```
09:16:19.3 {"action": "waiting", "after": 150.0, "log": "/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-ckpt-vacate/job.log", "trigger": "vacate"}
09:19:49.5 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1793024237.0, "job": "7093506.0", "last_event": "file_transfer", "trigger": "vacate"}
09:19:49.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "7093506.0"], "output": "Job 7093506.0 vacated\n", "rc": 0}
09:19:49.7 {"action": "done"}
```
