# Probe results: pstaging-r1

Generated 2026-10-28 15:14. Per-test details are in the per-site folders.

## chtc

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

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

## chtc_gpu

### P15a-parallel-staging

_Recipe 3's checkpoint (~88 GB) is written by one process per GPU at once (PyTorch Distributed Checkpoint). How fast is /staging with 1, 4 and 8 writers, each writing 1 or 4 files (20 GB in total, with fsync)? How fast can the same number of processes read it back (a resume), how long does deleting it take (retention), and how much of the job's memory does the page cache use meanwhile? Also records what the machine offers a big job: CPUs, host memory, the job's memory limit, memlock limit, /dev/shm, network links, and whether free space on /staging reflects the user's quota._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:02, Sys 0 00:04:41  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:02, Sys 0 00:04:41  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 40 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno2np1': -1, 'eno3': -1, 'eno4': -1, 'eth0': 10000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2559654.4 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=Tesla P100-PCIE-16GB, GPUs_GlobalMemoryMb=16269, Machine=<host-2>, Memory=16384, TotalCpus=40.0, TotalMemory=512521
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

### P15b-parallel-staging-full

_Same as P15a with a checkpoint as large as recipe 3's (90 GB), 4 and 8 writers, 1 or 2 files each. Does the speed measured at 20 GB hold at full size, and does a full save fit well inside the 600 s vacate window?_

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:03, Sys 0 00:16:20  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:03, Sys 0 00:16:20  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- pbench machine: 40 CPUs usable, host memory 541 GB, job memory limit none seen, memlock {'hard': 8388608, 'soft': 8388608}, /dev/shm 270.3 GB, network {'docker0': -1, 'eno2np1': -1, 'eno3': -1, 'eno4': -1, 'eth0': 10000, 'idrac': 425, 'virbr0': -1} Mbit/s, target /staging (fuse.ceph-fuse), target reports 2559916.7 GB free; CUDADeviceName=GPUs_DeviceName, Cpus=8, GPUs_DeviceName=Tesla P100-PCIE-16GB, GPUs_GlobalMemoryMb=16269, Machine=<host-2>, Memory=32768, TotalCpus=40.0, TotalMemory=512521
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
