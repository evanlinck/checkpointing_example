# Notes for when htcondor_ckpt becomes a package

Things we've learned, or still need to learn, that could change the interface. Add to this as the recipes use the modules.

## Open questions

- **`vacate_budget()` rule.** It returns min(MachineMaxVacateTime, JobMaxVacateTime) to be safe. Our probes saw a larger `job_max_vacate_time` (900 s) honored on CHTC CPU and OSPool slots, possibly because those slots have long retirement time left. It's untested on backfill (30 s retirement). Measure it there (P3c on `chtc_backfill`), then decide whether the rule should account for retirement.
- **`classad` evaluation.** The fallback only evaluates plain arithmetic (`10 * 60`). Not yet tested with the HTCondor Python bindings installed in a container. That test should happen together with the `condor_chirp` probe below.
- **Sharded checkpoints (DCP/FSDP).** `CheckpointStore.save(write_fn)` assumes one process writes the directory. With DCP every rank writes into the same `.tmp` directory, and rank 0 must wait (barrier) before writing `metadata.json` and renaming. Likely a `save()` split into `begin()` / `commit()`, or a `distributed=True` mode. Decide with recipe 3.
- **Async saves (recipe 3).** `StopPolicy.past_deadline()` exists for the "does a final save still fit?" decision. The policy itself (wait for the in-flight save / save / skip) isn't written yet.
- **Where the shared code lives on the execute point.** For now recipes send the directory with `transfer_input_files`. A package would be installed in the container instead.

## Decisions so far

- **The modules don't import each other,** so any single file can be copied. The cost is a little duplication (`EXIT_RESTART` and the environment-variable names in both `stop.py` and `launch.py`).
- **`StopPolicy` reads the stop and restart file paths from environment variables** set by `launch.py`. That way, training code needs no changes to run under the wrapper.
- **`exit_for_restart()` always writes the restart file if one is configured,** even on a single GPU. That's harmless, and it keeps one code path.
- **`CheckpointStore` creates its directory in `__init__`,** because spool mode holds the job if a directory named in `transfer_checkpoint_files` doesn't exist at the first exit 85.
- **Lessons from recipe 0's HTCondor tests:**
  - A checkpoint *directory* must be named in `transfer_output_files` as well as `transfer_checkpoint_files`. HTCondor's default output transfer brings back only top-level files.
  - `shell = exec python3 ...` delivers SIGTERM to Python.

## Later

- **`condor_chirp` support** (progress reporting only; the HTCondor manual advises against using chirp to move checkpoints): an optional `chirp.py` for low-frequency progress reporting, e.g. setting `LastCheckpointStep` once per checkpoint. First test whether chirp works inside a container via the `htcondor` Python bindings or `htchirp`, on CHTC and the OSPool. See CLAUDE.md.
- **Packaging:** a `pyproject.toml`, an `examples` command to copy starter files, and a version number.
