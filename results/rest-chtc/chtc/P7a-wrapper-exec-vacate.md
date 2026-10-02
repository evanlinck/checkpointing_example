# P7a-wrapper-exec-vacate on chtc

**Question.** When the executable is a shell script that execs python, does python receive the soft-kill signal?

Job: `6575116.0`   Test dir: `/home/<user>/probes/runs/rest-chtc/chtc/P7a-wrapper-exec-vacate`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=3 (condor_history).
- Restart after exit 85: gap 374 s, DIFFERENT host, sandbox NEW, restored step 5 (saved by: voluntary).
- Trigger vacate fired at 09:09:16.0 (AP clock).
- The trigger fired while no probe execution was running.
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).
- Wrapper said: WRAPPER run_exec.sh pid=142 about to exec python3 | WRAPPER run_exec.sh pid=76 about to exec python3

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| f3121493 | 09:07:36.8 | e4029 | False | 0 | None (None) |  | [(5, 'voluntary', 20.047)] | 85 |
| ba86a255 | 09:14:16.3 | e2483 | False | 1 | 5 (voluntary) |  | [] | 0 |

## HTCondor event log (AP clock)

- 09:06:56.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P7a-wrapper-exec-vacate"; JobBatchName = "probes.dag+6573176" ]
- 09:07:27.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4029.chtc.wisc.edu&noUDP&sock=slot1_14_1547003_4fd5_123353>
- 09:07:35.0 `040 file_transfer` Finished transferring input files 
- 09:07:35.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alia — SlotName: slot1_14@e4029.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_1656658/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:08:01.0 `040 file_transfer` Started transferring output files 
- 09:08:01.0 `040 file_transfer` Finished transferring output files 
- 09:08:01.0 `021 remote_error` Error from starter on slot1_14@e4029.chtc.wisc.edu: — Rescheduling self-checkpoint job after checkpoint upload because reactivating the claim would have failed.; Code 1025 Subcode 0
- 09:08:02.0 `004 evicted` Job was evicted. Code 1025 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 1050518  -  Run Bytes Sent By Job; 286337130  -  Run Bytes Received By Job; Reason: Error from slot1_14@e4029.chtc.wisc.edu: Rescheduling self-checkpoint job after checkpoint uploa
- 09:09:31.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e4086.chtc.wisc.edu&noUDP&sock=slot1_31_3546937_bcc4_128664>
- 09:09:32.0 `040 file_transfer` Finished transferring input files 
- 09:09:32.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 0  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            :     1136  20
- 09:10:11.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2483.chtc.wisc.edu&noUDP&sock=slot1_47_2337346_7400_103832>
- 09:14:15.0 `040 file_transfer` Finished transferring input files 
- 09:14:15.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_47@e2483.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3362134/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 09:14:16.0 `040 file_transfer` Started transferring output files 
- 09:14:16.0 `040 file_transfer` Finished transferring output files 
- 09:14:16.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 1051548  -  Run Bytes Sent By Job; 287387680 

## condor_history (selected)

```
CheckpointNumber = 0
CommittedSlotTime = 245.0
CommittedSuspensionTime = 0
CommittedTime = 270
ExitBySignal = false
ExitCode = 0
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790950456
JobCurrentStartTransferOutputDate = 1790950456
LastRemoteHost = slot1_47@e2483.chtc.wisc.edu
LastRemoteWallClockTime = 245.0
LastVacateTime = 1790950081
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 3
NumJobCompletions = 1
NumJobMatches = 3
NumJobStarts = 2
NumOutputTransferStarts = 2
NumRestarts = 0
NumShadowStarts = 3
NumSystemHolds = 0
NumVacates = 2
NumVacatesByReason = [ ScheddVacate = 1; SuccessfulCheckpoint = 1 ]
NumVacatesByReasonPreExecution = [ ScheddVacate = 1 ]
NumVacatesPreExecution = 1
RemoteWallClockTime = 282.0
SuccessCheckpointExitCode = 85
TransferCheckpoint = ckpt
TransferOutFinished = 1790950456
TransferOutStarted = 1790950456
TransferOutput = ckpt,out
TransferOutputStats = [ CedarSizeBytesTotal = 2102066; CedarFilesCountTotal = 19; CedarSizeBytesLastRun = 1051548; CedarFilesCountLastRun = 10 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
09:07:36.8 f3121493 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_1656658/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "f3121493", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_1656658/scratch"}
09:07:36.8 f3121493 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1656658/scratch/ckpt", "store": "spool"}
09:07:36.8 f3121493 restore                {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_1656658/scratch/ckpt", "exists": true, "found": false, "latest_pointer": null}
09:07:36.8 f3121493 loop_start             {"restored_step": 0, "step": 0, "total_steps": 240, "voluntary_exit_at": [5]}
09:07:41.8 f3121493 save_start             {"ckpt_files": 1, "ckpt_mb": 1, "reason": "voluntary", "step": 5}
09:08:01.8 f3121493 save_done              {"bytes": 1048576, "dir_fsync_ok": true, "reason": "voluntary", "seconds": 20.047, "step": 5, "write_seconds": 0.026}
09:08:01.8 f3121493 children_at_exit       {"alive": [], "exitcodes": []}
09:08:01.8 f3121493 exit                   {"code": 85, "reason": "voluntary exit at step 5", "step": 5}
09:14:16.3 ba86a255 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3362134/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "ba86a255", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3362134/scratch"}
09:14:16.3 ba86a255 history_attached       {"ckpt_dir": "/var/lib/condor/execute/slot1/dir_3362134/scratch/ckpt", "store": "spool"}
09:14:16.3 ba86a255 restore                {"chosen": "step_00000005", "ckpt_dir": "/var/lib/condor/execute/slot1/dir_3362134/scratch/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000005", "nested_dir_ok": true, "saved_at": 1790950061.8255377, "saved_by_exec": "f3121493", "saved_on_host": "e4029", "saved_reason": "voluntary
09:14:16.3 ba86a255 exit                   {"code": 0, "reason": "rescheduled (NumJobStarts=1, restored step 5, sandbox marker survived=False); --exit-on-restart", "step": 5}
```

## Trigger log (AP clock)

```
08:49:30.8 {"action": "waiting", "after": 90.0, "log": "/home/<user>/probes/runs/rest-chtc/chtc/P7a-wrapper-exec-vacate/job.log", "trigger": "vacate"}
09:09:16.0 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790950055.0, "job": "6575116.0", "last_event": "evicted", "trigger": "vacate"}
09:09:16.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6575116.0"], "output": "\nJob 6575116.0 not running to be vacated\n", "rc": 1}
09:09:32.0 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "6575116.0"], "output": "Job 6575116.0 vacated\n", "rc": 0}
09:09:32.0 {"action": "done"}
```
