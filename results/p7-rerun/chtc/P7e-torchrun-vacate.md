# P7e-torchrun-vacate on chtc

**Question.** OPT-IN, needs pytorch.sif. Does torchrun forward the signal to its workers, and how long does it wait before killing them? Does a worker's exit 85 reach HTCondor as 85?

Job: `6586480.0`   Test dir: `/home/<user>/probes/runs/p7-rerun/chtc/P7e-torchrun-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 1); Usr 0 00:00:04, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:04, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=2 (condor_history).
- Restart after ended without an exit record: gap -25 s, same host, sandbox kept (marker file survived), restored step None (saved by: None).
- Trigger did not fire: job ended before the trigger fired.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=None
- torchrun rank 1: signal=None, exit=None
- Wrapper said: WRAPPER run_torchrun.sh pid=141 about to exec torchrun

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 56bbfb46 | 11:25:38.4 | e2607 | False | 0 | None (None) |  | [(5, 'voluntary', 20.199)] | none (killed?) |
| 7e5ac25e | 11:25:38.4 | e2607 | True | 0 | None (None) |  | [(5, 'voluntary', 20.198)] | none (killed?) |

## HTCondor event log (AP clock)

- 11:13:27.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7e-torchrun-vacate"; JobBatchName = "probes.dag+6586475" ]
- 11:14:32.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2588.chtc.wisc.edu&noUDP&sock=slot1_30_2071214_623a_118576>
- 11:14:35.0 `040 file_transfer` Finished transferring input files 
- 11:14:35.0 `021 remote_error` Error from starter on slot1_30@e2588.chtc.wisc.edu: — Failed to transfer files: FILETRANSFER:1:non-zero exit (1) from /usr/libexec/condor/stash_plugin. |Error: Pelican Client Error: Attempt #3: from osdf-uw-cache.svc.osg-htc.org:8443: Specification.FileNotFound Error: Error code 5011: request failed (HTTP status 404): Unable to open (...Path...); no su
- 11:14:36.0 `004 evicted` Job was evicted. Code 13 Subcode 256 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 0  -  Run Bytes Received By Job; Reason: Transfer input files failure at execution point slot1_30@e2588.chtc.wisc.edu using protocol osdf. Details: Pel
- 11:14:36.0 `012 held` Job was held. — Transfer input files failure at execution point slot1_30@e2588.chtc.wisc.edu using protocol osdf. Details: Pelican Client Error: Attempt #3: from osdf-uw-cache.svc.osg-htc.org:8443: Specification.FileNotFound Error: Error code 5011: request failed (HTTP status 404): Unable to open (...Path...); no s
- 11:24:42.0 `013 released` Job was released. — via condor_release (by user <user>)
- 11:25:20.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2607.chtc.wisc.edu&noUDP&sock=slot1_82_2859674_c7f9_121328>
- 11:25:31.0 `040 file_transfer` Finished transferring input files 
- 11:25:31.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_82@e2607.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1232955/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 11:26:04.0 `040 file_transfer` Started transferring output files 
- 11:26:04.0 `040 file_transfer` Finished transferring output files 
- 11:26:05.0 `005 terminated` Job terminated. — (1) Normal termination (return value 1); Usr 0 00:00:04, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:04, Sys 0 00:00:01  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 2101207  -  Run Bytes Sent By Job; 286357653 

## condor_history (selected)

```
CommittedSlotTime = 90.0
CommittedSuspensionTime = 0
CommittedTime = 45
ExitBySignal = false
ExitCode = 1
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958364
JobCurrentStartTransferOutputDate = 1790958364
LastHoldReason = Transfer input files failure at execution point slot1_30@e2588.chtc.wisc.edu using protocol osdf. Details: Pelican Client Error: Attempt #3: from osdf-uw-cache.svc.osg-htc.org:8443: Specification.FileNotFound Error: Error code 5011: request failed (HTTP status 404): Unable to open (...Path...); no such file or directory: server returned 404 Not Found (0s elapsed, 300ms since start); Attempt #2: from dtn-pas.kans.nrp.internet2.edu:8443: Specification.FileNotFound Error: Error code 5011: request failed (HTTP status 404): Unable to open (...Path...); no such file or directory: server returned 404 Not Found (0s elapsed, 200ms since start); Attempt #1: from dtn-pas.cinc.nrp.internet2.edu:8443: Specification.FileNotFound Error: Error code 5011: request failed (HTTP status 404): Unable to open (...Path...); no such file or directory: server returned 404 Not Found (100ms since start) (Version: 7.27.0-rc.5) ( URL file = osdf:///chtc/staging/<user>/ckpt-probes/images/pytorch.sif )|
LastHoldReasonCode = 13
LastHoldReasonSubCode = 256
LastRemoteHost = slot1_82@e2607.chtc.wisc.edu
LastRemoteWallClockTime = 45.0
LastVacateTime = 1790957675
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ TransferInputError = 1 ]
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 1
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ TransferInputError = 1; TransferInputErrorPelican = 1 ]
NumVacatesByReasonPreExecution = [ TransferInputError = 1; TransferInputErrorPelican = 1 ]
NumVacatesPreExecution = 1
RemoteWallClockTime = 49.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958364
TransferOutStarted = 1790958364
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2101207; CedarFilesCountTotal = 20; CedarSizeBytesLastRun = 2101207; CedarFilesCountLastRun = 20 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:25:38.4 56bbfb46 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1232955/scratch", "mode": "run", "ppid": 141, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "56bbfb46", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch"}
11:25:38.4 56bbfb46 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
11:25:38.4 7e5ac25e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1232955/scratch", "mode": "run", "ppid": 141, "previous_starts_in_sandbox": 1, "python": "3.12.15", "rank": "0", "sandbox_created_by": "56bbfb46", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch"}
11:25:38.4 7e5ac25e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
11:25:38.4 56bbfb46 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
11:25:38.4 7e5ac25e restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1232955/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
11:25:38.4 56bbfb46 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
11:25:38.4 7e5ac25e loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
11:25:43.5 56bbfb46 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "voluntary", "step": 5}
11:25:43.5 7e5ac25e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "voluntary", "step": 5}
11:26:03.7 7e5ac25e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "voluntary", "seconds": 20.198, "step": 5, "write_seconds": 0.087}
11:26:03.7 56bbfb46 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "voluntary", "seconds": 20.199, "step": 5, "write_seconds": 0.087}
11:26:03.7 56bbfb46 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
11:26:03.7 7e5ac25e children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
```

## Trigger log (AP clock)

```
11:13:32.7 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/p7-rerun/chtc/P7e-torchrun-vacate/job.log", "trigger": "vacate"}
11:26:18.5 {"action": "gave_up", "end_event": "terminated", "end_text": "Job terminated.", "job": "6586480.0", "reason": "job ended before the trigger fired"}
```
