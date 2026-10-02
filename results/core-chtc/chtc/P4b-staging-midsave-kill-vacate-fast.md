# P4b-staging-midsave-kill-vacate-fast on chtc

**Question.** After a hard kill (condor_vacate_job -fast) in the middle of writing a 1 GB checkpoint to /staging, does the next start find a stale .tmp directory, and does it correctly resume from the previous complete checkpoint?

Job: `6527324.0`   Test dir: `runs/core-chtc/chtc/P4b-staging-midsave-kill-vacate-fast`

## Observations

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:55, Sys 0 00:07:35  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:56, Sys 0 00:07:45  -  Total Remote Usage;)
- Executions seen by the probe: 2; 'executing' events in job.log: 2 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=2, NumShadowStarts=2 (condor_history).
- Restart after ended without an exit record: gap 91 s, DIFFERENT host, sandbox NEW, restored step 8 (saved by: periodic), stale .tmp found: ['step_00000009.tmp'].
- Trigger vacate-fast fired at 13:55:39.3 (AP clock).
- Evicted execution logged NO signal (hard kill, or signal not delivered); its last logged moment was +5.7 s relative to the trigger (logging is every 1-10 s, so a negative value is normal for an immediate kill).
- Next execution restored step 8 (saved by: periodic).
- job.out contains output from 2 of 2 executions (tells whether stdout is kept across restarts).

## Executions

