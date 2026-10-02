# P3a-grace-default-vacate on ospool

**Question.** How long between the soft-kill signal and SIGKILL, with default settings? Is there a retirement delay between the trigger and the signal? Does condor_hold behave like a vacate?

Job: `6589084.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P3a-grace-default-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 259 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:43:37.2 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.8 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4c0334e0 | 11:41:59.8 | gpu-node006 | False | 0 | None (None) |  | [(5, 'voluntary', 0.006)] | 85 |
| d59f0413 | 11:42:06.4 | gpu-node006 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| bb098e9b | 11:57:55.8 | warlock21 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:39:30.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P3a-grace-default-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:41:53.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42949?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#14598064%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:41:58.0 `040 file_transfer` Finished transferring input files 
- 11:41:59.0 `021 remote_error` Message from starter on slot1_2@glidein_2078512_412968555@gpu-node006: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:41:59.0 `001 executing` Job executing on host: <<ip>:36569?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_2078512_412968555@gpu-node006; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_qXOG6B/execute/dir_1823514/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:42:05.0 `040 file_transfer` Started transferring output files 
- 11:42:05.0 `040 file_transfer` Finished transferring output files 
- 11:53:37.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051140  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 11:55:05.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:34783?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#14598478%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:57:53.0 `040 file_transfer` Finished transferring input files 
- 11:57:54.0 `021 remote_error` Message from starter on slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:57:54.0 `001 executing` Job executing on host: <<ip>:37419?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_e7SCVy/execute/dir_3452037/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:57:56.0 `040 file_transfer` Started transferring output files 
- 11:57:56.0 `040 file_transfer` Finished transferring output files 
- 11:57:56.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052117  -  Run Bytes Sent By Job; 287388050 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 171.0
CommittedSuspensionTime = 0
CommittedTime = 176
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790960276
JobCurrentStartTransferOutputDate = 1790960276
LastRemoteHost = slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu
LastRemoteWallClockTime = 171.0
LastVacateTime = 1790960017
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
RemoteWallClockTime = 876.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790960276
TransferOutStarted = 1790960276
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103257; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052117; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:41:59.8 4c0334e0 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4c0334e0", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:41:59.8 4c0334e0 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:41:59.8 4c0334e0 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:41:59.8 4c0334e0 loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:42:04.8 4c0334e0 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:42:04.8 4c0334e0 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 5, "write_seconds": 0.005}
11:42:04.8 4c0334e0 children_at_exit       {"alive": [], "exitcodes": []}
11:42:04.8 4c0334e0 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:42:06.4 d59f0413 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "4c0334e0", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:42:06.4 d59f0413 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:42:06.4 d59f0413 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790959324.7813063, "saved_by_exec": "4c0334e0", "saved_on_host": "gpu-node006", "saved_reason": "voluntary", "step": 5}
11:42:06.4 d59f0413 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:43:37.4 d59f0413 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790959417.299918, "role": "parent", "signal": "SIGTERM", "step": 95}
11:57:55.8 bb098e9b start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "bb098e9b", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:57:55.8 bb098e9b history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:57:55.8 bb098e9b restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790959324.7813063, "saved_by_exec": "4c0334e0", "saved_on_host": "gpu-node006", "saved_reason": "voluntary", "step": 5}
11:57:55.8 bb098e9b exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:50.4 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/ospool/ospool/P3a-grace-default-vacate/job.log", "trigger": "vacate"}
11:43:37.2 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790959319.0, "job": "6589084.0", "last_event": "image_size", "trigger": "vacate"}
11:43:37.2 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6589084.0"], "output": "Job 6589084.0 vacated\n", "rc": 0}
11:43:37.2 {"action": "done"}
```
