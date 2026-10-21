# Recipe 1: Small GPT on TinyStories (single GPU)

Read `CLAUDE.md` and recipe 0 first. This recipe must satisfy the full checkpointing contract in `CLAUDE.md`, using the shared modules in `htcondor_ckpt/` (shipped with the job via `transfer_input_files`).

## Goal

Train a small GPT-style language model from scratch on the TinyStories dataset, on a single H200, for many epochs. The run should take a few hours: long enough to be interrupted several times, short enough for users to try in an afternoon.

This recipe introduces the full contract, so the code should be the most heavily commented of the recipes that use `htcondor_ckpt/`. A user who reads only this recipe should understand what a resumable checkpoint is, why each piece of state is in it, and which HTCondor setup keeps it safe.

## What this recipe teaches

- Saving and restoring the complete training state, not just model weights.
- **Checkpointing at epoch boundaries vs. during an epoch,** side by side, and how to choose.
- Mid-epoch resume without repeating or skipping data.
- RNG state capture, so a resumed run continues the same random sequence.
- Atomic checkpoint writes and retention.
- The timed exit 85 and SIGTERM handling, within the measured 600 s vacate window.
- The difference between a resumable checkpoint and an exported "best model".
- Every storage mode: CHTC spool, CHTC spool **with backups on `/staging`**, CHTC `/staging`, OSPool spool.
- How often to back up, depending on how long the run takes.
- Running on GPU Lab slots and on backfill (`+is_resumable`).

## Data

- Dataset: TinyStories (`roneneldan/TinyStories` on the Hugging Face Hub). Execute points have internet access, but `prepare_data.py` runs once ahead of time (on the AP or in a short CPU job) and its output is staged, so training jobs don't re-download.
- Tokenizer: GPT-2 BPE via `tiktoken` (vocabulary 50257, padded to 50304 for efficiency).
- `prepare_data.py` tokenizes the train and validation splits once. It writes them as flat `uint16` NumPy memmap files (`train.bin`, `val.bin`) with an EOT token between stories. Print the token counts and record them in the README.
- Data reaches the job by file transfer from `/staging`. The files are a few hundred MB, so OSDF is fine. Document both CHTC and OSPool paths.
- Do not sample random-offset windows (the nanoGPT default). Instead, use a deterministic, epoch-based scheme, so "epoch" has a clear meaning and mid-epoch resume is easy to see:
  - split `train.bin` into non-overlapping fixed-length sequences;
  - shuffle their order with a seed derived from `(base_seed, epoch)`;
  - iterate in that order.

  The data position saved in the checkpoint is then just `(epoch, batch_index)`. Explain this choice in a comment.

## Model

A minimal GPT implementation in a single `model.py` (nanoGPT-style, written fresh and readable):

- 51M parameters as configured (measured: 26M of them are the 50,304 × 512 token embedding, shared with the output layer; ~25M in the transformer blocks). Starting point: 8 layers, 8 heads, embedding 512, context length 512. Expose all of these in config.
- Pre-LayerNorm, GELU MLP, weight-tied embeddings, `F.scaled_dot_product_attention`.
- bf16 autocast. `torch.compile` optional via config (default on), with the `_orig_mod.` save gotcha handled and commented.

## Training

- AdamW, cosine LR schedule with linear warmup, gradient clipping.
- Default 6 epochs: ~3.5 hours on an NVIDIA L40 at ~35 min per epoch (measured). The submit files don't restrict the GPU model: the recipe runs on any GPU Lab GPU, and the README reports the L40 numbers and shows how to require a GPU capability or memory size. `max_steps` (default 0) ends a run early, as if finished: for smoke runs and the HTCondor tests. **GPU memory floor:** with `+is_resumable` the job also matches research-group GPUs, including ~11 GB cards; at batch 64 × 512 the model ran out of memory on one (2026-10-19, a research-group machine). The submit files therefore set `gpus_minimum_memory = 20000`, and `train.py` logs peak GPU memory (first step and every checkpoint) so the README can state the real requirement. (Measured on the real data: 474M tokens and 14,465 steps per epoch at batch 64 × 512. First full run, 1 epoch on an NVIDIA L40, 2026-10-14: ~224k tokens/s, ~35 min per epoch, 21.5 s from process start to the first step (incl. `torch.compile`), final save 3.4 s / 615 MB / 2 files, val_loss 1.43. One timed checkpoint costs ~18–20 s (measured 2026-10-19 on an H100, see "Measurements from the HTCondor tests"), ~0.1% of a 6 h interval.)
- Evaluate validation loss on a fixed subset at a configurable interval and at each epoch end.
- Generate a few sample stories from fixed prompts at each epoch end and append them to `samples.txt`. Watching stories improve across restarts is a satisfying sanity check for users.
- Because the model is small and the data is reused many times, validation loss may eventually rise. Track the best validation loss and export best-model weights separately. Use this in the README to explain why "best model" and "latest resumable checkpoint" are different things.

