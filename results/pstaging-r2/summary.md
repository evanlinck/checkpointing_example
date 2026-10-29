# Probe results: pstaging-r2

Generated 2026-10-28 21:53. Per-test details are in the per-site folders.

## chtc

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

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

## chtc_gpu

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:03:28  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:03:28  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 2152 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 1075.8 GB, network {'docker0': 10000, 'eno2': -1, 'enp34s0f3u1u2c2': -1, 'eth0': 10000, 'veth3ffbc1b': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2566696.5 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-40GB, GPUs_GlobalMemoryMb=40442, Machine=<host-2>, Memory=16384, TotalCpus=96.0, TotalMemory=2048936
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

### P15b-parallel-staging-full

_Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:01, Sys 0 00:12:03  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:01, Sys 0 00:12:03  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 96 CPUs usable, host memory 2152 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 1075.8 GB, network {'docker0': 10000, 'eno2': -1, 'enp34s0f3u1u2c2': -1, 'eth0': 10000, 'veth3ffbc1b': 10000, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2566744.0 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=NVIDIA A100-SXM4-40GB, GPUs_GlobalMemoryMb=40442, Machine=<host-2>, Memory=32768, TotalCpus=96.0, TotalMemory=2048936
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
