# P8c-no-ckpt-code on chtc

**Question.** Sanity check: without checkpoint_exit_code, is exit 85 simply treated as the job finishing (with return value 85)?

Job: `6574106.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P8c-no-ckpt-code`

## Observations

- Final job state: terminated ((1) Normal termination (return value 85); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| b2aa7c6d | 08:58:45.6 | e2473 | False | 0 | None (None) |  | [(30, 'voluntary', 1.225)] | 85 |

## HTCondor event log (AP clock)

- 08:58:30.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P8c-no-ckpt-code"; JobBatchName = "probes.dag+6573176" ]
- 08:58:39.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2473.chtc.wisc.edu&noUDP&sock=slot1_19_342642_0927_94155>
- 08:58:44.0 `040 file_transfer` Finished transferring input files 
- 08:58:45.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_19@e2473.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3548336/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 08:59:17.0 `040 file_transfer` Started transferring output files 
- 08:59:17.0 `040 file_transfer` Finished transferring output files 
- 08:59:17.0 `005 terminated` Job terminated. — (1) Normal termination (return value 85); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1053700  -  Run Bytes Sent By Job; 286336878

## condor_history (selected)

```
CommittedSlotTime = 39.0
CommittedSuspensionTime = 0
CommittedTime = 39
ExitBySignal = false
ExitCode = 85
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790949557
LastRemoteHost = slot1_19@e2473.chtc.wisc.edu
LastRemoteWallClockTime = 39.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 39.0
TransferOutFinished = 1790949557
TransferOutStarted = 1790949557
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1053700; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 1053700; CedarFilesCountLastRun = 12 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
08:58:45.6 b2aa7c6d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3548336/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b2aa7c6d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3548336/scratch"}
08:58:45.6 b2aa7c6d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3548336/scratch/ckpt", "store": "spool"}
08:58:45.6 b2aa7c6d restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3548336/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
08:58:45.6 b2aa7c6d loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
08:59:15.7 b2aa7c6d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
08:59:16.9 b2aa7c6d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 1.225, "step": 30, "write_seconds": 0.92}
08:59:16.0 b2aa7c6d children_at_exit       {"alive": [], "exitcodes": []}
08:59:17.1 b2aa7c6d exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
```
