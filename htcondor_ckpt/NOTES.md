# Notes for when htcondor_ckpt becomes a package

Things we've learned, or still need to learn, that could change the interface. Add to this as the recipes use the modules.

## Open questions

- **`vacate_budget()` rule.** It returns min(MachineMaxVacateTime, JobMaxVacateTime) to be safe. Our probes saw a larger `job_max_vacate_time` (900 s) honored on CHTC CPU and OSPool slots, possibly because those slots have long retirement time left. It's untested on backfill (30 s retirement). Measure it there (P3c on `chtc_backfill`), then decide whether the rule should account for retirement.
- **`classad` evaluation.** The fallback only evaluates plain arithmetic (`10 * 60`). Not yet tested with the HTCondor Python bindings installed in a container. That test should happen together with the `condor_chirp` probe below.
- **Sharded checkpoints (DCP/FSDP).** `CheckpointStore.save(write_fn)` assumes one process writes the directory. With DCP every rank writes into the same `.tmp` directory, and rank 0 must wait (barrier) before writing `metadata.json` and renaming. Likely a `save()` split into `begin()` / `commit()`, or a `distributed=True` mode. Decide with recipe 3.
- **Async saves (recipe 3).** `StopPolicy.past_deadline()` exists for the "does a final save still fit?" decision. The policy itself (wait for the in-flight save / save / skip) isn't written yet.
- **Backups on the OSPool.** No `/staging` there. P13 (2026-10-26): `transfer_output_remaps` to `osdf://` uploads only at the job's final exit, never at an exit 85, so HTCondor can't make periodic OSDF backups. What works: a planned hand-off (save, exit 86 (P13b: a normal termination, outputs remapped as with 0) with the checkpoint remapped to a new OSDF path, the next job resumes from it as an `osdf://` input). Recipe 4 decides whether that becomes a helper (e.g. `store.handoff_paths()`), or stays in the recipe.
- ~~**Untested on HTCondor:** the backup helpers.~~ Done in recipe 1's "condor_rm + resubmit" test: the resubmitted job resumed from the `/staging` backup; copying 615 MB took 2.96 s.
- **Launcher behaviour depends on the torch version.** The `torchrun` measurements (30 s kill, 85 → 1, `--shutdown-timeout`) came from CPU torch 2.14.1; the recipe images use torch 2.8. `launch.py` avoids depending on any of it, but the docs' notes about `--shutdown-timeout` need the version they were confirmed in. Recipe 2 re-measures with its image.
- **Shared tools, not just modules.** Recipe 1's `compare_runs.py` (resume equivalence against two uninterrupted references, with a noise floor) and `plot_run.py` (one loss curve across restarts, from `metrics.jsonl`) apply to every recipe. For now each recipe copies them. A package could ship them as commands, which needs a stable `metrics.jsonl` schema (`train`, `eval`, `resumed`, `checkpoint`, `first_step` events).
- **Where the shared code lives on the execute point.** For now recipes send the directory with `transfer_input_files`. A package would be installed in the container instead.

## Decisions so far

- **`stop.runtime_limit()` and `stop.job_time_left()` (2026-10-27):** `runtime_limit(max_runtime_seconds)` returns the smallest of that, `GLIDEIN_ToDie - now - margin` (P12a: glidein ends are hard kills 104–355 s after it, no SIGTERM) and `AllowedExecuteDuration - margin` (P14a: each exit 85 starts a new execution), with its source, like `vacate_budget()`. It feeds `StopPolicy(max_runtime_seconds=...)`, so `StopPolicy` is unchanged. `job_time_left()` gives the time to `JobStartDate + AllowedJobDuration - margin` (P14b), for a hand-off (exit 86). Margin 900 s by default; a large checkpoint needs more. The core is now 593 lines, at the ~600 budget: the next addition should replace something.

- **The modules don't import each other,** so any single file can be copied. The cost is a little duplication (`EXIT_RESTART` and the environment-variable names in both `stop.py` and `launch.py`).
- **`StopPolicy` reads the stop and restart file paths from environment variables** set by `launch.py`. That way, training code needs no changes to run under the wrapper.
- **`exit_for_restart()` always writes the restart file if one is configured,** even on a single GPU. That's harmless, and it keeps one code path.
- **Backups are stateless:** `backup_due()` reads the newest backup's `saved_at` from its metadata instead of keeping a timer in memory, because every exit-85 restart is a new process and a resubmitted job is a new job. `load_newest()` takes the local store first on ties.
- **`CheckpointStore` creates its directory in `__init__`,** because spool mode holds the job if a directory named in `transfer_checkpoint_files` doesn't exist at the first exit 85.
- **Lessons from recipe 0's HTCondor tests:**
  - A checkpoint *directory* must be named in `transfer_output_files` as well as `transfer_checkpoint_files`. HTCondor's default output transfer brings back only top-level files.
  - `shell = exec python3 ...` delivers SIGTERM to Python.
- **Lesson from recipe 1's first HTCondor runs:** create every directory named in `transfer_output_files` as the very first thing the job does. A crash before they existed (e.g. a bad data path) turned into a hold for "No such file or directory" on output transfer, hiding the real error. `CheckpointStore` already creates its directory in `__init__`, but recipes should create both their checkpoint and output directories before loading data or building models.

- **Lessons from writing recipe 2 (DDP):**
  - `capture_rng()` read every visible GPU's generator (`get_rng_state_all()`). Under torchrun each worker sees all of the job's GPUs, so that would start a CUDA context on every GPU from every worker. It now takes `all_devices=False` for one-process-per-GPU runs; `restore_rng()` handles both, and checkpoints written before the option.
  - `agree(flag)` says *whether* to stop, not *why*. `agree_max(level)` carries the most urgent action any rank asked for (go on < periodic save < timed stop < stop file < signal), so every rank saves and logs the same reason with one all-reduce.
  - Under torchrun, a worker that exits while rank 0 is still saving makes torchrun stop the other workers, rank 0 included. So every rank waits at a barrier after the save, then all exit 85 together. (From torchrun's documented behaviour, not yet measured: `test_local.py --ddp` and the HTCondor tests will show it.)

## Later

- **`condor_chirp` support** (progress reporting only; the HTCondor manual advises against using chirp to move checkpoints): an optional `chirp.py` for low-frequency progress reporting, e.g. setting `LastCheckpointStep` once per checkpoint. First test whether chirp works inside a container via the `htcondor` Python bindings or `htchirp`, on CHTC and the OSPool. See CLAUDE.md.
- **Packaging:** a `pyproject.toml`, an `examples` command to copy starter files, and a version number.
