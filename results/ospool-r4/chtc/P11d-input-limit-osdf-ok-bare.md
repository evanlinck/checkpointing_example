# P11d-input-limit-osdf-ok-bare on chtc

**Question.** Control for P11d-input-limit-osdf: the same 100 MB osdf:// input with max_transfer_input_mb = 200. It should run normally.

Job: `7093576.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/ospool-r4/chtc/P11d-input-limit-osdf-ok-bare`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 0b79e29b | 09:35:13.5 | <host-1> | False | 0 | None (None) |  | [(20, 'final', 0.03)] | 0 |

## HTCondor event log (AP clock)

- 09:34:38.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P11d-input-limit-osdf-ok-bare"; JobBatchName = "probes.dag+7093501" ]
- 09:35:03.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_5_3179352_da00_86314>
- 09:35:13.0 `040 file_transfer` Finished transferring input files 
- 09:35:13.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_5@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3418642/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:35:33.0 `040 file_transfer` Started transferring output files 
- 09:35:33.0 `040 file_transfer` Finished transferring output files 
- 09:35:34.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 4612  -  Run Bytes Sent By Job; 104890553  - 

## condor_history (selected)

```
CommittedSlotTime = 32.0
CommittedSuspensionTime = 0
CommittedTime = 32
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793025333
JobCurrentStartTransferOutputDate = 1793025333
LastRemoteHost = slot1_5@<host-1>
LastRemoteWallClockTime = 32.0
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
RemoteWallClockTime = 32.0
TransferOutFinished = 1793025333
TransferOutStarted = 1793025333
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 4612; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 4612; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:35:13.5 0b79e29b start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3418642/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 3418642, "previous_starts_in_sandbox": 0, "python": "3.9.25", "sandbox_created_by": "0b79e29b", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/exe
09:35:13.5 0b79e29b history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3418642/scratch/ckpt", "store": "spool"}
09:35:13.5 0b79e29b restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3418642/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:35:13.5 0b79e29b loop_start             {"restored_step": 0, "step": 0, "total_steps": 20, "voluntary_exit_at": []}
09:35:33.6 0b79e29b save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 20}
09:35:33.6 0b79e29b save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.03, "step": 20, "write_seconds": 0.029}
09:35:33.6 0b79e29b children_at_exit       {"alive": [], "exitcodes": []}
09:35:33.6 0b79e29b exit                   {"code": 0, "reason": "finished 20 steps", "step": 20}
```
