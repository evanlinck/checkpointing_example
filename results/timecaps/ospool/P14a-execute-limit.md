# P14a-execute-limit on ospool

**Question.** OSPool access points cap each execution (ap40: AllowedExecuteDuration = 20 h, then a hold). Here allowed_execute_duration = 150 s and the probe exits 85 every 60 s (restarting in place). Does the job finish (each exit-85 restart starts a new execution, so a timed checkpoint keeps a job under the cap), or is it held ~150 s after it first started?

Job: `7195169.0`   Test dir: `/home/<user>/checkpointing_example/probes/runs/timecaps/ospool/P14a-execute-limit`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- First start 09:30:24.3; never held; job ad at first start: {'AllowedExecuteDuration': '150', 'JobStartDate': '1793111054'}.
- Executions seen by the probe: 6; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 4 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 240 (saved by: voluntary).
- Restart after exit 85: gap 2 s, same host, sandbox kept (marker file survived), restored step 300 (saved by: voluntary).
- job.out contains output from 6 of 6 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| fbd0f6cf | 09:30:24.3 | <host-1> | False | 0 | None (None) |  | [(60, 'voluntary', 0.005)] | 85 |
| f353d814 | 09:31:26.6 | <host-1> | True | 0 | 60 (voluntary) |  | [(120, 'voluntary', 0.126)] | 85 |
| 6aa7133a | 09:32:30.5 | <host-1> | True | 0 | 120 (voluntary) |  | [(180, 'voluntary', 0.006)] | 85 |
| 523e1d00 | 09:33:33.7 | <host-1> | True | 0 | 180 (voluntary) |  | [(240, 'voluntary', 0.006)] | 85 |
| 475b2e28 | 09:34:35.5 | <host-1> | True | 0 | 240 (voluntary) |  | [(300, 'voluntary', 0.009)] | 85 |
| 5628146f | 09:35:37.4 | <host-1> | True | 0 | 300 (voluntary) |  | [(360, 'final', 0.005)] | 0 |

## HTCondor event log (AP clock)

