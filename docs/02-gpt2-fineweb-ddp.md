# Recipe 2: GPT-2 124M on FineWeb-Edu (single node, multi-GPU DDP)

Read `CLAUDE.md` first. This recipe reuses the shared modules in `htcondor_ckpt/` and the model code from recipe 1 (generalized as needed), and must satisfy the full checkpointing contract.

## Goal

Reproduce GPT-2 small (124M parameters) trained from scratch on roughly 10B tokens of FineWeb-Edu, using DistributedDataParallel across the GPUs of a single node. The run is long enough that it will realistically be stopped and restarted many times (timed exits, runtime limits, evictions), which is the scenario users need to see working.

Multi-node training is out of scope: HTCondor's parallel universe adds complexity that would distract from checkpointing. Note this in the README and mention it as a possible future recipe.

## What this recipe teaches

- Checkpointing under DDP: rank 0 writes, all ranks load, and every rank agrees on the state.
- Coordinated stopping: all ranks must stop at the same step, or the job deadlocks.
- **Graceful shutdown through a launcher.** Plain `exec torchrun` breaks in two ways (measured, docs/environment.md §6): it kills workers ~30 s after SIGTERM, and it turns exit 85 into 1. The version-independent stop-file wrapper fixes both.
- Per-rank data position for sharded streaming data.
- Thinking in steps and tokens rather than epochs at this scale, and why.
- A run that spans many HTCondor executions, with metrics that read as one continuous run.

## Data

- Dataset: FineWeb-Edu, the `sample-10BT` subset (`HuggingFaceFW/fineweb-edu`). Confirm with the user before downloading. The tokenized output is ~20 GB as `uint16`.
- `prepare_data.py` tokenizes with GPT-2 BPE (`tiktoken`) using multiprocessing. It writes fixed-size shards (e.g. 100M tokens each) as `uint16` `.npy` files, plus one validation shard, on `/staging`. This step is CPU-heavy. Provide `prepare.sub` to run it as a CPU-only HTCondor job, and make it resumable at the shard level (skip shards that already exist and are complete).
- **Shard size vs. quota:** ~200 shards of ~200 MB fit the default `/staging` quota (100 GB, 1,000 files) alongside the checkpoints. Larger shards are also faster to read. State the file count in the README.
- Data loading: each rank reads a deterministic, disjoint slice of each shard. The checkpointed data position is `(shard_index, position_within_shard)`, identical in structure across ranks and derivable per rank from rank and world size. Document how to resume correctly if the world size changes. Resuming on a different GPU count is allowed in this recipe, but it should log a warning that the data order changes.

## On epochs at this scale

At 10B tokens the natural unit is tokens or steps, and a single pass over the data is normal. An "epoch" here takes hours (estimated: ~11 h on 1 GPU, ~3 h on 4), so checkpointing only at epoch boundaries is not an option. That is the contrast with recipe 1. Make the dataloader support multiple passes (`num_passes` in config, default 1), with a reshuffled shard order per pass, so the "epoch" concept from recipe 1 carries over. In the README, briefly explain why large-scale pretraining usually avoids many repeated passes, and why the checkpointing logic is identical either way.

## Model and training

- GPT-2 small: 12 layers, 12 heads, embedding 768, context 1024, vocab padded to 50304.
- AdamW (fused), cosine schedule with warmup, gradient clipping, gradient accumulation to reach ~0.5M tokens per optimizer step regardless of GPU count. Check the stop flag between micro-batches too, so a stop request never waits for a whole accumulation cycle.
- bf16 autocast, `torch.compile`, TF32 matmuls enabled, flash attention via SDPA.
- Validation loss at regular intervals. Optional HellaSwag evaluation (stage the eval data ahead of time).
- Default GPU count: **4** (the most a job can get on one node). Measure throughput and record expected wall time for 1, 2 and 4 GPUs in the README.

## Checkpointing specifics

