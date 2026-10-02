# P8a-missing-ckpt-file on chtc

**Question.** What happens when the job exits 85 but a path listed in transfer_checkpoint_files does not exist? (Hold? Error? Ignored?)

Job: `6574311.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P8a-missing-ckpt-file`

## Observations

- Final job state: aborted (The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE)
- Executions seen by the probe: 0; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|

## HTCondor event log (AP clock)

- 09:00:20.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P8a-missing-ckpt-file"; JobBatchName = "probes.dag+6573176" ]
- 09:00:42.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2598.chtc.wisc.edu&noUDP&sock=slot1_79_1183985_4a6b_115894>
- 09:00:48.0 `040 file_transfer` Finished transferring input files 
- 09:00:48.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_79@e2598.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_853191/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:01:19.0 `040 file_transfer` Started transferring output files 
- 09:01:19.0 `021 remote_error` Error from starter on slot1_79@e2598.chtc.wisc.edu: — Starter failed to upload checkpoint; Code 36 Subcode -1
- 09:01:29.0 `004 evicted` Job was evicted. Code 36 Subcode -1 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Error from slot1_79@e2598.chtc.wisc.edu: Starter failed to upload checkpoint; Cpus                 :  
- 09:01:29.0 `012 held` Job was held. — Error from slot1_79@e2598.chtc.wisc.edu: Starter failed to upload checkpoint; Code 36 Subcode -1
- 09:11:57.0 `009 aborted` Job was aborted. — The job attribute PeriodicRemove expression '((time() - QDate) > 7200) || (JobStatus == 5 && (time() - EnteredCurrentStatus) > 600)' evaluated to TRUE

## condor_history (selected)

```
CommittedSlotTime = 0
CommittedSuspensionTime = 0
CommittedTime = 0
ExitBySignal = false
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790949679
LastHoldReason = Error from slot1_79@e2598.chtc.wisc.edu: Starter failed to upload checkpoint
LastHoldReasonCode = 36
LastHoldReasonSubCode = -1
LastRemoteHost = slot1_79@e2598.chtc.wisc.edu
LastRemoteWallClockTime = 48.0
LastVacateTime = 1790949679
NumCkpts = 0
NumCkpts_RAW = 0
NumHolds = 1
NumHoldsByReason = [ FailedToCheckpoint = 1 ]
NumInputTransferStarts = 1
NumJobCompletions = 0
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ FailedToCheckpoint = 1 ]
RemoteWallClockTime = 48.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt, this_file_does_not_exist.txt
TransferOutStarted = 1790949679
TransferOutput = ckpt,out
TransferOutputStats = [  ]
VacateReason = Error from slot1_79@e2598.chtc.wisc.edu: Starter failed to upload checkpoint
VacateReasonCode = 36
VacateReasonSubCode = -1
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
```
