# Recipe 0: The minimal checkpointing job

Read `CLAUDE.md` first. This recipe implements the checkpointing contract inline, with **no dependency on `htcondor_ckpt`**, so a user can read one file and see everything their own job needs.

## Goal

The smallest complete, correct example of a job that survives HTCondor:
- it saves on a timer and on eviction;
- it exits 85 so HTCondor restarts it;
- it resumes exactly where it stopped;
- it exits 0 only when finished.

The model is deliberately boring. The checkpointing is the content.

## What this recipe teaches

- The five blocks every job needs, each marked with a `# ===== CHECKPOINT: <name> =====` banner:
  1. **Signal flag:** the SIGTERM handler only records the signal and the time.
  2. **Atomic save:** one file, written to `checkpoint.pt.tmp` and then renamed over `checkpoint.pt` (`os.replace`). No `fsync`, step directories, `latest` pointer or fallback: recipe 1 adds those.
  3. **Resume:** at startup, load `checkpoint.pt` if it exists. A leftover `.tmp` file is never loaded. (Recipe 0 has no `--resume` option; recipes 1–3 add `--resume auto | <path>`.)
  4. **Stop check:** at each step boundary, on the signal flag *or* the runtime limit: save, then `sys.exit(85)`.
  5. **Finish:** final save, then `exit 0`.
- Why exit 85 means "restart me" and exit 0 means "done".
- Which submit-file lines make a save after SIGTERM survive (`ON_EXIT_OR_EVICT`), and why the timed exit matters most on the OSPool.

## Files

- `train.py`: a flat script that reads top to bottom (settings → signal flag → the training problem → save → resume → loop with stop check → finish), ~175 lines, mostly comments, two small functions. Beginner-level explanatory comments take priority over brevity. Standard library + PyTorch + NumPy only.
- Submit files start the job with `shell = exec python3 train.py ...` (no wrapper script, no `universe` line; `container_image` alone runs the job in the container). `run.sh` (`exec python3 train.py "$@"`) is kept as the `executable =` alternative. Both explain why `exec` matters: HTCondor signals only the top process (docs/environment.md §6).
- The model is one line (`torch.nn.Linear(32, 4)`). Comments are written for someone checkpointing for the first time: a short note on what each line does, not just why.
- `job_chtc.sub`: CHTC, spool mode.
- `job_ospool.sub`: OSPool, spool mode.
- `README.md`.
- `requirements.txt`.

Copies of these files also go in `examples/minimal/` as the copyable starter.

## Workload

- A one-line model (`torch.nn.Linear`) on synthetic data, so there's nothing to download. It runs on CPU or any GPU in a few minutes.
- Deterministic data order per epoch (seeded shuffle of indices), so the data position is just `(epoch, batch_index)`.

## What is saved

Model, optimizer, LR scheduler, step, epoch, batch index, RNG states (Python, NumPy, torch, CUDA if present), and a small `metadata.json` (reason, timestamp, step). It is enough to show the full "what's in a checkpoint" table in miniature.

Out of scope (pointer to recipe 1 in comments): W&B, best-model export, config hashing, retention beyond "keep latest", in-epoch-vs-epoch switch.

## Behavior

- Only the options something actually sets are command-line options: `--max-runtime-seconds` (default 3600; triggers the timed exit 85), plus `--epochs`, `--log-every` and `--step-delay` for the tests. Everything else (checkpoint directory, batch size, learning rate, seed) is a named constant at the top of `train.py`.
- The checkpoint directory is `checkpoints/` in the sandbox (spool mode). It is created at startup, so it exists before any exit 85 (a missing listed path puts the job on hold).
- Log one line per save: step, reason, seconds, bytes.
- Log a "RESUMED from step X (reason)" line on resume.

## HTCondor files

Both submit files, every line commented:
```
shell                     = exec python3 train.py --max-runtime-seconds 3600
transfer_input_files      = train.py
checkpoint_exit_code      = 85
transfer_checkpoint_files = checkpoints
# without this, a save made after SIGTERM is lost:
when_to_transfer_output   = ON_EXIT_OR_EVICT
# directories are only copied back if named here:
transfer_output_files     = checkpoints
kill_sig                  = SIGTERM
container_image           = osdf:///chtc/staging/<user>/<image>.sif
```

`job_ospool.sub` adds `want_ospool = true` and `requirements = (Poolname =!= "CHTC")`. Its comments explain that OSPool evictions often come without SIGTERM, so the timed exit carries the protection there.

Also include a commented-out GPU block (`request_gpus`, `+WantGPULab`, `+GPUJobLength`, `+is_resumable`), and a short local CPU-only test recipe in the README.

## Acceptance criteria

- [ ] Runs to completion locally on CPU in a few minutes.
- [ ] Local `kill -TERM` test: exits 85 after saving; rerunning resumes from the saved step and finishes with exit 0.
- [ ] Resume-equivalence: the uninterrupted run and a run with ≥3 interruptions give identical loss curves on CPU (bitwise). Plot in the README.
- [ ] A hard kill (`kill -9`) in the middle of a save leaves a `.tmp` directory; the next run ignores it and resumes from the previous checkpoint.
- [ ] CHTC: a timed exit 85, `condor_vacate_job`, `condor_hold` + `condor_release`, and `condor_vacate_job -fast` each resume correctly. After the vacate and the hold, the job restores the save made after SIGTERM.
- [ ] OSPool: a timed exit 85 and `condor_vacate_job` resume correctly.
- [ ] `train.py` stays readable: ≤ ~200 lines, every checkpoint block bannered.

## User-facing README outline

1. **"The five things your job needs":** each block shown and explained, in file order.
2. **Two timelines:** "the timer fires → save → exit 85 → restart in place (seconds)" and "vacate → SIGTERM → finish step → save → exit 85 → reschedule (a minute or two)".
3. **The submit-file lines that matter and why:** `checkpoint_exit_code`, `transfer_checkpoint_files`, `ON_EXIT_OR_EVICT`, `kill_sig`.
4. **Testing locally:** `kill -TERM`, check `$?` is 85, rerun.
5. **Where to go next:** recipe 1 for the full contract, and `htcondor_ckpt/` for reusable code.
