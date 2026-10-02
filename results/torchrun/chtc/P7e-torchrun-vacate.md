# P7e-torchrun-vacate on chtc

**Question.** OPT-IN, needs pytorch.sif. When HTCondor sends SIGTERM to torchrun, do the workers receive it? If a worker's save takes 60 s, does torchrun wait for it, or kill the workers first (and after how long)?

Job: `6590836.0`   Test dir: `/home/<user>/probes/runs/torchrun/chtc/P7e-torchrun-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:12, Sys 0 00:00:02  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after killed (signal SIGTERM, no exit recorded): gap -86 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after killed (signal SIGTERM, no exit recorded): gap 172 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 0: gap -361 s, same host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 12:34:56.1 (AP clock).
- Evicted execution received SIGTERM 0.1 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It never exited on its own: last sign of life 0.5 s after the signal = effective grace before SIGKILL.
- Next execution restored step None (saved by: None).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=SIGTERM, exit=0
- torchrun rank 1: signal=SIGTERM, exit=0
- Wrapper said: WRAPPER run_torchrun.sh pid=14 about to exec torchrun | WRAPPER run_torchrun.sh pid=14 about to exec torchrun

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| a3eec175 | 12:33:30.2 | e2016.chtc.wisc.edu | False | 0 | None (None) | SIGTERM | [] | none (killed?) |
| aecfea0d | 12:33:30.3 | e2016.chtc.wisc.edu | False | 0 | None (None) | SIGTERM | [] | none (killed?) |
| 92e75e96 | 12:37:48.5 | e2016.chtc.wisc.edu | False | 1 | None (None) |  | [(300, 'final', 60.01)] | 0 |
| 11892bda | 12:37:48.5 | e2016.chtc.wisc.edu | False | 1 | None (None) |  | [(300, 'final', 60.017)] | 0 |

## HTCondor event log (AP clock)

- 12:31:52.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7e-torchrun-vacate"; JobBatchName = "probes.dag+6590835" ]
- 12:33:17.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_23_3486004_ed36_79019>
- 12:33:23.0 `040 file_transfer` Finished transferring input files 
- 12:33:23.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_23@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2335007/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 12:35:27.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:05, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286357878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        2         2; Disk (KB)            :   28
- 12:37:33.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2016.chtc.wisc.edu&noUDP&sock=slot1_23_3486004_ed36_79025>
- 12:37:41.0 `040 file_transfer` Finished transferring input files 
- 12:37:41.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_23@e2016.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2336513/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 12:43:50.0 `040 file_transfer` Started transferring output files 
- 12:43:50.0 `040 file_transfer` Finished transferring output files 
- 12:43:51.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:07, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:12, Sys 0 00:00:02  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 165044  -  Run Bytes Sent By Job; 286357878  

## condor_history (selected)

```
CommittedSlotTime = 758.0
CommittedSuspensionTime = 0
CommittedTime = 379
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790963030
JobCurrentStartTransferOutputDate = 1790963030
LastRemoteHost = slot1_23@e2016.chtc.wisc.edu
LastRemoteWallClockTime = 379.0
LastVacateTime = 1790962527
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 509.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790963030
TransferOutStarted = 1790963030
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 165044; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 165044; CedarFilesCountLastRun = 19 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## job.err (last lines)

```
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/run.py", line 1138, in main
    run(args)
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/run.py", line 1129, in run
    elastic_launch(
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 197, in __call__
    return launch_agent(
           ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 377, in launch_agent
    result = agent.run()
             ^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/elastic/metrics/api.py", line 134, in wrapper
    result = f(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/elastic/agent/server/api.py", line 745, in run
    result = self._invoke_run(role)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/elastic/agent/server/api.py", line 923, in _invoke_run
    time.sleep(monitor_interval)
  File "/usr/local/lib/python3.12/site-packages/torch/distributed/elastic/multiprocessing/api.py", line 86, in _terminate_process_handler
    raise SignalException(f"Process {os.getpid()} got signal: {sigval}", sigval=sigval)
torch.distributed.elastic.multiprocessing.api.SignalException: Process 14 got signal: 15
/usr/local/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:368: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /__w/pytorch/pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
```

## Probe timeline (EP clock; ticks omitted)

```
12:33:30.2 a3eec175 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2335007/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "a3eec175", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch"}
12:33:30.2 a3eec175 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
12:33:30.2 a3eec175 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
12:33:30.2 a3eec175 loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
12:33:30.3 aecfea0d start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2335007/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "aecfea0d", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch"}
12:33:30.3 aecfea0d history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
12:33:30.3 aecfea0d restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2335007/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
12:33:30.3 aecfea0d loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
12:34:56.2 aecfea0d signal                 {"first": true, "on_sigterm": "save85", "rank": "1", "received_at": 1790962496.16501, "role": "parent", "signal": "SIGTERM", "step": 85}
12:34:56.3 a3eec175 signal                 {"first": true, "on_sigterm": "save85", "rank": "0", "received_at": 1790962496.1646492, "role": "parent", "signal": "SIGTERM", "step": 85}
12:34:56.6 a3eec175 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "signal", "step": 86}
12:34:56.6 aecfea0d save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "signal", "step": 86}
12:37:48.5 92e75e96 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2336513/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "92e75e96", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch"}
12:37:48.5 92e75e96 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
12:37:48.5 92e75e96 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
12:37:48.5 92e75e96 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
12:37:48.5 11892bda start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2336513/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "11892bda", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch"}
12:37:48.5 11892bda history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
12:37:48.5 11892bda restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2336513/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
12:37:48.5 11892bda loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
12:42:49.6 11892bda save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "final", "step": 300}
12:42:49.7 92e75e96 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "final", "step": 300}
12:43:49.6 11892bda save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "final", "seconds": 60.017, "step": 300, "write_seconds": 0.01}
12:43:49.6 11892bda children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
12:43:49.6 11892bda exit                   {"code": 0, "rank": "0", "reason": "finished 300 steps", "step": 300}
12:43:49.7 92e75e96 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "final", "seconds": 60.01, "step": 300, "write_seconds": 0.003}
12:43:49.7 92e75e96 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
12:43:49.7 92e75e96 exit                   {"code": 0, "rank": "1", "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
12:31:55.9 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/torchrun/chtc/P7e-torchrun-vacate/job.log", "trigger": "vacate"}
12:34:56.1 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790962403.0, "job": "6590836.0", "last_event": "image_size", "trigger": "vacate"}
12:34:56.1 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6590836.0"], "output": "Job 6590836.0 vacated\n", "rc": 0}
12:34:56.1 {"action": "done"}
```
