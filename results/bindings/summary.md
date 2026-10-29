# Probe results: bindings

Generated 2026-10-28 14:31. Per-test details are in the per-site folders.

## chtc

### P16a-bindings

_In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330275', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.006, 'connect_s': 0.002}; .chirp.config present: True

## chtc_gpu

### P16a-bindings

_In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330276', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.003, 'connect_s': 0.001}; .chirp.config present: True

## ospool

### P16a-bindings

_In the shared recipes image (containers/recipes.def, with htcondor 25.x), can a job read its machine and job ads with classad2 (what vacate_budget() needs), and report progress with condor_chirp through htcondor2.htchirp: set LastCheckpointStep / LastCheckpointReason once, read them back, and see them in condor_history afterwards? P0 found the condor_chirp program on CHTC hosts but not inside a plain container._

- Final job state: terminated ((1) Normal termination (return value 0); Usr 0 00:00:00, Sys 0 00:00:00  -  Run Remote Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Run Local Usage; Usr 0 00:00:00, Sys 0 00:00:00  -  Total Remote Usage;)
- Executions seen by the probe: 1; 'executing' events in job.log: 1 (an exit-85 restart in the same sandbox does not log one); NumJobStarts=1, NumShadowStarts=1 (condor_history).
- job.out contains output from 1 of 1 executions (tells whether stdout is kept across restarts).
- bindings: modules {'classad': 'absent (ModuleNotFoundError)', 'classad2': 'imported', 'htcondor': 'absent (ModuleNotFoundError)', 'htcondor2': 'imported'}; classad2 eval {'JobMaxVacateTime': 'not in ad (KeyError)', 'MachineMaxVacateTime': 600}; chirp {'ClusterId': '7330277', 'LastCheckpointStep_readback': '12345', 'calls_s': 0.101, 'connect_s': 0.001}; .chirp.config present: True
