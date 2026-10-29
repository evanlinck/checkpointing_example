# P15a-parallel-staging on chtc_gpu

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7385702.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r3/chtc_gpu/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:02:39  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:02:39  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 128 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno8303': -1, 'eno8403': -1, 'ens6f1np1': -1, 'eth0': 100000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2574889.8 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-80GB, GPUs_GlobalMemoryMb=81154, Machine=<host-1>, Memory=16384, TotalCpus=128.0, TotalMemory=512484
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 84.3 s (237 MB/s; writers 84.3-84.3 s, 42% of it in fsync), rename 0.062 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 242.3 s (82 MB/s)
- pbench delete: 1 file(s) in 2.10 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 79.3 s (252 MB/s; writers 79.3-79.3 s, 47% of it in fsync), rename 0.039 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 294.3 s (68 MB/s)
- pbench delete: 4 file(s) in 2.18 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 55.1 s (363 MB/s; writers 41.1-55.1 s, 12% of it in fsync), rename 0.031 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 75.8 s (264 MB/s)
- pbench delete: 4 file(s) in 2.14 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 82.1 s (242 MB/s; writers 58.2-82.1 s, 65% of it in fsync), rename 0.018 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 112.5 s (176 MB/s)
- pbench delete: 16 file(s) in 2.37 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 107.2 s (186 MB/s; writers 43.4-107.2 s, 40% of it in fsync), rename 0.018 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 99.8 s (200 MB/s)
- pbench delete: 8 file(s) in 2.18 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 66.5 s (299 MB/s; writers 35.2-66.5 s, 45% of it in fsync), rename 0.018 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 99.5 s (200 MB/s)
- pbench delete: 32 file(s) in 2.68 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| ae943199 | 03:55:05.3 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 03:54:47.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc_gpu__P15a-parallel-staging"; JobBatchName = "probes.dag+7385700" ]
- 03:54:59.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot2_1_585302_f532_55935>
- 03:55:04.0 `040 file_transfer` Finished transferring input files 
- 03:55:04.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias — SlotName: slot2_1@<host-1>; AvailableGPUs = { GPUs_GPU_ebb6cfb4 }; CondorScratchDir = "/var/lib/condor/execute/slot2/dir_2559717/scratch"; Cpus = 8; Disk = 2097152; GPUs = 1; GPUs_GPU_ebb6cfb4 = [ Id = "GPU-ebb6cfb4"; Capability = 8.0; DeviceName = "NVIDIA A100-SXM4-80GB"; DeviceUuid = 
- 04:18:56.0 `040 file_transfer` Started transferring output files 
- 04:18:56.0 `040 file_transfer` Finished transferring output files 
- 04:18:56.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:02:39  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:02:39  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9039  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 11496.0
CommittedSuspensionTime = 0
CommittedTime = 1437
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1793265536
LastRemoteHost = slot2_1@<host-1>
LastRemoteWallClockTime = 1438.0
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
RemoteWallClockTime = 1438.0
TransferOutFinished = 1793265536
TransferOutStarted = 1793265536
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9039; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9039; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
03:55:05.3 ae943199 start                  {"cwd": "/var/lib/condor/execute/slot2/dir_2559717/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "ae943199", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
03:55:05.5 ae943199 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 128, "dev_shm": {"free_gb": 270.3, "total_gb": 270.3}, "machine_ad": {"CUDADeviceName": "GPUs_DeviceName", "Cpus": "8", "GPUs_DeviceName": "NVIDIA A100-SXM4-80GB", "GPUs_GlobalMemoryMb": "81154", "Machine": "<host-1>", "Memory": "16384", "Total
03:56:30.1 ae943199 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 84.35, "files": 1, "files_per_writer": 1, "fsync_share": 0.42, "job_memory_peak_gb": null, "mb_per_s": 237.1, "rename_seconds": 0.062, "slowest_writer_s": 84.35, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 84.35, "writers": 1}
04:00:35.1 ae943199 pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 82.5, "read_seconds": 242.33, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:00:37.2 ae943199 pbench_delete          {"delete_seconds": 2.1, "files": 1, "writers": 1}
04:01:56.7 ae943199 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 79.32, "files": 4, "files_per_writer": 4, "fsync_share": 0.47, "job_memory_peak_gb": null, "mb_per_s": 252.1, "rename_seconds": 0.039, "slowest_writer_s": 79.32, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 79.32, "writers": 1}
04:06:53.8 ae943199 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 67.9, "read_seconds": 294.34, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:06:55.0 ae943199 pbench_delete          {"delete_seconds": 2.18, "files": 4, "writers": 1}
04:07:51.3 ae943199 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 41.15, "files": 4, "files_per_writer": 1, "fsync_share": 0.12, "job_memory_peak_gb": null, "mb_per_s": 362.7, "rename_seconds": 0.031, "slowest_writer_s": 55.14, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 55.14, "writers": 4}
04:09:09.0 ae943199 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 263.9, "read_seconds": 75.78, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:09:12.1 ae943199 pbench_delete          {"delete_seconds": 2.14, "files": 4, "writers": 4}
04:10:34.4 ae943199 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 58.2, "files": 16, "files_per_writer": 4, "fsync_share": 0.65, "job_memory_peak_gb": null, "mb_per_s": 242.0, "rename_seconds": 0.018, "slowest_writer_s": 82.08, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 82.08, "writers": 4}
04:12:29.9 ae943199 pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 176.5, "read_seconds": 112.52, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:12:32.3 ae943199 pbench_delete          {"delete_seconds": 2.37, "files": 16, "writers": 4}
04:14:19.6 ae943199 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 43.35, "files": 8, "files_per_writer": 1, "fsync_share": 0.4, "job_memory_peak_gb": null, "mb_per_s": 186.5, "rename_seconds": 0.018, "slowest_writer_s": 107.25, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 107.25, "writers": 8
04:16:02.3 ae943199 pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 200.5, "read_seconds": 99.75, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:16:04.5 ae943199 pbench_delete          {"delete_seconds": 2.18, "files": 8, "writers": 8}
04:17:11.2 ae943199 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 35.19, "files": 32, "files_per_writer": 4, "fsync_share": 0.45, "job_memory_peak_gb": null, "mb_per_s": 298.6, "rename_seconds": 0.018, "slowest_writer_s": 66.52, "target": "/staging/<user>/ckpt-probes/runs/7385702.0", "write_seconds": 66.52, "writers": 8
04:18:53.8 ae943199 pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 199.6, "read_seconds": 99.53, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7385702.0"}
04:18:56.5 ae943199 pbench_delete          {"delete_seconds": 2.68, "files": 32, "writers": 8}
04:18:56.6 ae943199 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
