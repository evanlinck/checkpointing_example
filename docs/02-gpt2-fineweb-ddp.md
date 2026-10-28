# Recipe 2: GPT-2 124M on FineWeb-Edu (single node, multi-GPU DDP)

Read `CLAUDE.md` and recipe 1 first. This recipe reuses the shared modules in `htcondor_ckpt/`, recipe 1's container image, model code and test tools (generalized as needed), and must satisfy the full checkpointing contract.

## Goal

Reproduce GPT-2 small (124M parameters) trained from scratch on roughly 10B tokens of FineWeb-Edu, using DistributedDataParallel across the GPUs of a single node. **The point is the workflow:** a run that spans several HTCondor executions, through timed exits and evictions, under a launcher, and still reads as one continuous run.

Multi-node training is out of scope: HTCondor's parallel universe adds complexity that would distract from checkpointing. Note this in the README and mention it as a possible future recipe.

## What this recipe teaches

- Checkpointing under DDP: rank 0 writes, all ranks load, and every rank agrees on the state.
- Coordinated stopping: all ranks must stop at the same step, or the job deadlocks.
- **Graceful shutdown through a launcher.** Plain `exec torchrun` breaks in two ways (measured, `docs/environment.md` §6): it kills workers ~30 s after SIGTERM, and it turns exit 85 into 1. The version-independent stop-file wrapper fixes both.
- Per-rank data position for sharded streaming data.
- Thinking in steps and tokens rather than epochs at this scale, and why.
- A run that spans many HTCondor executions, with metrics that read as one continuous run.

## Measure first: a throughput smoke run

Recipe 1's estimates came from an L40. The same job ran **4.7× faster on an H200** (1.06M vs. 224k tokens/s) and finished in 48 min, inside a single timed interval. So recipe 2's wall time is **unknown until measured**. The earlier estimates (~11 h on 1 GPU, ~3 h on 4) were made before any H200 measurement and are probably several times too long.

Before anything else (after data preparation), run a few hundred steps on 1 and on 4 GPUs. That's well under 1 GPU-hour, but ask the user before submitting. It gives:
- tokens/s on 1 and 4 GPUs, hence the full run's wall time;
- peak GPU memory per rank at the chosen micro-batch, hence `gpus_minimum_memory` and the micro-batch default;
- start-up time under `torchrun` with 4 ranks and `torch.compile`;
- read throughput from the data shards (see Data).

These numbers set the defaults below that are marked "after the smoke run".

**Measured (2026-10-22):** 200 steps each, `job.sub` with `max_steps=200`; all GPUs were A100-SXM4-80GB, `micro_batch` 32, `torch.compile` on.

| | 1 GPU | 4 GPUs |
|---|---|---|
| Throughput, steady | 206.5k tokens/s | ~740k tokens/s (670–800k): 3.6×, ~90% scaling |
| Peak GPU memory per rank | 22.8 GB | 22.8 GB |
| Process start → first step | 25.0 s | 26.8 s |
| Time reading shards from `/staging` | 0–1% | 0–2% |
| Final save (1,494 MB, 2 files, to `/staging`) | 5.13 s | 5.01 s |
| Val loss at step 200 | 6.3194 | 6.3262 (difference 0.0068) |

- **Full run** (18,892 steps, 9.9B tokens, 106 shards): ~13 h on 1 A100, **~3.7 h on 4 A100s**. Faster GPUs shorten it further.
- **`gpus_minimum_memory = 30000M`:** 22.8 GB plus headroom. With `gpus_minimum_capability = 8.0` (bf16).
- **Data:** reading the shards directly from `/staging` doesn't limit training, so no prefetching is needed.

## Full run (2026-10-22, `job.sub`, 4 × L40S on a backfill slot)

| | |
|---|---|
| Result | 18,892 steps, 9.90B tokens, exit 0; **val loss 3.0424** (`loss_curve.png`) |
| Wall time | 6.28 h in 6 executions: 5 timed exits (1 h demo interval), no evictions |
| Throughput | median 491k tokens/s (p10–p90: 423–525k). The 4-A100 (NVLink) smoke run did ~740k. With `NCCL_P2P_LEVEL=NVL`, the L40S's gradient exchange goes through host memory, which probably accounts for part of the difference |
| Peak GPU memory | 22.8 GB per rank (fresh start), 23.8 GB after a resume |
| Data | 0.1% of the time reading shards from `/staging` (median) |
| Saves | 1.5 GB in 4.9–6.7 s (timed, periodic and final) |

