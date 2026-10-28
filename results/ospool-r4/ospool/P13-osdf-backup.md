# P13-osdf-backup on ospool

**Question.** A directory listed in transfer_checkpoint_files and remapped to osdf:// with transfer_output_remaps: does HTCondor upload it at every exit 85 (a backup that outlives the job, OSPool's advised path for large outputs), only at the end, or not at all? Does the job still resume normally?

Job: `7093561.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/ospool/P13-osdf-backup`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Backup files on OSDF (/staging): state_00000030.json at 09:25:36.7, state_00000060.json at 09:25:36.7, state_00000090.json at 09:25:36.7; probe exits: 85 at 09:24:22.3, 85 at 09:24:57.8, 0 at 09:25:33.5.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 7604077a | 09:23:50.0 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 1.377)] | 85 |
| a7a2f788 | 09:24:24.2 | <host-1> | True | 0 | 30 (voluntary) |  | [(60, 'voluntary', 1.674)] | 85 |
| 67a199e7 | 09:25:00.7 | <host-1> | True | 0 | 60 (voluntary) |  | [(90, 'final', 1.235)] | 0 |

## HTCondor event log (AP clock)

- 09:22:32.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P13-osdf-backup"; JobBatchName = "probes.dag+7093501" ]
- 09:23:42.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:37437?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#16960899%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 09:23:46.0 `040 file_transfer` Finished transferring input files 
- 09:23:47.0 `021 remote_error` Message from starter on slot1_4@glidein_2763275_692068300@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:23:47.0 `001 executing` Job executing on host: <<ip>:40993?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f — SlotName: slot1_4@glidein_2763275_692068300@<host-1>; CondorScratchDir = "/tmp/glide_BLwKX1/execute/dir_3942509/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:24:22.0 `040 file_transfer` Started transferring output files 
- 09:24:22.0 `040 file_transfer` Finished transferring output files 
- 09:24:58.0 `040 file_transfer` Started transferring output files 
- 09:24:58.0 `040 file_transfer` Finished transferring output files 
- 09:25:34.0 `040 file_transfer` Started transferring output files 
- 09:25:38.0 `040 file_transfer` Finished transferring output files 
- 09:25:39.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 14567  -  Run Bytes Sent By Job; 286339254  -

## condor_history (selected)

```
CheckpointNumber = 1
CommittedSlotTime = 41.0
CommittedSuspensionTime = 0
CommittedTime = 108
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024738
JobCurrentStartTransferOutputDate = 1793024733
LastRemoteHost = slot1_4@glidein_2763275_692068300@<host-1>
LastRemoteWallClockTime = 118.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 118.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt, backup
TransferOutFinished = 1793024738
TransferOutStarted = 1793024734
TransferOutput = ckpt,out,backup
TransferOutputRemaps = backup = osdf:///chtc/staging/<user>/ckpt-probes/p13/7093561.0/backup
TransferOutputStats = [ OSDFSizeBytesTotal = 388; CedarSizeBytesTotal = 14179; OSDFFilesCountTotal = 3; CedarFilesCountTotal = 16; OSDFSizeBytesLastRun = 388; CedarSizeBytesLastRun = 14179; OSDFFilesCountLastRun = 3; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:23:50.0 7604077a start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "UWM-Mortimer", "GLIDEIN_ToDie": "1793260198", "GLIDEIN_ToRetire": "1793224198", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_creat
09:23:50.0 7604077a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:23:50.5 7604077a restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:23:50.5 7604077a loop_start             {"restored_step": 0, "step": 0, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:24:20.9 7604077a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
09:24:22.3 7604077a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 1.377, "step": 30, "write_seconds": 1.335}
09:24:22.3 7604077a children_at_exit       {"alive": [], "exitcodes": []}
09:24:22.3 7604077a exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:24:24.2 a7a2f788 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "UWM-Mortimer", "GLIDEIN_ToDie": "1793260198", "GLIDEIN_ToRetire": "1793224198", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_creat
09:24:24.2 a7a2f788 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:24:24.2 a7a2f788 restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793024662.2121415, "saved_by_exec": "7604077a", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step":
09:24:24.2 a7a2f788 loop_start             {"restored_step": 30, "step": 30, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:24:55.0 a7a2f788 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:24:56.7 a7a2f788 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 1.674, "step": 60, "write_seconds": 1.09}
09:24:57.7 a7a2f788 children_at_exit       {"alive": [], "exitcodes": []}
09:24:57.8 a7a2f788 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:25:00.7 67a199e7 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "UWM-Mortimer", "GLIDEIN_ToDie": "1793260198", "GLIDEIN_ToRetire": "1793224198", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_creat
09:25:00.7 67a199e7 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:25:01.3 67a199e7 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793024695.3438451, "saved_by_exec": "a7a2f788", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step":
09:25:01.6 67a199e7 loop_start             {"restored_step": 60, "step": 60, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:25:32.0 67a199e7 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 90}
09:25:33.3 67a199e7 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 1.235, "step": 90, "write_seconds": 0.415}
09:25:33.4 67a199e7 children_at_exit       {"alive": [], "exitcodes": []}
09:25:33.5 67a199e7 exit                   {"code": 0, "reason": "finished 90 steps", "step": 90}
```