| exec | start | host | sandbox kept | NumJobStarts | restored | signal | saves (step, reason, s) | exit |
|---|---|---|---|---|---|---|---|---|
| c0f790fd | 13:53:32.6 | e2481 | False | 0 | None (None) |  | [(1, 'periodic', 25.311), (2, 'periodic', 14.323), (3, 'periodic', 13.991), (4, 'periodic', 11.213), (5, 'periodic', 10.149), (6, 'periodic', 13.546), (7, 'periodic', 11.215), (8, 'periodic', 16.345)] | none (killed?) |
| ae52dc46 | 13:57:15.9 | e2473 | False | 1 | 8 (periodic) |  | [(9, 'periodic', 10.666), (10, 'periodic', 12.055), (11, 'periodic', 24.339), (12, 'periodic', 10.901), (13, 'periodic', 7.554), (14, 'periodic', 13.04), (15, 'periodic', 12.131), (16, 'periodic', 17.022), (17, 'periodic', 16.727), (18, 'periodic', 13.213), (19, 'periodic', 16.042), (20, 'periodic', 9.48), (21, 'periodic', 10.071), (22, 'periodic', 10.506), (23, 'periodic', 10.532), (24, 'periodic', 17.734), (25, 'periodic', 13.281), (26, 'periodic', 8.553), (27, 'periodic', 10.165), (28, 'periodic', 9.237), (29, 'periodic', 10.186), (30, 'periodic', 10.78), (31, 'periodic', 11.374), (32, 'periodic', 12.116), (33, 'periodic', 10.742), (34, 'periodic', 8.59), (35, 'periodic', 10.268), (36, 'periodic', 10.285), (37, 'periodic', 10.072), (38, 'periodic', 12.387), (39, 'periodic', 12.858), (40, 'periodic', 9.694), (41, 'periodic', 14.627), (42, 'periodic', 12.388), (43, 'periodic', 10.124), (44, 'periodic', 10.454), (45, 'periodic', 11.328), (46, 'periodic', 16.454), (47, 'periodic', 8.993), (48, 'periodic', 12.256), (49, 'periodic', 12.102), (50, 'periodic', 11.568), (51, 'periodic', 10.65), (52, 'periodic', 11.666), (53, 'periodic', 9.905), (54, 'periodic', 9.885), (55, 'periodic', 10.677), (56, 'periodic', 11.649), (57, 'periodic', 10.751), (58, 'periodic', 13.18), (59, 'periodic', 11.991), (60, 'periodic', 11.478), (61, 'periodic', 11.503), (62, 'periodic', 10.903), (63, 'periodic', 10.579), (64, 'periodic', 10.22), (65, 'periodic', 11.529), (66, 'periodic', 9.228), (67, 'periodic', 10.749), (68, 'periodic', 10.834), (69, 'periodic', 13.109), (70, 'periodic', 14.5), (71, 'periodic', 8.956), (72, 'periodic', 12.016), (73, 'periodic', 13.79), (74, 'periodic', 11.278), (75, 'periodic', 12.877), (76, 'periodic', 12.586), (77, 'periodic', 14.045), (78, 'periodic', 18.992), (79, 'periodic', 10.735), (80, 'periodic', 9.249), (81, 'periodic', 11.504), (82, 'periodic', 7.69), (83, 'periodic', 9.14), (84, 'periodic', 11.22), (85, 'periodic', 11.761), (86, 'periodic', 11.657), (87, 'periodic', 20.329), (88, 'periodic', 11.855), (89, 'periodic', 9.801), (90, 'periodic', 10.969), (91, 'periodic', 11.673), (92, 'periodic', 13.792), (93, 'periodic', 9.977), (94, 'periodic', 10.765), (95, 'periodic', 9.902), (96, 'periodic', 11.041), (97, 'periodic', 9.473), (98, 'periodic', 8.138), (99, 'periodic', 9.796), (100, 'periodic', 9.692), (101, 'periodic', 8.845), (102, 'periodic', 9.773), (103, 'periodic', 10.534), (104, 'periodic', 9.745), (105, 'periodic', 9.916), (106, 'periodic', 10.559), (107, 'periodic', 10.154), (108, 'periodic', 12.981), (109, 'periodic', 11.363), (110, 'periodic', 12.271), (111, 'periodic', 9.713), (112, 'periodic', 10.268), (113, 'periodic', 17.175), (114, 'periodic', 8.095), (115, 'periodic', 9.914), (116, 'periodic', 10.779), (117, 'periodic', 10.784), (118, 'periodic', 10.766), (119, 'periodic', 12.062), (120, 'periodic', 11.837), (121, 'periodic', 9.369), (122, 'periodic', 12.14), (123, 'periodic', 11.398), (124, 'periodic', 11.096), (125, 'periodic', 12.776), (126, 'periodic', 11.325), (127, 'periodic', 11.095), (128, 'periodic', 11.73), (129, 'periodic', 16.868), (130, 'periodic', 12.718), (131, 'periodic', 10.31), (132, 'periodic', 14.518), (133, 'periodic', 10.599), (134, 'periodic', 14.202), (135, 'periodic', 9.382), (136, 'periodic', 10.188), (137, 'periodic', 15.93), (138, 'periodic', 12.383), (139, 'periodic', 15.01), (140, 'periodic', 15.281), (141, 'periodic', 9.7), (142, 'periodic', 11.578), (143, 'periodic', 9.089), (144, 'periodic', 12.366), (145, 'periodic', 12.442), (146, 'periodic', 10.447), (147, 'periodic', 13.032), (148, 'periodic', 9.194), (149, 'periodic', 11.075), (150, 'periodic', 11.516), (151, 'periodic', 9.865), (152, 'periodic', 10.705), (153, 'periodic', 9.322), (154, 'periodic', 12.202), (155, 'periodic', 9.07), (156, 'periodic', 36.961), (157, 'periodic', 10.387), (158, 'periodic', 8.359), (159, 'periodic', 11.221), (160, 'periodic', 8.816), (161, 'periodic', 7.36), (162, 'periodic', 9.346), (163, 'periodic', 8.599), (164, 'periodic', 10.325), (165, 'periodic', 11.968), (166, 'periodic', 9.008), (167, 'periodic', 11.218), (168, 'periodic', 11.749), (169, 'periodic', 9.882), (170, 'periodic', 7.942), (171, 'periodic', 14.102), (172, 'periodic', 9.781), (173, 'periodic', 8.786), (174, 'periodic', 8.672), (175, 'periodic', 10.486), (176, 'periodic', 11.074), (177, 'periodic', 8.459), (178, 'periodic', 7.733), (179, 'periodic', 8.421), (180, 'periodic', 9.535), (181, 'periodic', 8.184), (182, 'periodic', 8.365), (183, 'periodic', 8.545), (184, 'periodic', 8.966), (185, 'periodic', 10.511), (186, 'periodic', 8.636), (187, 'periodic', 10.638), (188, 'periodic', 11.863), (189, 'periodic', 9.78), (190, 'periodic', 7.642), (191, 'periodic', 10.114), (192, 'periodic', 8.696), (193, 'periodic', 9.303), (194, 'periodic', 7.586), (195, 'periodic', 7.048), (196, 'periodic', 6.775), (197, 'periodic', 7.998), (198, 'periodic', 9.707), (199, 'periodic', 10.012), (200, 'periodic', 9.463), (201, 'periodic', 8.445), (202, 'periodic', 9.437), (203, 'periodic', 10.066), (204, 'periodic', 10.734), (205, 'periodic', 10.52), (206, 'periodic', 9.554), (207, 'periodic', 11.293), (208, 'periodic', 12.889), (209, 'periodic', 9.373), (210, 'periodic', 10.184), (211, 'periodic', 12.936), (212, 'periodic', 9.02), (213, 'periodic', 10.472), (214, 'periodic', 16.604), (215, 'periodic', 16.24), (216, 'periodic', 11.988), (217, 'periodic', 13.706), (218, 'periodic', 7.735), (219, 'periodic', 7.293), (220, 'periodic', 11.411), (221, 'periodic', 6.808), (222, 'periodic', 11.184), (223, 'periodic', 11.523), (224, 'periodic', 9.691), (225, 'periodic', 8.962), (226, 'periodic', 9.703), (227, 'periodic', 9.682), (228, 'periodic', 9.662), (229, 'periodic', 10.045), (230, 'periodic', 8.285), (231, 'periodic', 8.387), (232, 'periodic', 10.61), (233, 'periodic', 23.705), (234, 'periodic', 9.19), (235, 'periodic', 8.15), (236, 'periodic', 10.125), (237, 'periodic', 9.065), (238, 'periodic', 11.361), (239, 'periodic', 10.867), (240, 'periodic', 45.017), (241, 'periodic', 12.098), (242, 'periodic', 10.734), (243, 'periodic', 9.782), (244, 'periodic', 10.15), (245, 'periodic', 9.75), (246, 'periodic', 10.785), (247, 'periodic', 10.931), (248, 'periodic', 11.041), (249, 'periodic', 10.849), (250, 'periodic', 12.226), (251, 'periodic', 11.398), (252, 'periodic', 10.256), (253, 'periodic', 10.556), (254, 'periodic', 11.605), (255, 'periodic', 9.721), (256, 'periodic', 9.769), (257, 'periodic', 9.027), (258, 'periodic', 12.018), (259, 'periodic', 9.862), (260, 'periodic', 10.508), (261, 'periodic', 10.189), (262, 'periodic', 10.857), (263, 'periodic', 10.529), (264, 'periodic', 9.443), (265, 'periodic', 10.813), (266, 'periodic', 10.373), (267, 'periodic', 11.655), (268, 'periodic', 11.753), (269, 'periodic', 8.806), (270, 'periodic', 9.912), (271, 'periodic', 6.69), (272, 'periodic', 7.811), (273, 'periodic', 9.971), (274, 'periodic', 10.202), (275, 'periodic', 9.875), (276, 'periodic', 18.053), (277, 'periodic', 10.848), (278, 'periodic', 10.806), (279, 'periodic', 11.827), (280, 'periodic', 8.909), (281, 'periodic', 10.933), (282, 'periodic', 11.77), (283, 'periodic', 9.696), (284, 'periodic', 10.825), (285, 'periodic', 9.915), (286, 'periodic', 22.548), (287, 'periodic', 9.935), (288, 'periodic', 11.896), (289, 'periodic', 12.678), (290, 'periodic', 9.645), (291, 'periodic', 54.197), (292, 'periodic', 9.807), (293, 'periodic', 9.277), (294, 'periodic', 9.056), (295, 'periodic', 9.972), (296, 'periodic', 11.223), (297, 'periodic', 9.99), (298, 'periodic', 9.678), (299, 'periodic', 9.112), (300, 'periodic', 10.821), (300, 'final', 12.211)] | 0 |

