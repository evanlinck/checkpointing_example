# P15b-parallel-staging-full on chtc_gpu

**Question.** Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?

Job: `7337860.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r2/chtc_gpu/P15b-parallel-staging-full`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:12:03  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:12:03  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 2152 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 1075.8 GB, network {'docker0': 10000, 'eno2': -1, 'enp34s0f3u1u2c2': -1, 'eth0': 10000, 'veth3ffbc1b': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2566744.0 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-40GB, GPUs_GlobalMemoryMb=40442, Machine=<host-1>, Memory=32768, TotalCpus=96.0, TotalMemory=2048936
- pbench write: 4 writer(s) x 1 file(s), 90.0 GB: 157.0 s (573 MB/s; writers 156.5-157.0 s, 0% of it in fsync), rename 0.023 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 90.0 GB: 173.0 s (520 MB/s)
- pbench delete: 4 file(s) in 7.80 s
- pbench write: 4 writer(s) x 2 file(s), 89.9 GB: 155.9 s (577 MB/s; writers 154.3-155.9 s, 0% of it in fsync), rename 0.036 s, job memory peak None GB
- pbench read: 4 reader(s), 8 file(s), 89.9 GB: 168.4 s (534 MB/s)
- pbench delete: 8 file(s) in 8.61 s
- pbench write: 8 writer(s) x 1 file(s), 89.9 GB: 156.1 s (576 MB/s; writers 152.2-156.1 s, 0% of it in fsync), rename 0.060 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 89.9 GB: 105.2 s (855 MB/s)
- pbench delete: 8 file(s) in 8.45 s
- pbench write: 8 writer(s) x 2 file(s), 89.9 GB: 152.6 s (590 MB/s; writers 150.1-152.6 s, 0% of it in fsync), rename 0.033 s, job memory peak None GB
- pbench read: 8 reader(s), 16 file(s), 89.9 GB: 108.0 s (832 MB/s)
- pbench delete: 16 file(s) in 8.35 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f3275fe7 | 21:32:43.4 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 21:27:44.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15b-parallel-staging-full"; JobBatchName = "probes.dag+7337820" ]
- 21:32:39.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_1_762743_31c2_57118>
- 21:32:42.0 `040 file_transfer` Finished transferring input files 
- 21:32:42.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias= — SlotName: slot2_1@<host-1>; AvailableGPUs = { GPUs_GPU_124d06a7 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1647243/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_124d06a7 = [ Id = "GPU-124d06a7"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-40GB"; DeviceUuid
- 21:53:35.0 `040 file_transfer` Started transferring output files 
- 21:53:35.0 `040 file_transfer` Finished transferring output files 
- 21:53:35.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:12:03  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:12:03  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 7200  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 10056.0
CommittedSuspensionTime = 0
CommittedTime = 1257
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793242415
JobCurrentStartTransferOutputDate = 1793242415
LastRemoteHost = slot2_1@<host-1>
LastRemoteWallClockTime = 1257.0
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
RemoteWallClockTime = 1257.0
TransferOutFinished = 1793242415
TransferOutStarted = 1793242415
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 7200; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 7200; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
21:32:43.4 f3275fe7 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1647243/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f3275fe7", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
21:32:43.5 f3275fe7 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 96, "dev_shm": {"free_gb": 1075.8, "total_gb": 1075.8}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "NVIDIA A100-SXM4-40GB", "GPUs_GlobalMemoryMb": "40442", "Machine": "<host-1>", "Memory": "32768", "T
21:35:20.7 f3275fe7 pbench_write           {"bytes": 89992986624, "fastest_writer_s": 156.5, "files": 4, "files_per_writer": 1, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 573.2, "rename_seconds": 0.023, "slowest_writer_s": 157.0, "target": "/staging/<user>/ckpt-probes/runs/7337860.0", "write_seconds": 157.0, "writers": 4}
21:38:24.1 f3275fe7 pbench_read            {"bytes": 89992986624, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 520.3, "read_seconds": 172.98, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337860.0"}
21:38:31.9 f3275fe7 pbench_delete          {"delete_seconds": 7.8, "files": 4, "writers": 4}
21:41:08.1 f3275fe7 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 154.34, "files": 8, "files_per_writer": 2, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 576.7, "rename_seconds": 0.036, "slowest_writer_s": 155.94, "target": "/staging/<user>/ckpt-probes/runs/7337860.0", "write_seconds": 155.94, "writers": 
21:44:06.8 f3275fe7 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 534.0, "read_seconds": 168.39, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337860.0"}
21:44:15.5 f3275fe7 pbench_delete          {"delete_seconds": 8.61, "files": 8, "writers": 4}
21:46:51.7 f3275fe7 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 152.25, "files": 8, "files_per_writer": 1, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 576.2, "rename_seconds": 0.06, "slowest_writer_s": 156.07, "target": "/staging/<user>/ckpt-probes/runs/7337860.0", "write_seconds": 156.07, "writers": 8
21:48:47.3 f3275fe7 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 855.0, "read_seconds": 105.18, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337860.0"}
21:48:55.7 f3275fe7 pbench_delete          {"delete_seconds": 8.45, "files": 8, "writers": 8}
21:51:28.5 f3275fe7 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 150.06, "files": 16, "files_per_writer": 2, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 589.5, "rename_seconds": 0.033, "slowest_writer_s": 152.55, "target": "/staging/<user>/ckpt-probes/runs/7337860.0", "write_seconds": 152.55, "writers":
21:53:26.9 f3275fe7 pbench_read            {"bytes": 89925877760, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 832.4, "read_seconds": 108.03, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337860.0"}
21:53:35.2 f3275fe7 pbench_delete          {"delete_seconds": 8.35, "files": 16, "writers": 8}
21:53:35.3 f3275fe7 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
