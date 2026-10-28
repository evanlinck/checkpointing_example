# P13-osdf-backup on chtc

**Question.** A directory listed in transfer_checkpoint_files and remapped to osdf:// with transfer_output_remaps: does HTCondor upload it at every exit 85 (a backup that outlives the job, OSPool's advised path for large outputs), only at the end, or not at all? Does the job still resume normally?

Job: `7093577.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P13-osdf-backup`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage;)
- Backup files on OSDF (/staging): state_00000030.json at 09:38:00.6, state_00000060.json at 09:38:00.6, state_00000090.json at 09:38:00.6; probe exits: 85 at 09:36:53.9, 85 at 09:37:25.8, 0 at 09:37:57.5.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 662a31de | 09:36:23.8 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 0.01)] | 85 |
| 53cbd413 | 09:36:55.5 | <host-1> | True | 0 | 30 (voluntary) |  | [(60, 'voluntary', 0.235)] | 85 |
| 923917df | 09:37:27.3 | <host-1> | True | 0 | 60 (voluntary) |  | [(90, 'final', 0.086)] | 0 |

## HTCondor event log (AP clock)

- 09:35:43.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P13-osdf-backup"; JobBatchName = "probes.dag+7093501" ]
- 09:36:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_41_622756_b065_96479>
- 09:36:22.0 `040 file_transfer` Finished transferring input files 
- 09:36:22.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_41@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3396581/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:36:54.0 `040 file_transfer` Started transferring output files 
- 09:36:54.0 `040 file_transfer` Finished transferring output files 
- 09:37:25.0 `040 file_transfer` Started transferring output files 
- 09:37:25.0 `040 file_transfer` Finished transferring output files 
- 09:37:58.0 `040 file_transfer` Started transferring output files 
- 09:38:02.0 `040 file_transfer` Finished transferring output files 
- 09:38:03.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:02  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 13276  -  Run Bytes Sent By Job; 286339254  -

## condor_history (selected)

```
CheckpointNumber = 1
CommittedSlotTime = 38.0
CommittedSuspensionTime = 0
CommittedTime = 99
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793025482
JobCurrentStartTransferOutputDate = 1793025477
LastRemoteHost = slot1_41@<host-1>
LastRemoteWallClockTime = 112.0
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
RemoteWallClockTime = 112.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt, backup
TransferOutFinished = 1793025482
TransferOutStarted = 1793025478
TransferOutput = ckpt,out,backup
TransferOutputRemaps = backup = osdf:///chtc/staging/<user>/ckpt-probes/p13/7093577.0/backup
TransferOutputStats = [ OSDFSizeBytesTotal = 307; CedarSizeBytesTotal = 12969; OSDFFilesCountTotal = 3; CedarFilesCountTotal = 16; OSDFSizeBytesLastRun = 307; CedarSizeBytesLastRun = 12969; OSDFFilesCountLastRun = 3; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:36:23.8 662a31de start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3396581/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "662a31de", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:36:23.8 662a31de history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "store": "spool"}
09:36:23.8 662a31de restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:36:23.8 662a31de loop_start             {"restored_step": 0, "step": 0, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:36:53.9 662a31de save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
09:36:53.9 662a31de save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.01, "step": 30, "write_seconds": 0.008}
09:36:53.9 662a31de children_at_exit       {"alive": [], "exitcodes": []}
09:36:53.9 662a31de exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:36:55.5 53cbd413 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3396581/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "662a31de", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:36:55.5 53cbd413 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "store": "spool"}
09:36:55.5 53cbd413 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793025413.933848, "saved_by_exec": "662a31de", "saved_on_host": "<host-1>", "saved_reason": "voluntary"
09:36:55.5 53cbd413 loop_start             {"restored_step": 30, "step": 30, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:37:25.6 53cbd413 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:37:25.8 53cbd413 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.235, "step": 60, "write_seconds": 0.218}
09:37:25.8 53cbd413 children_at_exit       {"alive": [], "exitcodes": []}
09:37:25.8 53cbd413 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:37:27.3 923917df start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3396581/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "662a31de", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:37:27.3 923917df history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "store": "spool"}
09:37:27.3 923917df restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3396581/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793025445.8009303, "saved_by_exec": "53cbd413", "saved_on_host": "<host-1>", "saved_reason": "voluntary
09:37:27.3 923917df loop_start             {"restored_step": 60, "step": 60, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:37:57.4 923917df save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 90}
09:37:57.5 923917df save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.086, "step": 90, "write_seconds": 0.055}
09:37:57.5 923917df children_at_exit       {"alive": [], "exitcodes": []}
09:37:57.5 923917df exit                   {"code": 0, "reason": "finished 90 steps", "step": 90}
```
