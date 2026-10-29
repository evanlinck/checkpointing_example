# P15a-parallel-staging on chtc_gpu

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7330268.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r1/chtc_gpu/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:04:41  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:04:41  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 40 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno2np1': -1, 'eno3': -1, 'eno4': -1, 'eth0': 10000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2559654.4 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=Tesla P100-PCIE-16GB, GPUs_GlobalMemoryMb=16269, Machine=<host-1>, Memory=16384, TotalCpus=40.0, TotalMemory=512521
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 56.8 s (352 MB/s; writers 56.8-56.8 s, 1% of it in fsync), rename 0.120 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 160.3 s (125 MB/s)
- pbench delete: 1 file(s) in 2.02 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 59.1 s (338 MB/s; writers 59.1-59.1 s, 6% of it in fsync), rename 0.067 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 154.5 s (129 MB/s)
- pbench delete: 4 file(s) in 2.19 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 40.2 s (498 MB/s; writers 39.3-40.2 s, 1% of it in fsync), rename 0.069 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 39.9 s (501 MB/s)
- pbench delete: 4 file(s) in 2.12 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 40.1 s (495 MB/s; writers 37.2-40.1 s, 6% of it in fsync), rename 0.135 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 42.0 s (473 MB/s)
- pbench delete: 16 file(s) in 2.56 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 38.5 s (519 MB/s; writers 35.8-38.5 s, 1% of it in fsync), rename 0.109 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 29.5 s (678 MB/s)
- pbench delete: 8 file(s) in 2.40 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 39.7 s (500 MB/s; writers 35.0-39.7 s, 5% of it in fsync), rename 0.061 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 27.1 s (732 MB/s)
- pbench delete: 32 file(s) in 3.37 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 85462457 | 14:39:12.3 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:26:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15a-parallel-staging"; JobBatchName = "probes.dag+7330266" ]
- 14:39:07.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_1_1321974_0637_57851>
- 14:39:10.0 `040 file_transfer` Finished transferring input files 
- 14:39:10.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot2_1@<host-1>; AvailableGPUs = { GPUs_GPU_ddc1c098 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_2540771/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_ddc1c098 = [ Id = "GPU-ddc1c098"; Capability = 6.0; DeviceName = "Tesla P100-PCIE-16GB"; DeviceUuid = "
- 14:51:54.0 `040 file_transfer` Started transferring output files 
- 14:51:54.0 `040 file_transfer` Finished transferring output files 
- 14:51:54.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:04:41  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:04:41  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9016  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 6136.0
CommittedSuspensionTime = 0
CommittedTime = 767
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793217114
JobCurrentStartTransferOutputDate = 1793217114
LastRemoteHost = slot2_1@<host-1>
LastRemoteWallClockTime = 767.0
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
RemoteWallClockTime = 767.0
TransferOutFinished = 1793217114
TransferOutStarted = 1793217114
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9016; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9016; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:39:12.3 85462457 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_2540771/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "85462457", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
14:39:13.8 85462457 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 40, "dev_shm": {"free_gb": 270.3, "total_gb": 270.3}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "Tesla P100-PCIE-16GB", "GPUs_GlobalMemoryMb": "16269", "Machine": "<host-1>", "Memory": "16384", "TotalCp
14:40:11.0 85462457 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 56.75, "files": 1, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 352.4, "rename_seconds": 0.12, "slowest_writer_s": 56.75, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 56.75, "writers": 1}
14:42:53.6 85462457 pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 124.8, "read_seconds": 160.29, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:42:55.7 85462457 pbench_delete          {"delete_seconds": 2.02, "files": 1, "writers": 1}
14:43:55.1 85462457 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 59.14, "files": 4, "files_per_writer": 4, "fsync_share": 0.06, "job_memory_peak_gb": null, "mb_per_s": 338.1, "rename_seconds": 0.067, "slowest_writer_s": 59.14, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 59.14, "writers": 1}
14:46:32.1 85462457 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 129.4, "read_seconds": 154.5, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:46:34.3 85462457 pbench_delete          {"delete_seconds": 2.19, "files": 4, "writers": 1}
14:47:14.7 85462457 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 39.29, "files": 4, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 498.0, "rename_seconds": 0.069, "slowest_writer_s": 40.16, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 40.16, "writers": 4}
14:47:56.9 85462457 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 500.8, "read_seconds": 39.93, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:47:59.0 85462457 pbench_delete          {"delete_seconds": 2.12, "files": 4, "writers": 4}
14:48:39.5 85462457 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 37.25, "files": 16, "files_per_writer": 4, "fsync_share": 0.06, "job_memory_peak_gb": null, "mb_per_s": 495.0, "rename_seconds": 0.135, "slowest_writer_s": 40.13, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 40.13, "writers": 4
14:49:24.3 85462457 pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 473.0, "read_seconds": 41.99, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:49:26.9 85462457 pbench_delete          {"delete_seconds": 2.56, "files": 16, "writers": 4}
14:50:05.7 85462457 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 35.77, "files": 8, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 518.8, "rename_seconds": 0.109, "slowest_writer_s": 38.55, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 38.55, "writers": 8}
14:50:37.6 85462457 pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 677.5, "read_seconds": 29.52, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:50:40.0 85462457 pbench_delete          {"delete_seconds": 2.4, "files": 8, "writers": 8}
14:51:20.0 85462457 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 35.01, "files": 32, "files_per_writer": 4, "fsync_share": 0.05, "job_memory_peak_gb": null, "mb_per_s": 500.2, "rename_seconds": 0.061, "slowest_writer_s": 39.71, "target": "/staging/<user>/ckpt-probes/runs/7330268.0", "write_seconds": 39.71, "writers": 8
14:51:50.4 85462457 pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 732.3, "read_seconds": 27.13, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330268.0"}
14:51:53.8 85462457 pbench_delete          {"delete_seconds": 3.37, "files": 32, "writers": 8}
14:51:54.3 85462457 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
