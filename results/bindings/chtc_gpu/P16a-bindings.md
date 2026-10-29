# P16a-bindings on chtc_gpu

**Question.** In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container.

Job: `7330276.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/bindings/chtc_gpu/P16a-bindings`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330276', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.003, 'connect_s': 0.001}; .chirp.config present: True

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| c3980735 | 14:31:16.7 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:27:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P16a-bindings"; JobBatchName = "probes.dag+7330274" ]
- 14:30:36.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot3_1_714763_f1a3_64953>
- 14:31:09.0 `040 file_transfer` Finished transferring input files 
- 14:31:09.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=z — SlotName: slot3_1@<host-1>; AvailableGPUs = { GPUs_GPU_83640fe1 }; CondorScratchDir = "/var/lib/condor/execute/slot3/dir_2093901/scratch"; Cpus = 1; Disk = 12582912; GPUs = 1; GPUs_GPU_83640fe1 = [ Id = "GPU-83640fe1"; Capability = 8.9; DeviceName = "NVIDIA L40S"; DeviceUuid = 
- 14:31:16.0 `033 attribute_update` Setting job attribute LastCheckpointStep to 12345 
- 14:31:16.0 `033 attribute_update` Setting job attribute LastCheckpointReason to "probe" 
- 14:31:16.0 `040 file_transfer` Started transferring output files 
- 14:31:16.0 `040 file_transfer` Finished transferring output files 
- 14:31:17.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1747  -  Run Bytes Sent By Job; 4481052207  -

## condor_history (selected)

```
CommittedSlotTime = 42.0
CommittedSuspensionTime = 0
CommittedTime = 42
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793215876
JobCurrentStartTransferOutputDate = 1793215876
LastCheckpointReason = probe
LastCheckpointStep = 12345
LastRemoteHost = slot3_1@<host-1>
LastRemoteWallClockTime = 42.0
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
RemoteWallClockTime = 42.0
TransferOutFinished = 1793215876
TransferOutStarted = 1793215876
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 1747; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 1747; CedarFilesCountLastRun = 3 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:31:16.7 c3980735 start                  {"cwd": "/var/lib/condor/execute/slot3/dir_2093901/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "bindings", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.11.13", "sandbox_created_by": "c3980735", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/exe
14:31:16.7 c3980735 bindings               {"chirp": {"ClusterId": "7330276", "LastCheckpointStep_readback": "12345", "calls_s": 0.003, "connect_s": 0.001}, "chirp_config_env": "/var/lib/condor/execute/slot3/dir_2093901/user/.chirp.config", "chirp_config_exists": true, "classad2_eval": {"JobMaxVacateTime": "not in ad (KeyError)", "MachineMax
14:31:16.7 c3980735 exit                   {"code": 0, "reason": "bindings done"}
```
