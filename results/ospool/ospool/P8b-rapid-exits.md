# P8b-rapid-exits on ospool

**Question.** What happens when a job exits 85 every 5 seconds, 12 times? Throttling, a hold after N restarts, or nothing?

Job: `6588468.0`   Test dir: `/home/<user>/probes/runs/ospool/ospool/P8b-rapid-exits`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 13; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 5 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 10 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 15 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 20 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 25 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 30 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 35 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 40 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 45 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 50 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 55 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- job.out contains output from 13 of 13 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| d1282ee3 | 11:32:06.4 | warlock21 | False | 0 | None (None) |  | [(5, 'voluntary', 0.175)] | 85 |
| ff760452 | 11:32:13.9 | warlock21 | True | 0 | 5 (voluntary) |  | [(10, 'voluntary', 0.086)] | 85 |
| 47a3c856 | 11:32:20.9 | warlock21 | True | 0 | 10 (voluntary) |  | [(15, 'voluntary', 0.109)] | 85 |
| 533aaeba | 11:32:28.6 | warlock21 | True | 0 | 15 (voluntary) |  | [(20, 'voluntary', 0.151)] | 85 |
| 2211b329 | 11:32:35.8 | warlock21 | True | 0 | 20 (voluntary) |  | [(25, 'voluntary', 0.109)] | 85 |
| e28aec7a | 11:32:42.0 | warlock21 | True | 0 | 25 (voluntary) |  | [(30, 'voluntary', 0.726)] | 85 |
| e60549f6 | 11:32:50.6 | warlock21 | True | 0 | 30 (voluntary) |  | [(35, 'voluntary', 0.119)] | 85 |
| 18cbaec1 | 11:32:57.8 | warlock21 | True | 0 | 35 (voluntary) |  | [(40, 'voluntary', 0.168)] | 85 |
| a9229d49 | 11:33:05.0 | warlock21 | True | 0 | 40 (voluntary) |  | [(45, 'voluntary', 0.109)] | 85 |
| f8c13a72 | 11:33:12.1 | warlock21 | True | 0 | 45 (voluntary) |  | [(50, 'voluntary', 0.118)] | 85 |
| d57cfa66 | 11:33:19.4 | warlock21 | True | 0 | 50 (voluntary) |  | [(55, 'voluntary', 0.126)] | 85 |
| 22238126 | 11:33:27.2 | warlock21 | True | 0 | 55 (voluntary) |  | [(60, 'voluntary', 0.111)] | 85 |
| ea7e72eb | 11:33:34.3 | warlock21 | True | 0 | 60 (voluntary) |  | [(70, 'final', 0.117)] | 0 |

## HTCondor event log (AP clock)

- 11:30:45.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P8b-rapid-exits"; JobBatchName = "probes.dag+6586482" ]
- 11:31:29.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:34035?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector2#14602058%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%26al
- 11:32:03.0 `040 file_transfer` Finished transferring input files 
- 11:32:04.0 `021 remote_error` Message from starter on slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 11:32:04.0 `001 executing` Job executing on host: <<ip>:37419?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93-2f59 — SlotName: slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu; CondorScratchDir = "/tmp/glide_e7SCVy/execute/dir_3368062/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 11:32:12.0 `040 file_transfer` Started transferring output files 
- 11:32:12.0 `040 file_transfer` Finished transferring output files 
- 11:32:19.0 `040 file_transfer` Started transferring output files 
- 11:32:19.0 `040 file_transfer` Finished transferring output files 
- 11:32:26.0 `040 file_transfer` Started transferring output files 
- 11:32:26.0 `040 file_transfer` Finished transferring output files 
- 11:32:34.0 `040 file_transfer` Started transferring output files 
- 11:32:34.0 `040 file_transfer` Finished transferring output files 
- 11:32:41.0 `040 file_transfer` Started transferring output files 
- 11:32:41.0 `040 file_transfer` Finished transferring output files 
- 11:32:48.0 `040 file_transfer` Started transferring output files 
- 11:32:49.0 `040 file_transfer` Finished transferring output files 
- 11:32:56.0 `040 file_transfer` Started transferring output files 
- 11:32:56.0 `040 file_transfer` Finished transferring output files 
- 11:33:03.0 `040 file_transfer` Started transferring output files 
- 11:33:03.0 `040 file_transfer` Finished transferring output files 
- 11:33:10.0 `040 file_transfer` Started transferring output files 
- 11:33:10.0 `040 file_transfer` Finished transferring output files 
- 11:33:17.0 `040 file_transfer` Started transferring output files 
- 11:33:17.0 `040 file_transfer` Finished transferring output files 
- 11:33:25.0 `040 file_transfer` Started transferring output files 
- 11:33:25.0 `040 file_transfer` Finished transferring output files 
- 11:33:32.0 `040 file_transfer` Started transferring output files 
- 11:33:32.0 `040 file_transfer` Finished transferring output files 
- 11:33:44.0 `040 file_transfer` Started transferring output files 
- 11:33:44.0 `040 file_transfer` Finished transferring output files 
- 11:33:45.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 86970  -  Run Bytes Sent By Job; 286336878  -

