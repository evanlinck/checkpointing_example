# P11d-input-limit-ckpt-ok-vacate on ospool

**Question.** Control for P11d-input-limit-ckpt: the same job with max_transfer_input_mb = 200. It should resume normally, showing that a hold in the 50 MB test comes from the limit.

Job: `7093569.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/ospool/P11d-input-limit-ckpt-ok-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 52 s, DIFFERENT host, sandbox NEW, restored step 153 (saved by: signal).
- Trigger vacate fired at 09:31:05.4 (AP clock).
- Evicted execution received SIGTERM 0.5 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 153 (saved by: signal) -> the SIGTERM save (step 153) SURVIVED.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 285b7355 | 09:28:27.7 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 0.243)] | 85 |
| c1a182bd | 09:29:03.1 | <host-1> | True | 0 | 30 (voluntary) | SIGTERM | [(153, 'signal', 0.277)] | 85 |
| b786f2a2 | 09:31:58.7 | <host-2> | False | 1 | 153 (signal) |  | [(300, 'final', 1.234)] | 0 |

## HTCondor event log (AP clock)

- 09:27:32.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P11d-input-limit-ckpt-ok-vacate"; JobBatchName = "probes.dag+7093501" ]
- 09:28:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:32857?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#16962983%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 09:28:25.0 `040 file_transfer` Finished transferring input files 
- 09:28:26.0 `021 remote_error` Message from starter on slot1_8@glidein_3203190_178546980@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:28:26.0 `001 executing` Job executing on host: <<ip>:43085?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_8@glidein_3203190_178546980@<host-1>; CondorScratchDir = "/tmp/jobs/889546/glide_gmJ7KU/execute/dir_2059435/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:28:58.0 `040 file_transfer` Started transferring output files 
- 09:29:01.0 `040 file_transfer` Finished transferring output files 
- 09:31:07.0 `040 file_transfer` Started transferring output files 
- 09:31:09.0 `040 file_transfer` Finished transferring output files 
- 09:31:10.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 104864366  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)          
- 09:31:47.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:41551?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#16963189%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26a
- 09:31:56.0 `040 file_transfer` Finished transferring input files 
- 09:31:57.0 `021 remote_error` Message from starter on slot1_3@glidein_3793958_188094244@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:31:57.0 `001 executing` Job executing on host: <<ip>:45757?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f5 — SlotName: slot1_3@glidein_3793958_188094244@<host-2>; CondorScratchDir = "/localscratch/condor/execute/dir_3779480/scratch/glide_pG2dvo/execute/dir_78335/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:34:29.0 `040 file_transfer` Started transferring output files 
- 09:34:29.0 `040 file_transfer` Finished transferring output files 
- 09:34:29.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 21816  -  Run Bytes Sent By Job; 391203660  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 164.0
CommittedSuspensionTime = 0
CommittedTime = 195
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793025269
JobCurrentStartTransferOutputDate = 1793025269
LastRemoteHost = slot1_3@glidein_3793958_188094244@<host-2>
LastRemoteWallClockTime = 164.0
LastVacateTime = 1793025070
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
RemoteWallClockTime = 345.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793025269
TransferOutStarted = 1793025269
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 104886182; CedarFilesCountTotal = 20; CedarSizeBytesLastRun = 21816; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## Probe timeline (EP clock; ticks omitted)

```
09:28:27.7 285b7355 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793237959", "GLIDEIN_ToRetire": "1793201959", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_cr
09:28:27.7 285b7355 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:28:27.7 285b7355 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:28:27.7 285b7355 loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
09:28:57.8 285b7355 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
09:28:58.0 285b7355 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.243, "step": 30, "write_seconds": 0.242}
09:28:58.0 285b7355 children_at_exit       {"alive": [], "exitcodes": []}
09:28:58.0 285b7355 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:29:03.1 c1a182bd start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793237959", "GLIDEIN_ToRetire": "1793201959", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_cr
09:29:03.1 c1a182bd history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:29:03.1 c1a182bd restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024938.039632, "saved_by_exec": "285b7355", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 30}
09:29:03.1 c1a182bd loop_start             {"restored_step": 30, "step": 30, "total_steps": 300, "voluntary_exit_at": [30]}
09:31:05.9 c1a182bd signal                 {"first": true, "on_sigterm": "save85", "received_at": 1793025065.8765385, "role": "parent", "signal": "SIGTERM", "step": 152}
09:31:06.3 c1a182bd save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "signal", "step": 153}
09:31:06.6 c1a182bd save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.277, "step": 153, "write_seconds": 0.252}
09:31:06.6 c1a182bd signal_save_finished   {"ok": true, "seconds_since_signal": 0.736}
09:31:06.6 c1a182bd children_at_exit       {"alive": [], "exitcodes": []}
09:31:06.6 c1a182bd exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 153}
09:31:58.7 b786f2a2 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "PSU-LIGO", "GLIDEIN_ToDie": "1793093151", "GLIDEIN_ToRetire": "1793057151", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
09:31:58.7 b786f2a2 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:31:58.7 b786f2a2 restore                {"chosen": "step_00000153", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000153", "nested_dir_ok": true, "saved_at": 1793025066.5830588, "saved_by_exec": "c1a182bd", "saved_on_host": "<host-1>", "saved_reason": "signal", "step": 153}
09:31:58.8 b786f2a2 loop_start             {"restored_step": 153, "step": 153, "total_steps": 300, "voluntary_exit_at": [30]}
09:34:27.5 b786f2a2 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "final", "step": 300}
09:34:28.7 b786f2a2 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "final", "seconds": 1.234, "step": 300, "write_seconds": 1.21}
09:34:28.7 b786f2a2 children_at_exit       {"alive": [], "exitcodes": []}
09:34:28.7 b786f2a2 exit                   {"code": 0, "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
09:16:19.5 {"action": "waiting", "after": 150.0, "log": "/home/<user>/checkpointing_example/probes/runs/ospool-r4/ospool/P11d-input-limit-ckpt-ok-vacate/job.log", "trigger": "vacate"}
09:31:05.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1793024906.0, "job": "7093569.0", "last_event": "file_transfer", "trigger": "vacate"}
09:31:05.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "7093569.0"], "output": "Job 7093569.0 vacated\n", "rc": 0}
09:31:05.4 {"action": "done"}
```
