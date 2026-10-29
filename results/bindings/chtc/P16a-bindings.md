# P16a-bindings on chtc

**Question.** In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container.

Job: `7330275.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/bindings/chtc/P16a-bindings`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330275', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.006, 'connect_s': 0.002}; .chirp.config present: True

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 3db74fa4 | 14:29:19.3 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:27:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P16a-bindings"; JobBatchName = "probes.dag+7330274" ]
- 14:27:58.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_66_800217_0476_74876>
- 14:29:00.0 `040 file_transfer` Finished transferring input files 
- 14:29:00.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_66@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_2640204/scratch"; Cpus = 1; Disk = 12582912; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:29:19.0 `033 attribute_update` Setting job attribute LastCheckpointStep to 12345 
- 14:29:19.0 `033 attribute_update` Setting job attribute LastCheckpointReason to "probe" 
- 14:29:19.0 `040 file_transfer` Started transferring output files 
- 14:29:19.0 `040 file_transfer` Finished transferring output files 
- 14:29:21.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1704  -  Run Bytes Sent By Job; 4481052207  -

## condor_history (selected)

```
CommittedSlotTime = 83.0
CommittedSuspensionTime = 0
CommittedTime = 83
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793215759
JobCurrentStartTransferOutputDate = 1793215759
LastCheckpointReason = probe
LastCheckpointStep = 12345
LastRemoteHost = slot1_66@<host-1>
LastRemoteWallClockTime = 83.0
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
RemoteWallClockTime = 83.0
TransferOutFinished = 1793215759
TransferOutStarted = 1793215759
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 1704; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 1704; CedarFilesCountLastRun = 3 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:29:19.3 3db74fa4 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_2640204/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "bindings", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.11.13", "sandbox_created_by": "3db74fa4", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/exe
14:29:19.6 3db74fa4 bindings               {"chirp": {"ClusterId": "7330275", "LastCheckpointStep_readback": "12345", "calls_s": 0.006, "connect_s": 0.002}, "chirp_config_env": "/var/lib/condor/execute/slot1/dir_2640204/user/.chirp.config", "chirp_config_exists": true, "classad2_eval": {"JobMaxVacateTime": "not in ad (KeyError)", "MachineMax
14:29:19.6 3db74fa4 exit                   {"code": 0, "reason": "bindings done"}
```
