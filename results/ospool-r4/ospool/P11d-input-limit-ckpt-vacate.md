# P11d-input-limit-ckpt-vacate on ospool

**Question.** With max_transfer_input_mb = 50, a 100 MB spooled checkpoint, and a vacate that forces a restart in a new sandbox: is the restart held for exceeding the input limit (so a checkpoint counts as input), or does it resume? (OSPool access points such as ap40 set MAX_TRANSFER_INPUT_MB = 5000 and don't let users change it.) The container variant also shows whether the osdf:// container image counts.

Job: `7093562.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/ospool/P11d-input-limit-ckpt-vacate`

## Observations

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE)
- Held at 09:27:26.0: Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Trigger vacate fired at 09:26:20.1 (AP clock).
- Evicted execution received SIGTERM 0.4 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 1.7 s after the signal.
- No later execution was observed.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 925b15fc | 09:23:48.5 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 2.245)] | 85 |
| e9544da3 | 09:24:23.8 | <host-1> | True | 0 | 30 (voluntary) | SIGTERM | [(146, 'signal', 1.296)] | 85 |

## HTCondor event log (AP clock)

- 09:22:52.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P11d-input-limit-ckpt-vacate"; JobBatchName = "probes.dag+7093501" ]
- 09:23:42.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42237?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#16962727%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 09:23:46.0 `040 file_transfer` Finished transferring input files 
- 09:23:47.0 `021 remote_error` Message from starter on slot1_1@glidein_615409_162190686@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:23:47.0 `001 executing` Job executing on host: <<ip>:35415?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f — SlotName: slot1_1@glidein_615409_162190686@<host-1>; CondorScratchDir = "/tmp/glide_C8b5Sx/execute/dir_3248692/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:24:21.0 `040 file_transfer` Started transferring output files 
- 09:24:22.0 `040 file_transfer` Finished transferring output files 
- 09:26:22.0 `040 file_transfer` Started transferring output files 
- 09:26:23.0 `040 file_transfer` Finished transferring output files 
- 09:26:23.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 104864929  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)          
- 09:27:14.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37667?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#16964791%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 09:27:26.0 `040 file_transfer` Finished transferring input files 
- 09:27:26.0 `021 remote_error` Error from starter on slot1_4@glidein_599723_231728740@<host-1>: — Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this fi
- 09:27:26.0 `004 evicted` Job was evicted. Code 32 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 0  -  Run Bytes Received By Job; Reason: Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW
- 09:27:26.0 `012 held` Job was held. — Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step
- 09:58:01.0 `009 aborted` Job was aborted. — The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 1800)' evaluated to TRUE

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 33
ExitBySignal = false
ExitCode = 85
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024783
JobCurrentStartTransferOutputDate = 1793024782
LastHoldReason = Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this file=100 MB); STARTER failed to receive file(s) from <<ip>:9618>
LastHoldReasonCode = 32
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_4@glidein_599723_231728740@<host-1>
LastRemoteWallClockTime = 13.0
LastVacateTime = 1793024783
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
RemoteWallClockTime = 175.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793024783
TransferOutStarted = 1793024782
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 104864929; CedarFilesCountTotal = 10; CedarSizeBytesLastRun = 104864929; CedarFilesCountLastRun = 10 ]
VacateReason = Error from slot1_4@glidein_599723_231728740@<host-1>: Failed to transfer files: SHADOW at <ip> failed to send file(s) to <<ip>:57009>: |Error: 1 total failures: first failure: sending file /var/lib/condor/spool/3562/0/cluster7093562.proc0.subproc0/ckpt/step_00000146/payload_000.bin: max total upload bytes exceeded (max=50 MB, this file=100 MB); STARTER failed to receive file(s) from <<ip>:9618>
VacateReasonCode = 32
VacateReasonSubCode = 0
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
09:23:48.5 925b15fc start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "UWM-Mortimer", "GLIDEIN_ToDie": "1793176113", "GLIDEIN_ToRetire": "1793140113", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_creat
09:23:48.5 925b15fc history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:23:48.5 925b15fc restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:23:48.6 925b15fc loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
09:24:18.7 925b15fc save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
09:24:20.0 925b15fc save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 2.245, "step": 30, "write_seconds": 2.095}
09:24:21.1 925b15fc children_at_exit       {"alive": [], "exitcodes": []}
09:24:21.2 925b15fc exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:24:23.8 e9544da3 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "UWM-Mortimer", "GLIDEIN_ToDie": "1793176113", "GLIDEIN_ToRetire": "1793140113", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_creat
09:24:23.8 e9544da3 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:24:23.9 e9544da3 restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024660.753933, "saved_by_exec": "925b15fc", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 
09:24:23.9 e9544da3 loop_start             {"restored_step": 30, "step": 30, "total_steps": 300, "voluntary_exit_at": [30]}
09:26:20.6 e9544da3 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793024780.479732, "role": "parent", "signal": "SIGTERM", "step": 145}
09:26:20.8 e9544da3 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "signal", "step": 146}
09:26:22.1 e9544da3 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "signal", "seconds": 1.296, "step": 146, "write_seconds": 1.208}
09:26:22.1 e9544da3 signal_save_finished   {"ok": true, "seconds_since_signal": 1.61}
09:26:22.1 e9544da3 children_at_exit       {"alive": [], "exitcodes": []}
09:26:22.1 e9544da3 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 146}
```

## Trigger log (AP clock)

```
09:16:19.5 {"action": "waiting", "after": 150.0, "log": "/home/<user>/checkpointing_example/probes/runs/ospool-r4/ospool/P11d-input-limit-ckpt-vacate/job.log", "trigger": "vacate"}
09:26:20.1 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1793024627.0, "job": "7093562.0", "last_event": "file_transfer", "trigger": "vacate"}
09:26:20.1 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "7093562.0"], "output": "Job 7093562.0 vacated\n", "rc": 0}
09:26:20.1 {"action": "done"}
```
