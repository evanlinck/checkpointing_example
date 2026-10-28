# P13b-osdf-handoff-exit86 on ospool

**Question.** Same as P13, but the job ends with exit 86 instead of 0 (a planned hand-off: "continue in a new job", since exit 0 should mean training is finished). Does the remapped directory still reach OSDF, and does the job leave the queue normally (return value 86, not a hold or a requeue)?

Job: `7195160.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/handoff/ospool/P13b-osdf-handoff-exit86`

## Observations

- Final job state: terminated ((1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Backup files on OSDF (/staging): state_00000030.json at 09:23:39.5, state_00000060.json at 09:23:36.0, state_00000090.json at 09:23:39.5; probe exits: 85 at 09:22:21.2, 85 at 09:22:55.9, 86 at 09:23:31.1.
- Executions seen by the probe: 3; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 5 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 36a1dd3a | 09:21:51.1 | <host-1> | False | 0 | None (None) |  | [(30, 'voluntary', 0.013)] | 85 |
| 365263aa | 09:22:25.8 | <host-1> | True | 0 | 30 (voluntary) |  | [(60, 'voluntary', 0.015)] | 85 |
| 0f836a40 | 09:23:01.1 | <host-1> | True | 0 | 60 (voluntary) |  | [(90, 'final', 0.014)] | 86 |

## HTCondor event log (AP clock)

- 09:19:22.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P13b-osdf-handoff-exit86"; JobBatchName = "probes.dag+7195158" ]
- 09:20:18.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:43783?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector3#17269118%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 09:21:49.0 `040 file_transfer` Finished transferring input files 
- 09:21:50.0 `021 remote_error` Message from starter on slot1_5@glidein_776313_111480645@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:21:50.0 `001 executing` Job executing on host: <<ip>:34211?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_5@glidein_776313_111480645@<host-1>; CondorScratchDir = "/tmp/jobs/904278/glide_CGqEBI/execute/dir_1762620/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:22:22.0 `040 file_transfer` Started transferring output files 
- 09:22:23.0 `040 file_transfer` Finished transferring output files 
- 09:22:57.0 `040 file_transfer` Started transferring output files 
- 09:22:59.0 `040 file_transfer` Finished transferring output files 
- 09:23:33.0 `040 file_transfer` Started transferring output files 
- 09:23:41.0 `040 file_transfer` Finished transferring output files 
- 09:23:43.0 `005 terminated` Job terminated. — (1) Normal termination (return value 86); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 13422  -  Run Bytes Sent By Job; 286339429  

## condor_history (selected)

```
CheckpointNumber = 1
CommittedSlotTime = 46.0
CommittedSuspensionTime = 0
CommittedTime = 108
ExitBySignal = false
ExitCode = 86
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793111021
JobCurrentStartTransferOutputDate = 1793111013
LastRemoteHost = slot1_5@glidein_776313_111480645@<host-1>
LastRemoteWallClockTime = 213.0
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
RemoteWallClockTime = 213.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt, backup
TransferOutFinished = 1793111021
TransferOutStarted = 1793111013
TransferOutput = ckpt,out,backup
TransferOutputRemaps = backup = osdf:///chtc/staging/<user>/ckpt-probes/p13/7195160.0/backup
TransferOutputStats = [ OSDFSizeBytesTotal = 311; CedarSizeBytesTotal = 13111; OSDFFilesCountTotal = 3; CedarFilesCountTotal = 16; OSDFSizeBytesLastRun = 311; CedarSizeBytesLastRun = 13111; OSDFFilesCountLastRun = 3; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:21:51.1 36a1dd3a start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793311390", "GLIDEIN_ToRetire": "1793275390", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_cr
09:21:51.1 36a1dd3a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:21:51.2 36a1dd3a restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:21:51.2 36a1dd3a loop_start             {"restored_step": 0, "step": 0, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:22:21.2 36a1dd3a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
09:22:21.2 36a1dd3a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.013, "step": 30, "write_seconds": 0.011}
09:22:21.2 36a1dd3a children_at_exit       {"alive": [], "exitcodes": []}
09:22:21.2 36a1dd3a exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
09:22:25.8 365263aa start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793311390", "GLIDEIN_ToRetire": "1793275390", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_cr
09:22:25.8 365263aa history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:22:25.8 365263aa restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1793110941.213063, "saved_by_exec": "36a1dd3a", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 30}
09:22:25.8 365263aa loop_start             {"restored_step": 30, "step": 30, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:22:55.8 365263aa save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:22:55.9 365263aa save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.015, "step": 60, "write_seconds": 0.013}
09:22:55.9 365263aa children_at_exit       {"alive": [], "exitcodes": []}
09:22:55.9 365263aa exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:23:01.1 0f836a40 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793311390", "GLIDEIN_ToRetire": "1793275390", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_cr
09:23:01.1 0f836a40 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:23:01.1 0f836a40 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793110975.848548, "saved_by_exec": "365263aa", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 60}
09:23:01.1 0f836a40 loop_start             {"restored_step": 60, "step": 60, "total_steps": 90, "voluntary_exit_at": [30, 60]}
09:23:31.1 0f836a40 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 90}
09:23:31.1 0f836a40 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.014, "step": 90, "write_seconds": 0.012}
09:23:31.1 0f836a40 children_at_exit       {"alive": [], "exitcodes": []}
09:23:31.1 0f836a40 exit                   {"code": 86, "reason": "finished 90 steps", "step": 90}
```