**Cost of one timed checkpoint** (from `metrics.jsonl`; restarts in place):

| Step | Save | Exit → new process | Process start → first step | Total |
|---|---|---|---|---|
| 3,337 | 5.2 s | 7.8 s | 21.6 s | 34.6 s |
| 6,365 | 5.0 s | 7.1 s | 20.8 s | 32.9 s |
| 9,609 | 4.9 s | 7.4 s | 25.4 s | 37.7 s |
| 12,757 | 4.9 s | **1,078 s** | 32.3 s | 1,115 s |
| 15,862 | 6.7 s | 7.9 s | 24.2 s | 38.8 s |

- **The cost:** typically **33–39 s, about 1% of the 1 h demo interval**, or 0.2% of a real 6 h one.
- **The one exception (step 12,757):** HTCondor rescheduled instead of restarting in place (`004 … Code 1025`, as in `docs/environment.md` §5), and the job restarted on the same machine 18 minutes later. That single gap cost more than all the other restarts together.

## Data

- Dataset: FineWeb-Edu, the `sample-10BT` subset (`HuggingFaceFW/fineweb-edu`). Confirm with the user before downloading. The tokenized output is ~20 GB as `uint16`.
- `prepare_data.py` tokenizes with GPT-2 BPE (`tiktoken`) using multiprocessing. It writes fixed-size shards (e.g. 100M tokens each) as `uint16` `.npy` files, plus one validation shard, on `/staging`. This step is CPU-heavy. Provide `prepare.sub` to run it as a CPU-only HTCondor job, and make it resumable at the shard level (skip shards that already exist and are complete).
- **Shard size vs. quota:** ~100–200 shards of 100–200 MB fit the default `/staging` quota (100 GB, 1,000 files) alongside the checkpoints. Larger shards are also faster to read (`/staging` is fast for few large files: 409 MB/s for 1 GB in 1 file; 11–42 MB/s for many small files, `docs/environment.md` §7). State the file count in the README.
- **How the shards reach the job:** read them directly from `/staging` (memory-mapped), not through `transfer_input_files`. 20 GB of input transfer would be repeated at every restart in a fresh sandbox (~16 s for recipe 1's 0.5 GB; far more here), and `/staging` mode already requires `HasCHTCStaging`. Measure the read throughput in the smoke run. If it limits training, prefetch the next shard into scratch in the background.
- Data loading: each rank reads a deterministic, disjoint slice of each shard. The checkpointed data position is `(shard_index, position_within_shard)`, identical in structure across ranks and derivable per rank from rank and world size. Document how to resume correctly if the world size changes. Resuming on a different GPU count is allowed in this recipe, but it should log a warning that the data order changes.

## On epochs at this scale

At 10B tokens the natural unit is tokens or steps, and a single pass over the data is normal. One pass is the whole run: hours on 1 GPU, and probably a few hours on 4 (to be measured). Checkpointing only at epoch boundaries would mean redoing the whole run after an eviction. That is the contrast with recipe 1, whose epochs took 7.5 min on an H200. Make the dataloader support multiple passes (`num_passes` in config, default 1), with a reshuffled shard order per pass, so the "epoch" concept from recipe 1 carries over. In the README, briefly explain why large-scale pretraining usually avoids many repeated passes, and why the checkpointing logic is identical either way.

## Model and training

- GPT-2 small: 12 layers, 12 heads, embedding 768, context 1024, vocab padded to 50304. Generalize recipe 1's `model.py` rather than writing a new one.
- AdamW (fused), cosine schedule with warmup, gradient clipping, gradient accumulation to reach ~0.5M tokens per optimizer step regardless of GPU count. The per-GPU micro-batch is a config value (set after the smoke run). Check the stop flag between micro-batches too, so a stop request never waits for a whole accumulation cycle.
- bf16 autocast, `torch.compile`, TF32 matmuls enabled, flash attention via SDPA.
- Validation loss at regular intervals, on a fixed set of batches (as in recipe 1, so values are comparable across restarts and runs). Optional HellaSwag evaluation (stage the eval data ahead of time).
- Default GPU count: **4** (the most a job can get on one node). Record measured throughput and wall time for 1, 2 and 4 GPUs in the README.

## Checkpointing specifics

- Rank 0 saves the model (unwrap DDP's `.module`, and the `torch.compile` wrapper: `torch_utils.unwrap()`), optimizer, step, tokens seen, data position, and its RNG states. As in recipe 1, the LR comes from the step, so no scheduler state is needed. Every rank's CUDA RNG state should also be saved (gather to rank 0, or have each rank write a tiny per-rank RNG file). Explain the choice.
- All ranks load the checkpoint (mapped to their own device). Use `dist.barrier()` around save and load where needed, and comment why.
- Checkpoint size will be roughly 1.5 GB (fp32 weights + two AdamW moments). Measure save time and size.
- **Storage:** `/staging` mode is the default (in-place periodic saves every 30 min are durable at once). Spool mode is a documented alternative: a 1 GB checkpoint added only ~5 s to an exit-85 restart (§7), and `ON_EXIT_OR_EVICT` keeps the save made after SIGTERM. Measure it, and state when spool stops being reasonable.
- **Timed exit: every hour, as a demonstration value.** `max_runtime_seconds` defaults to 3600 so the full run crosses several timed exits, which is the workflow this recipe exists to show. The config comment, submit file and README say plainly that this is shorter than you'd use for real work, and repeat CHTC's guidance: 6–10 h on backfill, 4–6 h on the OSPool (up to 8). The full run must span **at least 2 intervals**. Originally 2 h; the smoke run measured ~3.7 h for the full run on 4 A100s (less on faster GPUs), which would have given at most one timed exit, so the interval became 1 h (2026-10-22). The timed exit goes through the same rank agreement as the stop flag.
- **Cost of one timed checkpoint:** recipe 1's measured breakdown (`docs/01-tinystories-gpt.md`) is the baseline:
  - save 2.5–4.4 s for 615 MB;
  - spool transfer ≤ 2 s;
  - ~4 s until HTCondor restarts the job in place;
  - start-up ~11 s in place, ~19 s in a fresh sandbox (whose `torch.compile` cache is empty).

  Recipe 2 measures the same parts with `torchrun`, 4 ranks and a 1.5 GB checkpoint, and reports the total against the 1 h interval and against a real 6 h one.
- **Stop agreement:** `torch_utils.agree(flag)` all-reduces the local stop flag (`MAX`) every K steps (configurable, default every step; negligible next to a 0.5M-token step). The flag comes from the signal *or* the stop file. Whichever rank sees it first makes all ranks stop at the same step. Agree on the *reason* too (signal beats timed), so every rank logs and saves the same one.

## Launching

- **The `shell` line, as in recipe 1** (no `run.sh`):
  ```
  shell = export HOME=$PWD; exec python3 htcondor_ckpt/launch.py -- torchrun --standalone --nproc_per_node=4 train.py --config config.yaml --resume auto
  ```
  - `export HOME=$PWD`: the container is read-only, and `torch.compile`/Triton write caches under `$HOME`.
  - `exec`: the wrapper must be the job's top process, the one HTCondor signals (§6).
- **The wrapper** (`htcondor_ckpt/launch.py`, unit-tested in `tests/test_launch.py`):
  - on SIGTERM it creates a stop file and does not forward the signal;
  - workers treat the file like the signal (`StopPolicy` reads the path from the environment);
  - rank 0 records "restart requested";
  - the wrapper exits 85 when that record exists, otherwise passes on `torchrun`'s exit code.

  This depends on no `torchrun` feature. Its shell-script version was measured end to end (§6, P7h). Recipe 2 is the first HTCondor test of `launch.py` itself.
- **Documented alternative:** `torchrun --shutdown-timeout 420` (or `TORCH_ELASTIC_SHUTDOWN_TIMEOUT`). It still needs the exit-code mapping.
- **Torch version:** the container is `recipe1.sif`, PyTorch **2.8**. The `torchrun` behaviour in §6 was measured with **CPU torch 2.14.1**. So recipe 2 re-measures, with its own image and GPUs:
  - plain `exec torchrun` kills a > 30 s save;
  - exit 85 becomes 1;
  - whether `--shutdown-timeout` exists in 2.8.

  Record the results in `docs/environment.md` §6 with the version. The README's note on the alternative names the versions it was confirmed in.
- The README explains, with the measured numbers, why plain `exec torchrun` is not enough.

## HTCondor files

Follow recipe 1's submit files (every line commented in `job.sub`):
- `prepare.sub`: CPU-only data preparation job writing to `/staging` (as recipe 1's).
- `job.sub` (`/staging` mode, the default):
  - the `shell` line above, with `ckpt_dir` and `out_dir` under `/staging/<user>/<run_name>/`, and `data_dir` pointing at the shards;
  - `checkpoint_exit_code = 85`, `kill_sig = SIGTERM`, `requirements = (HasCHTCStaging =?= true)`;
  - `container_image = osdf:///chtc/staging/<user>/<path>/recipe1.sif`;
  - `request_gpus = 4` (parameterized), `gpus_minimum_memory` (after the smoke run: peak memory per rank plus headroom), `+WantGPULab = true`, `+GPUJobLength = "short"` (each execution ends within the 1 h interval, far below the 12 h guarantee), `+is_resumable = true`;
  - CPUs and memory: start from recipe 1's per-GPU numbers (4 CPUs, 24 GB host memory for 1 GPU, which was plenty) and scale; adjust after measuring. Smaller requests match sooner, and a 4-GPU slot is already the hard part.
  - `transfer_input_files`: the code and `htcondor_ckpt` only. The data is read from `/staging`.
- `job_spool.sub`: the documented spool alternative (recipe 1's four spool lines, with `checkpoints, outputs`).
- A commented-out backfill requirement (`TARGET.BackfillSlot =?= true`), with an explanation of backfill eviction: only when the owner needs the GPU (code 1011, "PREEMPT expression evaluated to True", observed in recipe 1's tests, §3).
- `<user>` placeholders everywhere. Personal paths come from environment variables in the test script.
- The README shows users how to see how many times their job has restarted. Use the job event log (eviction and file-transfer events) and the `RESUMED` lines / restart markers in `metrics.jsonl`, rather than polling `condor_q`. Note that `NumJobStarts` does not count exit-85 restarts.

## Carried over from recipe 1

- **Create the checkpoint and output directories first,** before loading data or building the model, so an early crash shows its real error instead of a transfer hold.
- **Log peak GPU memory** at the first step and at every checkpoint. Log the GPU name per rank.
- **Fall back to `compile=false`** with a warning if the container has no C compiler.
- **`metrics.jsonl` in `out_dir`,** append-only, with restart markers. In `/staging` mode it lives on `/staging`.
- **Tools, copied and generalized:**
  - `plot_run.py`: a loss curve with restarts marked;
  - `compare_runs.py`: resume equivalence against two uninterrupted references.

  Give them a recipe-neutral default title. Moving them to a shared location is a packaging question, noted in `htcondor_ckpt/NOTES.md`.
- **Downloaded results** go outside the recipe directory, or into ignored paths (`outputs/`, `job.*`, `test_*`).

## Testing

**`test_htcondor.sh`,** modeled on recipe 1's:
- **Inputs:** `RECIPE2_IMAGE`, `RECIPE2_DATA_DIR`, `RECIPE2_TEST_DIR` environment variables.
- **Isolation:** each test is named from the time plus the script's pid, and gets its own run directory under `$RECIPE2_TEST_DIR`. Tests started together don't collide.
- **Short runs:** `max_steps` plus a `step_delay`, so the test can interrupt the job before it finishes, whatever the GPU, and a timed exit every 2 minutes.
- **Modes:**
  - `timed`, `vacate`, `hold`, `fast` and `inspect`;
  - `reference`: uninterrupted, with `+is_resumable = false` to stay off backfill, and no timed exit.
- **Watching the job:** it reads only the event log. It reports a job that ended before the test could interrupt it, with its machine.
- **It prints every rank's stop line,** to check that all ranks stopped at the same step.

**Resume equivalence and the 1 vs. N GPU match** use recipe 1's method:
- **The comparison:** `compare_runs.py` against two uninterrupted references.
- **The pass rule:** the largest validation-loss difference is ≤ 0.01, or ≤ twice the reference-to-reference difference if that's larger.
- **Don't expect bitwise equality.** On GPUs, even two uninterrupted runs differ, especially on different GPU models (recipe 1: up to 0.0053 in val loss between two references).

## Acceptance criteria

- [ ] Data preparation runs as an HTCondor job and resumes correctly if interrupted. (Ran as an HTCondor job: 106 shards + val, 2026-10-21. Resuming tested locally with a simulated interruption; not yet interrupted on HTCondor.)
- [x] The throughput smoke run on 1 and 4 GPUs is recorded, and the defaults that depend on it are set:
  - the micro-batch;
  - `gpus_minimum_memory`;
  - the demo interval (shortened to 1 h).
- [ ] A short run (a few hundred steps) on 2+ GPUs matches the same run on 1 GPU with equivalent global batch size, by `compare_runs.py`'s rule. (Informally: 1 vs 4 A100s, val loss 0.0068 apart at step 200, within 0.01; the two-reference comparison is still to do.)
- [x] Local SIGTERM test on a multi-GPU node, sending the signal to the top process only as HTCondor does: all ranks stop at the same step, rank 0 saves, the job exits 85, and resume continues from the saved step and data position. (`test_local.py --ddp`, 2 CPU ranks, exact losses after resume; and on 2 H200s under HTCondor, `test_htcondor.sh vacate`, 2026-10-22.)
- [ ] A save that takes longer than 30 s completes under the wrapper. Under plain `exec torchrun` with this image (torch 2.8) it is killed, and exit 85 becomes 1: re-measured and recorded in `docs/environment.md` §6. (Done locally: 2 CPU ranks, torch 2.8. Not yet on GPUs.)
- [x] Resume-equivalence test on a reduced run (e.g. 2,000 steps, 3 interruptions) against two references, with a plot in the README. (2026-10-23, 300 steps, 2 GPUs: two uninterrupted references on H100s differed by up to 0.0061 in val loss; a run with 5 restarts (4 timed, 1 `condor_vacate_job`) on A100-SXM4-40GB differed from them by up to 0.0090, within the allowed 0.0122 (twice the noise floor). `resume_equivalence_gpu.png`; README pending.)
- [x] HTCondor tests on GPU Lab slots: a timed exit 85, `condor_vacate_job`, hold + release, and `-fast`. Logs from all ranks show a clean, coordinated stop. (2026-10-22, 2 GPUs each: `vacate` and `-fast` pass on H200s, with 2 timed exits each, which cover the timed-exit test. `hold` passes: held on L40S, released and resumed on A100-SXM4-40GB, i.e. across GPU types. One start-up after the release took 194 s to the first step, against 21–31 s everywhere else; cause unknown.)
- [x] One run on a backfill slot, with `request_gpus = 2` (or 1): 4 free GPUs on one backfill machine are rare. `BackfillSlot = true` confirmed in the machine ad. (`vacate` and `-fast` ran on a `backfill1_*` slot with 2 H200s; `backfill1_*` slots report `BackfillSlot = true` (condor_status, recipe 1). A 2-GPU `comm` run on an L40 backfill slot was evicted by its owner: `Code 1011`, and the save after SIGTERM worked.)
- [x] A full-length run (10B tokens, 4 GPUs, 1 h timed exits) completes across multiple HTCondor executions, producing one continuous loss curve with restart points marked (`plot_run.py`). (4 × L40S, 6 executions, val loss 3.0424; see "Full run".)
- [ ] Measured throughput, checkpoint size, save time, the cost of one timed checkpoint (save, transfer, restart, `torchrun` + compile start-up) and the `/staging` footprint recorded in the README. (Measured: see "Full run"; README pending.)

## User-facing README outline

1. What's new compared with recipe 1.
2. Quick start: prepare data (CPU job), submit training, monitor.
3. Why every rank must agree to stop, with a short diagram of the deadlock that happens otherwise.
4. How the stop request reaches your training processes: what HTCondor signals, what `torchrun` does with it, and how the wrapper fixes it (measured, with this image's torch version).
5. Choosing the timed-exit interval: why this recipe uses 1 h (to show the workflow) and what to use for real runs.
6. Results: continuous loss curve with restart markers, resume-equivalence plot, throughput table.
7. Adapting this to your own DDP code: a checklist (including `accelerate`/`deepspeed` launchers).
