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
- Every storage mode: CHTC spool, CHTC `/staging`, OSPool spool.
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

- ~20–30M parameters. Starting point: 8 layers, 8 heads, embedding 512, context length 512. Expose all of these in config.
- Pre-LayerNorm, GELU MLP, weight-tied embeddings, `F.scaled_dot_product_attention`.
- bf16 autocast. `torch.compile` optional via config (default on), with the `_orig_mod.` save gotcha handled and commented.

## Training

- AdamW, cosine LR schedule with linear warmup, gradient clipping.
- Default ~20–40 epochs (configurable). Measure tokens/s on an H200 during development, and pick a default so the full run lasts roughly 3–5 hours. Record the measured throughput and runtime in the README. (Estimated, not yet measured: ~0.5B tokens per epoch, ~5–15 min per epoch.)
- Evaluate validation loss on a fixed subset at a configurable interval and at each epoch end.
- Generate a few sample stories from fixed prompts at each epoch end and append them to `samples.txt`. Watching stories improve across restarts is a satisfying sanity check for users.
- Because the model is small and the data is reused many times, validation loss may eventually rise. Track the best validation loss and export best-model weights separately. Use this in the README to explain why "best model" and "latest resumable checkpoint" are different things.

## Checkpointing specifics

- Single-file checkpoint (`torch.save` of a dict) inside the checkpoint directory, plus `metadata.json`. Expected size: a few hundred MB with AdamW state. Record the actual size.
- Save time should be a few seconds. Record it. This recipe is comfortably within the 600 s budget, which is the point: get the logic right where timing isn't a problem.
- **Two checkpointing modes, chosen in config (`checkpoint_at`):**
  - `epoch`: save only at epoch ends (plus on stop requests). The data position is just the epoch.
  - `interval` (default): save on a wall-clock interval and on stop requests, with `(epoch, batch_index)`.

  The README compares them: an epoch here is short (minutes), so `epoch` mode is acceptable for this recipe. Explain why recipes 2–3 can't use it (epochs of hours). Both modes must pass the resume-equivalence test.
- **Timed exit:** `max_runtime_seconds` defaults to 3600. In spool mode this is the durable periodic checkpoint.
- **Periodic in-place saves:** every 15 minutes in `/staging` mode (durable at once). In spool mode, keep the timed exit as the periodic mechanism. In-place saves there would only be durable via `ON_EXIT_OR_EVICT`.
- Retention: 1 checkpoint plus the best model in spool mode (keeps transfers small). 2 checkpoints in `/staging` mode.

## HTCondor files

`run.sh` `exec`s `python train.py "$@"`. There are three submit files, every line commented:

| File | Mode | Key lines |
|---|---|---|
| `job_chtc.sub` | CHTC spool (default) | `checkpoint_exit_code = 85`, `transfer_checkpoint_files = checkpoints`, `when_to_transfer_output = ON_EXIT_OR_EVICT`, `transfer_output_files = checkpoints` |
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

## Acceptance criteria

- [ ] `prepare_data.py` produces `train.bin` and `val.bin`; token counts recorded.
- [ ] A full uninterrupted run completes; final validation loss and sample stories included in the README.
- [ ] Local `kill -TERM` test: the job saves, exits 85, resumes with `--resume auto`, and continues from the exact `(epoch, batch_index)`.
- [ ] Resume-equivalence test with at least 3 interruptions, including one mid-epoch, for **both** `checkpoint_at` modes; loss curves overlaid in a plot in the README.
- [ ] Corrupted-checkpoint fallback works: truncate the newest checkpoint file and confirm resume uses the previous one (`/staging` mode, where 2 are kept).
- [ ] HTCondor tests:
  - **CHTC spool:** a timed exit 85, `condor_vacate_job` (restores the save made after SIGTERM), `condor_hold` + release, and `-fast` (resumes from the last timed exit).
  - **CHTC `/staging`:** `condor_vacate_job` and `-fast`.
  - **OSPool:** a timed exit 85 and `condor_vacate_job`.
- [ ] At least one run on a backfill slot (`BackfillSlot = true` confirmed in the machine ad).
- [ ] Measured save time, checkpoint size, throughput and epoch time recorded in the README.

## User-facing README outline

1. What you'll learn (5 bullet points max).
2. Quick start: prepare data, submit, watch logs.
3. What's in a checkpoint and why (a table: field → why it's needed → what breaks without it).
4. Checkpointing at epochs vs. during epochs: when each is enough.
5. What happens when HTCondor stops your job: timelines for a timed exit, a vacate/hold, and a hard kill.
6. Choosing a storage mode: CHTC spool, CHTC `/staging`, OSPool.
7. Results: loss curve, resume-equivalence plots, sample stories.
8. Adapting this to your own model.
