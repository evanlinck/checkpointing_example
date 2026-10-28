# P12a-glidein-end-q4 on ospool

**Question.** OSPool glideins are killed at GLIDEIN_ToDie (most stop taking jobs 10 h before). Does a running job get SIGTERM first, and how long before it is killed? Is the kill at ToDie or earlier (the site's batch limit)? Decides whether reading GLIDEIN_ToDie from the machine ad is a useful checkpoint deadline.

Job: `7093517.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/glidein-end/ospool/P12a-glidein-end-q4`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:07, Sys 0 00:00:06  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after ended without an exit record: gap 70 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Execution on a glidein at BEOCAT-SLATE was interrupted with NO signal (hard kill); last sign of life at 19:51:47.8; GLIDEIN_ToDie was -355 s from its last sign of life (negative: died after ToDie); it started 10.5 h before ToDie.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 00e7c93c | 09:17:28.0 | <host-1> | False | 0 | None (None) |  | [(5, 'voluntary', 0.205)] | 85 |
| b654a349 | 09:17:35.4 | <host-1> | True | 0 | 5 (voluntary) |  | [] | none (killed?) |
| 8ac15898 | 19:52:58.0 | <host-2> | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:16:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P12a-glidein-end-q4"; JobBatchName = "probes.dag+7093513" ]
- 09:16:57.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:43407?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#16962802%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 09:17:26.0 `040 file_transfer` Finished transferring input files 
- 09:17:26.0 `021 remote_error` Message from starter on slot1_2@glidein_622935_278937504@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:17:26.0 `001 executing` Job executing on host: <<ip>:36397?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_622935_278937504@<host-1>; CondorScratchDir = "/tmp/glide_oWey9l/execute/dir_60186/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:17:34.0 `040 file_transfer` Started transferring output files 
- 09:17:34.0 `040 file_transfer` Finished transferring output files 
- 19:51:55.0 `004 evicted` Job was evicted. Code 1013 Subcode 0 — (0) CPU times; Usr 0 00:00:07, Sys 0 00:00:06  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050426  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Startd was shutdown; Cpus                 :      0.00        1         1; Disk (KB)            :
- 19:52:52.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:40845?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector4#17062005%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26
- 19:52:55.0 `040 file_transfer` Finished transferring input files 
- 19:52:56.0 `021 remote_error` Message from starter on slot1_2@glidein_4014230_386081688@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 19:52:56.0 `001 executing` Job executing on host: <<ip>:37221?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f — SlotName: slot1_2@glidein_4014230_386081688@<host-2>; CondorScratchDir = "/localscratch/condor/execute/dir_3989114/scratch/glide_f86GVL/execute/dir_1675298/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 19:52:58.0 `040 file_transfer` Started transferring output files 
- 19:52:58.0 `040 file_transfer` Finished transferring output files 
- 19:52:58.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:07, Sys 0 00:00:06  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051393  -  Run Bytes Sent By Job; 287389712 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 8.0
CommittedSuspensionTime = 0
CommittedTime = 14
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793062378
JobCurrentStartTransferOutputDate = 1793062378
LastRemoteHost = slot1_2@glidein_4014230_386081688@<host-2>
LastRemoteWallClockTime = 9.0
LastVacateTime = 1793062311
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
RemoteWallClockTime = 38108.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793062378
TransferOutStarted = 1793062378
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2101819; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051393; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:28.0 00e7c93c start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "BEOCAT-SLATE", "GLIDEIN_ToDie": "1793061953", "GLIDEIN_ToRetire": "1793025953", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_create
09:17:28.0 00e7c93c history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:28.4 00e7c93c restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:28.5 00e7c93c loop_start             {"restored_step": 0, "step": 0, "total_steps": 43200, "voluntary_exit_at": [5]}
09:17:33.7 00e7c93c save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:17:33.9 00e7c93c save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.205, "step": 5, "write_seconds": 0.163}
09:17:33.9 00e7c93c children_at_exit       {"alive": [], "exitcodes": []}
09:17:33.9 00e7c93c exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:17:35.4 b654a349 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "BEOCAT-SLATE", "GLIDEIN_ToDie": "1793061953", "GLIDEIN_ToRetire": "1793025953", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_create
09:17:35.4 b654a349 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:35.4 b654a349 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024253.8011642, "saved_by_exec": "00e7c93c", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
09:17:35.4 b654a349 loop_start             {"restored_step": 5, "step": 5, "total_steps": 43200, "voluntary_exit_at": [5]}
19:52:58.0 8ac15898 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "PSU-LIGO", "GLIDEIN_ToDie": "1793101585", "GLIDEIN_ToRetire": "1793065585", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
19:52:58.0 8ac15898 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
19:52:58.1 8ac15898 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024253.8011642, "saved_by_exec": "00e7c93c", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
19:52:58.1 8ac15898 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```
