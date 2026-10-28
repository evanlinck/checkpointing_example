# P12a-glidein-end-q3 on ospool

**Question.** OSPool glideins are killed at GLIDEIN_ToDie (most stop taking jobs 10 h before). Does a running job get SIGTERM first, and how long before it is killed? Is the kill at ToDie or earlier (the site's batch limit)? Decides whether reading GLIDEIN_ToDie from the machine ad is a useful checkpoint deadline.

Job: `7093516.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/glidein-end/ospool/P12a-glidein-end-q3`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:13, Sys 0 00:00:20  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after ended without an exit record: gap 68 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Execution on a glidein at Michigan was interrupted with NO signal (hard kill); last sign of life at 19:01:13.4; GLIDEIN_ToDie was -137 s from its last sign of life (negative: died after ToDie); it started 9.7 h before ToDie.
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| bb803993 | 09:17:14.1 | <host-1> | False | 0 | None (None) |  | [(5, 'voluntary', 0.005)] | 85 |
| e8322932 | 09:17:22.2 | <host-1> | True | 0 | 5 (voluntary) |  | [] | none (killed?) |
| 78893214 | 19:02:21.3 | <host-2> | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:16:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P12a-glidein-end-q3"; JobBatchName = "probes.dag+7093513" ]
- 09:16:57.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:38337?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector9#16962248%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 09:17:07.0 `040 file_transfer` Finished transferring input files 
- 09:17:10.0 `021 remote_error` Message from starter on slot1@glidein_920612_257258465@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:17:10.0 `001 executing` Job executing on host: <<ip>:34211?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1@glidein_920612_257258465@<host-1>; CondorScratchDir = "/var/lib/condor/execute/dir_920607/glide_8xm5Xa/execute/dir_1014611/scratch"; Cpus = 1; Disk = 22034073; GPUs = 0; Memory = 2500
- 09:17:19.0 `040 file_transfer` Started transferring output files 
- 09:17:19.0 `040 file_transfer` Finished transferring output files 
- 19:01:18.0 `004 evicted` Job was evicted. Code 1013 Subcode 0 — (0) CPU times; Usr 0 00:00:13, Sys 0 00:00:20  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050522  -  Run Bytes Sent By Job; 286339254  -  Run Bytes Received By Job; Reason: Startd was shutdown; Cpus                 :      0.00        1         1; Disk (KB)            :
- 19:01:37.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42289?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector8#17056173%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26a
- 19:02:19.0 `040 file_transfer` Finished transferring input files 
- 19:02:20.0 `021 remote_error` Message from starter on slot1@glidein_1550625_80272222@<host-2>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 19:02:20.0 `001 executing` Job executing on host: <<ip>:45917?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f5 — SlotName: slot1@glidein_1550625_80272222@<host-2>; CondorScratchDir = "/tmp/osg01/glide_3nsjb6/execute/dir_1914922/scratch"; Cpus = 1; Disk = 88887367; GPUs = 0; Memory = 2048
- 19:02:21.0 `040 file_transfer` Started transferring output files 
- 19:02:21.0 `040 file_transfer` Finished transferring output files 
- 19:02:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:13, Sys 0 00:00:20  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051505  -  Run Bytes Sent By Job; 287389808 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 46.0
CommittedSuspensionTime = 0
CommittedTime = 52
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793059341
JobCurrentStartTransferOutputDate = 1793059341
LastRemoteHost = slot1@glidein_1550625_80272222@<host-2>
LastRemoteWallClockTime = 46.0
LastVacateTime = 1793059278
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
RemoteWallClockTime = 35108.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793059341
TransferOutStarted = 1793059341
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102027; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051505; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:17:14.1 bb803993 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "36000", "GLIDEIN_Site": "Michigan", "GLIDEIN_ToDie": "1793059136", "GLIDEIN_ToRetire": "1793025426", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by
09:17:14.1 bb803993 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:14.1 bb803993 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:17:14.1 bb803993 loop_start             {"restored_step": 0, "step": 0, "total_steps": 43200, "voluntary_exit_at": [5]}
09:17:19.2 bb803993 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:17:19.2 bb803993 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.005, "step": 5, "write_seconds": 0.004}
09:17:19.2 bb803993 children_at_exit       {"alive": [], "exitcodes": []}
09:17:19.2 bb803993 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:17:22.2 e8322932 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "36000", "GLIDEIN_Site": "Michigan", "GLIDEIN_ToDie": "1793059136", "GLIDEIN_ToRetire": "1793025426", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by
09:17:22.2 e8322932 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:17:22.2 e8322932 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024239.158616, "saved_by_exec": "bb803993", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
09:17:22.2 e8322932 loop_start             {"restored_step": 5, "step": 5, "total_steps": 43200, "voluntary_exit_at": [5]}
19:02:21.3 78893214 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "MSU-DataMachine", "GLIDEIN_ToDie": "1793098587", "GLIDEIN_ToRetire": "1793062587", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_cre
19:02:21.3 78893214 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
19:02:21.4 78893214 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1793024239.158616, "saved_by_exec": "bb803993", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 5}
19:02:21.4 78893214 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```
