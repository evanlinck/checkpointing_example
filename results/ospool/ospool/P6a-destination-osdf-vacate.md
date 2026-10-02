# P6a-destination-osdf-vacate on ospool

**Question.** Does checkpoint_destination = osdf://... (our /staging namespace) work, from CHTC and from the OSPool? After a vacate, does the restart get the checkpoint back from there?

Job: `6588669.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P6a-destination-osdf-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 14 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 54 s, DIFFERENT host, sandbox NEW, restored step 60 (saved by: voluntary).
- Trigger vacate fired at 11:37:36.9 (AP clock).
- Evicted execution received SIGTERM 0.3 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 0.7 s after the signal.
- Next execution restored step 60 (saved by: voluntary) -> the SIGTERM save (step 137) was LOST.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| c87997be | 11:35:06.0 | n010.cluster.com | False | 0 | None (None) |  | [(60, 'voluntary', 0.004)] | 85 |
| 3347fc60 | 11:36:20.8 | n010.cluster.com | True | 0 | 60 (voluntary) | SIGTERM | [(137, 'signal', 0.005)] | 85 |
| a7be09e5 | 11:38:31.5 | a248.anvil.rcac.purdue.edu | False | 1 | 60 (voluntary) |  | [(360, 'final', 0.006)] | 0 |

## HTCondor event log (AP clock)

- 11:31:35.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P6a-destination-osdf-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:32:22.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:39301?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#14602492%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 11:35:05.0 `040 file_transfer` Finished transferring input files 
- 11:35:06.0 `021 remote_error` Message from starter on slot1_12@glidein_20317_460887261@n010.cluster.com: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:35:06.0 `001 executing` Job executing on host: <<ip>:33509?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f — SlotName: slot1_12@glidein_20317_460887261@n010.cluster.com; CondorScratchDir = "/scratch/glide_97pDc0/execute/dir_410737/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:36:07.0 `040 file_transfer` Started transferring output files 
- 11:36:19.0 `040 file_transfer` Finished transferring output files 
- 11:37:38.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051993  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.07        1         1; Disk (KB)           
- 11:38:24.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42107?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector10#14593203%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 11:38:29.0 `040 file_transfer` Finished transferring input files 
- 11:38:30.0 `021 remote_error` Message from starter on slot1_57@glidein_3994679_188702304@a248.anvil.rcac.purdue.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:38:30.0 `001 executing` Job executing on host: <<ip>:42597?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f5 — SlotName: slot1_57@glidein_3994679_188702304@a248.anvil.rcac.purdue.edu; CondorScratchDir = "/tmp/glide_in9OrC/execute/dir_2793998/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:43:32.0 `040 file_transfer` Started transferring output files 
- 11:43:32.0 `040 file_transfer` Finished transferring output files 
- 11:43:33.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 19963  -  Run Bytes Sent By Job; 287389561  -

## condor_history (selected)

```
CheckpointDestination = osdf:///chtc/staging/<user>/ckpt-probes/ckptdest/6588669.0
CheckpointNumber = 0
CommittedSlotTime = 311.0
CommittedSuspensionTime = 0
CommittedTime = 372
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790959412
LastRemoteHost = slot1_57@glidein_3994679_188702304@a248.anvil.rcac.purdue.edu
LastRemoteWallClockTime = 311.0
LastVacateTime = 1790959058
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
RemoteWallClockTime = 629.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790959412
TransferOutStarted = 1790959412
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 20531; CedarFilesCountTotal = 16; CedarSizeBytesLastRun = 19963; CedarFilesCountLastRun = 15 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:35:06.0 c87997be start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "c87997be", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:35:06.0 c87997be history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "destination"}
11:35:06.0 c87997be restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:35:06.0 c87997be loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60]}
11:36:07.0 c87997be save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:36:07.0 c87997be save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.004, "step": 60, "write_seconds": 0.004}
11:36:07.0 c87997be children_at_exit       {"alive": [], "exitcodes": []}
11:36:07.0 c87997be exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:36:20.8 3347fc60 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "c87997be", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:36:20.8 3347fc60 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "destination"}
11:36:20.8 3347fc60 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958967.0441701, "saved_by_exec": "c87997be", "saved_on_host": "n010.cluster.com", "saved_reason": "voluntary", "step": 60}
11:36:20.8 3347fc60 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60]}
11:37:37.3 3347fc60 signal                 {"first": true, "on_sigterm": "save85", "received_at": 1790959057.2326312, "role": "parent", "signal": "SIGTERM", "step": 136}
11:37:37.9 3347fc60 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "signal", "step": 137}
11:37:37.9 3347fc60 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "signal", "seconds": 0.005, "step": 137, "write_seconds": 0.004}
11:37:37.9 3347fc60 signal_save_finished   {"ok": true, "seconds_since_signal": 0.652}
11:37:37.9 3347fc60 children_at_exit       {"alive": [], "exitcodes": []}
11:37:37.9 3347fc60 exit                   {"code": 85, "reason": "signal SIGTERM, on_sigterm=save85", "step": 137}
11:38:31.5 a7be09e5 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a7be09e5", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:38:31.5 a7be09e5 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "destination"}
11:38:31.5 a7be09e5 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958967.0441701, "saved_by_exec": "c87997be", "saved_on_host": "n010.cluster.com", "saved_reason": "voluntary", "step": 60}
11:38:31.5 a7be09e5 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60]}
11:43:31.0 a7be09e5 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 360}
11:43:31.0 a7be09e5 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.006, "step": 360, "write_seconds": 0.005}
11:43:31.0 a7be09e5 children_at_exit       {"alive": [], "exitcodes": []}
11:43:31.0 a7be09e5 exit                   {"code": 0, "reason": "finished 360 steps", "step": 360}
```

## Trigger log (AP clock)

```
11:13:50.5 {"action": "waiting", "after": 150.0, "log": "/home/<user>/probes/runs/ospool/ospool/P6a-destination-osdf-vacate/job.log", "trigger": "vacate"}
11:37:36.9 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790958906.0, "job": "6588669.0", "last_event": "file_transfer", "trigger": "vacate"}
11:37:36.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6588669.0"], "output": "Job 6588669.0 vacated\n", "rc": 0}
11:37:36.0 {"action": "done"}
```
