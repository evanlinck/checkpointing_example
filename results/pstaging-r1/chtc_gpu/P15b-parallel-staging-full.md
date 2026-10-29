# P15b-parallel-staging-full on chtc_gpu

**Question.** Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?

Job: `7330680.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r1/chtc_gpu/P15b-parallel-staging-full`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:03, Sys 0 00:16:20  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:03, Sys 0 00:16:20  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 40 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno2np1': -1, 'eno3': -1, 'eno4': -1, 'eth0': 10000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2559916.7 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=Tesla P100-PCIE-16GB, GPUs_GlobalMemoryMb=16269, Machine=<host-1>, Memory=32768, TotalCpus=40.0, TotalMemory=512521
- pbench write: 4 writer(s) x 1 file(s), 90.0 GB: 169.2 s (532 MB/s; writers 167.4-169.2 s, 0% of it in fsync), rename 0.058 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 90.0 GB: 174.7 s (515 MB/s)
- pbench delete: 4 file(s) in 5.76 s
- pbench write: 4 writer(s) x 2 file(s), 89.9 GB: 168.9 s (532 MB/s; writers 166.3-168.9 s, 1% of it in fsync), rename 0.122 s, job memory peak None GB
- pbench read: 4 reader(s), 8 file(s), 89.9 GB: 172.9 s (520 MB/s)
- pbench delete: 8 file(s) in 6.06 s
- pbench write: 8 writer(s) x 1 file(s), 89.9 GB: 165.5 s (544 MB/s; writers 161.3-165.5 s, 0% of it in fsync), rename 0.142 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 89.9 GB: 114.3 s (787 MB/s)
- pbench delete: 8 file(s) in 6.28 s
- pbench write: 8 writer(s) x 2 file(s), 89.9 GB: 163.7 s (550 MB/s; writers 161.1-163.7 s, 0% of it in fsync), rename 0.071 s, job memory peak None GB
- pbench read: 8 reader(s), 16 file(s), 89.9 GB: 112.9 s (796 MB/s)
- pbench delete: 16 file(s) in 6.30 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 3181f802 | 14:52:09.9 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:44:07.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15b-parallel-staging-full"; JobBatchName = "probes.dag+7330266" ]
- 14:52:01.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_1_1321974_0637_57871>
- 14:52:08.0 `040 file_transfer` Finished transferring input files 
- 14:52:08.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_1@<host-1>; AvailableGPUs = { GPUs_GPU_ddc1c098 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_2543027/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_ddc1c098 = [ Id = "GPU-ddc1c098"; Capability = 6.0; DeviceName = "Tesla P100-PCIE-16GB"; DeviceUuid = "
- 15:13:47.0 `040 file_transfer` Started transferring output files 
- 15:13:47.0 `040 file_transfer` Finished transferring output files 
- 15:13:47.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:03, Sys 0 00:16:20  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:03, Sys 0 00:16:20  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 7142  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 10448.0
CommittedSuspensionTime = 0
CommittedTime = 1306
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793218427
JobCurrentStartTransferOutputDate = 1793218427
LastRemoteHost = slot2_1@<host-1>
LastRemoteWallClockTime = 1306.0
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
RemoteWallClockTime = 1306.0
TransferOutFinished = 1793218427
TransferOutStarted = 1793218427
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 7142; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 7142; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:52:09.9 3181f802 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_2543027/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "3181f802", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
14:52:11.6 3181f802 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 40, "dev_shm": {"free_gb": 270.3, "total_gb": 270.3}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "Tesla P100-PCIE-16GB", "GPUs_GlobalMemoryMb": "16269", "Machine": "<host-1>", "Memory": "32768", "TotalCp
14:55:01.0 3181f802 pbench_write           {"bytes": 89992986624, "fastest_writer_s": 167.45, "files": 4, "files_per_writer": 1, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 531.9, "rename_seconds": 0.058, "slowest_writer_s": 169.2, "target": "/staging/<user>/ckpt-probes/runs/7330680.0", "write_seconds": 169.2, "writers": 4}
14:58:02.0 3181f802 pbench_read            {"bytes": 89992986624, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 515.1, "read_seconds": 174.72, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330680.0"}
14:58:07.8 3181f802 pbench_delete          {"delete_seconds": 5.76, "files": 4, "writers": 4}
15:00:57.1 3181f802 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 166.33, "files": 8, "files_per_writer": 2, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 532.4, "rename_seconds": 0.122, "slowest_writer_s": 168.91, "target": "/staging/<user>/ckpt-probes/runs/7330680.0", "write_seconds": 168.91, "writers":
15:03:56.8 3181f802 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 520.2, "read_seconds": 172.86, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330680.0"}
15:04:02.9 3181f802 pbench_delete          {"delete_seconds": 6.06, "files": 8, "writers": 4}
15:06:48.8 3181f802 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 161.3, "files": 8, "files_per_writer": 1, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 543.5, "rename_seconds": 0.142, "slowest_writer_s": 165.47, "target": "/staging/<user>/ckpt-probes/runs/7330680.0", "write_seconds": 165.47, "writers": 8
15:08:50.1 3181f802 pbench_read            {"bytes": 89925877760, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 786.8, "read_seconds": 114.3, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330680.0"}
15:08:56.4 3181f802 pbench_delete          {"delete_seconds": 6.28, "files": 8, "writers": 8}
15:11:40.2 3181f802 pbench_write           {"bytes": 89925877760, "fastest_writer_s": 161.05, "files": 16, "files_per_writer": 2, "fsync_share": 0.0, "job_memory_peak_gb": null, "mb_per_s": 549.5, "rename_seconds": 0.071, "slowest_writer_s": 163.66, "target": "/staging/<user>/ckpt-probes/runs/7330680.0", "write_seconds": 163.66, "writers":
15:13:40.4 3181f802 pbench_read            {"bytes": 89925877760, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 796.2, "read_seconds": 112.94, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330680.0"}
15:13:46.7 3181f802 pbench_delete          {"delete_seconds": 6.3, "files": 16, "writers": 8}
15:13:47.0 3181f802 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
