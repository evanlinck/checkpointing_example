# P0-fingerprint on chtc

**Question.** What does this pool give a job? HTCondor version, vacate/retirement settings, /staging, internet, container, condor_chirp, GPUs, inherited signal masks.

Job: `6527259.0`   Test dir: `/home/<user>/probes/runs/smoke/chtc/P0-fingerprint`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1; NumJobStarts=?, NumShadowStarts=? (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- Python 3.12.14; container: {'apptainer_env': True, 'dockerenv': False, 'singularity_d': True}; scratch free 282.4 GB.
- Machine ad: CondorVersion=$CondorVersion: 25.14.0 2026-09-03 BuildID: 949436 PackageID: 25.14.0-0.949436 RC $, DockerVersion=Docker version 29.1.2, build 890dcca, HasChtcStaging=HasRaddusHtcCephFS, MachineMaxVacateTime=10 * 60, MaxJobRetirementTime=JobRuntimeGuarantee, OpSysAndVer=CentOS9, PelicanPluginVersion=7.27.0-rc.5, PoolName=CHTC, RetirementTimeRemaining=0, SingularityVersion=apptainer version 1.5.3-1.el9, UtsnameVersion=#1 SMP PREEMPT_DYNAMIC Fri Sep 26 01:13:23 UTC 2025
- Paths: {"/cvmfs": {"exists": true, "isdir": true}, "/cvmfs/singularity.opensciencegrid.org": {"exists": true, "isdir": true}, "/staging": {"exists": true, "isdir": true}, "/staging/<user>/ckpt-probes/runs/6527259.0": {"exists": false, "isdir": false, "writable": true}}
- Internet: github.com=True, huggingface.co=True, pypi.org=True
- condor_chirp: None; chirp test: not run
- Inherited signal masks: {'SigBlk': '0000000000000000', 'SigCgt': '0000000000004a07', 'SigIgn': '0000000001001000'}

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| 4e73c945 | 13:28:59.6 | e2456 | False | 0 | None (None) |  | [] | 0 |

## HTCondor event log (AP clock)

- 13:27:57.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P0-fingerprint"; JobBatchName = "probes.dag+6527258" ]
- 13:28:44.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2456.chtc.wisc.edu&noUDP&sock=slot1_78_2170601_8424_96203>
- 13:28:58.0 `040 file_transfer` Finished transferring input files 
- 13:28:58.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_78@e2456.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3712635/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:29:00.0 `040 file_transfer` Started transferring output files 
- 13:29:09.0 `040 file_transfer` Finished transferring output files 
- 13:29:15.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 33273  -  Run Bytes Sent By Job; 286336162  -

## Probe timeline (EP clock; ticks omitted)

```
13:28:59.6 4e73c945 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3712635/scratch", "mode": "fingerprint", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "4e73c945", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3712635/scratch"}
13:28:59.0 4e73c945 fingerprint            {"container": {"apptainer_env": true, "dockerenv": false, "singularity_d": true}, "cwd": "/var/lib/condor/execute/slot1/dir_3712635/scratch", "internet": {"https://github.com": {"ok": true, "seconds": 0.06, "status": 200}, "https://huggingface.co/api/models?limit=1": {"ok": true, "seconds": 0.05, "s
13:28:59.0 4e73c945 exit                   {"code": 0, "reason": "fingerprint done"}
```
