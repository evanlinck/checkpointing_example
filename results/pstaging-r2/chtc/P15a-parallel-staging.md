# P15a-parallel-staging on chtc

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7337821.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r2/chtc/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:03:51  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:03:51  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 256 CPUs usable, host memory 540 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.2 GB, network {'docker0': 10000, 'eno12409np1': -1, 'eno8303': -1, 'eno8403': -1, 'eth0': 25000, 'idrac': 425, 'veth1a390db': 10000, 'veth1c36001': 10000, 'veth3fa21f2': 10000, 'veth42b6d13': 10000, 'veth61788e1': 10000, 'veth6cc5e2e': 10000, 'veth76b0683': 10000, 'veth7a00d68': 10000, 'veth881911c': 10000, 'veth960db5c': 10000, 'veth9b2ecde': 10000, 'veth9f63cb3': 10000, 'vetha673a87': 10000, 'vethe1c03df': 10000, 'vethe517128': 10000, 'vethf748701': 10000, 'vethf97e617': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2566776.4 GB free; Cpus=8, Machine=<host-1>, Memory=16384, TotalCpus=256.0, TotalMemory=512313
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 44.0 s (454 MB/s; writers 44.0-44.0 s, 1% of it in fsync), rename 0.224 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 144.7 s (138 MB/s)
- pbench delete: 1 file(s) in 3.14 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 43.8 s (457 MB/s; writers 43.8-43.8 s, 5% of it in fsync), rename 0.070 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 150.3 s (133 MB/s)
- pbench delete: 4 file(s) in 4.54 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 38.8 s (515 MB/s; writers 38.2-38.8 s, 2% of it in fsync), rename 0.100 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 41.9 s (478 MB/s)
- pbench delete: 4 file(s) in 3.97 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 39.4 s (504 MB/s; writers 36.4-39.4 s, 5% of it in fsync), rename 0.061 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 45.3 s (439 MB/s)
- pbench delete: 16 file(s) in 4.88 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 37.1 s (539 MB/s; writers 35.7-37.1 s, 1% of it in fsync), rename 0.155 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 25.9 s (771 MB/s)
- pbench delete: 8 file(s) in 4.07 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 36.9 s (538 MB/s; writers 33.1-36.9 s, 5% of it in fsync), rename 0.098 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 27.1 s (732 MB/s)
- pbench delete: 32 file(s) in 5.87 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 0f5c2325 | 21:15:25.6 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 21:14:49.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P15a-parallel-staging"; JobBatchName = "probes.dag+7337820" ]
- 21:15:19.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_58_3214489_0bf5_98440>
- 21:15:24.0 `040 file_transfer` Finished transferring input files 
- 21:15:24.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_58@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3547255/scratch"; Cpus = 8; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 16384
- 21:27:36.0 `040 file_transfer` Started transferring output files 
- 21:27:36.0 `040 file_transfer` Finished transferring output files 
- 21:27:36.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:03:51  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:03:51  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9619  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 5904.0
CommittedSuspensionTime = 0
CommittedTime = 738
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793240856
JobCurrentStartTransferOutputDate = 1793240856
LastRemoteHost = slot1_58@<host-1>
LastRemoteWallClockTime = 738.0
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
RemoteWallClockTime = 738.0
TransferOutFinished = 1793240856
TransferOutStarted = 1793240856
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9619; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9619; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
21:15:25.6 0f5c2325 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3547255/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "0f5c2325", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
21:15:26.2 0f5c2325 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 256, "dev_shm": {"free_gb": 270.2, "total_gb": 270.2}, "machine_ad": {"Cpus": "8", "Machine": "<host-1>", "Memory": "16384", "TotalCpus": "256.0", "TotalMemory": "512313"}, "memavailable": 426170839040, "memlock_limit": {"hard": 8388608, "soft": 
21:16:10.6 0f5c2325 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 44.03, "files": 1, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 454.2, "rename_seconds": 0.224, "slowest_writer_s": 44.03, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 44.03, "writers": 1}
21:18:38.6 0f5c2325 pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 138.2, "read_seconds": 144.74, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:18:41.7 0f5c2325 pbench_delete          {"delete_seconds": 3.14, "files": 1, "writers": 1}
21:19:25.7 0f5c2325 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 43.8, "files": 4, "files_per_writer": 4, "fsync_share": 0.05, "job_memory_peak_gb": null, "mb_per_s": 456.6, "rename_seconds": 0.07, "slowest_writer_s": 43.8, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 43.8, "writers": 1}
21:22:00.4 0f5c2325 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 133.1, "read_seconds": 150.3, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:22:04.0 0f5c2325 pbench_delete          {"delete_seconds": 4.54, "files": 4, "writers": 1}
21:22:43.0 0f5c2325 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 38.24, "files": 4, "files_per_writer": 1, "fsync_share": 0.02, "job_memory_peak_gb": null, "mb_per_s": 515.2, "rename_seconds": 0.1, "slowest_writer_s": 38.81, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 38.81, "writers": 4}
21:23:29.4 0f5c2325 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 477.8, "read_seconds": 41.85, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:23:33.4 0f5c2325 pbench_delete          {"delete_seconds": 3.97, "files": 4, "writers": 4}
21:24:12.9 0f5c2325 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 36.36, "files": 16, "files_per_writer": 4, "fsync_share": 0.05, "job_memory_peak_gb": null, "mb_per_s": 504.0, "rename_seconds": 0.061, "slowest_writer_s": 39.41, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 39.41, "writers": 4
21:25:03.1 0f5c2325 pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 438.8, "read_seconds": 45.27, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:25:08.0 0f5c2325 pbench_delete          {"delete_seconds": 4.88, "files": 16, "writers": 4}
21:25:45.5 0f5c2325 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 35.66, "files": 8, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 539.0, "rename_seconds": 0.155, "slowest_writer_s": 37.1, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 37.1, "writers": 8}
21:26:15.3 0f5c2325 pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 771.3, "read_seconds": 25.93, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:26:19.3 0f5c2325 pbench_delete          {"delete_seconds": 4.07, "files": 8, "writers": 8}
21:26:56.6 0f5c2325 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 33.14, "files": 32, "files_per_writer": 4, "fsync_share": 0.05, "job_memory_peak_gb": null, "mb_per_s": 537.9, "rename_seconds": 0.098, "slowest_writer_s": 36.93, "target": "/staging/<user>/ckpt-probes/runs/7337821.0", "write_seconds": 36.93, "writers": 8
21:27:29.7 0f5c2325 pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 732.1, "read_seconds": 27.13, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7337821.0"}
21:27:35.6 0f5c2325 pbench_delete          {"delete_seconds": 5.87, "files": 32, "writers": 8}
21:27:36.1 0f5c2325 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
