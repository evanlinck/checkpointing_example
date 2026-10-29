# P15b-parallel-staging-full on chtc_gpu

**Question.** Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?

Job: `7390788.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r3/chtc_gpu/P15b-parallel-staging-full`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:07:21  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:07:21  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'bond0': 25000, 'docker0': 10000, 'eno1': -1, 'eno2': -1, 'eth0': -1, 'eth1': 25000, 'veth4bf9f09': 10000, 'veth4de2ca6': 10000, 'veth61c721e': 10000, 'veth6e90460': 10000, 'veth82408eb': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2574658.5 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA L40, GPUs_GlobalMemoryMb=45468, Machine=<host-1>, Memory=32768, TotalCpus=96.0, TotalMemory=512535
- pbench write: 4 writer(s) x 1 file(s), 90.0 GB: 230.3 s (391 MB/s; writers 224.4-230.3 s, 1% of it in fsync), rename 0.061 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 90.0 GB: 303.3 s (297 MB/s)
- pbench delete: 4 file(s) in 3.08 s
- pbench write: 4 writer(s) x 2 file(s), 89.9 GB: 277.7 s (324 MB/s; writers 244.6-277.7 s, 13% of it in fsync), rename 0.027 s, job memory peak None GB
- pbench read: 4 reader(s), 8 file(s), 89.9 GB: 316.4 s (284 MB/s)
- pbench delete: 8 file(s) in 3.68 s
- pbench write: 8 writer(s) x 1 file(s), 89.9 GB: 328.2 s (274 MB/s; writers 273.3-328.2 s, 11% of it in fsync), rename 0.037 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 89.9 GB: 232.8 s (386 MB/s)
- pbench delete: 8 file(s) in 3.31 s
- pbench write: 8 writer(s) x 2 file(s), 89.9 GB: 239.6 s (375 MB/s; writers 211.1-239.6 s, 6% of it in fsync), rename 0.021 s, job memory peak None GB
- pbench read: 8 reader(s), 16 file(s), 89.9 GB: 327.7 s (274 MB/s)
- pbench delete: 16 file(s) in 3.31 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 37a57968 | 04:19:16.0 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 04:19:04.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15b-parallel-staging-full"; JobBatchName = "probes.dag+7385700" ]
- 04:19:12.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_10_2045376_2ce0_67346>
- 04:19:15.0 `040 file_transfer` Finished transferring input files 
- 04:19:15.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_10@<host-1>; AvailableGPUs = { GPUs_GPU_5d7c2345 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_280069/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_5d7c2345 = [ Id = "GPU-5d7c2345"; Capability = 8.9; DeviceName = "NVIDIA L40"; DeviceUuid = "5d7c2345-6
- 04:57:22.0 `040 file_transfer` Started transferring output files 
- 04:57:22.0 `040 file_transfer` Finished transferring output files 
- 04:57:22.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:07:21  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:07:21  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 7356  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 18320.0
CommittedSuspensionTime = 0
CommittedTime = 2290
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1793267842
LastRemoteHost = slot2_10@<host-1>
LastRemoteWallClockTime = 2291.0
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
RemoteWallClockTime = 2291.0
TransferOutFinished = 1793267842
TransferOutStarted = 1793267842
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 7356; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 7356; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
04:19:16.0 37a57968 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_280069/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "37a57968", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execut
04:19:16.2 37a57968 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 96, "dev_shm": {"free_gb": 270.3, "total_gb": 270.3}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "NVIDIA L40", "GPUs_GlobalMemoryMb": "45468", "Machine": "<host-1>", "Memory": "32768", "TotalCpus": "96.0
04:23:06.7 37a57968 pbench_write           {"bytes": 89992986624, "fastest_writer_s": 224.4, "files": 4, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 390.7, "rename_seconds": 0.061, "slowest_writer_s": 230.32, "target": "/staging/<user>/ckpt-probes/runs/7390788.0", "write_seconds": 230.32, "writers": 
04:28:13.0 37a57968 pbench_read            {"bytes": 89992986624, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 296.7, "read_seconds": 303.32, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7390788.0"}
04:28:17.0 37a57968 pbench_delete          {"delete_seconds": 3.08, "files": 4, "writers": 4}
04:32:54.8 37a57968 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 244.58, "files": 8, "files_per_writer": 2, "fsync_share": 0.13, "job_memory_peak_gb": null, "mb_per_s": 323.9, "rename_seconds": 0.027, "slowest_writer_s": 277.66, "target": "/staging/<user>/ckpt-probes/runs/7390788.0", "write_seconds": 277.66, "writers":
04:38:15.1 37a57968 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 284.2, "read_seconds": 316.36, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7390788.0"}
04:38:18.8 37a57968 pbench_delete          {"delete_seconds": 3.68, "files": 8, "writers": 4}
04:43:47.2 37a57968 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 273.34, "files": 8, "files_per_writer": 1, "fsync_share": 0.11, "job_memory_peak_gb": null, "mb_per_s": 274.0, "rename_seconds": 0.037, "slowest_writer_s": 328.18, "target": "/staging/<user>/ckpt-probes/runs/7390788.0", "write_seconds": 328.18, "writers":
04:47:44.0 37a57968 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 386.2, "read_seconds": 232.84, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7390788.0"}
04:47:47.4 37a57968 pbench_delete          {"delete_seconds": 3.31, "files": 8, "writers": 8}
04:51:47.0 37a57968 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 211.14, "files": 16, "files_per_writer": 2, "fsync_share": 0.06, "job_memory_peak_gb": null, "mb_per_s": 375.3, "rename_seconds": 0.021, "slowest_writer_s": 239.58, "target": "/staging/<user>/ckpt-probes/runs/7390788.0", "write_seconds": 239.58, "writers"
04:57:18.7 37a57968 pbench_read            {"bytes": 89925877760, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 274.4, "read_seconds": 327.7, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7390788.0"}
04:57:22.0 37a57968 pbench_delete          {"delete_seconds": 3.31, "files": 16, "writers": 8}
04:57:22.2 37a57968 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