## Checkpointing specifics

- Single-file checkpoint (`torch.save` of a dict) inside the checkpoint directory, plus `metadata.json`. Expected size: a few hundred MB with AdamW state. Record the actual size.
- Save time should be a few seconds. Record it. This recipe is comfortably within the 600 s budget, which is the point: get the logic right where timing isn't a problem.
- **Two checkpointing modes, chosen in config (`checkpoint_at`):**
  - `interval` (default): save whenever a stop is requested (SIGTERM, stop file or the timed checkpoint), mid-epoch if need be, with `(epoch, batch_index)`; optional in-place saves every `save_every_minutes`.
  - `epoch`: save only at epoch ends. A timed checkpoint waits for the end of the epoch. A SIGTERM mid-epoch exits 85 *without saving*, and the restart redoes that epoch from its start. That's the honest trade-off: simpler state, but up to one epoch of lost work, and a timed stop that waits for the epoch end must still notice a SIGTERM (`StopPolicy` lets an eviction replace a pending timed stop).

  The README compares them: an epoch here is short (minutes), so `epoch` mode is acceptable for this recipe. Explain why recipes 2–3 can't use it (epochs of hours). Both modes must pass the resume-equivalence test.
- **Timed exit:** `max_runtime_seconds` defaults to 6 h on CHTC (CHTC usually suggests 4–6 hours on the OSPool (up to 8) and 6–10 hours on CHTC backfill) and 5 h on the OSPool. Tests use minutes. In spool mode this is the durable periodic checkpoint. The README reports the measured cost of one timed checkpoint (save + spool transfer + restart/restore) as a percentage of the interval.
- **Periodic in-place saves:** every 15 minutes in `/staging` mode (durable at once). In spool mode, keep the timed exit as the periodic mechanism. In-place saves there would only be durable via `ON_EXIT_OR_EVICT`.
- Retention: 1 checkpoint plus the best model in spool mode (keeps transfers small). 2 checkpoints in `/staging` mode.
- **Backups (spool + `/staging`):** `--backup-dir /staging/<user>/<run_name>/backups --backup-every-hours H`. At timed checkpoints, if `backup_due()`, the new checkpoint is copied there with `backup()` (`keep=2`). At startup, `load_newest([local, backups])` resumes from whichever is newer. Use the run name, not the job id, so a resubmitted job finds its backups. Never back up in the SIGTERM path. The README includes the backup-frequency table from `htcondor_ckpt/README.md`, with recipe 1's measured backup time and size.

## HTCondor files

Submit files start the job with `shell = exec python3 train.py ...` (measured in recipe 0; no `run.sh`). Two directories travel with the job: `checkpoints/` (resumable state) and `outputs/` (best model, `samples.txt`, `metrics.jsonl`), both listed in `transfer_checkpoint_files` and `transfer_output_files`. Settings come from `config.yaml`, overridden with `--set name=value`. `prepare.sub` runs `prepare_data.py` as a CPU job writing to `/staging`. The submit files, every line commented in `job_chtc.sub`:

| File | Mode | Key lines |
|---|---|---|
| `job_chtc.sub` | CHTC spool (default) | `checkpoint_exit_code = 85`, `transfer_checkpoint_files = checkpoints`, `when_to_transfer_output = ON_EXIT_OR_EVICT`, `transfer_output_files = checkpoints` |
| `job_chtc_backup.sub` | CHTC spool + backups on `/staging` | as `job_chtc.sub` + `requirements = HasCHTCStaging =?= true` and `--backup-dir /staging/<user>/<run_name>/backups --backup-every-hours 1` (short for the demo; the README explains real values) |
| `job_chtc_staging.sub` | CHTC `/staging` | `checkpoint_exit_code = 85`, `requirements = HasCHTCStaging =?= true`, `--ckpt-dir /staging/<user>/...` |
| `job_ospool.sub` | OSPool spool | as `job_chtc.sub` + `want_ospool = true`, `requirements = (Poolname =!= "CHTC")` |

