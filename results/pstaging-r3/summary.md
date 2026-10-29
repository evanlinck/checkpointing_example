# Probe results: pstaging-r3

Generated 2026-10-29 05:12. Per-test details are in the per-site folders.

## chtc

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

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

## chtc_gpu

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:02:39  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:02:39  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 128 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno8303': -1, 'eno8403': -1, 'ens6f1np1': -1, 'eth0': 100000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2574889.8 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-80GB, GPUs_GlobalMemoryMb=81154, Machine=<host-2>, Memory=16384, TotalCpus=128.0, TotalMemory=512484
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

### P15b-parallel-staging-full

_Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:07:21  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:07:21  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'bond0': 25000, 'docker0': 10000, 'eno1': -1, 'eno2': -1, 'eth0': -1, 'eth1': 25000, 'veth4bf9f09': 10000, 'veth4de2ca6': 10000, 'veth61c721e': 10000, 'veth6e90460': 10000, 'veth82408eb': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2574658.5 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA L40, GPUs_GlobalMemoryMb=45468, Machine=<host-3>, Memory=32768, TotalCpus=96.0, TotalMemory=512535
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