- Rank 0 saves the model (unwrap DDP's `.module`), optimizer, scheduler, step, tokens seen, data position, and its RNG states. Every rank's CUDA RNG state should also be saved (gather to rank 0, or have each rank write a tiny per-rank RNG file). Explain the choice.
- All ranks load the checkpoint (mapped to their own device). Use `dist.barrier()` around save and load where needed, and comment why.
- Checkpoint size will be roughly 1.5 GB (fp32 weights + two AdamW moments). Measure save time and size.
- **Storage:** `/staging` mode is the default (in-place periodic saves every 30 min are durable at once). Spool mode is a documented alternative: a 1 GB checkpoint added only ~5 s to an exit-85 restart, and `ON_EXIT_OR_EVICT` keeps the save made after SIGTERM. Measure it, and state when spool stops being reasonable.
- **Timed exit:** `max_runtime_seconds` default ~1 h, through the same rank agreement as the stop flag.
- **Stop agreement:** `htcondor_ckpt/torch_utils.py` provides a helper that all-reduces the local stop flag (`MAX`) every K steps (configurable, default every step; negligible next to a 0.5M-token step). The flag comes from the signal *or* the stop file. Whichever rank sees it first makes all ranks stop at the same step.
- **Restart cost:** each `torchrun` (re)start took ~18 s before workers ran (measured with CPU torch). Measure the real cost with CUDA initialization and `torch.compile`, and use it to justify the timed-exit interval.

## Launching

- **Default:** `run.sh` `exec`s the stop-file wrapper (`htcondor_ckpt/launch.py`), which runs `torchrun --standalone --nproc_per_node=N train.py ...`:
  - on SIGTERM it creates a stop file and does not forward the signal;
  - workers treat the file like the signal;
  - rank 0 records "restart requested";
  - the wrapper exits 85 when that record exists, otherwise passes on `torchrun`'s exit code.

  This depends on no `torchrun` feature. It was measured end to end (docs/environment.md §6, P7h).
- **Documented alternative:** `torchrun --shutdown-timeout 420` (or `TORCH_ELASTIC_SHUTDOWN_TIMEOUT`). It works in torch 2.14.1; note that older versions may not have it. It still needs the exit-code mapping.
- The README explains, with the measured numbers, why plain `exec torchrun` is not enough.

## HTCondor files

- `prepare.sub`: CPU-only data preparation job.
- `job.sub`, every line commented:
  - `request_gpus = N` (parameterized, default 4), with CPUs and memory proportional to GPU count (start at 8 CPUs and 32 GB per GPU; adjust after measuring);
  - `+WantGPULab = true`, `+GPUJobLength` (state which length suits the run), `+is_resumable = true`;
  - `checkpoint_exit_code = 85`, `kill_sig = SIGTERM`, `requirements = HasCHTCStaging =?= true`;
  - checkpoint and data directories on `/staging`, and `--resume auto`.
- A commented-out backfill requirement (`TARGET.BackfillSlot =?= true`), with an explanation of backfill eviction (only when the owner needs the GPU).
- The README shows users how to see how many times their job has restarted. Use the job event log (eviction and file-transfer events) rather than polling `condor_q`, and note that `NumJobStarts` does not count exit-85 restarts.

## Acceptance criteria

- [ ] Data preparation runs as an HTCondor job and resumes correctly if interrupted.
- [ ] A short run (a few hundred steps) on 2+ GPUs matches the loss of the same run on 1 GPU with equivalent global batch size, within tolerance.
- [ ] Local SIGTERM test on a multi-GPU node, sending the signal to the top process only as HTCondor does: all ranks stop at the same step, rank 0 saves, the job exits 85, and resume continues from the saved step and data position.
- [ ] A save that takes longer than 30 s completes under the wrapper (it would be killed under plain `exec torchrun`).
- [ ] Resume-equivalence test on a reduced run (e.g. 2,000 steps, 3 interruptions), with a plot in the README.
- [ ] HTCondor tests on GPU Lab slots: a timed exit 85, `condor_vacate_job`, hold + release, and `-fast`. Logs from all ranks show a clean, coordinated stop.
- [ ] One run on a backfill slot.
- [ ] A full-length run completes across multiple HTCondor executions, producing one continuous loss curve with restart points marked.
- [ ] Measured throughput, checkpoint size, save time, restart cost and `/staging` footprint recorded.

## User-facing README outline

1. What's new compared with recipe 1.
2. Quick start: prepare data (CPU job), submit training, monitor.
3. Why every rank must agree to stop, with a short diagram of the deadlock that happens otherwise.
4. How the stop request reaches your training processes: what HTCondor signals, what `torchrun` does with it, and how the wrapper fixes it (measured).
5. Results: continuous loss curve with restart markers, resume-equivalence plot, throughput table.
6. Adapting this to your own DDP code: a checklist (including `accelerate`/`deepspeed` launchers).
