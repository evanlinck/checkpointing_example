# P15a-parallel-staging on chtc_gpu

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7337822.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r2/chtc_gpu/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:03:28  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:03:28  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 2152 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 1075.8 GB, network {'docker0': 10000, 'eno2': -1, 'enp34s0f3u1u2c2': -1, 'eth0': 10000, 'veth3ffbc1b': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2566696.5 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-40GB, GPUs_GlobalMemoryMb=40442, Machine=<host-1>, Memory=16384, TotalCpus=96.0, TotalMemory=2048936
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 41.6 s (480 MB/s; writers 41.6-41.6 s, 1% of it in fsync), rename 0.049 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 155.3 s (129 MB/s)
- pbench delete: 1 file(s) in 2.69 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 42.8 s (467 MB/s; writers 42.8-42.8 s, 6% of it in fsync), rename 0.027 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 160.2 s (125 MB/s)
- pbench delete: 4 file(s) in 2.73 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 37.6 s (532 MB/s; writers 36.9-37.6 s, 1% of it in fsync), rename 0.045 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 40.0 s (499 MB/s)
- pbench delete: 4 file(s) in 2.92 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 36.4 s (546 MB/s; writers 35.0-36.4 s, 4% of it in fsync), rename 0.043 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 41.7 s (476 MB/s)
- pbench delete: 16 file(s) in 3.01 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 36.5 s (548 MB/s; writers 35.1-36.5 s, 1% of it in fsync), rename 0.052 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 26.2 s (764 MB/s)
- pbench delete: 8 file(s) in 3.01 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 35.5 s (560 MB/s; writers 34.3-35.5 s, 5% of it in fsync), rename 1.005 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 28.0 s (710 MB/s)
- pbench delete: 32 file(s) in 3.24 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| b5c818cd | 21:18:58.5 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 21:14:49.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15a-parallel-staging"; JobBatchName = "probes.dag+7337820" ]
- 21:18:52.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_1_762743_31c2_57096>
- 21:18:57.0 `040 file_transfer` Finished transferring input files 
- 21:18:57.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias= — SlotName: slot2_1@<host-1>; AvailableGPUs = { GPUs_GPU_124d06a7 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_1638249/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_124d06a7 = [ Id = "GPU-124d06a7"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-40GB"; DeviceUuid
- 21:31:02.0 `040 file_transfer` Started transferring output files 
- 21:31:02.0 `040 file_transfer` Finished transferring output files 
- 21:31:03.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:03:28  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:03:28  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9098  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 5856.0
CommittedSuspensionTime = 0
CommittedTime = 732
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793241062
JobCurrentStartTransferOutputDate = 1793241062
LastRemoteHost = slot2_1@<host-1>
LastRemoteWallClockTime = 732.0
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
RemoteWallClockTime = 732.0
TransferOutFinished = 1793241062
TransferOutStarted = 1793241062
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9098; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9098; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
21:18:58.5 b5c818cd start                  {"cwd": "/var/lib/condor/execute/slot2/dir_1638249/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b5c818cd", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
21:18:58.8 b5c818cd pbench_env             {"cgroup_memory_max": null, "cpus_usable": 96, "dev_shm": {"free_gb": 1075.8, "total_gb": 1075.8}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "NVIDIA A100-SXM4-40GB", "GPUs_GlobalMemoryMb": "40442", "Machine": "<host-1>", "Memory": "16384", "T
21:19:40.5 b5c818cd pbench_write           {"bytes": 19998441472, "fastest_writer_s": 41.62, "files": 1, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 480.5, "rename_seconds": 0.049, "slowest_writer_s": 41.62, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 41.62, "writers": 1}
21:22:19.3 b5c818cd pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 128.8, "read_seconds": 155.31, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:22:21.0 b5c818cd pbench_delete          {"delete_seconds": 2.69, "files": 1, "writers": 1}
21:23:04.9 b5c818cd pbench_write           {"bytes": 19998441472, "fastest_writer_s": 42.82, "files": 4, "files_per_writer": 4, "fsync_share": 0.06, "job_memory_peak_gb": null, "mb_per_s": 467.0, "rename_seconds": 0.027, "slowest_writer_s": 42.82, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 42.82, "writers": 1}
21:25:48.8 b5c818cd pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 124.8, "read_seconds": 160.23, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:25:51.5 b5c818cd pbench_delete          {"delete_seconds": 2.73, "files": 4, "writers": 1}
21:26:29.3 b5c818cd pbench_write           {"bytes": 19998441472, "fastest_writer_s": 36.92, "files": 4, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 531.8, "rename_seconds": 0.045, "slowest_writer_s": 37.61, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 37.61, "writers": 4}
21:27:13.1 b5c818cd pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 499.4, "read_seconds": 40.04, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:27:16.0 b5c818cd pbench_delete          {"delete_seconds": 2.92, "files": 4, "writers": 4}
21:27:52.5 b5c818cd pbench_write           {"bytes": 19864223744, "fastest_writer_s": 35.04, "files": 16, "files_per_writer": 4, "fsync_share": 0.04, "job_memory_peak_gb": null, "mb_per_s": 545.8, "rename_seconds": 0.043, "slowest_writer_s": 36.4, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 36.4, "writers": 4}
21:28:38.2 b5c818cd pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 476.2, "read_seconds": 41.71, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:28:41.3 b5c818cd pbench_delete          {"delete_seconds": 3.01, "files": 16, "writers": 4}
21:29:17.0 b5c818cd pbench_write           {"bytes": 19998441472, "fastest_writer_s": 35.09, "files": 8, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 548.4, "rename_seconds": 0.052, "slowest_writer_s": 36.47, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 36.47, "writers": 8}
21:29:47.8 b5c818cd pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 763.6, "read_seconds": 26.19, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:29:50.9 b5c818cd pbench_delete          {"delete_seconds": 3.01, "files": 8, "writers": 8}
21:30:27.5 b5c818cd pbench_write           {"bytes": 19864223744, "fastest_writer_s": 34.34, "files": 32, "files_per_writer": 4, "fsync_share": 0.05, "job_memory_peak_gb": null, "mb_per_s": 559.8, "rename_seconds": 1.005, "slowest_writer_s": 35.48, "target": "/staging/<user>/ckpt-probes/runs/7337822.0", "write_seconds": 35.48, "writers": 8
21:30:59.4 b5c818cd pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 709.9, "read_seconds": 27.98, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337822.0"}
21:31:02.6 b5c818cd pbench_delete          {"delete_seconds": 3.24, "files": 32, "writers": 8}
21:31:02.8 b5c818cd exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
