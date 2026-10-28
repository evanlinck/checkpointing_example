# P12a-glidein-end-q1 on ospool

**Question.** OSPool glideins are killed at GLIDEIN_ToDie (most stop taking jobs 10 h before). Does a running job get SIGTERM first, and how long before it is killed? Is the kill at ToDie or earlier (the site's batch limit)? Decides whether reading GLIDEIN_ToDie from the machine ad is a useful checkpoint deadline.

Job: `7093514.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/glidein-end/ospool/P12a-glidein-end-q1`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:17, Sys 0 00:00:17  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after ended without an exit record: gap 52 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Execution on a glidein at UChicago was interrupted with NO signal (hard kill); last sign of life at 19:24:23.2; GLIDEIN_ToDie was -323 s from its last sign of life (negative: died after ToDie); it started 10.0 h before ToDie.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 968850aa | 09:17:02.6 | <host-1> | False | 0 | None (None) |  | [(5, 'voluntary', 0.011)] | 85 |
| 62c3b650 | 09:17:09.2 | <host-1> | True | 0 | 5 (voluntary) |  | [] | none (killed?) |
| 4fa3e91b | 19:25:15.6 | <host-2> | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:16:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P12a-glidein-end-q1"; JobBatchName = "probes.dag+7093513" ]
- 09:16:57.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:33645?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#16964091%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618
- 09:17:00.0 `040 file_transfer` Finished transferring input files 
- 09:17:01.0 `021 remote_error` Message from starter on slot1_7@glidein_3810138_142889215@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:17:01.0 `001 executing` Job executing on host: <<ip>:43727?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93 — SlotName: slot1_7@glidein_3810138_142889215@<host-1>; CondorScratchDir = "/var/lib/condor/execute/dir_3810136/glide_zc4t8u/execute/dir_2825880/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:17:07.0 `040 file_transfer` Started transferring output files 
- 09:17:08.0 `040 file_transfer` Finished transferring output files 
- 19:24:25.0 `004 evicted` Job was evicted. Code 1013 Subcode 0 — (0) CPU times; Usr 0 00:00:17, Sys 0 00:00:17  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050521  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Startd was shutdown; Cpus                 :      0.00        1         1; Disk (KB)            :
- 19:24:55.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42743?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#17060912%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 19:25:12.0 `040 file_transfer` Finished transferring input files 
- 19:25:14.0 `021 remote_error` Message from starter on slot1@glidein_3865305_552968910@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 19:25:14.0 `001 executing` Job executing on host: <<ip>:42281?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1@glidein_3865305_552968910@<host-2>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3865262/scratch/glide_afNrTn/execute/dir_1859456/scratch"; Cpus = 1; Disk = 10010267; GPUs = 0; Memory = 2500
- 19:25:15.0 `040 file_transfer` Started transferring output files 
- 19:25:15.0 `040 file_transfer` Finished transferring output files 
- 19:25:16.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:17, Sys 0 00:00:17  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051478  -  Run Bytes Sent By Job; 287389807 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 22.0
CommittedSuspensionTime = 0
CommittedTime = 27
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793060715
JobCurrentStartTransferOutputDate = 1793060715
LastRemoteHost = slot1@glidein_3865305_552968910@<host-2>
LastRemoteWallClockTime = 22.0
LastVacateTime = 1793060665
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
RemoteWallClockTime = 36471.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793060715
TransferOutStarted = 1793060715
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2101999; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051478; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:02.6 968850aa start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "86400", "GLIDEIN_Site": "UChicago", "GLIDEIN_ToDie": "1793060340", "GLIDEIN_ToRetire": "1793024340", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
09:17:02.6 968850aa history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:02.6 968850aa restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:02.6 968850aa loop_start             {"restored_step": 0, "step": 0, "total_steps": 43200, "voluntary_exit_at": [5]}
09:17:07.6 968850aa save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:17:07.6 968850aa save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.011, "step": 5, "write_seconds": 0.01}
09:17:07.7 968850aa children_at_exit       {"alive": [], "exitcodes": []}
09:17:07.7 968850aa exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:17:09.2 62c3b650 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "86400", "GLIDEIN_Site": "UChicago", "GLIDEIN_ToDie": "1793060340", "GLIDEIN_ToRetire": "1793024340", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by
09:17:09.2 62c3b650 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:09.2 62c3b650 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024227.6475573, "saved_by_exec": "968850aa", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
09:17:09.2 62c3b650 loop_start             {"restored_step": 5, "step": 5, "total_steps": 43200, "voluntary_exit_at": [5]}
19:25:15.6 4fa3e91b start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "82800", "GLIDEIN_Site": "CHTC", "GLIDEIN_ToDie": "1793098611", "GLIDEIN_ToRetire": "1793062611", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "
19:25:15.6 4fa3e91b history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
19:25:15.6 4fa3e91b restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024227.6475573, "saved_by_exec": "968850aa", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
19:25:15.6 4fa3e91b exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```
