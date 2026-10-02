# P8d-empty-ckpt-dir on ospool

**Question.** What happens when the job exits 85 and the checkpoint directory exists but is empty? (The probe stops after 3 such exits in one sandbox.)

Job: `6587960.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P8d-empty-ckpt-dir`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 97ead266 | 11:28:02.1 | dwarf33 | False | 0 | None (None) |  | [] | 85 |
| 5db6f69e | 11:28:34.3 | dwarf33 | True | 0 | None (None) |  | [] | 85 |
| 8c9dee10 | 11:29:06.1 | dwarf33 | True | 0 | None (None) |  | [] | 85 |
| 5578d54a | 11:29:38.3 | dwarf33 | True | 0 | None (None) |  | [(60, 'final', 0.118)] | 0 |

## HTCondor event log (AP clock)

- 11:27:14.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P8d-empty-ckpt-dir"; JobBatchName = "probes.dag+6586482" ]
- 11:27:21.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:33989?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector4#14594246%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:28:00.0 `040 file_transfer` Finished transferring input files 
- 11:28:00.0 `021 remote_error` Message from starter on slot1_1@glidein_3478735_241008756@dwarf33.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:28:00.0 `001 executing` Job executing on host: <<ip>:39599?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_1@glidein_3478735_241008756@dwarf33.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_QV501P/execute/dir_1294066/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:28:32.0 `040 file_transfer` Started transferring output files 
- 11:28:32.0 `040 file_transfer` Finished transferring output files 
- 11:29:04.0 `040 file_transfer` Started transferring output files 
- 11:29:04.0 `040 file_transfer` Finished transferring output files 
- 11:29:36.0 `040 file_transfer` Started transferring output files 
- 11:29:36.0 `040 file_transfer` Finished transferring output files 
- 11:30:38.0 `040 file_transfer` Started transferring output files 
- 11:30:39.0 `040 file_transfer` Finished transferring output files 
- 11:30:39.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 26560  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 2
CommittedSlotTime = 63.0
CommittedSuspensionTime = 0
CommittedTime = 156
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958639
JobCurrentStartTransferOutputDate = 1790958638
LastRemoteHost = slot1_1@glidein_3478735_241008756@dwarf33.beocat.ksu.edu
LastRemoteWallClockTime = 198.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 4
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 198.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958639
TransferOutStarted = 1790958638
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 26560; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 26560; CedarFilesCountLastRun = 12 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:28:02.1 97ead266 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "97ead266", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:28:02.1 97ead266 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:28:02.1 97ead266 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:28:02.2 97ead266 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:28:32.7 97ead266 emptied_checkpoint_dir {"step": 30}
11:28:32.7 97ead266 children_at_exit       {"alive": [], "exitcodes": []}
11:28:32.7 97ead266 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:28:34.3 5db6f69e start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "97ead266", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:28:34.3 5db6f69e history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:28:34.3 5db6f69e restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:28:34.3 5db6f69e loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:29:04.4 5db6f69e emptied_checkpoint_dir {"step": 30}
11:29:04.5 5db6f69e children_at_exit       {"alive": [], "exitcodes": []}
11:29:04.5 5db6f69e exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:29:06.1 8c9dee10 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "97ead266", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:29:06.1 8c9dee10 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:29:06.1 8c9dee10 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:29:06.1 8c9dee10 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:29:36.2 8c9dee10 emptied_checkpoint_dir {"step": 30}
11:29:36.3 8c9dee10 children_at_exit       {"alive": [], "exitcodes": []}
11:29:36.3 8c9dee10 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:29:38.3 5578d54a start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "97ead266", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:29:38.3 5578d54a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:29:38.3 5578d54a restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:29:38.4 5578d54a loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:30:08.5 5578d54a voluntary_exit_skipped {"reason": "max_voluntary_exits reached in this sandbox", "step": 30}
11:30:38.6 5578d54a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 60}
11:30:38.8 5578d54a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.118, "step": 60, "write_seconds": 0.093}
11:30:38.8 5578d54a children_at_exit       {"alive": [], "exitcodes": []}
11:30:38.8 5578d54a exit                   {"code": 0, "reason": "finished 60 steps", "step": 60}
```
