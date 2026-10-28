# P12a-glidein-end-q5 on ospool

**Question.** OSPool glideins are killed at GLIDEIN_ToDie (most stop taking jobs 10 h before). Does a running job get SIGTERM first, and how long before it is killed? Is the kill at ToDie or earlier (the site's batch limit)? Decides whether reading GLIDEIN_ToDie from the machine ad is a useful checkpoint deadline.

Job: `7093518.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/glidein-end/ospool/P12a-glidein-end-q5`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:14, Sys 0 00:00:15  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after ended without an exit record: gap 34 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Execution on a glidein at UChicago was interrupted with NO signal (hard kill); last sign of life at 19:46:57.5; GLIDEIN_ToDie was -104 s from its last sign of life (negative: died after ToDie); it started 10.4 h before ToDie.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| a2eb2e71 | 09:18:08.2 | <host-1> | False | 0 | None (None) |  | [(5, 'voluntary', 0.008)] | 85 |
| fb25b4a7 | 09:18:14.8 | <host-1> | True | 0 | 5 (voluntary) |  | [] | none (killed?) |
| 3a00cc56 | 19:47:31.2 | <host-2> | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:16:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P12a-glidein-end-q5"; JobBatchName = "probes.dag+7093513" ]
- 09:17:54.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:38733?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector6#16960531%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618
- 09:18:06.0 `040 file_transfer` Finished transferring input files 
- 09:18:06.0 `021 remote_error` Message from starter on slot1_5@glidein_2083105_42595542@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:18:06.0 `001 executing` Job executing on host: <<ip>:40865?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93 — SlotName: slot1_5@glidein_2083105_42595542@<host-1>; CondorScratchDir = "/scratch.local/condor/execute/dir_2083103/glide_AILS7U/execute/dir_972417/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:18:13.0 `040 file_transfer` Started transferring output files 
- 09:18:13.0 `040 file_transfer` Finished transferring output files 
- 19:46:59.0 `004 evicted` Job was evicted. Code 1013 Subcode 0 — (0) CPU times; Usr 0 00:00:14, Sys 0 00:00:15  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050686  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Startd was shutdown; Cpus                 :      0.00        1         1; Disk (KB)            :
- 19:47:26.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:41227?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector10#17059836%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 19:47:29.0 `040 file_transfer` Finished transferring input files 
- 19:47:29.0 `021 remote_error` Message from starter on slot1_4@glidein_1766463_227358495@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 19:47:30.0 `001 executing` Job executing on host: <<ip>:42421?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_4@glidein_1766463_227358495@<host-2>; CondorScratchDir = "/localscratch/condor/execute/dir_1765939/scratch/glide_n0Jnww/execute/dir_3102422/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 19:47:31.0 `040 file_transfer` Started transferring output files 
- 19:47:31.0 `040 file_transfer` Finished transferring output files 
- 19:47:32.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:14, Sys 0 00:00:15  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051681  -  Run Bytes Sent By Job; 287389972 

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
JobCurrentFinishTransferOutputDate = 1793062051
JobCurrentStartTransferOutputDate = 1793062051
LastRemoteHost = slot1_4@glidein_1766463_227358495@<host-2>
LastRemoteWallClockTime = 7.0
LastVacateTime = 1793062019
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
RemoteWallClockTime = 37753.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793062051
TransferOutStarted = 1793062051
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102367; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051681; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:18:08.2 a2eb2e71 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "86400", "GLIDEIN_Site": "UChicago", "GLIDEIN_ToDie": "1793061913", "GLIDEIN_ToRetire": "1793025913", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
09:18:08.2 a2eb2e71 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:18:08.2 a2eb2e71 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:18:08.2 a2eb2e71 loop_start             {"restored_step": 0, "step": 0, "total_steps": 43200, "voluntary_exit_at": [5]}
09:18:13.2 a2eb2e71 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:18:13.2 a2eb2e71 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.008, "step": 5, "write_seconds": 0.007}
09:18:13.2 a2eb2e71 children_at_exit       {"alive": [], "exitcodes": []}
09:18:13.2 a2eb2e71 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:18:14.8 fb25b4a7 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "86400", "GLIDEIN_Site": "UChicago", "GLIDEIN_ToDie": "1793061913", "GLIDEIN_ToRetire": "1793025913", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by
09:18:14.8 fb25b4a7 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:18:14.8 fb25b4a7 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024293.1734586, "saved_by_exec": "a2eb2e71", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "st
09:18:14.8 fb25b4a7 loop_start             {"restored_step": 5, "step": 5, "total_steps": 43200, "voluntary_exit_at": [5]}
19:47:31.2 3a00cc56 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "PSU-LIGO", "GLIDEIN_ToDie": "1793100991", "GLIDEIN_ToRetire": "1793064991", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
19:47:31.2 3a00cc56 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
19:47:31.2 3a00cc56 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024293.1734586, "saved_by_exec": "a2eb2e71", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "st
19:47:31.2 3a00cc56 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```