## HTCondor event log (AP clock)

- 13:53:10.0 `000 submitted` Job submitted from host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&al — [ DAGNodeName = "chtc__P4b-staging-midsave-kill-vacate-fast"; JobBatchName = "probes.dag+6527287" ]
- 13:53:27.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2481.chtc.wisc.edu&noUDP&sock=slot1_9_3564670_3d75_92183>
- 13:53:31.0 `040 file_transfer` Finished transferring input files 
- 13:53:31.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_9@e2481.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3378175/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 13:55:48.0 `004 evicted` Job was evicted. Code 1022 Subcode 0 — (0) CPU times; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; 0  -  Run Bytes Sent By Job; 286336878  -  Run Bytes Received By Job; Reason: Job vacated by schedd; Cpus                 :        0        1         1; Disk (KB)            :   27
- 13:56:59.0 `040 file_transfer` Started transferring input files — Transferring to host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e2473.chtc.wisc.edu&noUDP&sock=slot1_49_342642_0927_91286>
- 13:57:14.0 `040 file_transfer` Finished transferring input files 
- 13:57:15.0 `001 executing` Job executing on host: <<ip>:9618?addrs=<ip>-9618+[<ipv6>]-9618&alias=e — SlotName: slot1_49@e2473.chtc.wisc.edu; CondorScratchDir = "/var/lib/condor/execute/slot1/dir_3327853/scratch"; Cpus = 1; Disk = 2097152; GPUs = 0; IoHeavy = 0; Memory = 1024
- 14:59:04.0 `040 file_transfer` Started transferring output files 
- 14:59:04.0 `040 file_transfer` Finished transferring output files 
- 14:59:04.0 `005 terminated` Job terminated. — (1) Normal termination (return value 0); Usr 0 00:00:55, Sys 0 00:07:35  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:56, Sys 0 00:07:45  -  Total Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Local Usage; 201836  -  Run Bytes Sent By Job; 286336878  

## condor_history (selected)

```
CommittedSlotTime = 3726.0
CommittedSuspensionTime = 0
CommittedTime = 3726
ExitBySignal = false
ExitCode = 0
ExitReason = died on signal 9 (Killed)
ExitSignal = 9
ExitStatus = 0
JobCurrentFinishTransferOutputDate = 1790884744
JobCurrentStartTransferOutputDate = 1790884744
LastRemoteHost = slot1_49@e2473.chtc.wisc.edu
LastRemoteWallClockTime = 3726.0
LastVacateTime = 1790880941
NumCkpts = 0
NumCkpts_RAW = 0
NumInputTransferStarts = 2
NumJobCompletions = 1
NumJobMatches = 2
NumJobStarts = 2
NumOutputTransferStarts = 1
NumRestarts = 0
NumShadowStarts = 2
NumSystemHolds = 0
NumVacates = 1
NumVacatesByReason = [ ScheddVacate = 1 ]
RemoteWallClockTime = 3870.0
SuccessCheckpointExitCode = 85
TransferOutFinished = 1790884744
TransferOutStarted = 1790884744
TransferOutput = out
TransferOutputStats = [ CedarSizeBytesTotal = 201836; CedarFilesCountTotal = 2; CedarSizeBytesLastRun = 201836; CedarFilesCountLastRun = 2 ]
WantFTOnCheckpoint = true
WhenToTransferOutput = ON_EXIT
```

## Probe timeline (EP clock; ticks omitted)

