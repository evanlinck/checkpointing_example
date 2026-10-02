# P7g-torchrun-shutdown-timeout-vacate on chtc

**Question.** OPT-IN, needs pytorch.sif. With TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120, does torchrun let the workers finish a 60 s save after SIGTERM (P7e showed it kills them after ~30 s by default)? Does the installed torch support the setting at all?

Job: `6591392.0`   Test dir: `/home/<user>/probes/runs/torchrun2/chtc/P7g-torchrun-shutdown-timeout-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:09, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:18, Sys 0 00:00:04  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after exit 85: gap -139 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 85: gap 37 s, same host, sandbox NEW, restored step None (saved by: None).
- Restart after exit 0: gap -361 s, same host, sandbox NEW, restored step None (saved by: None).
- Trigger vacate fired at 13:09:48.7 (AP clock).
- Evicted execution received SIGTERM 0.0 s after the trigger (includes any retirement time and AP/EP clock offset); 1 signal(s) total.
- It exited with code 85, 60.9 s after the signal.
- Next execution restored step None (saved by: None) -> the SIGTERM save (step 79) was LOST.
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).
- torchrun rank 0: signal=SIGTERM, exit=0
- torchrun rank 1: signal=SIGTERM, exit=0
- Wrapper said: WRAPPER torch 2.14.1+cpu; torchrun --shutdown-timeout supported: yes; TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120 | WRAPPER run_torchrun.sh pid=76 about to exec torchrun | WRAPPER torch 2.14.1+cpu; torchrun --shutdown-timeout supported: yes; TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120 | WRAPPER run_torchrun.sh pid=14 about to exec torchrun

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 0ac02fc4 | 13:08:30.2 | e2472 | False | 0 | None (None) | SIGTERM | [(79, 'signal', 60.096)] | 85 |
| 45dc3b54 | 13:08:30.2 | e2472 | False | 0 | None (None) | SIGTERM | [(79, 'signal', 60.107)] | 85 |
| c68cac33 | 13:11:26.5 | e2472 | False | 1 | None (None) |  | [(300, 'final', 60.098)] | 0 |
| 971dbf0a | 13:11:26.5 | e2472 | False | 1 | None (None) |  | [(300, 'final', 60.082)] | 0 |

## HTCondor event log (AP clock)

- 13:07:32.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7g-torchrun-shutdown-timeout-vacate"; JobBatchName = "probes.dag+6591390" ]
- 13:08:13.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2472.chtc.wisc.edu&noUDP&sock=slot1_13_3663014_7c14_102215>
- 13:08:16.0 `040 file_transfer` Finished transferring input files 
- 13:08:16.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_13@e2472.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2749066/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:10:50.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:09, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286359198  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        2         2; Disk (KB)            :   28
- 13:11:05.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2472.chtc.wisc.edu&noUDP&sock=slot1_13_3663014_7c14_102233>
- 13:11:14.0 `040 file_transfer` Finished transferring input files 
- 13:11:14.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_13@e2472.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2755701/scratch"; Cpus = 2; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 4096
- 13:17:28.0 `040 file_transfer` Started transferring output files 
- 13:17:28.0 `040 file_transfer` Finished transferring output files 
- 13:17:29.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:09, Sys 0 00:00:02  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:18, Sys 0 00:00:04  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 167779  -  Run Bytes Sent By Job; 286359198  

## condor_history (selected)

```
CommittedSlotTime = 766.0
CommittedSuspensionTime = 0
CommittedTime = 383
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1790965048
LastRemoteHost = slot1_13@e2472.chtc.wisc.edu
LastRemoteWallClockTime = 384.0
LastVacateTime = 1790964650
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
RemoteWallClockTime = 542.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790965048
TransferOutStarted = 1790965048
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 167779; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 167779; CedarFilesCountLastRun = 19 ]
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
torch.distributed.elastic.multiprocessing.api.SignalException: Process 76 got signal: 15
/usr/local/lib/python3.12/site-packages/torch/_subclasses/functional_tensor.py:368: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /__w/pytorch/pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
```

## Probe timeline (EP clock; ticks omitted)

```
13:08:30.2 0ac02fc4 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2749066/scratch", "mode": "run", "ppid": 76, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "0ac02fc4", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch"}
13:08:30.2 0ac02fc4 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:08:30.2 0ac02fc4 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
13:08:30.2 0ac02fc4 loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
13:08:30.2 45dc3b54 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2749066/scratch", "mode": "run", "ppid": 76, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "45dc3b54", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch"}
13:08:30.2 45dc3b54 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:08:30.2 45dc3b54 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2749066/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
13:08:30.2 45dc3b54 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
13:09:48.7 45dc3b54 signal                 {"first": true, "on_sigterm": "save85", "rank": "1", "received_at": 1790964588.6864345, "role": "parent", "signal": "SIGTERM", "step": 78}
13:09:48.7 0ac02fc4 signal                 {"first": true, "on_sigterm": "save85", "rank": "0", "received_at": 1790964588.6864045, "role": "parent", "signal": "SIGTERM", "step": 78}
13:09:49.4 45dc3b54 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "signal", "step": 79}
13:09:49.5 0ac02fc4 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "signal", "step": 79}
13:10:49.5 45dc3b54 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "signal", "seconds": 60.107, "step": 79, "write_seconds": 0.034}
13:10:49.5 45dc3b54 signal_save_finished   {"ok": true, "rank": "1", "seconds_since_signal": 60.857}
13:10:49.5 45dc3b54 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
13:10:49.5 45dc3b54 exit                   {"code": 85, "rank": "1", "reason": "signal SIGTERM, on_sigterm=save85", "step": 79}
13:10:49.6 0ac02fc4 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "signal", "seconds": 60.096, "step": 79, "write_seconds": 0.023}
13:10:49.6 0ac02fc4 signal_save_finished   {"ok": true, "rank": "0", "seconds_since_signal": 60.872}
13:10:49.6 0ac02fc4 children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
13:10:49.6 0ac02fc4 exit                   {"code": 85, "rank": "0", "reason": "signal SIGTERM, on_sigterm=save85", "step": 79}
13:11:26.5 c68cac33 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2755701/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "1", "sandbox_created_by": "c68cac33", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch"}
13:11:26.5 c68cac33 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch/ckpt/rank1", "rank": "1", "store": "spool"}
13:11:26.5 c68cac33 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch/ckpt/rank1", "exists": true, "found": false, "latest_pointer": null, "rank": "1"}
13:11:26.5 c68cac33 loop_start             {"rank": "1", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
13:11:26.5 971dbf0a start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2755701/scratch", "mode": "run", "ppid": 14, "previous_starts_in_sandbox": 0, "python": "3.12.15", "rank": "0", "sandbox_created_by": "971dbf0a", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch"}
13:11:26.5 971dbf0a history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch/ckpt/rank0", "rank": "0", "store": "spool"}
13:11:26.5 971dbf0a restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2755701/scratch/ckpt/rank0", "exists": true, "found": false, "latest_pointer": null, "rank": "0"}
13:11:26.5 971dbf0a loop_start             {"rank": "0", "restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
13:16:27.5 c68cac33 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "1", "reason": "final", "step": 300}
13:16:27.5 971dbf0a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "rank": "0", "reason": "final", "step": 300}
13:17:27.6 971dbf0a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "0", "reason": "final", "seconds": 60.082, "step": 300, "write_seconds": 0.01}
13:17:27.6 971dbf0a children_at_exit       {"alive": [], "exitcodes": [], "rank": "0"}
13:17:27.6 971dbf0a exit                   {"code": 0, "rank": "0", "reason": "finished 300 steps", "step": 300}
13:17:27.6 c68cac33 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "rank": "1", "reason": "final", "seconds": 60.098, "step": 300, "write_seconds": 0.013}
13:17:27.6 c68cac33 children_at_exit       {"alive": [], "exitcodes": [], "rank": "1"}
13:17:27.6 c68cac33 exit                   {"code": 0, "rank": "1", "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
13:07:33.5 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/torchrun2/chtc/P7g-torchrun-shutdown-timeout-vacate/job.log", "trigger": "vacate"}
13:09:48.7 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790964496.0, "job": "6591392.0", "last_event": "image_size", "trigger": "vacate"}
13:09:48.7 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6591392.0"], "output": "Job 6591392.0 vacated\n", "rc": 0}
13:09:48.7 {"action": "done"}
```
