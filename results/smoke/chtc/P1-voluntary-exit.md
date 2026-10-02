# P1-voluntary-exit on chtc

**Question.** After exit 85, does the job restart in the same sandbox on the same host? Does a file outside transfer_checkpoint_files survive? Do nested directories transfer? How long is the exit-to-restart gap? Is stdout appended or truncated across restarts? Does an exit-85 restart write a new "executing" event? Does the final exit 0 complete normally?

Job: `6527261.0`   Test dir: `/home/<user>/probes/runs/smoke/chtc/P1-voluntary-exit`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 4; 'executing' events in job.log: 1; NumJobStarts=?, NumShadowStarts=? (condor_history).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 60 (saved by: voluntary).
- Restart after exit 85: gap 3 s, same host, sandbox kept (marker file survived), restored step 120 (saved by: voluntary).
- Restart after exit 85: gap 1 s, same host, sandbox kept (marker file survived), restored step 180 (saved by: voluntary).
- job.out contains output from 4 of 4 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| b6c7a236 | 13:28:59.7 | e2475 | False | 0 | None (None) |  | [(60, 'voluntary', 0.03)] | 85 |
| da88c925 | 13:30:01.3 | e2475 | True | 0 | 60 (voluntary) |  | [(120, 'voluntary', 0.014)] | 85 |
| a9e03250 | 13:31:04.1 | e2475 | True | 0 | 120 (voluntary) |  | [(180, 'voluntary', 0.027)] | 85 |
| 91ee46cf | 13:32:05.3 | e2475 | True | 0 | 180 (voluntary) |  | [(240, 'final', 0.017)] | 0 |

## HTCondor event log (AP clock)

- 13:27:57.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P1-voluntary-exit"; JobBatchName = "probes.dag+6527258" ]
- 13:28:44.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2475.chtc.wisc.edu&noUDP&sock=slot1_20_1013765_e6e2_98973>
- 13:28:58.0 `040 file_transfer` Finished transferring input files 
- 13:28:58.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_20@e2475.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3105179/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:30:00.0 `040 file_transfer` Started transferring output files 
- 13:30:00.0 `040 file_transfer` Finished transferring output files 
- 13:31:01.0 `040 file_transfer` Started transferring output files 
- 13:31:02.0 `040 file_transfer` Finished transferring output files 
- 13:32:04.0 `040 file_transfer` Started transferring output files 
- 13:32:04.0 `040 file_transfer` Finished transferring output files 
- 13:33:05.0 `040 file_transfer` Started transferring output files 
- 13:33:05.0 `040 file_transfer` Finished transferring output files 
- 13:33:06.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 35705  -  Run Bytes Sent By Job; 286336162  -

## Probe timeline (EP clock; ticks omitted)

```
13:28:59.7 b6c7a236 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3105179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "b6c7a236", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch"}
13:28:59.7 b6c7a236 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "store": "spool"}
13:28:59.7 b6c7a236 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:28:59.7 b6c7a236 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
13:30:00.0 b6c7a236 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 60}
13:30:00.0 b6c7a236 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.03, "step": 60, "write_seconds": 0.026}
13:30:00.0 b6c7a236 children_at_exit       {"alive": [], "exitcodes": []}
13:30:00.0 b6c7a236 exit                   {"code": 85, "reason": "voluntary exit at step 60", "step": 60}
13:30:01.3 da88c925 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3105179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 1, "python": "3.12.14", "sandbox_created_by": "b6c7a236", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch"}
13:30:01.3 da88c925 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "store": "spool"}
13:30:01.3 da88c925 restore                {"chosen": "step_00000060", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000060", "nested_dir_ok": true, "saved_at": 1790879400.0235186, "saved_by_exec": "b6c7a236", "saved_on_host": "e2475", "saved_reason": "voluntary
13:30:01.3 da88c925 loop_start             {"restored_step": 60, "step": 60, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
13:31:01.5 da88c925 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 120}
13:31:01.5 da88c925 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.014, "step": 120, "write_seconds": 0.012}
13:31:01.5 da88c925 children_at_exit       {"alive": [], "exitcodes": []}
13:31:01.5 da88c925 exit                   {"code": 85, "reason": "voluntary exit at step 120", "step": 120}
13:31:04.1 a9e03250 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3105179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 2, "python": "3.12.14", "sandbox_created_by": "b6c7a236", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch"}
13:31:04.1 a9e03250 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "store": "spool"}
13:31:04.1 a9e03250 restore                {"chosen": "step_00000120", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000120", "nested_dir_ok": true, "saved_at": 1790879461.4794981, "saved_by_exec": "da88c925", "saved_on_host": "e2475", "saved_reason": "voluntary
13:31:04.1 a9e03250 loop_start             {"restored_step": 120, "step": 120, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
13:32:04.2 a9e03250 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 180}
13:32:04.2 a9e03250 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 0.027, "step": 180, "write_seconds": 0.02}
13:32:04.2 a9e03250 children_at_exit       {"alive": [], "exitcodes": []}
13:32:04.2 a9e03250 exit                   {"code": 85, "reason": "voluntary exit at step 180", "step": 180}
13:32:05.3 91ee46cf start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3105179/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 3, "python": "3.12.14", "sandbox_created_by": "b6c7a236", "sandbox_marker_survived": true, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch"}
13:32:05.3 91ee46cf history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "store": "spool"}
13:32:05.3 91ee46cf restore                {"chosen": "step_00000180", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3105179/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000180", "nested_dir_ok": true, "saved_at": 1790879524.2260332, "saved_by_exec": "a9e03250", "saved_on_host": "e2475", "saved_reason": "voluntary
13:32:05.3 91ee46cf loop_start             {"restored_step": 180, "step": 180, "total_steps": 240, "voluntary_exit_at": [60, 120, 180]}
13:33:05.5 91ee46cf save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "final", "step": 240}
13:33:05.5 91ee46cf save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "final", "seconds": 0.017, "step": 240, "write_seconds": 0.013}
13:33:05.5 91ee46cf children_at_exit       {"alive": [], "exitcodes": []}
13:33:05.5 91ee46cf exit                   {"code": 0, "reason": "finished 240 steps", "step": 240}
```
