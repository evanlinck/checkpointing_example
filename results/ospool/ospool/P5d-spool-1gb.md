# P5d-spool-1gb on ospool

**Question.** How long is the gap between exit 85 and the restart when the checkpoint is 1000 MB (transfer to the AP's spool)?

Job: `6589422.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P5d-spool-1gb`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 7 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 23935cb5 | 11:53:55.8 | wizard26 | False | 0 | None (None) |  | [(30, 'voluntary', 13.15)] | 85 |
| d329a27a | 11:54:45.0 | wizard26 | True | 0 | 30 (voluntary) |  | [(60, 'final', 6.063)] | 0 |

## HTCondor event log (AP clock)

- 11:51:36.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P5d-spool-1gb"; JobBatchName = "probes.dag+6586482" ]
- 11:53:13.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:33291?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector4#14594989%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:53:53.0 `040 file_transfer` Finished transferring input files 
- 11:53:54.0 `021 remote_error` Message from starter on slot1_2@glidein_938111_11644727@wizard26.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:53:54.0 `001 executing` Job executing on host: <<ip>:46453?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_938111_11644727@wizard26.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_pBgXzP/execute/dir_3294382/scratch"; Cpus = 1; Disk = 4194304; GPUs = 0; Memory = 1024
- 11:54:39.0 `040 file_transfer` Started transferring output files 
- 11:54:44.0 `040 file_transfer` Finished transferring output files 
- 11:55:22.0 `040 file_transfer` Started transferring output files 
- 11:55:22.0 `040 file_transfer` Finished transferring output files 
- 11:55:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 13937  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 43.0
CommittedSuspensionTime = 0
CommittedTime = 87
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790960122
JobCurrentStartTransferOutputDate = 1790960122
LastRemoteHost = slot1_2@glidein_938111_11644727@wizard26.beocat.ksu.edu
LastRemoteWallClockTime = 131.0
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
RemoteWallClockTime = 131.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790960122
TransferOutStarted = 1790960122
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 13937; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 13937; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:53:55.8 23935cb5 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "23935cb5", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:53:55.8 23935cb5 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:53:55.9 23935cb5 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:53:55.9 23935cb5 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:54:26.0 23935cb5 save_start             {"ckpt_files": 1, "ckpt_mb": 1000, "reason": "voluntary", "step": 30}
11:54:39.2 23935cb5 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 13.15, "step": 30, "write_seconds": 13.083}
11:54:39.2 23935cb5 children_at_exit       {"alive": [], "exitcodes": []}
11:54:39.2 23935cb5 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:54:45.0 d329a27a start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "23935cb5", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:54:45.0 d329a27a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:54:45.0 d329a27a restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790960079.04091, "saved_by_exec": "23935cb5", "saved_on_host": "wizard26", "saved_reason": "voluntary", "step": 30}
11:54:45.0 d329a27a loop_start             {"restored_step": 30, "step": 30, "total_steps": 60, "voluntary_exit_at": [30]}
11:55:16.1 d329a27a save_start             {"ckpt_files": 1, "ckpt_mb": 1000, "reason": "final", "step": 60}
11:55:22.2 d329a27a save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "final", "seconds": 6.063, "step": 60, "write_seconds": 5.911}
11:55:22.3 d329a27a children_at_exit       {"alive": [], "exitcodes": []}
11:55:22.4 d329a27a exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
