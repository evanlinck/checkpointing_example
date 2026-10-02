# P7h-torchrun-stopfile-vacate on chtc

**Question.** OPT-IN, needs pytorch.sif. If a wrapper turns SIGTERM into a STOP file instead of forwarding it, do the torchrun workers finish a 60 s save (no 30 s kill)? Does the wrapper's mapping make a voluntary exit 85 restart the job in place, and does the SIGTERM save survive eviction?

Job: `6591597.0`   Test dir: `/home/<user>/probes/runs/torchrun3/chtc/P7h-torchrun-stopfile-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:21, Sys 0 00:00:06  -  Total Remote Usage;)
- Executions seen by the probe: 6; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -70 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 12 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap -134 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 47 s, DIFFERENT host, sandbox NEW, restored step 84 (saved by: signal).
- Restart after exit 0: gap 0 s, same host, sandbox NEW, restored step 84 (saved by: signal).
- Trigger vacate fired at 13:27:21.4 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +60.9 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 84 (saved by: signal) -> the SIGTERM save (step 84) SURVIVED.
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=None, exit=0
- torchrun rank 1: signal=None, exit=0
- job.err shows an error (see 'job.err (last lines)' below):   cpu = _conversion_method_template(device=torch.device("cpu"))
- Wrapper said: WRAPPER torch 2.14.1+cpu | WRAPPER torchrun exited with 1 at 1790965556.171341573 | WRAPPER workers saved and asked for a restart: | WRAPPER torch 2.14.1+cpu | WRAPPER got SIGTERM at 1790965641.396042193; creating /var/lib/condor/execute/slot1/dir_3898946/scratch/STOP_REQUESTED (not forwarding the signal) | WRAPPER torchrun exited with 1 at 1790965702.968469630 | WRAPPER workers saved and asked fo

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 5de9da7e | 13:24:45.3 | e2623 | False | 0 | None (None) |  | [(10, 'voluntary', 60.126)] | 85 |
| 675e5e76 | 13:24:45.3 | e2623 | False | 0 | None (None) |  | [(10, 'voluntary', 60.126)] | 85 |
| 990830c7 | 13:26:07.7 | e2623 | True | 0 | 10 (voluntary) |  | [(84, 'signal', 60.103)] | 85 |
| a83c619d | 13:26:07.8 | e2623 | True | 0 | 10 (voluntary) |  | [(84, 'signal', 60.103)] | 85 |
| 17677f5b | 13:29:09.4 | e2471 | False | 1 | 84 (signal) |  | [] | 0 |
| 2cc443a1 | 13:29:09.4 | e2471 | False | 1 | 84 (signal) |  | [] | 0 |

## HTCondor event log (AP clock)

- 13:23:48.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7h-torchrun-stopfile-vacate"; JobBatchName = "probes.dag+6591596" ]
- 13:24:27.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2623.chtc.wisc.edu&noUDP&sock=slot1_36_1919404_815d_111071>
- 13:24:33.0 `040 file_transfer` Finished transferring input files 
- 13:24:33.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_36@e2623.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3898946/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:25:56.0 `040 file_transfer` Started transferring output files 
- 13:25:56.0 `040 file_transfer` Finished transferring output files 
- 13:28:23.0 `040 file_transfer` Started transferring output files 
- 13:28:23.0 `040 file_transfer` Finished transferring output files 
- 13:28:23.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:14, Sys 0 00:00:04  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 4232429  -  Run Bytes Sent By Job; 286359967  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        2         2; Disk (KB)            
- 13:28:45.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2471.chtc.wisc.edu&noUDP&sock=slot1_2_3046204_0a5a_105227>
- 13:28:59.0 `040 file_transfer` Finished transferring input files 
- 13:28:59.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_2@e2471.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_969583/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:29:10.0 `040 file_transfer` Started transferring output files 
- 13:29:10.0 `040 file_transfer` Finished transferring output files 
- 13:29:10.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:21, Sys 0 00:00:06  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 4234647  -  Run Bytes Sent By Job; 290592524 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 52.0
CommittedSuspensionTime = 0
CommittedTime = 108
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790965750
JobCurrentStartTransferOutputDate = 1790965750
LastRemoteHost = slot1_2@e2471.chtc.wisc.edu
LastRemoteWallClockTime = 26.0
LastVacateTime = 1790965703
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
RemoteWallClockTime = 262.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790965750
TransferOutStarted = 1790965750
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 8467076; CedarFilesCountTotal = 64; CedarSizeBytesLastRun = 4234647; CedarFilesCountLastRun = 32 ]
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
  time      : 2026-10-02_13:28:22
  host      : e2623.chtc.wisc.edu
  rank      : 1 (local_rank: 1)
  exitcode  : 85 (pid: 150)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-10-02_13:28:22
  host      : e2623.chtc.wisc.edu
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
13:24:45.3 5de9da7e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3898946/scratch", "mode": "run", "ppid": 144, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "5de9da7e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch"}
13:24:45.3 5de9da7e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:24:45.3 675e5e76 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3898946/scratch", "mode": "run", "ppid": 144, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "675e5e76", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch"}
13:24:45.3 675e5e76 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:24:45.3 5de9da7e restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
13:24:45.3 675e5e76 loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": [10]}
13:24:55.5 5de9da7e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "voluntary", "step": 10}
13:24:55.5 675e5e76 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "voluntary", "step": 10}
13:25:55.6 675e5e76 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "voluntary", "seconds": 60.126, "step": 10, "write_seconds": 0.005}
13:25:55.6 5de9da7e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "voluntary", "seconds": 60.126, "step": 10, "write_seconds": 0.013}
13:25:55.6 5de9da7e exit                   {"code": 85, "rank": "1", "reason": "voluntary exit at step 10", "step": 10}
13:25:55.6 675e5e76 exit                   {"code": 85, "rank": "0", "reason": "voluntary exit at step 10", "step": 10}
13:26:07.7 990830c7 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3898946/scratch", "mode": "run", "ppid": 145, "previous_starts_in_sandbox": 1, "python": "3.12.15", "rank": "0", "sandbox_created_by": "675e5e76", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch"}
13:26:07.7 990830c7 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:26:07.7 990830c7 restore                {"chosen": "step_00000010", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank0", "exists": true, "found": true, "latest_pointer": "step_00000010", "nested_dir_ok": true, "rank": "0", "saved_at": 1790965495.4660213, "saved_by_exec": "675e5e76", "saved_on_host": "e2623", "saved_
13:26:07.7 990830c7 loop_start             {"rank": "0", "restored_step": 10, "step": 10, "total_steps": 300, "voluntary_exit_at": [10]}
13:26:07.8 a83c619d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3898946/scratch", "mode": "run", "ppid": 145, "previous_starts_in_sandbox": 1, "python": "3.12.15", "rank": "1", "sandbox_created_by": "5de9da7e", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch"}
13:26:07.8 a83c619d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:26:07.8 a83c619d restore                {"chosen": "step_00000010", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3898946/scratch/ckpt/rank1", "exists": true, "found": true, "latest_pointer": "step_00000010", "nested_dir_ok": true, "rank": "1", "saved_at": 1790965495.473772, "saved_by_exec": "5de9da7e", "saved_on_host": "e2623", "saved_r
13:26:07.8 a83c619d loop_start             {"rank": "1", "restored_step": 10, "step": 10, "total_steps": 300, "voluntary_exit_at": [10]}
13:27:22.1 990830c7 stop_file_seen         {"path": "/var/lib/condor/execute/slot1/dir_3898946/scratch/STOP_REQUESTED", "rank": "0", "step": 84}
13:27:22.1 990830c7 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "signal", "step": 84}
13:27:22.1 a83c619d stop_file_seen         {"path": "/var/lib/condor/execute/slot1/dir_3898946/scratch/STOP_REQUESTED", "rank": "1", "step": 84}
13:27:22.1 a83c619d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "signal", "step": 84}
13:28:22.2 990830c7 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "signal", "seconds": 60.103, "step": 84, "write_seconds": 0.004}
13:28:22.2 990830c7 signal_save_finished   {"ok": true, "rank": "0", "seconds_since_signal": 60.119}
13:28:22.2 990830c7 children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
13:28:22.2 990830c7 exit                   {"code": 85, "rank": "0", "reason": "signal STOPFILE, on_sigterm=save85", "step": 84}
13:28:22.2 a83c619d save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "signal", "seconds": 60.103, "step": 84, "write_seconds": 0.019}
13:28:22.2 a83c619d signal_save_finished   {"ok": true, "rank": "1", "seconds_since_signal": 60.104}
13:28:22.2 a83c619d children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
13:28:22.2 a83c619d exit                   {"code": 85, "rank": "1", "reason": "signal STOPFILE, on_sigterm=save85", "step": 84}
13:29:09.4 17677f5b start                  {"cwd": "/var/lib/condor/execute/slot1/dir_969583/scratch", "mode": "run", "ppid": 19, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "17677f5b", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch"}
13:29:09.4 17677f5b history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:29:09.4 17677f5b restore                {"chosen": "step_00000084", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch/ckpt/rank0", "exists": true, "found": true, "latest_pointer": "step_00000084", "nested_dir_ok": true, "rank": "0", "saved_at": 1790965642.0731287, "saved_by_exec": "990830c7", "saved_on_host": "e2623", "saved_r
13:29:09.4 17677f5b exit                   {"code": 0, "rank": "0", "reason": "rescheduled (NumJobStarts=1, restored step 84, sandbox marker survived=False); --exit-on-restart", "step": 84}
13:29:09.4 2cc443a1 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_969583/scratch", "mode": "run", "ppid": 19, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "2cc443a1", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch"}
13:29:09.4 2cc443a1 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:29:09.4 2cc443a1 restore                {"chosen": "step_00000084", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_969583/scratch/ckpt/rank1", "exists": true, "found": true, "latest_pointer": "step_00000084", "nested_dir_ok": true, "rank": "1", "saved_at": 1790965642.12768, "saved_by_exec": "a83c619d", "saved_on_host": "e2623", "saved_rea
13:29:09.4 2cc443a1 exit                   {"code": 0, "rank": "1", "reason": "rescheduled (NumJobStarts=1, restored step 84, sandbox marker survived=False); --exit-on-restart", "step": 84}
```

## Trigger log (AP clock)

```
13:23:51.2 {"action": "waiting", "after": 160.0, "log": "/home/<user>/probes/runs/torchrun3/chtc/P7h-torchrun-stopfile-vacate/job.log", "trigger": "vacate"}
13:27:21.4 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790965473.0, "job": "6591597.0", "last_event": "file_transfer", "trigger": "vacate"}
13:27:21.4 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6591597.0"], "output": "Job 6591597.0 vacated\n", "rc": 0}
13:27:21.4 {"action": "done"}
```
