# P13b-osdf-handoff-exit86 on chtc

**Question.** Same as P13, but the job ends with exit 86 instead of 0 (a planned hand-off: "continue in a new job", since exit 0 should mean training is finished). Does the remapped directory still reach OSDF, and does the job leave the queue normally (return value 86, not a hold or a requeue)?

Job: `7195159.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/handoff/chtc/P13b-osdf-handoff-exit86`

## Observations

- Final job state: terminated ((1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Backup files on OSDF (/staging): state_00000030.json at 09:22:06.1, state_00000060.json at 09:22:06.1, state_00000090.json at 09:22:06.1; probe exits: 85 at 09:20:56.7, 85 at 09:21:28.9, 86 at 09:22:00.0.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| eca8fc08 | 09:20:26.5 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 0.03)] | 85 |
| 897aff96 | 09:20:58.7 | <host-1> | True | 0 | 30 (voluntary) |  | [(60, 'voluntary', 0.011)] | 85 |
| 2ec194df | 09:21:30.8 | <host-1> | True | 0 | 60 (voluntary) |  | [(90, 'final', 0.013)] | 86 |

## HTCondor event log (AP clock)

- 09:19:22.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P13b-osdf-handoff-exit86"; JobBatchName = "probes.dag+7195158" ]
- 09:19:55.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_4_2025754_b382_85260>
- 09:20:24.0 `040 file_transfer` Finished transferring input files 
- 09:20:24.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_4@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2626705/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:20:56.0 `040 file_transfer` Started transferring output files 
- 09:20:56.0 `040 file_transfer` Finished transferring output files 
- 09:21:29.0 `040 file_transfer` Started transferring output files 
- 09:21:29.0 `040 file_transfer` Finished transferring output files 
- 09:22:03.0 `040 file_transfer` Started transferring output files 
- 09:22:08.0 `040 file_transfer` Finished transferring output files 
- 09:22:09.0 `005 terminated` Job terminated. — (1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 13728  -  Run Bytes Sent By Job; 286339429  

## condor_history (selected)

```
CheckpointNumber = 1
CommittedSlotTime = 40.0
CommittedSuspensionTime = 0
CommittedTime = 102
ExitBySignal = false
ExitCode = 86
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793110928
JobCurrentStartTransferOutputDate = 1793110921
LastRemoteHost = slot1_4@<host-1>
LastRemoteWallClockTime = 134.0
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
RemoteWallClockTime = 134.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt, backup
TransferOutFinished = 1793110928
TransferOutStarted = 1793110923
TransferOutput = ckpt,out,backup
TransferOutputRemaps = backup = osdf:///chtc/staging/<user>/ckpt-probes/p13/7195159.0/backup
TransferOutputStats = [ OSDFSizeBytesTotal = 305; CedarSizeBytesTotal = 13423; OSDFFilesCountTotal = 3; CedarFilesCountTotal = 16; OSDFSizeBytesLastRun = 305; CedarSizeBytesLastRun = 13423; OSDFFilesCountLastRun = 3; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:20:26.5 eca8fc08 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2626705/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "eca8fc08", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:20:26.5 eca8fc08 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "store": "spool"}
09:20:26.5 eca8fc08 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:20:26.5 eca8fc08 loop_start             {"restored_step": 0, "step": 0, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:20:56.7 eca8fc08 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
09:20:56.7 eca8fc08 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.03, "step": 30, "write_seconds": 0.022}
09:20:56.7 eca8fc08 children_at_exit       {"alive": [], "exitcodes": []}
09:20:56.7 eca8fc08 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:20:58.7 897aff96 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2626705/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "eca8fc08", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:20:58.7 897aff96 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "store": "spool"}
09:20:58.7 897aff96 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793110856.724551, "saved_by_exec": "eca8fc08", "saved_on_host": "<host-1>", "saved_reason": "voluntary"
09:20:58.7 897aff96 loop_start             {"restored_step": 30, "step": 30, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:21:28.9 897aff96 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:21:28.9 897aff96 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.011, "step": 60, "write_seconds": 0.009}
09:21:28.9 897aff96 children_at_exit       {"alive": [], "exitcodes": []}
09:21:28.9 897aff96 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:21:30.8 2ec194df start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2626705/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "eca8fc08", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/s
09:21:30.8 2ec194df history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "store": "spool"}
09:21:30.8 2ec194df restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_2626705/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793110888.89773, "saved_by_exec": "897aff96", "saved_on_host": "<host-1>", "saved_reason": "voluntary",
09:21:30.8 2ec194df loop_start             {"restored_step": 60, "step": 60, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:22:00.9 2ec194df save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 90}
09:22:00.0 2ec194df save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.013, "step": 90, "write_seconds": 0.01}
09:22:00.0 2ec194df children_at_exit       {"alive": [], "exitcodes": []}
09:22:00.0 2ec194df exit                   {"code": 86, "reason": "finished 90 steps", "step": 90}
```
