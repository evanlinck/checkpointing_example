# P15a-parallel-staging on chtc

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7385701.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r3/chtc/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:04:16  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:04:16  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 256 CPUs usable, host memory 540 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.2 GB, network {'docker0': 10000, 'eno12409np1': -1, 'eno8303': -1, 'eno8403': -1, 'eth0': 25000, 'idrac': 425, 'veth4dc0b12': 10000, 'veth9b2ecde': 10000, 'vethd1d668f': 10000, 'vethd5b0c82': 10000, 'vethf748701': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2574889.7 GB free; Cpus=8, Machine=<host-1>, Memory=16384, TotalCpus=256.0, TotalMemory=512313
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 117.0 s (171 MB/s; writers 117.0-117.0 s, 42% of it in fsync), rename 0.137 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 1542.3 s (13 MB/s)
- pbench delete: 1 file(s) in 4.19 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 211.5 s (95 MB/s; writers 211.5-211.5 s, 77% of it in fsync), rename 0.043 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 935.9 s (21 MB/s)
- pbench delete: 4 file(s) in 3.72 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 66.9 s (299 MB/s; writers 66.2-66.9 s, 20% of it in fsync), rename 0.095 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 354.4 s (56 MB/s)
- pbench delete: 4 file(s) in 3.49 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 97.4 s (204 MB/s; writers 74.6-97.4 s, 69% of it in fsync), rename 0.223 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 168.8 s (118 MB/s)
- pbench delete: 16 file(s) in 5.03 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 78.1 s (256 MB/s; writers 56.9-78.1 s, 13% of it in fsync), rename 0.376 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 268.2 s (75 MB/s)
- pbench delete: 8 file(s) in 4.12 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 67.9 s (292 MB/s; writers 45.0-67.9 s, 35% of it in fsync), rename 0.155 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 643.1 s (31 MB/s)
- pbench delete: 32 file(s) in 5.77 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4afb0b98 | 03:55:24.2 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 03:54:47.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P15a-parallel-staging"; JobBatchName = "probes.dag+7385700" ]
- 03:55:19.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_2_3214489_0bf5_101607>
- 03:55:23.0 `040 file_transfer` Finished transferring input files 
- 03:55:23.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_2@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3747296/scratch"; Cpus = 8; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 16384
- 05:12:11.0 `040 file_transfer` Started transferring output files 
- 05:12:11.0 `040 file_transfer` Finished transferring output files 
- 05:12:12.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:04:16  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:04:16  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9053  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 36904.0
CommittedSuspensionTime = 0
CommittedTime = 4613
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = -1
JobCurrentStartTransferOutputDate = 1793268731
LastRemoteHost = slot1_2@<host-1>
LastRemoteWallClockTime = 4613.0
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
RemoteWallClockTime = 4613.0
TransferOutFinished = 1793268731
TransferOutStarted = 1793268731
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9053; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9053; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
03:55:24.2 4afb0b98 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3747296/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4afb0b98", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
03:55:24.3 4afb0b98 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 256, "dev_shm": {"free_gb": 270.2, "total_gb": 270.2}, "machine_ad": {"Cpus": "8", "Machine": "<host-1>", "Memory": "16384", "TotalCpus": "256.0", "TotalMemory": "512313"}, "memavailable": 400206065664, "memlock_limit": {"hard": 8388608, "soft": 
03:57:21.6 4afb0b98 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 117.01, "files": 1, "files_per_writer": 1, "fsync_share": 0.42, "job_memory_peak_gb": null, "mb_per_s": 170.9, "rename_seconds": 0.137, "slowest_writer_s": 117.01, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 117.01, "writers":
04:23:07.3 4afb0b98 pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 13.0, "read_seconds": 1542.26, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
04:23:11.5 4afb0b98 pbench_delete          {"delete_seconds": 4.19, "files": 1, "writers": 1}
04:26:43.3 4afb0b98 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 211.49, "files": 4, "files_per_writer": 4, "fsync_share": 0.77, "job_memory_peak_gb": null, "mb_per_s": 94.6, "rename_seconds": 0.043, "slowest_writer_s": 211.49, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 211.49, "writers": 
04:42:22.7 4afb0b98 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 21.4, "read_seconds": 935.88, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
04:42:26.4 4afb0b98 pbench_delete          {"delete_seconds": 3.72, "files": 4, "writers": 1}
04:43:33.7 4afb0b98 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 66.22, "files": 4, "files_per_writer": 1, "fsync_share": 0.2, "job_memory_peak_gb": null, "mb_per_s": 298.8, "rename_seconds": 0.095, "slowest_writer_s": 66.94, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 66.94, "writers": 4}
04:49:31.5 4afb0b98 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 56.4, "read_seconds": 354.44, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
04:49:34.0 4afb0b98 pbench_delete          {"delete_seconds": 3.49, "files": 4, "writers": 4}
04:51:12.8 4afb0b98 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 74.57, "files": 16, "files_per_writer": 4, "fsync_share": 0.69, "job_memory_peak_gb": null, "mb_per_s": 203.9, "rename_seconds": 0.223, "slowest_writer_s": 97.42, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 97.42, "writers": 4
04:54:06.3 4afb0b98 pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 117.6, "read_seconds": 168.84, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
04:54:11.3 4afb0b98 pbench_delete          {"delete_seconds": 5.03, "files": 16, "writers": 4}
04:55:29.8 4afb0b98 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 56.85, "files": 8, "files_per_writer": 1, "fsync_share": 0.13, "job_memory_peak_gb": null, "mb_per_s": 256.2, "rename_seconds": 0.376, "slowest_writer_s": 78.06, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 78.06, "writers": 8}
05:00:02.2 4afb0b98 pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 74.6, "read_seconds": 268.16, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
05:00:06.3 4afb0b98 pbench_delete          {"delete_seconds": 4.12, "files": 8, "writers": 8}
05:01:14.6 4afb0b98 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 45.0, "files": 32, "files_per_writer": 4, "fsync_share": 0.35, "job_memory_peak_gb": null, "mb_per_s": 292.4, "rename_seconds": 0.155, "slowest_writer_s": 67.94, "target": "/staging/<user>/ckpt-probes/runs/7385701.0", "write_seconds": 67.94, "writers": 8}
05:12:05.2 4afb0b98 pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 30.9, "read_seconds": 643.11, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7385701.0"}
05:12:10.0 4afb0b98 pbench_delete          {"delete_seconds": 5.77, "files": 32, "writers": 8}
05:12:11.5 4afb0b98 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
