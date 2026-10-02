# P5c-spool-100mb on ospool

**Question.** How long is the gap between exit 85 and the restart when the checkpoint is 100 MB (transfer to the AP's spool)?

Job: `6589425.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P5c-spool-100mb`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 70f61ee8 | 11:57:36.3 | scigrid5.physics.fsu.edu | False | 0 | None (None) |  | [(30, 'voluntary', 1.03)] | 85 |
| 5bf81805 | 11:58:11.1 | scigrid5.physics.fsu.edu | True | 0 | 30 (voluntary) |  | [(60, 'final', 1.789)] | 0 |

## HTCondor event log (AP clock)

- 11:56:06.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P5c-spool-100mb"; JobBatchName = "probes.dag+6586482" ]
- 11:56:51.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37819?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector3#14596495%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 11:57:33.0 `040 file_transfer` Finished transferring input files 
- 11:57:34.0 `021 remote_error` Message from starter on slot1_4@glidein_1804341_240472785@scigrid5.physics.fsu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:57:34.0 `001 executing` Job executing on host: <<ip>:36013?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_4@glidein_1804341_240472785@scigrid5.physics.fsu.edu; CondorScratchDir = "/scratch/glide_n67Nk2/execute/dir_1987184/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:58:07.0 `040 file_transfer` Started transferring output files 
- 11:58:09.0 `040 file_transfer` Finished transferring output files 
- 11:58:44.0 `040 file_transfer` Started transferring output files 
- 11:58:44.0 `040 file_transfer` Finished transferring output files 
- 11:58:44.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 15074  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 37.0
CommittedSuspensionTime = 0
CommittedTime = 69
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790960324
JobCurrentStartTransferOutputDate = 1790960324
LastRemoteHost = slot1_4@glidein_1804341_240472785@scigrid5.physics.fsu.edu
LastRemoteWallClockTime = 115.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 115.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790960324
TransferOutStarted = 1790960324
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 15074; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 15074; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:57:36.3 70f61ee8 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "70f61ee8", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:57:36.3 70f61ee8 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:57:36.3 70f61ee8 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:57:36.3 70f61ee8 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:58:06.5 70f61ee8 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "voluntary", "step": 30}
11:58:07.5 70f61ee8 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 1.03, "step": 30, "write_seconds": 0.989}
11:58:07.5 70f61ee8 children_at_exit       {"alive": [], "exitcodes": []}
11:58:07.6 70f61ee8 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:58:11.1 5bf81805 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "70f61ee8", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:58:11.1 5bf81805 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:58:11.1 5bf81805 restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790960287.4665785, "saved_by_exec": "70f61ee8", "saved_on_host": "scigrid5.physics.fsu.edu", "saved_reason": "voluntary", "step": 30}
11:58:11.2 5bf81805 loop_start             {"restored_step": 30, "step": 30, "total_steps": 60, "voluntary_exit_at": [30]}
11:58:41.4 5bf81805 save_start             {"ckpt_files": 1, "ckpt_mb": 100, "reason": "final", "step": 60}
11:58:43.2 5bf81805 save_done              {"bytes": 104857600, "dir_fsync_ok": true, "reason": "final", "seconds": 1.789, "step": 60, "write_seconds": 1.275}
11:58:43.6 5bf81805 children_at_exit       {"alive": [], "exitcodes": []}
11:58:43.7 5bf81805 exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
