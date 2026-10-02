# P7f-torchrun-exitcode on chtc

**Question.** OPT-IN, needs pytorch.sif. If every torchrun worker saves and exits 85, what exit code does HTCondor see from torchrun: 85 (restart) or something else (job completes or fails)?

Job: `6590838.0`   Test dir: `/home/<user>/probes/runs/torchrun/chtc/P7f-torchrun-exitcode`

## Observations

- Final job state: terminated ((1) Normal termination (return value 1); Usr 0 00:00:02, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap -30 s, same host, sandbox NEW, restored step None (saved by: None).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=85
- torchrun rank 1: signal=None, exit=85
- job.err shows an error (see 'job.err (last lines)' below): ============================================================
- Wrapper said: WRAPPER run_torchrun.sh pid=15 about to exec torchrun

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 83845500 | 12:33:26.2 | e2464.chtc.wisc.edu | False | 0 | None (None) |  | [(30, 'voluntary', 0.007)] | 85 |
| 92959aa2 | 12:33:26.2 | e2464.chtc.wisc.edu | False | 0 | None (None) |  | [(30, 'voluntary', 0.006)] | 85 |

## HTCondor event log (AP clock)

- 12:31:52.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7f-torchrun-exitcode"; JobBatchName = "probes.dag+6590835" ]
- 12:33:17.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2464.chtc.wisc.edu&noUDP&sock=slot1_1_1734380_5bf9_14429>
- 12:33:23.0 `040 file_transfer` Finished transferring input files 
- 12:33:23.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_1@e2464.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3733957/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 12:33:57.0 `040 file_transfer` Started transferring output files 
- 12:33:57.0 `040 file_transfer` Finished transferring output files 
- 12:33:57.0 `005 terminated` Job terminated. — (1) Normal termination (return value 1); Usr 0 00:00:02, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 2102201  -  Run Bytes Sent By Job; 286357878 

## condor_history (selected)

```
CommittedSlotTime = 80.0
CommittedSuspensionTime = 0
CommittedTime = 40
ExitBySignal = false
ExitCode = 1
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790962437
JobCurrentStartTransferOutputDate = 1790962437
LastRemoteHost = slot1_1@e2464.chtc.wisc.edu
LastRemoteWallClockTime = 40.0
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
RemoteWallClockTime = 40.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790962437
TransferOutStarted = 1790962437
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102201; CedarFilesCountTotal = 20; CedarSizeBytesLastRun = 2102201; CedarFilesCountLastRun = 20 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## job.err (last lines)

```
           ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 386, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
============================================================
probe.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2026-10-02_12:33:56
  host      : e2464.chtc.wisc.edu
  rank      : 1 (local_rank: 1)
  exitcode  : 85 (pid: 21)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-10-02_12:33:56
  host      : e2464.chtc.wisc.edu
  rank      : 0 (local_rank: 0)
  exitcode  : 85 (pid: 20)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
```

## Probe timeline (EP clock; ticks omitted)

```
12:33:26.2 83845500 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3733957/scratch", "mode": "run", "ppid": 15, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "83845500", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch"}
12:33:26.2 83845500 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
12:33:26.2 92959aa2 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3733957/scratch", "mode": "run", "ppid": 15, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "92959aa2", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch"}
12:33:26.2 92959aa2 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
12:33:26.2 83845500 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
12:33:26.2 92959aa2 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3733957/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
12:33:26.2 83845500 loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
12:33:26.2 92959aa2 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 60, "voluntary_exit_at": [30]}
12:33:56.3 83845500 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "voluntary", "step": 30}
12:33:56.3 92959aa2 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "voluntary", "step": 30}
12:33:56.3 83845500 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "voluntary", "seconds": 0.007, "step": 30, "write_seconds": 0.004}
12:33:56.3 83845500 children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
12:33:56.3 83845500 exit                   {"code": 85, "rank": "0", "reason": "voluntary exit at step 30", "step": 30}
12:33:56.3 92959aa2 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "voluntary", "seconds": 0.006, "step": 30, "write_seconds": 0.006}
12:33:56.3 92959aa2 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
12:33:56.3 92959aa2 exit                   {"code": 85, "rank": "1", "reason": "voluntary exit at step 30", "step": 30}
```