## condor_history (selected)

```
CheckpointNumber = 11
CommittedSlotTime = 13.0
CommittedSuspensionTime = 0
CommittedTime = 86
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790958824
JobCurrentStartTransferOutputDate = 1790958824
LastRemoteHost = slot1_2@glidein_1647465_211537788@warlock21.beocat.ksu.edu
LastRemoteWallClockTime = 137.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 13
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 137.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790958824
TransferOutStarted = 1790958824
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 86970; CedarFilesCountTotal = 17; CedarSizeBytesLastRun = 86970; CedarFilesCountLastRun = 17 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
11:32:06.4 d1282ee3 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": false, "scratch_dir": "/srv/scratch"}
11:32:06.4 d1282ee3 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:06.5 d1282ee3 restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
11:32:06.5 d1282ee3 loop_start             {"restored_step": 0, "step": 0, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:11.8 d1282ee3 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
11:32:11.0 d1282ee3 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.175, "step": 5, "write_seconds": 0.142}
11:32:11.0 d1282ee3 children_at_exit       {"alive": [], "exitcodes": []}
11:32:12.0 d1282ee3 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
11:32:13.9 ff760452 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:13.9 ff760452 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:13.0 ff760452 restore                {"chosen": "step_00000005", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790958731.9320962, "saved_by_exec": "d1282ee3", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 5}
11:32:13.0 ff760452 loop_start             {"restored_step": 5, "step": 5, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:18.0 ff760452 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 10}
11:32:19.1 ff760452 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.086, "step": 10, "write_seconds": 0.061}
11:32:19.1 ff760452 children_at_exit       {"alive": [], "exitcodes": []}
11:32:19.1 ff760452 exit                   {"code": 85, "reason": "voluntary exit at step 10", "step": 10}
11:32:20.9 47a3c856 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:20.9 47a3c856 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:20.0 47a3c856 restore                {"chosen": "step_00000010", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000010", "nested_dir_ok": true, "saved_at": 1790958739.046124, "saved_by_exec": "ff760452", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 10}
11:32:20.0 47a3c856 loop_start             {"restored_step": 10, "step": 10, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:26.0 47a3c856 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 15}
11:32:26.1 47a3c856 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.109, "step": 15, "write_seconds": 0.084}
11:32:26.2 47a3c856 children_at_exit       {"alive": [], "exitcodes": []}
11:32:26.2 47a3c856 exit                   {"code": 85, "reason": "voluntary exit at step 15", "step": 15}
11:32:28.6 533aaeba start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:28.6 533aaeba history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:28.6 533aaeba restore                {"chosen": "step_00000015", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000015", "nested_dir_ok": true, "saved_at": 1790958746.1020606, "saved_by_exec": "47a3c856", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 15}
11:32:28.6 533aaeba loop_start             {"restored_step": 15, "step": 15, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:33.7 533aaeba save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 20}
11:32:33.8 533aaeba save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.151, "step": 20, "write_seconds": 0.117}
11:32:33.9 533aaeba children_at_exit       {"alive": [], "exitcodes": []}
11:32:33.9 533aaeba exit                   {"code": 85, "reason": "voluntary exit at step 20", "step": 20}
11:32:35.8 2211b329 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 4, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:35.8 2211b329 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:35.8 2211b329 restore                {"chosen": "step_00000020", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000020", "nested_dir_ok": true, "saved_at": 1790958753.8010025, "saved_by_exec": "533aaeba", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 20}
11:32:35.8 2211b329 loop_start             {"restored_step": 20, "step": 20, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:40.9 2211b329 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 25}
11:32:40.0 2211b329 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.109, "step": 25, "write_seconds": 0.075}
11:32:40.0 2211b329 children_at_exit       {"alive": [], "exitcodes": []}
11:32:40.0 2211b329 exit                   {"code": 85, "reason": "voluntary exit at step 25", "step": 25}
11:32:42.0 e28aec7a start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 5, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:42.0 e28aec7a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:42.0 e28aec7a restore                {"chosen": "step_00000025", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000025", "nested_dir_ok": true, "saved_at": 1790958760.906674, "saved_by_exec": "2211b329", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 25}
11:32:42.0 e28aec7a loop_start             {"restored_step": 25, "step": 25, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:48.0 e28aec7a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 30}
11:32:48.8 e28aec7a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.726, "step": 30, "write_seconds": 0.692}
11:32:48.8 e28aec7a children_at_exit       {"alive": [], "exitcodes": []}
11:32:48.8 e28aec7a exit                   {"code": 85, "reason": "voluntary exit at step 30", "step": 30}
11:32:50.6 e60549f6 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 6, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:50.6 e60549f6 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:50.7 e60549f6 restore                {"chosen": "step_00000030", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000030", "nested_dir_ok": true, "saved_at": 1790958768.7044077, "saved_by_exec": "e28aec7a", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 30}
11:32:50.7 e60549f6 loop_start             {"restored_step": 30, "step": 30, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:32:55.7 e60549f6 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 35}
11:32:55.8 e60549f6 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.119, "step": 35, "write_seconds": 0.084}
11:32:55.9 e60549f6 children_at_exit       {"alive": [], "exitcodes": []}
11:32:55.9 e60549f6 exit                   {"code": 85, "reason": "voluntary exit at step 35", "step": 35}
11:32:57.8 18cbaec1 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 7, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:32:57.8 18cbaec1 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:32:57.8 18cbaec1 restore                {"chosen": "step_00000035", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000035", "nested_dir_ok": true, "saved_at": 1790958775.793942, "saved_by_exec": "e60549f6", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 35}
11:32:57.8 18cbaec1 loop_start             {"restored_step": 35, "step": 35, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:02.9 18cbaec1 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 40}
11:33:03.0 18cbaec1 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.168, "step": 40, "write_seconds": 0.142}
11:33:03.0 18cbaec1 children_at_exit       {"alive": [], "exitcodes": []}
11:33:03.0 18cbaec1 exit                   {"code": 85, "reason": "voluntary exit at step 40", "step": 40}
11:33:05.0 a9229d49 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 8, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:33:05.0 a9229d49 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:33:05.1 a9229d49 restore                {"chosen": "step_00000040", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000040", "nested_dir_ok": true, "saved_at": 1790958782.9759257, "saved_by_exec": "18cbaec1", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 40}
11:33:05.1 a9229d49 loop_start             {"restored_step": 40, "step": 40, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:10.1 a9229d49 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 45}
11:33:10.2 a9229d49 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.109, "step": 45, "write_seconds": 0.083}
11:33:10.2 a9229d49 children_at_exit       {"alive": [], "exitcodes": []}
11:33:10.2 a9229d49 exit                   {"code": 85, "reason": "voluntary exit at step 45", "step": 45}
11:33:12.1 f8c13a72 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 9, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:33:12.1 f8c13a72 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:33:12.1 f8c13a72 restore                {"chosen": "step_00000045", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000045", "nested_dir_ok": true, "saved_at": 1790958790.1730096, "saved_by_exec": "a9229d49", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 45}
11:33:12.1 f8c13a72 loop_start             {"restored_step": 45, "step": 45, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:17.1 f8c13a72 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 50}
11:33:17.3 f8c13a72 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.118, "step": 50, "write_seconds": 0.092}
11:33:17.3 f8c13a72 children_at_exit       {"alive": [], "exitcodes": []}
11:33:17.3 f8c13a72 exit                   {"code": 85, "reason": "voluntary exit at step 50", "step": 50}
11:33:19.4 d57cfa66 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 10, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:33:19.4 d57cfa66 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:33:20.0 d57cfa66 restore                {"chosen": "step_00000050", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000050", "nested_dir_ok": true, "saved_at": 1790958797.212134, "saved_by_exec": "f8c13a72", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 50}
11:33:20.1 d57cfa66 loop_start             {"restored_step": 50, "step": 50, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:25.1 d57cfa66 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 55}
11:33:25.2 d57cfa66 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.126, "step": 55, "write_seconds": 0.092}
11:33:25.3 d57cfa66 children_at_exit       {"alive": [], "exitcodes": []}
11:33:25.3 d57cfa66 exit                   {"code": 85, "reason": "voluntary exit at step 55", "step": 55}
11:33:27.2 22238126 start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 11, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:33:27.2 22238126 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:33:27.2 22238126 restore                {"chosen": "step_00000055", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000055", "nested_dir_ok": true, "saved_at": 1790958805.1677046, "saved_by_exec": "d57cfa66", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 55}
11:33:27.3 22238126 loop_start             {"restored_step": 55, "step": 55, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:32.3 22238126 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
11:33:32.4 22238126 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.111, "step": 60, "write_seconds": 0.085}
11:33:32.4 22238126 children_at_exit       {"alive": [], "exitcodes": []}
11:33:32.4 22238126 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
11:33:34.3 ea7e72eb start                  {"cwd": "/srv/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 12, "python": "3.12.14", "sandbox_created_by": "d1282ee3", "sandbox_marker_survived": true, "scratch_dir": "/srv/scratch"}
11:33:34.3 ea7e72eb history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
11:33:34.4 ea7e72eb restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790958812.350866, "saved_by_exec": "22238126", "saved_on_host": "warlock21", "saved_reason": "voluntary", "step": 60}
11:33:34.4 ea7e72eb loop_start             {"restored_step": 60, "step": 60, "total_steps": 70, "voluntary_exit_at": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}
11:33:44.5 ea7e72eb save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 70}
11:33:44.6 ea7e72eb save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.117, "step": 70, "write_seconds": 0.091}
11:33:44.6 ea7e72eb children_at_exit       {"alive": [], "exitcodes": []}
11:33:44.6 ea7e72eb exit                   {"code": 0, "reason": "finished 70 steps", "step": 70}
```
