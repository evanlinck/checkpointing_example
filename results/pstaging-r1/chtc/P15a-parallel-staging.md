# P15a-parallel-staging on chtc

**Question.** Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota.

Job: `7330267.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/pstaging-r1/chtc/P15a-parallel-staging`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:03, Sys 0 00:05:33  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:03, Sys 0 00:05:33  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 256 CPUs usable, host memory 540 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.2 GB, network {'docker0': 10000, 'eno12409np1': -1, 'eno8303': -1, 'eno8403': -1, 'eth0': 25000, 'idrac': 425, 'veth092900c': 10000, 'veth4766bcf': 10000, 'veth49c11e7': 10000, 'veth77da478': 10000, 'veth97283d9': 10000, 'vethcbe5710': 10000, 'vethf30c6bd': 10000, 'vethf5dca5b': 10000, 'vethf7bbd97': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2559922.2 GB free; Cpus=8, Machine=<host-1>, Memory=16384, TotalCpus=256.0, TotalMemory=512313
- pbench write: 1 writer(s) x 1 file(s), 20.0 GB: 49.0 s (408 MB/s; writers 49.0-49.0 s, 1% of it in fsync), rename 0.486 s, job memory peak None GB
- pbench read: 1 reader(s), 1 file(s), 20.0 GB: 199.6 s (100 MB/s)
- pbench delete: 1 file(s) in 6.11 s
- pbench write: 1 writer(s) x 4 file(s), 20.0 GB: 65.3 s (306 MB/s; writers 65.3-65.3 s, 4% of it in fsync), rename 0.302 s, job memory peak None GB
- pbench read: 1 reader(s), 4 file(s), 20.0 GB: 190.6 s (105 MB/s)
- pbench delete: 4 file(s) in 7.99 s
- pbench write: 4 writer(s) x 1 file(s), 20.0 GB: 42.0 s (476 MB/s; writers 40.5-42.0 s, 1% of it in fsync), rename 0.276 s, job memory peak None GB
- pbench read: 4 reader(s), 4 file(s), 20.0 GB: 67.6 s (296 MB/s)
- pbench delete: 4 file(s) in 8.34 s
- pbench write: 4 writer(s) x 4 file(s), 19.9 GB: 44.7 s (444 MB/s; writers 38.8-44.7 s, 4% of it in fsync), rename 0.444 s, job memory peak None GB
- pbench read: 4 reader(s), 16 file(s), 19.9 GB: 70.4 s (282 MB/s)
- pbench delete: 16 file(s) in 9.43 s
- pbench write: 8 writer(s) x 1 file(s), 20.0 GB: 41.1 s (487 MB/s; writers 37.3-41.1 s, 1% of it in fsync), rename 0.172 s, job memory peak None GB
- pbench read: 8 reader(s), 8 file(s), 20.0 GB: 33.9 s (590 MB/s)
- pbench delete: 8 file(s) in 8.16 s
- pbench write: 8 writer(s) x 4 file(s), 19.9 GB: 45.8 s (434 MB/s; writers 40.7-45.8 s, 4% of it in fsync), rename 0.163 s, job memory peak None GB
- pbench read: 8 reader(s), 32 file(s), 19.9 GB: 35.6 s (559 MB/s)
- pbench delete: 32 file(s) in 14.04 s

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f1768ab8 | 14:27:19.1 | <host-1> | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 14:26:46.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P15a-parallel-staging"; JobBatchName = "probes.dag+7330266" ]
- 14:27:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=<host-1>&noUDP&sock=slot1_3_512999_f416_95650>
- 14:27:17.0 `040 file_transfer` Finished transferring input files 
- 14:27:17.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_3@<host-1>; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3333374/scratch"; Cpus = 8; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 16384
- 14:43:58.0 `040 file_transfer` Started transferring output files 
- 14:43:58.0 `040 file_transfer` Finished transferring output files 
- 14:43:59.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:03, Sys 0 00:05:33  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:03, Sys 0 00:05:33  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 9252  -  Run Bytes Sent By Job; 286354997  - 

## condor_history (selected)

```
CommittedSlotTime = 8072.0
CommittedSuspensionTime = 0
CommittedTime = 1009
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793216638
JobCurrentStartTransferOutputDate = 1793216638
LastRemoteHost = slot1_3@<host-1>
LastRemoteWallClockTime = 1009.0
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
RemoteWallClockTime = 1009.0
TransferOutFinished = 1793216638
TransferOutStarted = 1793216638
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 9252; CedarFilesCountTotal = 4; CedarSizeBytesLastRun = 9252; CedarFilesCountLastRun = 4 ]
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
14:27:19.1 f1768ab8 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3333374/scratch", "machine_ad": {"MachineMaxVacateTime": "10 * 60"}, "mode": "pbench", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f1768ab8", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execu
14:27:22.5 f1768ab8 pbench_env             {"cgroup_memory_max": null, "cpus_usable": 256, "dev_shm": {"free_gb": 270.2, "total_gb": 270.2}, "machine_ad": {"Cpus": "8", "Machine": "<host-1>", "Memory": "16384", "TotalCpus": "256.0", "TotalMemory": "512313"}, "memavailable": 372350234624, "memlock_limit": {"hard": 8388608, "soft": 
14:28:12.5 f1768ab8 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 49.04, "files": 1, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 407.8, "rename_seconds": 0.486, "slowest_writer_s": 49.04, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 49.04, "writers": 1}
14:31:37.3 f1768ab8 pbench_read            {"bytes": 19998441472, "files": 1, "job_memory_peak_gb": null, "mb_per_s": 100.2, "read_seconds": 199.55, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:31:43.4 f1768ab8 pbench_delete          {"delete_seconds": 6.11, "files": 1, "writers": 1}
14:32:49.5 f1768ab8 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 65.31, "files": 4, "files_per_writer": 4, "fsync_share": 0.04, "job_memory_peak_gb": null, "mb_per_s": 306.2, "rename_seconds": 0.302, "slowest_writer_s": 65.31, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 65.31, "writers": 1}
14:36:06.7 f1768ab8 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 104.9, "read_seconds": 190.56, "readers": 1, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:36:14.7 f1768ab8 pbench_delete          {"delete_seconds": 7.99, "files": 4, "writers": 1}
14:36:57.1 f1768ab8 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 40.5, "files": 4, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 476.5, "rename_seconds": 0.276, "slowest_writer_s": 41.97, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 41.97, "writers": 4}
14:38:11.0 f1768ab8 pbench_read            {"bytes": 19998441472, "files": 4, "job_memory_peak_gb": null, "mb_per_s": 296.0, "read_seconds": 67.57, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:38:20.3 f1768ab8 pbench_delete          {"delete_seconds": 8.34, "files": 4, "writers": 4}
14:39:05.8 f1768ab8 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 38.83, "files": 16, "files_per_writer": 4, "fsync_share": 0.04, "job_memory_peak_gb": null, "mb_per_s": 444.2, "rename_seconds": 0.444, "slowest_writer_s": 44.72, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 44.72, "writers": 4
14:40:26.8 f1768ab8 pbench_read            {"bytes": 19864223744, "files": 16, "job_memory_peak_gb": null, "mb_per_s": 282.2, "read_seconds": 70.38, "readers": 4, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:40:36.3 f1768ab8 pbench_delete          {"delete_seconds": 9.43, "files": 16, "writers": 4}
14:41:17.7 f1768ab8 pbench_write           {"bytes": 19998441472, "fastest_writer_s": 37.34, "files": 8, "files_per_writer": 1, "fsync_share": 0.01, "job_memory_peak_gb": null, "mb_per_s": 486.9, "rename_seconds": 0.172, "slowest_writer_s": 41.07, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 41.07, "writers": 8}
14:41:59.5 f1768ab8 pbench_read            {"bytes": 19998441472, "files": 8, "job_memory_peak_gb": null, "mb_per_s": 589.6, "read_seconds": 33.92, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:42:07.6 f1768ab8 pbench_delete          {"delete_seconds": 8.16, "files": 8, "writers": 8}
14:42:54.9 f1768ab8 pbench_write           {"bytes": 19864223744, "fastest_writer_s": 40.73, "files": 32, "files_per_writer": 4, "fsync_share": 0.04, "job_memory_peak_gb": null, "mb_per_s": 433.8, "rename_seconds": 0.163, "slowest_writer_s": 45.79, "target": "/staging/<user>/ckpt-probes/runs/7330267.0", "write_seconds": 45.79, "writers": 8
14:43:43.2 f1768ab8 pbench_read            {"bytes": 19864223744, "files": 32, "job_memory_peak_gb": null, "mb_per_s": 558.6, "read_seconds": 35.56, "readers": 8, "target": "/staging/<user>/ckpt-probes/runs/7330267.0"}
14:43:57.3 f1768ab8 pbench_delete          {"delete_seconds": 14.04, "files": 32, "writers": 8}
14:43:58.7 f1768ab8 exit                   {"code": 0, "job_memory_peak_gb": null, "reason": "pbench done"}
```
