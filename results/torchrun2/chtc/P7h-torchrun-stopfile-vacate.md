# P7h-torchrun-stopfile-vacate on chtc

**Question.** OPT-IN, needs pytorch.sif. If a wrapper turns SIGTERM into a STOP file instead of forwarding it, do the torchrun workers finish a 60 s save (no 30 s kill)? Does the wrapper's mapping make a voluntary exit 85 restart the job in place, and does the SIGTERM save survive eviction?

Job: `6591394.0`   Test dir: `/home/<user>/probes/runs/torchrun2/chtc/P7h-torchrun-stopfile-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:06, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:22, Sys 0 00:00:05  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -90 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 80 s, DIFFERENT host, sandbox NEW, restored step 30 (saved by: voluntary).
- Restart after exit 0: gap 0 s, same host, sandbox NEW, restored step 30 (saved by: voluntary).
- Trigger vacate fired at 13:10:03.7 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=0
- torchrun rank 1: signal=None, exit=0
- job.err shows an error (see 'job.err (last lines)' below):   cpu = _conversion_method_template(device=torch.device("cpu"))
- Wrapper said: WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 1 at 1790964602.467652729 | WRAPPER workers saved and asked for a restart: | WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 0 at 1790964682.857533974

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| df592b3e | 13:08:31.6 | e2621 | False | 0 | None (None) |  | [(30, 'voluntary', 60.079)] | 85 |
| 53e85148 | 13:08:31.6 | e2621 | False | 0 | None (None) |  | [(30, 'voluntary', 60.084)] | 85 |
| e2bbec2b | 13:11:21.9 | e2611 | False | 1 | 30 (voluntary) |  | [] | 0 |
| dfcaf004 | 13:11:21.0 | e2611 | False | 1 | 30 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 13:07:32.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7h-torchrun-stopfile-vacate"; JobBatchName = "probes.dag+6591390" ]
- 13:08:13.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2621.chtc.wisc.edu&noUDP&sock=slot1_78_364047_cb6d_121675>
- 13:08:19.0 `040 file_transfer` Finished transferring input files 
- 13:08:19.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_78@e2621.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1197778/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:10:02.0 `040 file_transfer` Started transferring output files 
- 13:10:02.0 `040 file_transfer` Finished transferring output files 
- 13:10:04.0 `040 file_transfer` Started transferring output files 
- 13:10:04.0 `040 file_transfer` Finished transferring output files 
- 13:10:04.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:16, Sys 0 00:00:04  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 2111372  -  Run Bytes Sent By Job; 286359967  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :                 2         2; Disk (KB)            
- 13:11:05.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2611.chtc.wisc.edu&noUDP&sock=slot1_50_3488743_ccc6_116460>
- 13:11:10.0 `040 file_transfer` Finished transferring input files 
- 13:11:10.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_50@e2611.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3637188/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:11:22.0 `040 file_transfer` Started transferring output files 
- 13:11:22.0 `040 file_transfer` Finished transferring output files 
- 13:11:23.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:06, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:22, Sys 0 00:00:05  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 2113575  -  Run Bytes Sent By Job; 288471419 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 36.0
CommittedSuspensionTime = 0
CommittedTime = 120
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790964682
JobCurrentStartTransferOutputDate = 1790964682
LastRemoteHost = slot1_50@e2611.chtc.wisc.edu
LastRemoteWallClockTime = 19.0
LastVacateTime = 1790964604
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 3
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 131.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790964682
TransferOutStarted = 1790964682
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 4224947; CedarFilesCountTotal = 40; CedarSizeBytesLastRun = 2113575; CedarFilesCountLastRun = 20 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT_OR_EVICT
```

## job.err (last lines)

```
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
============================================================
probe.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2026-10-02_13:10:01
  host      : e2621.chtc.wisc.edu
  rank      : 1 (local_rank: 1)
  exitcode  : 85 (pid: 150)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-10-02_13:10:01
  host      : e2621.chtc.wisc.edu
  rank      : 0 (local_rank: 0)
  exitcode  : 85 (pid: 149)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
/usr/local/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:368: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /__w/pytorch/pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
```

## Probe timeline (EP clock; ticks omitted)

```
13:08:31.6 df592b3e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1197778/scratch", "mode": "run", "ppid": 145, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "df592b3e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch"}
13:08:31.6 df592b3e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:08:31.6 53e85148 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1197778/scratch", "mode": "run", "ppid": 145, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "53e85148", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch"}
13:08:31.6 53e85148 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:08:31.6 df592b3e restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
13:08:31.6 53e85148 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1197778/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
13:08:31.6 df592b3e loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
13:08:31.6 53e85148 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [30]}
13:09:01.7 df592b3e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "voluntary", "step": 30}
13:09:01.7 53e85148 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "voluntary", "step": 30}
13:10:01.7 df592b3e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "voluntary", "seconds": 60.079, "step": 30, "write_seconds": 0.01}
13:10:01.7 df592b3e children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
13:10:01.7 df592b3e exit                   {"code": 85, "rank": "0", "reason": "voluntary exit at step 30", "step": 30}
13:10:01.7 53e85148 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "voluntary", "seconds": 60.084, "step": 30, "write_seconds": 0.007}
13:10:01.7 53e85148 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
13:10:01.7 53e85148 exit                   {"code": 85, "rank": "1", "reason": "voluntary exit at step 30", "step": 30}
13:11:21.9 e2bbec2b start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3637188/scratch", "mode": "run", "ppid": 144, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "e2bbec2b", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch"}
13:11:21.9 e2bbec2b history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:11:21.9 e2bbec2b restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch/ckpt/rank0", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "rank": "0", "saved_at": 1790964541.6717103, "saved_by_exec": "df592b3e", "saved_on_host": "e2621", "saved_
13:11:21.9 e2bbec2b exit                   {"code": 0, "rank": "0", "reason": "rescheduled (NumJobStarts=1, restored step 30, sandbox marker survived=False); --exit-on-restart", "step": 30}
13:11:21.0 dfcaf004 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3637188/scratch", "mode": "run", "ppid": 144, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "dfcaf004", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch"}
13:11:21.0 dfcaf004 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:11:21.0 dfcaf004 restore                {"chosen": "step_00000030", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3637188/scratch/ckpt/rank1", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "rank": "1", "saved_at": 1790964541.669091, "saved_by_exec": "53e85148", "saved_on_host": "e2621", "saved_r
13:11:21.0 dfcaf004 exit                   {"code": 0, "rank": "1", "reason": "rescheduled (NumJobStarts=1, restored step 30, sandbox marker survived=False); --exit-on-restart", "step": 30}
```

## Trigger log (AP clock)

```
13:07:33.5 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/torchrun2/chtc/P7h-torchrun-stopfile-vacate/job.log", "trigger": "vacate"}
13:10:03.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790964499.0, "job": "6591394.0", "last_event": "file_transfer", "trigger": "vacate"}
13:10:03.9 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6591394.0"], "output": "Job 6591394.0 vacated\n", "rc": 0}
13:10:03.9 {"action": "done"}
```