All three include `kill_sig = SIGTERM`, the container image via `osdf://`, `request_gpus = 1`, `+WantGPULab = true`, `+GPUJobLength = "short"` and `+is_resumable = true`. The CHTC files also carry a commented-out `TARGET.BackfillSlot =?= true` requirement with an explanation. Starting point:

```
universe                  = vanilla
executable                = run.sh
arguments                 = --config config.yaml --resume auto
checkpoint_exit_code      = 85
transfer_checkpoint_files = checkpoints
when_to_transfer_output   = ON_EXIT_OR_EVICT
transfer_output_files     = checkpoints
kill_sig                  = SIGTERM
container_image           = osdf:///chtc/staging/<user>/<image>.sif
request_gpus              = 1
+WantGPULab               = true
+GPUJobLength             = "short"
+is_resumable             = true
request_cpus              = 8
request_memory            = 48GB
request_disk              = 20GB
output                    = logs/$(Cluster).$(Process).out
error                     = logs/$(Cluster).$(Process).err
log                       = logs/$(Cluster).log
queue
```

## Full run (2026-10-19, job 6799802, `job_chtc.sub`, NVIDIA H200, GPU Lab)

| | |
|---|---|
| Steps, epochs | 86,790 steps (6 × 14,465), uninterrupted, exit 0 |
| Throughput | ~1.06M tokens/s, median of the logged steps (p10–p90: 1.053–1.061M); 4.7× the L40's ~224k |
| Epoch time | ~7.5 min (474M tokens per epoch) |
| Job time | 47 min 55 s from start to termination (event log); ~45 min of it training |
| Start-up | 20.0 s from process start to the first step |
| Peak GPU memory | 15.4 GB (the submit files' floor is 20 GB) |
| Val loss after each epoch | 1.4935, 1.4351, 1.3935, 1.3543, 1.3226, **1.3076** |
| Final save | 2.62 s, 615 MB, 2 files; output transfer 2 s |

- **No timed checkpoint fired:** the 48 min run is far below the 6 h interval.
- **On an L40 the same run takes ~3.5 h,** still below the interval.
- **The README should say this plainly.** On fast GPUs, recipe 1 is protected by its SIGTERM saves; the timed exit is insurance against hard kills.

## Measurements from the HTCondor tests (2026-10-19)

Test settings: `test_htcondor.sh` (3,000 steps, 0.1 s pause per step, timed exit every 120 s, `deterministic=true`). Run 6799595 on an NVIDIA H100 80GB (backfill), with 4 restarts. Times come from `metrics.jsonl` (process side) and the event log (HTCondor side, 1 s resolution).

**The cost of one timed checkpoint (CHTC spool, restart in place):**

| | step 1276 | step 2258 |
|---|---|---|
| Save (615 MB, 2 files) | 2.5 s | 4.4 s |
| Exit → new process starts (includes the spool transfer, logged 12:25:26–27 and 12:27:38–39: ≤ 2 s) | 4.5 s | 4.1 s |
| Process start → first step (imports, data, model, load, `torch.compile`) | 10.9 s | 11.1 s |
| **Total, save start → first step** | **17.9 s** | **19.6 s** |

- **The restart was in place:** no new `001` or input-transfer events. It's consistent with `docs/environment.md` §5.
- **Against the interval:** about 20 s against the 6 h default (CHTC) is ~0.1%; against 5 h (OSPool) it is also ~0.1%. The full run (~3.5 h on an L40) is shorter than either interval, so on a GPU that fast no timed checkpoint fires at all. The timed exit only matters on slower GPUs, or for longer runs.
- **Restarts on a new slot cost more.** These were the two SIGTERM saves; for both, the save was durable and no work was lost:

  | Restart after | Save | Exit → resumed | Process start → first step |
  |---|---|---|---|
  | The backfill eviction | 12.4 s | 116 s | 18.8 s |
  | `condor_vacate_job` | 4.1 s | 55 s | 19.1 s |

  - "Exit → resumed" covers queue time, input transfer (~16 s) and process start.
  - A fresh sandbox also needs ~8 s more start-up than an in-place restart, probably because the `torch.compile` caches under `$HOME=$PWD` survive only in place.

**Resume equivalence on GPUs** (`compare_runs.py`, plot `recipes/01_tinystories/resume_equivalence_gpu.png`):
- **The runs:** two uninterrupted references (an H200, and an RTX PRO 6000 Blackwell), plus the resumed run (H100: 2 SIGTERM saves, 2 timed exits).
- **Results:**
  - **The two references against each other:** val loss up to 0.0053 apart (0.0001 at step 3000).
  - **The resumed run against them:** up to 0.0068 apart (0.0009–0.0010 at step 3000). That's within the tolerance: 0.01, or twice the noise between the two references, whichever is larger.
  - **Training loss** per logged step differs by up to 0.016 in both comparisons.
- **No jump after a restart.** The largest training-loss gap (step 400, just after the restart at 397) is the same size as the gaps between the two references.
- **Not bitwise-equal, unlike the CPU test:** the two references already differ at step 50. They ran on different GPU models, so different kernels and `torch.compile` tuning produce different bf16 rounding, and the differences grow.

**Backup:** in the backup test (`job_chtc_backup.sub`), the copy of a 615 MB checkpoint (2 files) to `/staging` took 2.96 s.

**Backfill** (also in `docs/environment.md` §3):
- **A real eviction:** the GPU's owner reclaimed the slots (`Code 1011`, "PREEMPT expression evaluated to True"). Two test jobs on the same machine got SIGTERM, saved (12.4 / 12.5 s, slower than usual because both wrote at once), exited 85 and resumed.
- **GPU floor:** a gpu_check job on `backfill1_4` got an A30 (24 GB), which passes the 20 GB floor.

## Acceptance criteria

- [x] `prepare_data.py` produces `train.bin` and `val.bin`; token counts recorded.
- [x] A full uninterrupted run completes; final validation loss and sample stories included in the README. (H200, 48 min, val_loss 1.3076; `loss_curve.png`.)
- [x] Local `kill -TERM` test: the job saves, exits 85, resumes with `--resume auto`, and continues from the exact `(epoch, batch_index)`.
- [x] Resume-equivalence test with at least 3 interruptions, including one mid-epoch, for **both** `checkpoint_at` modes; loss curves overlaid in a plot in the README. (CPU, `test_local.py`: identical losses in both modes. GPU, `compare_runs.py`: within tolerance, see above. Both plots are in the README.)
- [x] Corrupted-checkpoint fallback works: truncate the newest checkpoint file and confirm resume uses the previous one, with 2 checkpoints kept as in `/staging` mode. (Tested locally in `test_local.py`.)
- [x] Backup recovery: run `job_chtc_backup.sub` until at least one backup exists, `condor_rm` it, resubmit, and confirm it resumes from the `/staging` backup ("RESUMED … from /staging/…").
- [x] HTCondor tests:
  - **CHTC spool:** a timed exit 85, `condor_vacate_job` (restores the save made after SIGTERM), `condor_hold` + release, and `-fast` (resumes from the last timed exit).
  - **CHTC `/staging`:** `condor_vacate_job` and `-fast`.
  - **OSPool:** a timed exit 85 and `condor_vacate_job`.
- [x] At least one run on a backfill slot (`BackfillSlot = true` confirmed in the machine ad). It also went through a real backfill eviction.
- [x] Measured save time, checkpoint size, throughput and epoch time recorded in the README, with the cost of one timed checkpoint.

## User-facing README outline

1. What you'll learn (5 bullet points max).
2. Quick start: prepare data, submit, watch logs.
3. What's in a checkpoint and why (a table: field → why it's needed → what breaks without it).
4. Checkpointing at epochs vs. during epochs: when each is enough.
5. What happens when HTCondor stops your job: timelines for a timed exit, a vacate/hold, and a hard kill.
6. Choosing a storage mode: CHTC spool, CHTC spool + `/staging` backups, CHTC `/staging`, OSPool. How often to back up for runs of different lengths.
7. Results: loss curve, resume-equivalence plots, sample stories.
8. Adapting this to your own model.
