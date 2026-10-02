# Recipe 3: Full fine-tune of a ~7–8B model with FSDP2 and Distributed Checkpoint

Read `CLAUDE.md` first. This recipe reuses the shared modules in `htcondor_ckpt/` (including the launcher wrapper from recipe 2) and must satisfy the full checkpointing contract, with the adaptations described below for sharded state.

## Goal

Full-parameter supervised fine-tuning of an open ~7–8B decoder model on an instruction dataset, sharded across the GPUs of one node with FSDP2, and checkpointed with PyTorch Distributed Checkpoint (DCP). The model itself is not the point. The point is that at this scale **checkpoints are large enough that both the 600 s vacate window and `/staging` storage become real engineering constraints.**

## What this recipe teaches

- Why `torch.save` on rank 0 doesn't work for sharded models.
- Sharded checkpoints with DCP: every rank writes its own shard in parallel.
- Asynchronous checkpointing: training continues while a checkpoint is written.
- Resharding: saving on N GPUs and resuming on M GPUs.
- Budgeting checkpoint time against the vacate window, and choosing a strategy when a full save might not fit.
- **Budgeting storage:** sizing the checkpoint footprint and requesting a `/staging` quota.
- Exporting a consolidated model (e.g. Hugging Face safetensors) separately from resumable checkpoints.

## Model and data

- Model: an open-weight ~7–8B model that does not require gated access, so users can run the recipe without extra approvals. Ask the user which model family CHTC prefers, and keep the model name a config value. Stage the weights on `/staging` ahead of time.
- Load with Hugging Face `transformers` for convenience, then apply FSDP2 (`fully_shard`) per transformer block and to the root module. Use a bf16 mixed-precision policy with fp32 reduction where appropriate, and activation checkpointing (configurable). Comment why each choice is made.
- Dataset: a standard open instruction-tuning dataset (ask the user; keep it configurable). `prepare_data.py` applies the model's chat template, tokenizes, masks prompt tokens out of the loss, and packs or buckets sequences into fixed-length blocks saved to disk.
- Training is framed in steps. Fine-tunes typically run 1–3 epochs. The README must state plainly that running many epochs of fine-tuning usually hurts quality, so users don't copy that pattern. Long wall time here comes from model size, not epoch count (estimated ~1–8 h per epoch on 4 GPUs, depending on the dataset).

## Memory sanity check

Write a short calculation in the README: 8B parameters × (bf16 weights + fp32 master weights + two fp32 AdamW moments + gradients). That totals roughly 130–150 GB before activations, which fits when sharded across **4 H200s** (564 GB total, the most a job can get on one node) with activation checkpointing. Confirm empirically and record peak memory per GPU.

## Storage budget and quota (central lesson, part 1)

- A resumable checkpoint with AdamW state is on the order of 100 GB. The default `/staging` quota is **100 GB and 1,000 files per user** (docs/environment.md §1). One checkpoint fills it, before even counting a second copy and a save in progress.
- The README includes a **footprint worksheet**:
  - checkpoint size × checkpoints kept, + 1 in progress (+ staged weights and data);
  - files per checkpoint × checkpoints kept, + `.tmp` leftovers.

  It shows the numbers for the default config, and tells users to **request a larger `/staging` quota from CHTC** with those numbers. This is a normal request. Don't design around the default.
- **Few, large files.** `/staging` writes many small files 10–40× slower than a few large ones (measured, docs/environment.md §7). Configure DCP's writer for a small number of files per rank (e.g. one or a few per rank, not one per tensor). Measure files per checkpoint and record it.
- Retention: default 2 resumable checkpoints, configurable down to 1. The README explains the risk trade-off of keeping only one (a corrupt newest checkpoint has no fallback).

## Checkpointing specifics

- Use `torch.distributed.checkpoint.state_dict.get_state_dict` / `set_state_dict` to obtain and restore sharded model and optimizer state dicts. Wrap the full training state in an object implementing the DCP `Stateful` protocol, so a single `dcp.save` / `dcp.load` call handles model, optimizer, scheduler, step counters and data position.
- RNG states and other small per-rank state: save alongside (a per-rank file, or included in the stateful object). Explain the choice.
- Atomicity: DCP writes many files. Keep the same contract as the other recipes: write into a `.tmp` directory, have all ranks finish (barrier), then rank 0 writes `metadata.json`, renames the directory and updates `latest`. Confirm DCP's own metadata file is present before treating a checkpoint as complete.
- **Async save:** use `dcp.async_save` for periodic checkpoints. Only one async save may be in flight; wait for the previous one before starting another. On a stop request, wait for any in-flight save before deciding what to do next. Note in comments that async save stages a copy of state in CPU memory, and request enough job memory for it.
- Periodic in-place saves: every 30 minutes (configurable). Timed exit: `max_runtime_seconds` default ~1 h, but weigh it against the measured restart cost (model load + FSDP setup); a longer interval may be justified here.