- 09:24:08.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "ospool__P14a-execute-limit"; JobBatchName = "probes.dag+7195166" ]
- 09:24:19.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:42149?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[<ipv6>]-9618%26alias%3dospool-ccb.osg.chtc.io%26noUDP%26sock%3dcollector1#17278428%2067.58.49.91:9618%3faddrs%3d67.58.49.91-9618+[<ipv6>]-9618%
- 09:30:23.0 `040 file_transfer` Finished transferring input files 
- 09:30:23.0 `021 remote_error` Message from starter on slot1_1@glidein_28890_202180062@<host-1>: — PREPARE_JOB (prepare-hook) succeeded (reported status 000): Using Singularity image python312.sif
- 09:30:23.0 `001 executing` Job executing on host: <<ip>:36747?CCBID=<ip>:9618%3faddrs%3d128.105.82.148-9618+[2607-f388-2200-93- — SlotName: slot1_1@glidein_28890_202180062@<host-1>; CondorScratchDir = "/tmp/jobs/892429/glide_SmvL9J/execute/dir_666248/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; Memory = 1024
- 09:31:25.0 `040 file_transfer` Started transferring output files 
- 09:31:25.0 `040 file_transfer` Finished transferring output files 
- 09:32:27.0 `040 file_transfer` Started transferring output files 
- 09:32:29.0 `040 file_transfer` Finished transferring output files 
- 09:33:31.0 `040 file_transfer` Started transferring output files 
- 09:33:32.0 `040 file_transfer` Finished transferring output files 
- 09:34:34.0 `040 file_transfer` Started transferring output files 
- 09:34:34.0 `040 file_transfer` Finished transferring output files 
- 09:35:36.0 `040 file_transfer` Started transferring output files 
- 09:35:36.0 `040 file_transfer` Finished transferring output files 
- 09:36:38.0 `040 file_transfer` Started transferring output files 
- 09:36:38.0 `040 file_transfer` Finished transferring output files 
- 09:36:39.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 31909  -  Run Bytes Sent By Job; 152121767  -

## condor_history (selected)

```
CheckpointNumber = 4
CommittedSlotTime = 63.0
CommittedSuspensionTime = 0
CommittedTime = 364
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1793111798
JobCurrentStartTransferOutputDate = 1793111798
LastRemoteHost = slot1_1@glidein_28890_202180062@<host-1>
LastRemoteWallClockTime = 745.0
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 1
NumJobCompletions = 1
NumJobMatches = 1
NumJobStarts = 1
NumOutputTransferStarts = 6
NumRestarts = 0
NumShadowStarts = 1
NumSystemHolds = 0
RemoteWallClockTime = 745.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1793111798
TransferOutStarted = 1793111798
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 31909; CedarFilesCountTotal = 16; CedarSizeBytesLastRun = 31909; CedarFilesCountLastRun = 16 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:30:24.3 fbd0f6cf start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_cr
09:30:24.3 fbd0f6cf history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:30:24.3 fbd0f6cf restore                {"ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:30:24.3 fbd0f6cf loop_start             {"restored_step": 0, "step": 0, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:31:24.4 fbd0f6cf save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
09:31:24.4 fbd0f6cf save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.005, "step": 60, "write_seconds": 0.005}
09:31:24.4 fbd0f6cf children_at_exit       {"alive": [], "exitcodes": []}
09:31:24.4 fbd0f6cf exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
09:31:26.6 f353d814 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_cr
09:31:26.6 f353d814 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:31:26.7 f353d814 restore                {"chosen": "step_00000060", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1793111484.405397, "saved_by_exec": "fbd0f6cf", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 60}
09:31:26.7 f353d814 loop_start             {"restored_step": 60, "step": 60, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:32:26.9 f353d814 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 120}
09:32:27.0 f353d814 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.126, "step": 120, "write_seconds": 0.126}
09:32:27.0 f353d814 children_at_exit       {"alive": [], "exitcodes": []}
09:32:27.0 f353d814 exit                   {"code": 85, "reason": "voluntary exit at step 120", "step": 120}
09:32:30.5 6aa7133a start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_cr
09:32:30.5 6aa7133a history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:32:30.5 6aa7133a restore                {"chosen": "step_00000120", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000120", "nested_dir_ok": true, "saved_at": 1793111547.013378, "saved_by_exec": "f353d814", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 120}
09:32:30.5 6aa7133a loop_start             {"restored_step": 120, "step": 120, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:33:30.6 6aa7133a save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 180}
09:33:30.6 6aa7133a save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 180, "write_seconds": 0.005}
09:33:30.6 6aa7133a children_at_exit       {"alive": [], "exitcodes": []}
09:33:30.6 6aa7133a exit                   {"code": 85, "reason": "voluntary exit at step 180", "step": 180}
09:33:33.7 523e1d00 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_cr
09:33:33.7 523e1d00 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:33:33.7 523e1d00 restore                {"chosen": "step_00000180", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000180", "nested_dir_ok": true, "saved_at": 1793111610.6025233, "saved_by_exec": "6aa7133a", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 180}
09:33:33.7 523e1d00 loop_start             {"restored_step": 180, "step": 180, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:34:33.8 523e1d00 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 240}
09:34:33.8 523e1d00 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.006, "step": 240, "write_seconds": 0.006}
09:34:33.8 523e1d00 children_at_exit       {"alive": [], "exitcodes": []}
09:34:33.8 523e1d00 exit                   {"code": 85, "reason": "voluntary exit at step 240", "step": 240}
09:34:35.5 475b2e28 start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 4, "python": "3.12.14", "sandbox_cr
09:34:35.5 475b2e28 history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:34:35.6 475b2e28 restore                {"chosen": "step_00000240", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000240", "nested_dir_ok": true, "saved_at": 1793111673.8008513, "saved_by_exec": "523e1d00", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 240}
09:34:35.6 475b2e28 loop_start             {"restored_step": 240, "step": 240, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:35:35.7 475b2e28 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 300}
09:35:35.7 475b2e28 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.009, "step": 300, "write_seconds": 0.008}
09:35:35.7 475b2e28 children_at_exit       {"alive": [], "exitcodes": []}
09:35:35.7 475b2e28 exit                   {"code": 85, "reason": "voluntary exit at step 300", "step": 300}
09:35:37.4 5628146f start                  {"cwd": "/srv/scratch", "machine_ad": {"GLIDEIN_Max_Walltime": "257400", "GLIDEIN_Site": "MTState-Tempest", "GLIDEIN_ToDie": "1793275707", "GLIDEIN_ToRetire": "1793239707", "MachineMaxVacateTime": "10 * 60"}, "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 5, "python": "3.12.14", "sandbox_cr
09:35:37.4 5628146f history_attached       {"ckpt_dir": "/srv/scratch/ckpt", "store": "spool"}
09:35:37.4 5628146f restore                {"chosen": "step_00000300", "ckpt_dir": "/srv/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000300", "nested_dir_ok": true, "saved_at": 1793111735.696423, "saved_by_exec": "475b2e28", "saved_on_host": "<host-1>", "saved_reason": "voluntary", "step": 300}
09:35:37.4 5628146f loop_start             {"restored_step": 300, "step": 300, "total_steps": 360, "voluntary_exit_at": [60, 120, 180, 240, 300]}
09:36:37.5 5628146f save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 360}
09:36:37.5 5628146f save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.005, "step": 360, "write_seconds": 0.004}
09:36:37.5 5628146f children_at_exit       {"alive": [], "exitcodes": []}
09:36:37.5 5628146f exit                   {"code": 0, "reason": "finished 360 steps", "step": 360}
```
