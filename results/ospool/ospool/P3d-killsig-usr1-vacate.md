# P3d-killsig-usr1-vacate on ospool

**Question.** Is kill_sig honoured? The job asks for SIGUSR1; does it receive SIGUSR1 instead of SIGTERM?

Job: `6589424.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P3d-killsig-usr1-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 3; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after killed (signal SIGUSR1, no exit recorded): gap 78 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 11:58:38.2 (AP clock).
- Evicted execution received SIGUSR1 0.6 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 599.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step 5 (saved by: voluntary).
- job.out contains output from 3 of 3 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 948071eb | 11:56:55.4 | mwt2-c166.campuscluster.illinois.edu | False | 0 | None (None) |  | [(5, 'voluntary', 0.049)] | 85 |
| 82adecec | 11:57:02.1 | mwt2-c166.campuscluster.illinois.edu | True | 0 | 5 (voluntary) | SIGUSR1 | [] | none (killed?) |
| a3d31c6c | 12:09:56.5 | gpu-node007 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 11:55:31.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P3d-killsig-usr1-vacate"; JobBatchName = "probes.dag+6586482" ]
- 11:56:50.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:43167?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14602636%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618
- 11:56:53.0 `040 file_transfer` Finished transferring input files 
- 11:56:54.0 `021 remote_error` Message from starter on slot1_5@glidein_2642342_542725722@mwt2-c166.campuscluster.illinois.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:56:54.0 `001 executing` Job executing on host: <<ip>:37579?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93 — SlotName: slot1_5@glidein_2642342_542725722@mwt2-c166.campuscluster.illinois.edu; CondorScratchDir = "/scratch.local/condor/execute/dir_2642340/glide_Jbf56e/execute/dir_4188992/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:57:00.0 `040 file_transfer` Started transferring output files 
- 11:57:00.0 `040 file_transfer` Finished transferring output files 
- 12:08:39.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1051451  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :      0.00        1         1; Disk (KB)           
- 12:09:46.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:41759?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector3#14596961%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 12:09:54.0 `040 file_transfer` Finished transferring input files 
- 12:09:55.0 `021 remote_error` Message from starter on slot1_2@glidein_274178_123184125@gpu-node007: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 12:09:55.0 `001 executing` Job executing on host: <<ip>:44119?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_274178_123184125@gpu-node007; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_7p1DYF/execute/dir_2009471/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 12:09:56.0 `040 file_transfer` Started transferring output files 
- 12:09:57.0 `040 file_transfer` Finished transferring output files 
- 12:09:57.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1052455  -  Run Bytes Sent By Job; 287388361 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 12.0
CommittedSuspensionTime = 0
CommittedTime = 18
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790960997
JobCurrentStartTransferOutputDate = 1790960996
KillSig = SIGUSR1
LastRemoteHost = slot1_2@glidein_274178_123184125@gpu-node007
LastRemoteWallClockTime = 12.0
LastVacateTime = 1790960919
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
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 722.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790960997
TransferOutStarted = 1790960996
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2103906; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1052455; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:56:55.4 948071eb start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "948071eb", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:56:55.4 948071eb history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:56:55.4 948071eb restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:56:55.4 948071eb loop_start             {"restored_step": 0, "step": 0, "total_steps": 3000, "voluntary_exit_at": [5]}
11:57:00.5 948071eb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:57:00.6 948071eb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.049, "step": 5, "write_seconds": 0.023}
11:57:00.6 948071eb children_at_exit       {"alive": [], "exitcodes": []}
11:57:00.6 948071eb exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:57:02.1 82adecec start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "948071eb", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:57:02.1 82adecec history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:57:02.1 82adecec restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790960220.5408814, "saved_by_exec": "948071eb", "saved_on_host": "mwt2-c166.campuscluster.illinois.edu", "saved_reason": "voluntary", "st
11:57:02.1 82adecec loop_start             {"restored_step": 5, "step": 5, "total_steps": 3000, "voluntary_exit_at": [5]}
11:58:38.8 82adecec signal                 {"first": true, "on_sigterm": "ignore", "received_at": 1790960318.7566857, "role": "parent", "signal": "SIGUSR1", "step": 99}
12:09:56.5 a3d31c6c start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "a3d31c6c", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
12:09:56.5 a3d31c6c history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
12:09:56.5 a3d31c6c restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790960220.5408814, "saved_by_exec": "948071eb", "saved_on_host": "mwt2-c166.campuscluster.illinois.edu", "saved_reason": "voluntary", "st
12:09:56.5 a3d31c6c exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
11:13:50.5 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/ospool/ospool/P3d-killsig-usr1-vacate/job.log", "trigger": "vacate"}
11:58:38.2 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790960214.0, "job": "6589424.0", "last_event": "image_size", "trigger": "vacate"}
11:58:38.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6589424.0"], "output": "Job 6589424.0 vacated\n", "rc": 0}
11:58:38.4 {"action": "done"}
```