### The time-budget decision (central lesson, part 2)

Measure, at full scale and on the real `/staging`:
- `T_save`: wall time of a synchronous DCP save.
- `T_async_block`: how long training is blocked by an async save before continuing.
- Checkpoint size and file count.
- `T_load` and the total restart cost.

Then implement the stop policy in `htcondor_ckpt/stop.py` as an explicit, documented decision. The budget comes from `vacate_budget()` (machine/job ads; 600 s on every slot measured), not a hard-coded constant:
- If an async save is in flight, wait for it to finish (bounded by the deadline), then exit 85.
- Else, if the estimated save time (last measured `T_save` plus a safety margin) fits within the remaining budget, do a final synchronous save, then exit 85.
- Else, skip the final save, log clearly how much work since the last periodic checkpoint will be redone, and exit 85.

Write the measured numbers and the resulting recommendation into the README. If `T_save` is uncomfortably close to the budget, recommend a shorter periodic interval as the real protection, and say so plainly: on large jobs, periodic checkpoints carry the safety; the save made after SIGTERM is a bonus. Do not raise `job_max_vacate_time` above 600 s to make a save fit. It was honored on some slots in testing, but on backfill that time belongs to the GPU's owner.

## Resharding

- Demonstrate saving on N GPUs and resuming on a different count (e.g. 4 → 2, if the model still fits on 2 GPUs with CPU offload; otherwise 4 → 3). The data position must be stored in a world-size-independent form (global sample index), with each rank deriving its slice on load.
- Global batch size stays constant across resharding by adjusting gradient accumulation. Log the adjustment.

## Exporting the model

- A separate `export.py` loads a DCP checkpoint and writes a consolidated Hugging Face-format model (safetensors) for inference. This runs as its own job, not inside training.
- Document the conversion, so users understand that resumable checkpoints and exported models serve different purposes and have different formats. The export's size also counts toward the `/staging` quota.

## HTCondor files

- `job.sub`, every line commented:
  - `request_gpus = 4` (parameterized) and generous `request_memory` to cover async-save CPU staging;
  - `+WantGPULab = true`, `+GPUJobLength`, `+is_resumable = true`;
  - `checkpoint_exit_code = 85`, `kill_sig = SIGTERM`, `requirements = HasCHTCStaging =?= true`;
  - checkpoint directory on `/staging`, `--resume auto`;
  - launched through the stop-file wrapper (`htcondor_ckpt/launch.py`).

  Note in comments that checkpoints of this size must never use spool transfer.
- `export.sub`: a short job (CPU or single GPU, whichever works best) to run `export.py`.

## Acceptance criteria

- [ ] Memory calculation and measured peak memory per GPU recorded.
- [ ] Storage footprint worksheet filled in with measured size and file count; quota request guidance written.
- [ ] Synchronous save, async save and load all work; `T_save`, `T_async_block`, `T_load`, restart cost, checkpoint size and file count measured and recorded.
- [ ] Stop policy implemented, with each of its three branches exercised by a test (force the "skip" branch with an artificially small budget in config).
- [ ] Local stop test during an in-flight async save: the job waits for it, exits 85, and resumes correctly.
- [ ] Resharding test: save on N GPUs, resume on M GPUs, loss continues smoothly.
- [ ] Resume-equivalence test on a reduced run, with a plot in the README.
- [ ] `condor_vacate_job` test with the full-size model: total time from SIGTERM to exit recorded and confirmed under 600 s. Also a timed exit 85 and `-fast` (resumes from the last periodic checkpoint).
- [ ] `export.py` produces a model that loads in `transformers` and generates sensible text.

## User-facing README outline

1. Why big models need different checkpointing.
2. Quick start: stage weights and data, request quota, submit training, export.
3. How DCP and async saves work, briefly and with a diagram.
4. Budgets: the 600-second window and the `/staging` footprint, with measured numbers and the decision policy.
5. Resharding: changing GPU count between runs.
6. Resumable checkpoints vs. exported models.
7. Adapting this to your own FSDP code: a checklist.
