# P2a-save85-vacate-fast on ospool

**Question.** KEY TEST. If SIGTERM arrives after a voluntary checkpoint (step A) and the handler saves step B and exits 85, which step does the restarted job see: A or B? (Only checkpoint_exit_code is set.)

Job: `6586488.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P2a-save85-vacate-fast`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after ended without an exit record: gap 28 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate-fast fired at 11:18:44.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was -0.8 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| a885e6ea | 11:16:14.4 | dwarf31 | False | 0 | None (None) |  | [(60, 'voluntary', 0.121)] | 85 |
| 48ee5d9a | 11:17:32.1 | dwarf31 | True | 0 | 60 (voluntary) |  | [] | none (killed?) |
| 2507b4cf | 11:19:11.0 | a221.anvil.rcac.purdue.edu | False | 1 | 60 (voluntary) |  | [(420, 'final', 0.006)] | 0 |

## HTCondor event log (AP clock)

- 11:13:37.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P2a-save85-vacate-fast"; JobBatchName = "probes.dag+6586482" ]
- 11:15:44.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42997?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector7#14589385%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:16:12.0 `040 file_transfer` Finished transferring input files 
- 11:16:13.0 `021 remote_error` Message from starter on slot1_2@glidein_3360985_97281786@dwarf31.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:16:13.0 `001 executing` Job executing on host: <<ip>:38359?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_3360985_97281786@dwarf31.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_mU9kM1/execute/dir_758688/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:17:30.0 `040 file_transfer` Started transferring output files 
- 11:17:30.0 `040 file_transfer` Finished transferring output files 
- 11:18:44.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051382  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.03        1         1; Disk (KB)           
- 11:19:07.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37463?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector2#14601661%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 11:19:10.0 `040 file_transfer` Finished transferring input files 
- 11:19:10.0 `021 remote_error` Message from starter on slot1_11@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:19:10.0 `001 executing` Job executing on host: <<ip>:33881?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_11@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_YjcjOc/execute/dir_2045658/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:25:12.0 `040 file_transfer` Started transferring output files 
- 11:25:12.0 `040 file_transfer` Finished transferring output files 
- 11:25:13.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 21596  -  Run Bytes Sent By Job; 287388292  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 367.0
CommittedSuspensionTime = 0
CommittedTime = 443
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958312
JobCurrentStartTransferOutputDate = 1790958312
LastRemoteHost = slot1_11@glidein_1045805_160726900@a221.anvil.rcac.purdue.edu
LastRemoteWallClockTime = 367.0
LastVacateTime = 1790957924
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
RemoteWallClockTime = 549.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958312
TransferOutStarted = 1790958312
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1072978; CedarFilesCountTotal = 24; CedarSizeBytesLastRun = 21596; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:16:14.4 a885e6ea start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a885e6ea", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:16:14.4 a885e6ea history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:16:14.4 a885e6ea restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:16:14.4 a885e6ea loop_start             {"restored_step": 0, "step": 0, "total_steps": 420, "voluntary_exit_at": [60]}
11:17:30.2 a885e6ea save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:17:30.3 a885e6ea save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.121, "step": 60, "write_seconds": 0.08}
11:17:30.4 a885e6ea children_at_exit       {"alive": [], "exitcodes": []}
11:17:30.4 a885e6ea exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:17:32.1 48ee5d9a start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "a885e6ea", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:17:32.1 48ee5d9a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:17:32.2 48ee5d9a restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790957850.2795098, "saved_by_exec": "a885e6ea", "saved_on_host": "dwarf31", "saved_reason": "voluntary", "step": 60}
11:17:32.2 48ee5d9a loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:19:11.0 2507b4cf start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "2507b4cf", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:19:11.0 2507b4cf history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:19:11.0 2507b4cf restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790957850.2795098, "saved_by_exec": "a885e6ea", "saved_on_host": "dwarf31", "saved_reason": "voluntary", "step": 60}
11:19:11.0 2507b4cf loop_start             {"restored_step": 60, "step": 60, "total_steps": 420, "voluntary_exit_at": [60]}
11:25:12.6 2507b4cf save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 420}
11:25:12.6 2507b4cf save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.006, "step": 420, "write_seconds": 0.005}
11:25:12.6 2507b4cf children_at_exit       {"alive": [], "exitcodes": []}
11:25:12.6 2507b4cf exit                   {"code": 0, "reason": "finished 420 steps", "step": 420}
```

## Trigger log (AP clock)

```
11:13:44.0 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P2a-save85-vacate-fast/job.log", "trigger": "vacate-fast"}
11:18:44.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790957773.0, "job": "6586488.0", "last_event": "file_transfer", "trigger": "vacate-fast"}
11:18:44.3 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "-fast", "6586488.0"], "output": "Job 6586488.0 fast-vacated\n", "rc": 0}
11:18:44.3 {"action": "done"}
```
