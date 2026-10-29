# P16a-bindings on ospool

**Question.** In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container.

Job: `7330277.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/bindings/ospool/P16a-bindings`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330277', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.101, 'connect_s': 0.001}; .chirp.config present: True

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 37ebce90 | 14:29:28.9 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:27:17.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P16a-bindings"; JobBatchName = "probes.dag+7330274" ]
- 14:28:18.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:44767?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#17495585%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%2
- 14:28:58.0 `040 file_transfer` Finished transferring input files 
- 14:28:59.0 `021 remote_error` Message from starter on slot1_4@glidein_3735843_342852224@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image ckpt-recipes-v1.sif
- 14:28:59.0 `001 executing` Job executing on host: <<ip>:43783?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2 — SlotName: slot1_4@glidein_3735843_342852224@<host-1>; CondorScratchDir = "/localscratch/condor/execute/dir_3735717/scratch/glide_DA7ZG4/execute/dir_111695/scratch"; Cpus = 1; Disk = 12582912; GPUs = 0; Memory = 1024
- 14:29:29.0 `033 attribute_update` Setting job attribute LastCheckpointStep to 12345 
- 14:29:29.0 `033 attribute_update` Setting job attribute LastCheckpointReason to "probe" 
- 14:29:29.0 `040 file_transfer` Started transferring output files 
- 14:29:29.0 `040 file_transfer` Finished transferring output files 
- 14:29:30.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1741  -  Run Bytes Sent By Job; 4481052207  -

## condor_history (selected)

```
CommittedSlotTime = 73.0
CommittedSuspensionTime = 0
CommittedTime = 73
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793215769
JobCurrentStartTransferOutputDate = 1793215769
LastCheckpointReason = probe
LastCheckpointStep = 12345
LastRemoteHost = slot1_4@glidein_3735843_342852224@<host-1>
LastRemoteWallClockTime = 73.0
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
RemoteWallClockTime = 73.0
TransferOutFinished = 1793215769
TransferOutStarted = 1793215769
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 1741; CedarFilesCountTotal = 3; CedarSizeBytesLastRun = 1741; CedarFilesCountLastRun = 3 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:29:28.9 37ebce90 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "84600", "GLIDEIN_Site": "PSU-LIGO", "GLIDEIN_ToDie": "1793280863", "GLIDEIN_ToRetire": "1793244863", "MachineMaxVacateTime": "10 * 60"}, "mode": "bindings", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.11.13", "sandbox_creat
14:29:29.3 37ebce90 bindings               {"chirp": {"ClusterId": "7330277", "LastCheckpointStep_readback": "12345", "calls_s": 0.101, "connect_s": 0.001}, "chirp_config_env": "/srv/user/.chirp.config", "chirp_config_exists": true, "classad2_eval": {"JobMaxVacateTime": "not in ad (KeyError)", "MachineMaxVacateTime": 600}, "modules": {"class
14:29:29.3 37ebce90 exit                   {"code": 0, "reason": "bindings done"}
```
