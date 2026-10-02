# P3c-grace-jmvt900-vacate on ospool

**Question.** If a job asks for job_max_vacate_time = 900, is it capped by the machine's MachineMaxVacateTime?

Job: `6589423.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P3c-grace-jmvt900-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 89 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:55:07.9 (AP clock).
- Evicted execution received SIGTERM 0.2 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 899.6 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f2612a9f | 11:53:27.2 | iut2-c341.iu.edu | False | 0 | None (None) |  | [(5, 'voluntary', 0.007)] | 85 |
| 8fa40b69 | 11:53:34.2 | iut2-c341.iu.edu | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| 483f35c7 | 12:11:36.5 | gpu-node007 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:52:41.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P3c-grace-jmvt900-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:53:13.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:35583?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector4#14594990%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 11:53:25.0 `040 file_transfer` Finished transferring input files 
- 11:53:25.0 `021 remote_error` Message from starter on slot1_5@glidein_1465173_624946780@iut2-c341.iu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:53:25.0 `001 executing` Job executing on host: <<ip>:42443?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_5@glidein_1465173_624946780@iut2-c341.iu.edu; CondorScratchDir = "/var/lib/condor/execute/dir_1465168/glide_yaw8ei/execute/dir_3329397/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:53:32.0 `040 file_transfer` Started transferring output files 
- 11:53:32.0 `040 file_transfer` Finished transferring output files 
- 12:10:08.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051203  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 12:11:31.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37779?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector2#14603424%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 12:11:34.0 `040 file_transfer` Finished transferring input files 
- 12:11:35.0 `021 remote_error` Message from starter on slot1_2@glidein_274175_175400355@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 12:11:35.0 `001 executing` Job executing on host: <<ip>:39443?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274175_175400355@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_om0aIN/execute/dir_2011705/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 12:11:36.0 `040 file_transfer` Started transferring output files 
- 12:11:37.0 `040 file_transfer` Finished transferring output files 
- 12:11:37.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052191  -  Run Bytes Sent By Job; 287388113 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 7.0
CommittedSuspensionTime = 0
CommittedTime = 13
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790961097
JobCurrentStartTransferOutputDate = 1790961096
JobMaxVacateTime = 900
LastRemoteHost = slot1_2@glidein_274175_175400355@gpu-node007
LastRemoteWallClockTime = 7.0
LastVacateTime = 1790961008
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
RemoteWallClockTime = 1023.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790961097
TransferOutStarted = 1790961096
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103394; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052191; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:53:27.2 f2612a9f start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f2612a9f", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:53:27.2 f2612a9f history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:53:27.2 f2612a9f restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:53:27.2 f2612a9f loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:53:32.2 f2612a9f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:53:32.3 f2612a9f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 5, "write_seconds": 0.007}
11:53:32.3 f2612a9f children_at_exit       {"alive": [], "exitcodes": []}
11:53:32.3 f2612a9f exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:53:34.2 8fa40b69 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "f2612a9f", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:53:34.2 8fa40b69 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:53:34.2 8fa40b69 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790960012.2511365, "saved_by_exec": "f2612a9f", "saved_on_host": "iut2-c341.iu.edu", "saved_reason": "voluntary", "step": 5}
11:53:34.2 8fa40b69 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:55:08.3 8fa40b69 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790960108.1615932, "role": "parent", "signal": "SIGTERM", "step": 98}
12:11:36.5 483f35c7 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "483f35c7", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
12:11:36.5 483f35c7 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
12:11:36.5 483f35c7 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790960012.2511365, "saved_by_exec": "f2612a9f", "saved_on_host": "iut2-c341.iu.edu", "saved_reason": "voluntary", "step": 5}
12:11:36.5 483f35c7 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:50.5 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/ospool/ospool/P3c-grace-jmvt900-vacate/job.log", "trigger": "vacate"}
11:55:07.9 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790960005.0, "job": "6589423.0", "last_event": "image_size", "trigger": "vacate"}
11:55:07.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6589423.0"], "output": "Job 6589423.0 vacated\n", "rc": 0}
11:55:07.0 {"action": "done"}
```
