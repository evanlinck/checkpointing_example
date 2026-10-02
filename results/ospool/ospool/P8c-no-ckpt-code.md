# P8c-no-ckpt-code on ospool

**Question.** Sanity check: without checkpoint_exit_code, is exit 85 simply treated as the job finishing (with return value 85)?

Job: `6588265.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P8c-no-ckpt-code`

## Observations

- Final job state: terminated ((1) Normal termination (return value 85); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d6962f40 | 11:29:52.5 | gpu-node006 | False | 0 | None (None) |  | [(30, 'voluntary', 0.007)] | 85 |

## HTCondor event log (AP clock)

- 11:29:25.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P8c-no-ckpt-code"; JobBatchName = "probes.dag+6586482" ]
- 11:29:45.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:39629?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#14601797%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:29:50.0 `040 file_transfer` Finished transferring input files 
- 11:29:51.0 `021 remote_error` Message from starter on slot1_2@glidein_2078512_412968555@gpu-node006: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:29:51.0 `001 executing` Job executing on host: <<ip>:36569?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_2078512_412968555@gpu-node006; AvailableGPUs = {  }; CondorScratchDir = "/local/scratch/glide_qXOG6B/execute/dir_1788983/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:30:22.0 `040 file_transfer` Started transferring output files 
- 11:30:22.0 `040 file_transfer` Finished transferring output files 
- 11:30:23.0 `005 terminated` Job terminated. — (1) Normal termination (return value 85); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1053612  -  Run Bytes Sent By Job; 286336878

## condor_history (selected)

```
CommittedSlotTime = 39.0
CommittedSuspensionTime = 0
CommittedTime = 39
ExitBySignal = false
ExitCode = 85
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958622
JobCurrentStartTransferOutputDate = 1790958622
LastRemoteHost = slot1_2@glidein_2078512_412968555@gpu-node006
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
TransferOutFinished = 1790958622
TransferOutStarted = 1790958622
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 1053612; CedarFilesCountTotal = 12; CedarSizeBytesLastRun = 1053612; CedarFilesCountLastRun = 12 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:29:52.5 d6962f40 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d6962f40", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:29:52.5 d6962f40 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:29:52.5 d6962f40 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:29:52.5 d6962f40 loop_start             {"restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
11:30:22.6 d6962f40 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
11:30:22.6 d6962f40 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.007, "step": 30, "write_seconds": 0.006}
11:30:22.6 d6962f40 children_at_exit       {"alive": [], "exitcodes": []}
11:30:22.6 d6962f40 exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
```
