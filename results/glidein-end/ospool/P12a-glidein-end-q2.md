# P12a-glidein-end-q2 on ospool

**Question.** OSPool glideins are killed at GLIDEIN_ToDie (most stop taking jobs 10 h before). Does a running job get SIGTERM first, and how long before it is killed? Is the kill at ToDie or earlier (the site's batch limit)? Decides whether reading GLIDEIN_ToDie from the machine ad is a useful checkpoint deadline.

Job: `7093515.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/glidein-end/ospool/P12a-glidein-end-q2`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:10, Sys 0 00:00:08  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after ended without an exit record: gap 56 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Execution on a glidein at FANDM-ITS was interrupted with NO signal (hard kill); last sign of life at 19:30:42.6; GLIDEIN_ToDie was -158 s from its last sign of life (negative: died after ToDie); it started 10.2 h before ToDie.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| eece8043 | 09:18:03.0 | <host-1> | False | 0 | None (None) |  | [(5, 'voluntary', 0.005)] | 85 |
| 5d57d3e1 | 09:18:09.8 | <host-1> | True | 0 | 5 (voluntary) |  | [] | none (killed?) |
| bd0b9d2d | 19:31:38.4 | <host-2> | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:16:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P12a-glidein-end-q2"; JobBatchName = "probes.dag+7093513" ]
- 09:17:54.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:40451?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector4#16957636%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26alia
- 09:18:01.0 `040 file_transfer` Finished transferring input files 
- 09:18:01.0 `021 remote_error` Message from starter on slot1_5@glidein_4061313_22447348@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:18:02.0 `001 executing` Job executing on host: <<ip>:41381?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59-6 — SlotName: slot1_5@glidein_4061313_22447348@<host-1>; CondorScratchDir = "/scratch/glide_AndagA/execute/dir_1458070/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:18:08.0 `040 file_transfer` Started transferring output files 
- 09:18:08.0 `040 file_transfer` Finished transferring output files 
- 19:30:44.0 `004 evicted` Job was evicted. Code 1013 Subcode 0 — (0) CPU times; Usr 0 00:00:10, Sys 0 00:00:08  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050461  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Startd was shutdown; Cpus                 :      0.00        1         1; Disk (KB)            :
- 19:31:33.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42643?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#17062910%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618
- 19:31:36.0 `040 file_transfer` Finished transferring input files 
- 19:31:37.0 `021 remote_error` Message from starter on slot1_3@glidein_1762601_75991130@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 19:31:37.0 `001 executing` Job executing on host: <<ip>:45147?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93 — SlotName: slot1_3@glidein_1762601_75991130@<host-2>; CondorScratchDir = "/var/lib/condor/execute/dir_1762599/glide_Wiwkjp/execute/dir_662934/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 19:31:38.0 `040 file_transfer` Started transferring output files 
- 19:31:38.0 `040 file_transfer` Finished transferring output files 
- 19:31:39.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:10, Sys 0 00:00:08  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051449  -  Run Bytes Sent By Job; 287389747 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 7.0
CommittedSuspensionTime = 0
CommittedTime = 12
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793061098
JobCurrentStartTransferOutputDate = 1793061098
LastRemoteHost = slot1_3@glidein_1762601_75991130@<host-2>
LastRemoteWallClockTime = 7.0
LastVacateTime = 1793061043
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
NumVacatesByReason = [ StartdShutdown = 1 ]
RemoteWallClockTime = 36778.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793061098
TransferOutStarted = 1793061098
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2101910; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051449; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:18:03.0 eece8043 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "FANDM-ITS", "GLIDEIN_ToDie": "1793060885", "GLIDEIN_ToRetire": "1793024885", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_
09:18:03.0 eece8043 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:18:03.0 eece8043 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:18:03.0 eece8043 loop_start             {"restored_step": 0, "step": 0, "total_steps": 43200, "voluntary_exit_at": [5]}
09:18:08.0 eece8043 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:18:08.0 eece8043 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.005, "step": 5, "write_seconds": 0.002}
09:18:08.0 eece8043 children_at_exit       {"alive": [], "exitcodes": []}
09:18:08.0 eece8043 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:18:09.8 5d57d3e1 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "FANDM-ITS", "GLIDEIN_ToDie": "1793060885", "GLIDEIN_ToRetire": "1793024885", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_
09:18:09.8 5d57d3e1 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:18:09.8 5d57d3e1 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024288.0147169, "saved_by_exec": "eece8043", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
09:18:09.8 5d57d3e1 loop_start             {"restored_step": 5, "step": 5, "total_steps": 43200, "voluntary_exit_at": [5]}
19:31:38.4 bd0b9d2d start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "86400", "GLIDEIN_Site": "UChicago", "GLIDEIN_ToDie": "1793098858", "GLIDEIN_ToRetire": "1793062858", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
19:31:38.4 bd0b9d2d history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
19:31:38.4 bd0b9d2d restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024288.0147169, "saved_by_exec": "eece8043", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
19:31:38.4 bd0b9d2d exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```
