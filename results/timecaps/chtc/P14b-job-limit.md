# P14b-job-limit on chtc

**Question.** OSPool access points cap a self-checkpointing job's total time (ap40: AllowedJobDuration = 14 days, then a hold). Here allowed_job_duration = 240 s and the probe exits 85 every 60 s. When is the job held: 240 s after it first started (wall clock, across restarts), or after 240 s of running? With what message? Can the job compute its own deadline from JobStartDate + AllowedJobDuration in its job ad?

Job: `7195168.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/timecaps/chtc/P14b-job-limit`

## Observations

- Final job state: aborted (via condor_rm (by user <user>))
- First start 09:24:49.4; held 240 s later; job ad at first start: {'AllowedExecuteDuration': '259200', 'AllowedJobDuration': '240', 'JobStartDate': '1793111075'} -> deadline the job could compute: 09:28:35.0.
- Held at 09:28:49.0: The job exceeded allowed job duration of 04:00; Code 46 Subcode 0
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 8 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 7c2a2271 | 09:24:49.4 | <host-1> | False | 0 | None (None) |  | [(60, 'voluntary', 0.024)] | 85 |
| f3867c37 | 09:25:51.7 | <host-1> | True | 0 | 60 (voluntary) |  | [(120, 'voluntary', 0.014)] | 85 |
| d08e8ccb | 09:26:53.8 | <host-1> | True | 0 | 120 (voluntary) |  | [(180, 'voluntary', 0.024)] | 85 |
| 6510f61c | 09:28:02.6 | <host-1> | True | 0 | 180 (voluntary) | SIGTERM | [(226, 'signal', 0.074)] | 85 |

## HTCondor event log (AP clock)

- 09:24:08.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P14b-job-limit"; JobBatchName = "probes.dag+7195166" ]
- 09:24:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_35_1171405_8aec_110028>
- 09:24:47.0 `040 file_transfer` Finished transferring input files 
- 09:24:47.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_35@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_90902/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:25:49.0 `040 file_transfer` Started transferring output files 
- 09:25:49.0 `040 file_transfer` Finished transferring output files 
- 09:26:52.0 `040 file_transfer` Started transferring output files 
- 09:26:52.0 `040 file_transfer` Finished transferring output files 
- 09:27:54.0 `040 file_transfer` Started transferring output files 
- 09:27:54.0 `040 file_transfer` Finished transferring output files 
- 09:28:49.0 `012 held` Job was held. — The job exceeded allowed job duration of 04:00; Code 46 Subcode 0
- 09:42:46.0 `009 aborted` Job was aborted. — via condor_rm (by user <user>)

## condor_history (selected)

```
CheckpointNumber = 2
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 183
ExitBySignal = false
ExitCode = 85
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793111274
JobCurrentStartTransferOutputDate = 1793111274
LastHoldReason = The job exceeded allowed job duration of 04:00
LastHoldReasonCode = 46
LastHoldReasonSubCode = 0
LastRemoteHost = slot1_35@<host-1>
LastRemoteWallClockTime = 254.0
LastVacateTime = 1793111329
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 3
NumHoldsByReason = [ JobDurationExceeded = 3 ]
NumInputTransferStarts = 1
NumJobCompletions = 0
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
NumVacates = 2
NumVacatesByReason = [ ClaimDeactivated = 2 ]
RemoteWallClockTime = 254.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793111274
TransferOutStarted = 1793111274
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2105324; CedarFilesCountTotal = 16; CedarSizeBytesLastRun = 2105324; CedarFilesCountLastRun = 16 ]
VacateReason = Claim deactivated
VacateReasonCode = 1009
VacateReasonSubCode = 0
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:24:49.4 7c2a2271 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_90902/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "7c2a2271", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/sl
09:24:49.4 7c2a2271 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "store": "spool"}
09:24:49.4 7c2a2271 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:24:49.4 7c2a2271 loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:25:49.6 7c2a2271 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:25:49.7 7c2a2271 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.024, "step": 60, "write_seconds": 0.023}
09:25:49.7 7c2a2271 children_at_exit       {"alive": [], "exitcodes": []}
09:25:49.7 7c2a2271 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:25:51.7 f3867c37 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_90902/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "7c2a2271", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slo
09:25:51.7 f3867c37 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "store": "spool"}
09:25:51.7 f3867c37 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793111149.6690161, "saved_by_exec": "7c2a2271", "saved_on_host": "<host-1>", "saved_reason": "voluntary",
09:25:51.7 f3867c37 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:26:51.0 f3867c37 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 120}
09:26:51.0 f3867c37 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.014, "step": 120, "write_seconds": 0.01}
09:26:51.0 f3867c37 children_at_exit       {"alive": [], "exitcodes": []}
09:26:51.0 f3867c37 exit                   {"code": 85, "reason": "voluntary exit at step 120", "step": 120}
09:26:53.8 d08e8ccb start                  {"cwd": "/var/lib/condor/execute/slot1/dir_90902/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "7c2a2271", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slo
09:26:53.8 d08e8ccb history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "store": "spool"}
09:26:53.8 d08e8ccb restore                {"chosen": "step_00000120", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000120", "nested_dir_ok": true, "saved_at": 1793111211.988902, "saved_by_exec": "f3867c37", "saved_on_host": "<host-1>", "saved_reason": "voluntary", 
09:26:53.8 d08e8ccb loop_start             {"restored_step": 120, "step": 120, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:27:54.1 d08e8ccb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 180}
09:27:54.1 d08e8ccb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.024, "step": 180, "write_seconds": 0.008}
09:27:54.1 d08e8ccb children_at_exit       {"alive": [], "exitcodes": []}
09:27:54.2 d08e8ccb exit                   {"code": 85, "reason": "voluntary exit at step 180", "step": 180}
09:28:02.6 6510f61c start                  {"cwd": "/var/lib/condor/execute/slot1/dir_90902/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "7c2a2271", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slo
09:28:02.6 6510f61c history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "store": "spool"}
09:28:02.6 6510f61c restore                {"chosen": "step_00000180", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_90902/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000180", "nested_dir_ok": true, "saved_at": 1793111274.1295877, "saved_by_exec": "d08e8ccb", "saved_on_host": "<host-1>", "saved_reason": "voluntary",
09:28:02.6 6510f61c loop_start             {"restored_step": 180, "step": 180, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:28:48.8 6510f61c signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793111328.8438208, "role": "parent", "signal": "SIGTERM", "step": 225}
09:28:48.8 6510f61c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 226}
09:28:48.9 6510f61c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.074, "step": 226, "write_seconds": 0.049}
09:28:48.9 6510f61c signal_save_finished   {"ok": true, "seconds_since_signal": 0.08}
09:28:48.9 6510f61c children_at_exit       {"alive": [], "exitcodes": []}
09:28:48.9 6510f61c exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 226}
```