```
13:53:32.6 c0f790fd start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3378175/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "c0f790fd", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3378175/scratch"}
13:53:33.6 c0f790fd history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527324.0/ckpt", "store": "staging"}
13:53:33.8 c0f790fd restore                {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527324.0/ckpt", "exists": true, "found": false, "latest_pointer": null}
13:53:33.8 c0f790fd loop_start             {"restored_step": 0, "step": 0, "total_steps": 300, "voluntary_exit_at": []}
13:53:36.4 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 1}
13:54:01.8 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 25.311, "step": 1, "write_seconds": 24.883}
13:54:03.4 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 2}
13:54:17.7 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.323, "step": 2, "write_seconds": 14.193}
13:54:20.2 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 3}
13:54:34.2 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.991, "step": 3, "write_seconds": 12.715}
13:54:35.6 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 4}
13:54:46.8 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.213, "step": 4, "write_seconds": 10.775}
13:54:48.2 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 5}
13:54:58.4 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.149, "step": 5, "write_seconds": 8.946}
13:54:59.7 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 6}
13:55:13.3 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.546, "step": 6, "write_seconds": 12.499}
13:55:14.5 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 7}
13:55:25.7 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.215, "step": 7, "write_seconds": 10.531}
13:55:27.1 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 8}
13:55:43.5 c0f790fd save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.345, "step": 8, "write_seconds": 16.049}
13:55:44.0 c0f790fd save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 9}
13:57:15.9 ae52dc46 start                  {"cwd": "/var/lib/condor/execute/slot1/dir_3327853/scratch", "mode": "run", "ppid": 1, "previous_starts_in_sandbox": 0, "python": "3.12.14", "sandbox_created_by": "ae52dc46", "sandbox_marker_survived": false, "scratch_dir": "/var/lib/condor/execute/slot1/dir_3327853/scratch"}
13:57:15.9 ae52dc46 history_attached       {"ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527324.0/ckpt", "store": "staging"}
13:57:16.6 ae52dc46 restore                {"chosen": "step_00000008", "ckpt_dir": "/staging/<user>/ckpt-probes/runs/6527324.0/ckpt", "exists": true, "found": true, "latest_pointer": "step_00000008", "nested_dir_ok": true, "saved_at": 1790880942.4564204, "saved_by_exec": "c0f790fd", "saved_on_host": "e2481", "saved_reason": "periodic", "st
13:57:16.8 ae52dc46 loop_start             {"restored_step": 8, "step": 8, "total_steps": 300, "voluntary_exit_at": []}
13:57:19.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 9}
13:57:29.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.666, "step": 9, "write_seconds": 10.373}
13:57:30.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 10}
13:57:43.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.055, "step": 10, "write_seconds": 11.612}
13:57:44.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 11}
13:58:08.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 24.339, "step": 11, "write_seconds": 22.964}
13:58:10.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 12}
13:58:21.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.901, "step": 12, "write_seconds": 10.629}
13:58:22.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 13}
13:58:30.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.554, "step": 13, "write_seconds": 7.294}
13:58:31.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 14}
13:58:44.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.04, "step": 14, "write_seconds": 8.564}
13:58:46.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 15}
13:58:58.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.131, "step": 15, "write_seconds": 11.744}
13:58:59.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 16}
13:59:16.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 17.022, "step": 16, "write_seconds": 13.495}
13:59:18.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 17}
13:59:35.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.727, "step": 17, "write_seconds": 15.107}
13:59:36.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 18}
13:59:49.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.213, "step": 18, "write_seconds": 12.302}
13:59:53.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 19}
14:00:09.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.042, "step": 19, "write_seconds": 15.44}
14:00:10.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 20}
14:00:20.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.48, "step": 20, "write_seconds": 9.168}
14:00:21.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 21}
14:00:31.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.071, "step": 21, "write_seconds": 9.276}
14:00:33.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 22}
14:00:44.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.506, "step": 22, "write_seconds": 8.903}
14:00:46.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 23}
14:00:56.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.532, "step": 23, "write_seconds": 9.104}
14:00:58.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 24}
14:01:16.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 17.734, "step": 24, "write_seconds": 17.545}
14:01:17.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 25}
14:01:30.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.281, "step": 25, "write_seconds": 13.094}
14:01:31.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 26}
14:01:40.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.553, "step": 26, "write_seconds": 7.891}
14:01:41.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 27}
14:01:51.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.165, "step": 27, "write_seconds": 9.442}
14:01:53.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 28}
14:02:02.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.237, "step": 28, "write_seconds": 9.021}
14:02:03.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 29}
14:02:13.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.186, "step": 29, "write_seconds": 9.897}
14:02:15.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 30}
14:02:25.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.78, "step": 30, "write_seconds": 9.7}
14:02:27.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 31}
14:02:38.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.374, "step": 31, "write_seconds": 10.92}
14:02:40.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 32}
14:02:52.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.116, "step": 32, "write_seconds": 11.292}
14:02:54.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 33}
14:03:05.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.742, "step": 33, "write_seconds": 10.396}
14:03:06.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 34}
14:03:15.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.59, "step": 34, "write_seconds": 8.057}
14:03:16.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 35}
14:03:26.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.268, "step": 35, "write_seconds": 9.29}
14:03:27.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 36}
14:03:37.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.285, "step": 36, "write_seconds": 9.94}
14:03:39.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 37}
14:03:49.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.072, "step": 37, "write_seconds": 9.661}
14:03:50.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 38}
14:04:02.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.387, "step": 38, "write_seconds": 11.485}
14:04:04.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 39}
14:04:17.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.858, "step": 39, "write_seconds": 12.311}
14:04:18.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 40}
14:04:28.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.694, "step": 40, "write_seconds": 9.239}
14:04:29.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 41}
14:04:44.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.627, "step": 41, "write_seconds": 14.194}
14:04:46.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 42}
14:04:58.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.388, "step": 42, "write_seconds": 11.656}
14:05:00.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 43}
14:05:10.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.124, "step": 43, "write_seconds": 9.896}
14:05:12.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 44}
14:05:22.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.454, "step": 44, "write_seconds": 9.977}
14:05:24.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 45}
14:05:35.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.328, "step": 45, "write_seconds": 10.436}
14:05:36.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 46}
14:05:53.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.454, "step": 46, "write_seconds": 13.612}
14:05:57.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 47}
14:06:06.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.993, "step": 47, "write_seconds": 8.505}
14:06:08.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 48}
14:06:20.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.256, "step": 48, "write_seconds": 11.967}
14:06:21.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 49}
14:06:33.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.102, "step": 49, "write_seconds": 10.51}
14:06:35.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 50}
14:06:46.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.568, "step": 50, "write_seconds": 10.645}
14:06:48.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 51}
14:06:58.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.65, "step": 51, "write_seconds": 10.201}
14:07:00.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 52}
14:07:12.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.666, "step": 52, "write_seconds": 10.833}
14:07:13.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 53}
14:07:23.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.905, "step": 53, "write_seconds": 9.545}
14:07:24.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 54}
14:07:34.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.885, "step": 54, "write_seconds": 9.6}
14:07:35.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 55}
14:07:46.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.677, "step": 55, "write_seconds": 10.089}
14:07:47.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 56}
14:07:59.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.649, "step": 56, "write_seconds": 10.793}
14:08:00.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 57}
14:08:11.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.751, "step": 57, "write_seconds": 10.46}
14:08:12.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 58}
14:08:25.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.18, "step": 58, "write_seconds": 12.648}
14:08:27.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 59}
14:08:39.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.991, "step": 59, "write_seconds": 11.631}
14:08:40.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 60}
14:08:52.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.478, "step": 60, "write_seconds": 10.637}
14:08:53.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 61}
14:09:04.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.503, "step": 61, "write_seconds": 10.958}
14:09:06.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 62}
14:09:17.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.903, "step": 62, "write_seconds": 9.775}
14:09:18.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 63}
14:09:29.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.579, "step": 63, "write_seconds": 10.231}
14:09:30.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 64}
14:09:40.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.22, "step": 64, "write_seconds": 9.444}
14:09:42.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 65}
14:09:53.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.529, "step": 65, "write_seconds": 11.36}
14:09:54.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 66}
14:10:04.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.228, "step": 66, "write_seconds": 8.763}
14:10:05.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 67}
14:10:16.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.749, "step": 67, "write_seconds": 10.333}
14:10:17.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 68}
14:10:28.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.834, "step": 68, "write_seconds": 10.346}
14:10:29.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 69}
14:10:42.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.109, "step": 69, "write_seconds": 12.752}
14:10:44.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 70}
14:10:58.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.5, "step": 70, "write_seconds": 13.765}
14:10:59.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 71}
14:11:08.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.956, "step": 71, "write_seconds": 8.542}
14:11:10.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 72}
14:11:22.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.016, "step": 72, "write_seconds": 11.472}
14:11:23.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 73}
14:11:37.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.79, "step": 73, "write_seconds": 13.19}
14:11:38.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 74}
14:11:49.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.278, "step": 74, "write_seconds": 10.341}
14:11:51.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 75}
14:12:04.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.877, "step": 75, "write_seconds": 12.082}
14:12:05.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 76}
14:12:18.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.586, "step": 76, "write_seconds": 12.119}
14:12:19.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 77}
14:12:33.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.045, "step": 77, "write_seconds": 12.403}
14:12:35.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 78}
14:12:54.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 18.992, "step": 78, "write_seconds": 17.356}
14:12:56.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 79}
14:13:06.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.735, "step": 79, "write_seconds": 10.035}
14:13:08.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 80}
14:13:17.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.249, "step": 80, "write_seconds": 8.872}
14:13:18.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 81}
14:13:30.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.504, "step": 81, "write_seconds": 11.046}
14:13:31.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 82}
14:13:39.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.69, "step": 82, "write_seconds": 7.091}
14:13:40.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 83}
14:13:49.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.14, "step": 83, "write_seconds": 8.814}
14:13:50.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 84}
14:14:01.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.22, "step": 84, "write_seconds": 9.785}
14:14:03.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 85}
14:14:14.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.761, "step": 85, "write_seconds": 11.178}
14:14:16.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 86}
14:14:28.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.657, "step": 86, "write_seconds": 11.383}
14:14:29.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 87}
14:14:49.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 20.329, "step": 87, "write_seconds": 11.236}
14:14:53.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 88}
14:15:05.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.855, "step": 88, "write_seconds": 11.666}
14:15:06.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 89}
14:15:16.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.801, "step": 89, "write_seconds": 9.375}
14:15:17.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 90}
14:15:28.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.969, "step": 90, "write_seconds": 10.213}
14:15:30.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 91}
14:15:41.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.673, "step": 91, "write_seconds": 11.124}
14:15:42.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 92}
14:15:56.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.792, "step": 92, "write_seconds": 12.422}
14:15:58.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 93}
14:16:07.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.977, "step": 93, "write_seconds": 9.051}
14:16:09.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 94}
14:16:20.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.765, "step": 94, "write_seconds": 10.096}
14:16:21.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 95}
14:16:31.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.902, "step": 95, "write_seconds": 9.128}
14:16:32.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 96}
14:16:43.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.041, "step": 96, "write_seconds": 10.657}
14:16:45.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 97}
14:16:54.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.473, "step": 97, "write_seconds": 9.128}
14:16:55.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 98}
14:17:04.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.138, "step": 98, "write_seconds": 7.72}
14:17:05.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 99}
14:17:14.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.796, "step": 99, "write_seconds": 9.297}
14:17:16.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 100}
14:17:25.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.692, "step": 100, "write_seconds": 9.383}
14:17:27.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 101}
14:17:36.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.845, "step": 101, "write_seconds": 8.598}
14:17:37.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 102}
14:17:47.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.773, "step": 102, "write_seconds": 8.609}
14:17:48.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 103}
14:17:59.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.534, "step": 103, "write_seconds": 10.175}
14:18:00.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 104}
14:18:10.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.745, "step": 104, "write_seconds": 9.14}
14:18:11.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 105}
14:18:21.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.916, "step": 105, "write_seconds": 9.202}
14:18:22.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 106}
14:18:33.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.559, "step": 106, "write_seconds": 10.308}
14:18:34.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 107}
14:18:44.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.154, "step": 107, "write_seconds": 9.838}
14:18:46.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 108}
14:18:59.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.981, "step": 108, "write_seconds": 10.684}
14:19:00.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 109}
14:19:12.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.363, "step": 109, "write_seconds": 10.062}
14:19:13.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 110}
14:19:25.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.271, "step": 110, "write_seconds": 10.843}
14:19:27.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 111}
14:19:36.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.713, "step": 111, "write_seconds": 9.548}
14:19:38.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 112}
14:19:48.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.268, "step": 112, "write_seconds": 9.376}
14:19:49.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 113}
14:20:06.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 17.175, "step": 113, "write_seconds": 15.634}
14:20:08.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 114}
14:20:16.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.095, "step": 114, "write_seconds": 7.76}
14:20:17.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 115}
14:20:27.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.914, "step": 115, "write_seconds": 8.811}
14:20:28.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 116}
14:20:39.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.779, "step": 116, "write_seconds": 10.154}
14:20:40.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 117}
14:20:51.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.784, "step": 117, "write_seconds": 10.055}
14:20:52.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 118}
14:21:03.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.766, "step": 118, "write_seconds": 9.974}
14:21:04.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 119}
14:21:16.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.062, "step": 119, "write_seconds": 11.459}
14:21:17.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 120}
14:21:29.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.837, "step": 120, "write_seconds": 11.53}
14:21:30.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 121}
14:21:40.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.369, "step": 121, "write_seconds": 8.978}
14:21:41.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 122}
14:21:53.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.14, "step": 122, "write_seconds": 11.576}
14:21:55.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 123}
14:22:06.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.398, "step": 123, "write_seconds": 10.964}
14:22:08.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 124}
14:22:19.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.096, "step": 124, "write_seconds": 10.484}
14:22:21.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 125}
14:22:33.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.776, "step": 125, "write_seconds": 12.307}
14:22:35.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 126}
14:22:46.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.325, "step": 126, "write_seconds": 10.981}
14:22:47.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 127}
14:22:58.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.095, "step": 127, "write_seconds": 10.327}
14:23:00.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 128}
14:23:11.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.73, "step": 128, "write_seconds": 10.76}
14:23:13.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 129}
14:23:29.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.868, "step": 129, "write_seconds": 16.47}
14:23:31.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 130}
14:23:44.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.718, "step": 130, "write_seconds": 11.799}
14:23:46.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 131}
14:23:56.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.31, "step": 131, "write_seconds": 9.143}
14:23:58.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 132}
14:24:12.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.518, "step": 132, "write_seconds": 12.756}
14:24:13.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 133}
14:24:24.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.599, "step": 133, "write_seconds": 9.097}
14:24:25.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 134}
14:24:39.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.202, "step": 134, "write_seconds": 12.41}
14:24:41.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 135}
14:24:50.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.382, "step": 135, "write_seconds": 8.876}
14:24:52.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 136}
14:25:02.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.188, "step": 136, "write_seconds": 9.549}
14:25:03.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 137}
14:25:19.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 15.93, "step": 137, "write_seconds": 14.103}
14:25:21.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 138}
14:25:33.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.383, "step": 138, "write_seconds": 11.798}
14:25:34.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 139}
14:25:49.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 15.01, "step": 139, "write_seconds": 14.413}
14:25:51.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 140}
14:26:06.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 15.281, "step": 140, "write_seconds": 14.447}
14:26:07.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 141}
14:26:17.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.7, "step": 141, "write_seconds": 9.082}
14:26:18.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 142}
14:26:30.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.578, "step": 142, "write_seconds": 11.093}
14:26:31.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 143}
14:26:40.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.089, "step": 143, "write_seconds": 8.746}
14:26:41.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 144}
14:26:54.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.366, "step": 144, "write_seconds": 11.657}
14:26:56.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 145}
14:27:08.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.442, "step": 145, "write_seconds": 12.273}
14:27:09.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 146}
14:27:20.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.447, "step": 146, "write_seconds": 9.223}
14:27:21.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 147}
14:27:34.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.032, "step": 147, "write_seconds": 11.476}
14:27:36.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 148}
14:27:45.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.194, "step": 148, "write_seconds": 8.89}
14:27:46.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 149}
14:27:57.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.075, "step": 149, "write_seconds": 10.459}
14:27:59.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 150}
14:28:10.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.516, "step": 150, "write_seconds": 10.327}
14:28:11.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 151}
14:28:21.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.865, "step": 151, "write_seconds": 9.338}
14:28:23.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 152}
14:28:33.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.705, "step": 152, "write_seconds": 9.804}
14:28:35.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 153}
14:28:44.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.322, "step": 153, "write_seconds": 9.033}
14:28:45.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 154}
14:28:58.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.202, "step": 154, "write_seconds": 11.722}
14:28:59.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 155}
14:29:08.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.07, "step": 155, "write_seconds": 8.531}
14:29:09.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 156}
14:29:46.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 36.961, "step": 156, "write_seconds": 31.752}
14:29:47.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 157}
14:29:58.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.387, "step": 157, "write_seconds": 9.871}
14:29:59.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 158}
14:30:07.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.359, "step": 158, "write_seconds": 8.024}
14:30:08.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 159}
14:30:20.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.221, "step": 159, "write_seconds": 10.599}
14:30:21.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 160}
14:30:30.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.816, "step": 160, "write_seconds": 8.128}
14:30:31.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 161}
14:30:38.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.36, "step": 161, "write_seconds": 7.183}
14:30:39.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 162}
14:30:49.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.346, "step": 162, "write_seconds": 8.661}
14:30:50.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 163}
14:30:59.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.599, "step": 163, "write_seconds": 7.794}
14:31:00.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 164}
14:31:10.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.325, "step": 164, "write_seconds": 9.575}
14:31:12.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 165}
14:31:23.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.968, "step": 165, "write_seconds": 11.283}
14:31:25.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 166}
14:31:34.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.008, "step": 166, "write_seconds": 8.328}
14:31:35.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 167}
14:31:47.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.218, "step": 167, "write_seconds": 10.37}
14:31:48.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 168}
14:32:00.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.749, "step": 168, "write_seconds": 10.755}
14:32:01.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 169}
14:32:11.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.882, "step": 169, "write_seconds": 9.425}
14:32:12.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 170}
14:32:20.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.942, "step": 170, "write_seconds": 7.71}
14:32:22.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 171}
14:32:36.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 14.102, "step": 171, "write_seconds": 13.632}
14:32:37.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 172}
14:32:47.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.781, "step": 172, "write_seconds": 8.919}
14:32:48.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 173}
14:32:57.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.786, "step": 173, "write_seconds": 8.433}
14:32:58.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 174}
14:33:07.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.672, "step": 174, "write_seconds": 8.352}
14:33:08.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 175}
14:33:18.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.486, "step": 175, "write_seconds": 9.904}
14:33:19.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 176}
14:33:30.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.074, "step": 176, "write_seconds": 10.255}
14:33:32.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 177}
14:33:40.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.459, "step": 177, "write_seconds": 8.262}
14:33:41.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 178}
14:33:49.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.733, "step": 178, "write_seconds": 7.482}
14:33:50.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 179}
14:33:59.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.421, "step": 179, "write_seconds": 8.175}
14:34:00.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 180}
14:34:09.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.535, "step": 180, "write_seconds": 9.177}
14:34:11.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 181}
14:34:19.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.184, "step": 181, "write_seconds": 7.68}
14:34:20.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 182}
14:34:29.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.365, "step": 182, "write_seconds": 8.19}
14:34:30.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 183}
14:34:39.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.545, "step": 183, "write_seconds": 7.706}
14:34:40.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 184}
14:34:49.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.966, "step": 184, "write_seconds": 8.089}
14:34:50.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 185}
14:35:01.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.511, "step": 185, "write_seconds": 10.094}
14:35:02.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 186}
14:35:11.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.636, "step": 186, "write_seconds": 7.76}
14:35:12.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 187}
14:35:23.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.638, "step": 187, "write_seconds": 9.916}
14:35:24.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 188}
14:35:36.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.863, "step": 188, "write_seconds": 11.339}
14:35:37.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 189}
14:35:47.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.78, "step": 189, "write_seconds": 9.421}
14:35:48.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 190}
14:35:56.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.642, "step": 190, "write_seconds": 7.082}
14:35:57.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 191}
14:36:07.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.114, "step": 191, "write_seconds": 9.588}
14:36:08.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 192}
14:36:17.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.696, "step": 192, "write_seconds": 8.283}
14:36:18.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 193}
14:36:27.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.303, "step": 193, "write_seconds": 8.944}
14:36:29.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 194}
14:36:37.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.586, "step": 194, "write_seconds": 7.42}
14:36:38.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 195}
14:36:45.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.048, "step": 195, "write_seconds": 6.647}
14:36:46.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 196}
14:36:53.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 6.775, "step": 196, "write_seconds": 6.585}
14:36:54.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 197}
14:37:02.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.998, "step": 197, "write_seconds": 7.505}
14:37:03.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 198}
14:37:13.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.707, "step": 198, "write_seconds": 9.343}
14:37:14.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 199}
14:37:24.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.012, "step": 199, "write_seconds": 9.75}
14:37:25.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 200}
14:37:35.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.463, "step": 200, "write_seconds": 9.144}
14:37:36.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 201}
14:37:44.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.445, "step": 201, "write_seconds": 7.878}
14:37:45.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 202}
14:37:55.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.437, "step": 202, "write_seconds": 8.538}
14:37:56.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 203}
14:38:06.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.066, "step": 203, "write_seconds": 9.514}
14:38:07.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 204}
14:38:18.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.734, "step": 204, "write_seconds": 9.822}
14:38:19.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 205}
14:38:30.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.52, "step": 205, "write_seconds": 9.632}
14:38:31.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 206}
14:38:41.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.554, "step": 206, "write_seconds": 8.443}
14:38:42.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 207}
14:38:53.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.293, "step": 207, "write_seconds": 10.766}
14:38:54.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 208}
14:39:07.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.889, "step": 208, "write_seconds": 11.744}
14:39:09.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 209}
14:39:18.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.373, "step": 209, "write_seconds": 8.433}
14:39:19.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 210}
14:39:29.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.184, "step": 210, "write_seconds": 9.607}
14:39:31.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 211}
14:39:44.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.936, "step": 211, "write_seconds": 11.792}
14:39:45.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 212}
14:39:54.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.02, "step": 212, "write_seconds": 8.51}
14:39:55.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 213}
14:40:06.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.472, "step": 213, "write_seconds": 10.002}
14:40:07.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 214}
14:40:24.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.604, "step": 214, "write_seconds": 14.745}
14:40:25.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 215}
14:40:41.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 16.24, "step": 215, "write_seconds": 14.434}
14:40:43.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 216}
14:40:55.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.988, "step": 216, "write_seconds": 10.278}
14:40:56.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 217}
14:41:10.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 13.706, "step": 217, "write_seconds": 13.375}
14:41:11.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 218}
14:41:19.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.735, "step": 218, "write_seconds": 7.48}
14:41:20.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 219}
14:41:27.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.293, "step": 219, "write_seconds": 6.897}
14:41:29.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 220}
14:41:40.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.411, "step": 220, "write_seconds": 11.171}
14:41:41.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 221}
14:41:48.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 6.808, "step": 221, "write_seconds": 6.662}
14:41:49.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 222}
14:42:00.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.184, "step": 222, "write_seconds": 10.281}
14:42:02.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 223}
14:42:13.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.523, "step": 223, "write_seconds": 9.743}
14:42:14.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 224}
14:42:24.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.691, "step": 224, "write_seconds": 8.657}
14:42:25.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 225}
14:42:34.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.962, "step": 225, "write_seconds": 8.16}
14:42:36.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 226}
14:42:45.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.703, "step": 226, "write_seconds": 8.858}
14:42:47.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 227}
14:42:56.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.682, "step": 227, "write_seconds": 8.624}
14:42:58.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 228}
14:43:07.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.662, "step": 228, "write_seconds": 8.664}
14:43:09.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 229}
14:43:19.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.045, "step": 229, "write_seconds": 9.518}
14:43:20.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 230}
14:43:28.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.285, "step": 230, "write_seconds": 7.786}
14:43:29.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 231}
14:43:38.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.387, "step": 231, "write_seconds": 7.743}
14:43:39.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 232}
14:43:49.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.61, "step": 232, "write_seconds": 10.303}
14:43:51.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 233}
14:44:14.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 23.705, "step": 233, "write_seconds": 23.057}
14:44:15.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 234}
14:44:25.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.19, "step": 234, "write_seconds": 8.932}
14:44:26.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 235}
14:44:34.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.15, "step": 235, "write_seconds": 7.903}
14:44:35.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 236}
14:44:45.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.125, "step": 236, "write_seconds": 9.454}
14:44:47.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 237}
14:44:56.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.065, "step": 237, "write_seconds": 8.27}
14:44:57.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 238}
14:45:08.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.361, "step": 238, "write_seconds": 10.815}
14:45:10.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 239}
14:45:20.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.867, "step": 239, "write_seconds": 9.83}
14:45:22.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 240}
14:46:07.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 45.017, "step": 240, "write_seconds": 44.446}
14:46:08.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 241}
14:46:20.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.098, "step": 241, "write_seconds": 11.362}
14:46:21.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 242}
14:46:32.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.734, "step": 242, "write_seconds": 9.962}
14:46:33.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 243}
14:46:43.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.782, "step": 243, "write_seconds": 9.258}
14:46:44.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 244}
14:46:54.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.15, "step": 244, "write_seconds": 9.33}
14:46:56.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 245}
14:47:05.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.75, "step": 245, "write_seconds": 8.891}
14:47:07.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 246}
14:47:18.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.785, "step": 246, "write_seconds": 9.771}
14:47:19.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 247}
14:47:30.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.931, "step": 247, "write_seconds": 10.753}
14:47:31.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 248}
14:47:42.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.041, "step": 248, "write_seconds": 10.652}
14:47:43.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 249}
14:47:54.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.849, "step": 249, "write_seconds": 9.927}
14:47:56.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 250}
14:48:08.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.226, "step": 250, "write_seconds": 11.158}
14:48:09.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 251}
14:48:21.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.398, "step": 251, "write_seconds": 10.701}
14:48:23.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 252}
14:48:33.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.256, "step": 252, "write_seconds": 9.64}
14:48:34.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 253}
14:48:45.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.556, "step": 253, "write_seconds": 10.014}
14:48:46.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 254}
14:48:58.1 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.605, "step": 254, "write_seconds": 10.578}
14:48:59.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 255}
14:49:09.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.721, "step": 255, "write_seconds": 9.468}
14:49:10.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 256}
14:49:20.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.769, "step": 256, "write_seconds": 9.308}
14:49:21.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 257}
14:49:30.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.027, "step": 257, "write_seconds": 8.397}
14:49:31.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 258}
14:49:43.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.018, "step": 258, "write_seconds": 11.123}
14:49:45.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 259}
14:49:55.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.862, "step": 259, "write_seconds": 9.353}
14:49:56.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 260}
14:50:06.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.508, "step": 260, "write_seconds": 9.857}
14:50:08.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 261}
14:50:18.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.189, "step": 261, "write_seconds": 9.897}
14:50:19.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 262}
14:50:30.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.857, "step": 262, "write_seconds": 9.745}
14:50:31.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 263}
14:50:42.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.529, "step": 263, "write_seconds": 9.193}
14:50:43.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 264}
14:50:53.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.443, "step": 264, "write_seconds": 8.755}
14:50:54.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 265}
14:51:05.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.813, "step": 265, "write_seconds": 10.348}
14:51:06.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 266}
14:51:16.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.373, "step": 266, "write_seconds": 9.342}
14:51:17.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 267}
14:51:29.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.655, "step": 267, "write_seconds": 10.659}
14:51:30.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 268}
14:51:42.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.753, "step": 268, "write_seconds": 11.321}
14:51:43.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 269}
14:51:52.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.806, "step": 269, "write_seconds": 8.353}
14:51:53.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 270}
14:52:03.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.912, "step": 270, "write_seconds": 9.388}
14:52:04.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 271}
14:52:11.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 6.69, "step": 271, "write_seconds": 6.507}
14:52:12.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 272}
14:52:20.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 7.811, "step": 272, "write_seconds": 7.198}
14:52:21.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 273}
14:52:31.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.971, "step": 273, "write_seconds": 9.052}
14:52:32.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 274}
14:52:43.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.202, "step": 274, "write_seconds": 8.146}
14:52:44.3 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 275}
14:52:54.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.875, "step": 275, "write_seconds": 9.459}
14:52:55.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 276}
14:53:13.5 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 18.053, "step": 276, "write_seconds": 17.482}
14:53:14.7 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 277}
14:53:25.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.848, "step": 277, "write_seconds": 10.106}
14:53:26.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 278}
14:53:37.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.806, "step": 278, "write_seconds": 10.303}
14:53:38.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 279}
14:53:50.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.827, "step": 279, "write_seconds": 10.605}
14:53:51.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 280}
14:54:00.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 8.909, "step": 280, "write_seconds": 8.166}
14:54:01.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 281}
14:54:12.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.933, "step": 281, "write_seconds": 9.89}
14:54:13.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 282}
14:54:25.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.77, "step": 282, "write_seconds": 11.293}
14:54:26.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 283}
14:54:36.6 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.696, "step": 283, "write_seconds": 8.935}
14:54:37.9 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 284}
14:54:48.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.825, "step": 284, "write_seconds": 10.597}
14:54:50.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 285}
14:55:00.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.915, "step": 285, "write_seconds": 9.363}
14:55:02.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 286}
14:55:25.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 22.548, "step": 286, "write_seconds": 21.873}
14:55:26.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 287}
14:55:36.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.935, "step": 287, "write_seconds": 9.198}
14:55:38.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 288}
14:55:49.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.896, "step": 288, "write_seconds": 11.442}
14:55:51.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 289}
14:56:03.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 12.678, "step": 289, "write_seconds": 12.097}
14:56:05.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 290}
14:56:14.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.645, "step": 290, "write_seconds": 8.966}
14:56:15.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 291}
14:57:10.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 54.197, "step": 291, "write_seconds": 53.59}
14:57:11.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 292}
14:57:21.2 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.807, "step": 292, "write_seconds": 9.135}
14:57:22.6 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 293}
14:57:31.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.277, "step": 293, "write_seconds": 9.021}
14:57:32.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 294}
14:57:42.0 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.056, "step": 294, "write_seconds": 8.198}
14:57:43.4 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 295}
14:57:53.3 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.972, "step": 295, "write_seconds": 9.726}
14:57:54.5 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 296}
14:58:05.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 11.223, "step": 296, "write_seconds": 10.87}
14:58:06.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 297}
14:58:16.8 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.99, "step": 297, "write_seconds": 9.413}
14:58:18.0 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 298}
14:58:27.7 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.678, "step": 298, "write_seconds": 8.72}
14:58:28.8 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 299}
14:58:37.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 9.112, "step": 299, "write_seconds": 8.417}
14:58:39.1 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "periodic", "step": 300}
14:58:49.9 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "periodic", "seconds": 10.821, "step": 300, "write_seconds": 9.888}
14:58:50.2 ae52dc46 save_start             {"ckpt_files": 8, "ckpt_mb": 1000, "reason": "final", "step": 300}
14:59:02.4 ae52dc46 save_done              {"bytes": 1048576000, "dir_fsync_ok": true, "reason": "final", "seconds": 12.211, "step": 300, "write_seconds": 11.062}
14:59:03.9 ae52dc46 children_at_exit       {"alive": [], "exitcodes": []}
14:59:03.0 ae52dc46 exit                   {"code": 0, "reason": "finished 300 steps", "step": 300}
```

## Trigger log (AP clock)

```
13:43:23.5 {"action": "waiting", "after": 120.0, "log": "/home/<user>/probes/runs/core-chtc/chtc/P4b-staging-midsave-kill-vacate-fast/job.log", "trigger": "vacate-fast"}
13:55:39.3 {"action": "firing", "executions_so_far": 1, "first_execute_t": 1790880811.0, "job": "6527324.0", "last_event": "image_size", "trigger": "vacate-fast"}
13:55:40.8 {"action": "command", "cmd": ["/usr/bin/condor_vacate_job", "-fast", "6527324.0"], "output": "Job 6527324.0 fast-vacated\n", "rc": 0}
13:55:40.8 {"action": "done"}
```
