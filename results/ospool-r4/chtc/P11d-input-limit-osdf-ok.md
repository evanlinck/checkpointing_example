# P11d-input-limit-osdf-ok on chtc

**Question.** Control for P11d-input-limit-osdf: the same 100 MB osdf:// input with max_transfer_input_mb = 200. It should run normally.

Job: `7093567.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-osdf-ok`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| b1fd319e | 09:27:06.4 | <host-1> | False | 0 | None (None) |  | [(20, 'final', 0.011)] | 0 |

## HTCondor event log (AP clock)

- 09:25:47.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P11d-input-limit-osdf-ok"; JobBatchName = "probes.dag+7093501" ]
- 09:26:43.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_21_337527_0e37_94484>
- 09:27:04.0 `040 file_transfer` Finished transferring input files 
- 09:27:04.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_21@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2717382/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:27:26.0 `040 file_transfer` Started transferring output files 
- 09:27:26.0 `040 file_transfer` Finished transferring output files 
- 09:27:27.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:01  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:01  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 4453  -  Run Bytes Sent By Job; 391196919  - 

## condor_history (selected)

```
CommittedSlotTime = 45.0
CommittedSuspensionTime = 0
CommittedTime = 45
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793024846
JobCurrentStartTransferOutputDate = 1793024846
LastRemoteHost = slot1_21@<host-1>
LastRemoteWallClockTime = 45.0
MaxTransferInputMB = 200
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
RemoteWallClockTime = 45.0
TransferOutFinished = 1793024846
TransferOutStarted = 1793024846
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 4453; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 4453; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:27:06.4 b1fd319e start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2717382/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b1fd319e", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/
09:27:06.4 b1fd319e history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2717382/scratch/ckpt", "store": "spool"}
09:27:06.4 b1fd319e restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_2717382/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:27:06.4 b1fd319e loop_start             {"restored_step": 0, "step": 0, "total_steps": 20, "voluntary_exit_at": []}
09:27:26.5 b1fd319e save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 20}
09:27:26.5 b1fd319e save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.011, "step": 20, "write_seconds": 0.009}
09:27:26.5 b1fd319e children_at_exit       {"alive": [], "exitcodes": []}
09:27:26.5 b1fd319e exit                   {"code": 0, "reason": "finished 20 steps", "step": 20}
```
