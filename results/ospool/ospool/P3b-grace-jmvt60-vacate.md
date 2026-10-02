# P3b-grace-jmvt60-vacate on ospool

**Question.** Is job_max_vacate_time = 60 honoured (grace about 60 s)?

Job: `6589089.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P3b-grace-jmvt60-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGTERM, no exit recorded): gap 184 s, same host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:47:22.4 (AP clock).
- Evicted execution received SIGTERM 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 59.4 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 07c6f7ab | 11:45:53.4 | warlock21 | False | 0 | None (None) |  | [(5, 'voluntary', 0.126)] | 85 |
| d00d5605 | 11:46:01.1 | warlock21 | True | 0 | 5 (voluntary) | SIGTERM | [] | none (killed?) |
| 70ce0a0f | 11:51:26.8 | warlock21 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:43:50.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P3b-grace-jmvt60-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:45:16.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:43037?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector5#14599762%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:45:51.0 `040 file_transfer` Finished transferring input files 
- 11:45:51.0 `021 remote_error` Message from starter on slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:45:51.0 `001 executing` Job executing on host: <<ip>:37419?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_e7SCVy/execute/dir_3400840/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:45:59.0 `040 file_transfer` Started transferring output files 
- 11:45:59.0 `040 file_transfer` Finished transferring output files 
- 11:48:26.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051100  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.02        1         1; Disk (KB)           
- 11:49:19.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:38423?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#14603025%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:51:24.0 `040 file_transfer` Finished transferring input files 
- 11:51:25.0 `021 remote_error` Message from starter on slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:51:25.0 `001 executing` Job executing on host: <<ip>:37419?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_e7SCVy/execute/dir_3421114/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:51:27.0 `040 file_transfer` Started transferring output files 
- 11:51:27.0 `040 file_transfer` Finished transferring output files 
- 11:51:27.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052072  -  Run Bytes Sent By Job; 287388010 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 129.0
CommittedSuspensionTime = 0
CommittedTime = 135
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790959887
JobCurrentStartTransferOutputDate = 1790959887
JobMaxVacateTime = 60
LastRemoteHost = slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu
LastRemoteWallClockTime = 129.0
LastVacateTime = 1790959706
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
RemoteWallClockTime = 320.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959887
TransferOutStarted = 1790959887
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103172; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052072; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:45:53.4 07c6f7ab start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "07c6f7ab", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:45:53.4 07c6f7ab history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:45:53.5 07c6f7ab restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:45:53.5 07c6f7ab loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:45:58.8 07c6f7ab save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:45:58.0 07c6f7ab save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.126, "step": 5, "write_seconds": 0.084}
11:45:59.0 07c6f7ab children_at_exit       {"alive": [], "exitcodes": []}
11:45:59.0 07c6f7ab exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:46:01.1 d00d5605 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "07c6f7ab", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:46:01.1 d00d5605 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:46:01.1 d00d5605 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790959558.8926113, "saved_by_exec": "07c6f7ab", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 5}
11:46:01.2 d00d5605 loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:47:23.1 d00d5605 signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790959643.0742633, "role": "parent", "signal": "SIGTERM", "step": 83}
11:51:26.8 70ce0a0f start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "70ce0a0f", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:51:26.8 70ce0a0f history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:51:26.9 70ce0a0f restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790959558.8926113, "saved_by_exec": "07c6f7ab", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 5}
11:51:26.9 70ce0a0f exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:50.4 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/ospool/ospool/P3b-grace-jmvt60-vacate/job.log", "trigger": "vacate"}
11:47:22.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790959551.0, "job": "6589089.0", "last_event": "file_transfer", "trigger": "vacate"}
11:47:22.5 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6589089.0"], "output": "Job 6589089.0 vacated\n", "rc": 0}
11:47:22.5 {"action": "done"}
```
