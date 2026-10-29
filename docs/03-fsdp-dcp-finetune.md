# Recipe 3: Full fine-tune of a ~7–8B model with FSDP2 and Distributed Checkpoint

Read `CLAUDE.md` first. This recipe reuses the shared modules in `htcondor_ckpt/` (including the launcher wrapper from recipe 2) and must satisfy the full checkpointing contract, with the adaptations described below for sharded state.

## Decisions (2026-10-28)

| Decision | Why |
|---|---|
| **Style:** advanced content is fine, but easy to read and modify, like recipes 0 and 4. `train.py` in numbered sections listed in its docstring; each advanced feature (async save, the stop decision, resharding) in its own labeled section that says what it does, why, and what to change; FSDP/DCP mechanics in `torch_utils.py` helpers with plain names; plain-language README with tables, "Run it" steps and "Using it for your own model" | The user wants every recipe skimmable and modifiable by someone with a little knowledge. This is the advanced recipe that most beginners won't need, and the README says so up front |
| **Model:** OLMo 3 7B base (`allenai/Olmo-3-1025-7B`, ~7.3B parameters, Apache-2.0, not gated); name in config | A different model family in each recipe (GPT, GPT-2, Qwen, OLMo). Fully open weights, data and code. Fallback: `allenai/OLMo-2-1124-7B`. Confirm the license and parameter count when writing `prepare_data.py` |
| **Data:** a configurable random subset of the Tülu 3 SFT mixture (`allenai/tulu-3-sft-mixture`, ODC-BY), sized so one epoch takes a few hours on 4 GPUs | It's the data AI2 used for OLMo's own instruct models. Dolly-15k (recipe 4) would make an epoch take minutes. Alternative: SmolTalk (Apache-2.0) |
| **Container:** the shared image `containers/recipes.def` (PyTorch 2.8 + CUDA 12.8, transformers 4.57.6, which is the first with OLMo 3) | One image for recipes 1–4. Recipe 0 keeps its own CPU image. transformers 5.x would mean also updating recipe 4's code |
| **GPUs:** 4 GPUs chosen by memory, `gpus_minimum_memory = 79000M` (A100-80GB, H100, H200; RTX PRO 6000 too, see the Blackwell row), not by model name. A documented "start sooner" option with 2 GPUs (same floor). L40S (48 GB) opt-in only if measured to fit | Estimated ~40–45 GB per GPU on 4 GPUs (16 bytes per parameter for weights, gradients and AdamW, plus activations), ~70 GB on 2. Pool history (`docs/environment.md` §11): ~9–11 machines qualify; waiting for 4 free GPUs takes a median ~14 h (41 % over a day), for 2 about 1 h; naming one model makes it 2–3× longer; a 4-GPU backfill job is evicted after a median ~14 h. The README sets these expectations |
| **Backfill built in (decided 2026-10-28):** the default `job.sub` matches GPU Lab *and* backfill slots (`+is_resumable = true`, no requirement either way), and the job adapts at every start (see Checkpointing specifics). The README also gives the one-line requirements for "backfill only" and "GPU Lab only" | Backfill is often free, and we want long jobs to use it. The pool had 4 free ≥ 75 GB backfill GPUs about as often as GPU Lab ones (16 % vs 18 % of snapshots) and the two only partly overlap, so allowing both shortens the wait. The price is evictions (median ~14 h on backfill), which the frequent in-place saves on `/staging` make cheap: a backfill eviction costs at most one save interval plus the wait for new GPUs |
| **Blackwell (RTX PRO 6000):** decided after `probes/gpu_comm/` | They pass the memory floor and the CUDA 12.8 image runs on them, but they're PCIe-only and need `NCCL_P2P_LEVEL=NVL`, which routes FSDP's ~60 GB per GPU per step through host memory. If that's much slower, add `gpus_maximum_capability = 9.0` |
| **Host memory: as small as the measurements allow.** Async saves are optional (a config switch), and the README gives both costs: sync saves need roughly 50–60 GB of host memory but pause training for the whole save (minutes per save); async saves pause it for seconds but hold a CPU copy of every rank's share of the state (~22 GB per rank, ~90 GB in all), so the request roughly doubles. Pick the default after measuring both; load the base model so no rank holds a full copy | Large memory requests take longer to match, in the maintainer's experience, even though the pool history shows plenty of free memory on the machines whenever 4 GPUs were free (§11, which can't see matching). |
| **Checkpoints: in-place saves and the timed exit both follow the slot type the job landed on** (agreed 2026-10-28). GPU Lab (open capacity): in-place saves every 60 min, one timed exit just before the `+GPUJobLength` window ends. Backfill: in-place saves every 30 min, a timed exit every 6–10 h (CHTC's guidance for backfill) | CHTC's 4–6 h (OSPool) and 6–10 h (backfill) intervals are for capacity that can disappear; GPU Lab capacity lasts for the job-length window, so the job can run to it. Fewer exits also matter here: each exit 85 risks losing the 4-GPU claim, and getting 4 GPUs back can take a day (§11; recipe 2 saw 1 reschedule in 5 timed exits, §5). On `/staging` the hourly in-place saves protect against hard kills. See "Checkpointing specifics" |
| **Measure the pool first:** P15 (parallel `/staging` writes and reads), `probes/gpu_comm/` (GPU-to-GPU speed), `probes/gpu_machines.sh` (machines, host memory, how often 4 GPUs are free) | The recipe's defaults (files per rank, save interval, whether a final save is normally attempted, `request_memory`, which GPUs) should rest on numbers |
| **`/staging` quota:** the README keeps the footprint worksheet and the quota request | The maintainer has 1 TB, but a normal user has the default 100 GB, which one checkpoint (~88 GB) fills |

## Measured so far (2026-10-28)

- **`/staging` speed** (P15, `docs/environment.md` §7): a 90 GB save from 4–8 writers took **153–169 s** normally and **230–330 s** in a slow period; loading it with 8 readers took 105–114 s (233–328 s slow). So a final save after SIGTERM normally fits the 600 s window (and the ~420 s target), but a slow period gets close: keep the decision based on the *measured* save time. Write ~1–2 files per rank and **load with ≥ 2 threads per rank** (one stream reads only 100–140 MB/s). An hourly *synchronous* save would pause training 2.5–5.5 min per hour (4–9 %), which argues for async saves despite their memory cost (measure). Deleting an old checkpoint takes seconds.
- **The quota can't be read from inside the job** (free space shows the whole filesystem), so the space check needs a `staging_quota_gb` setting, or a clear message when a write fails.
- **memlock is 8 MB:** confirm `dcp.async_save`'s pinned-memory staging works, or falls back.
- **GPU-to-GPU speed** (`probes/gpu_comm/`): on an NVLink H100 machine, FSDP's communication is ~0.13 s per step: negligible. PCIe machines (L40S, RTX PRO 6000) not measured yet.
- **chirp works in the container** on CHTC and the OSPool: the recipe can report `LastCheckpointStep` / `LastCheckpointReason` to `condor_q` once per checkpoint (optional `htcondor_ckpt/chirp.py`).

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

- Model: OLMo 3 7B base (see Decisions), not gated, so users can run the recipe without extra approvals. Keep the model name a config value. Stage the weights on `/staging` ahead of time (a `prepare.sub` CPU job, as in recipe 4).
- Load with Hugging Face `transformers` for convenience, then apply FSDP2 (`fully_shard`) per transformer block and to the root module. Use a bf16 mixed-precision policy with fp32 reduction where appropriate, and activation checkpointing (configurable). Comment why each choice is made.
- Dataset: a subset of the Tülu 3 SFT mixture (see Decisions; keep it configurable). `prepare_data.py` applies a chat template (a base model may not ship one: then use the matching OLMo 3 instruct model's template, and say so), tokenizes, masks prompt tokens out of the loss, and packs or buckets sequences into fixed-length blocks saved to disk.
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
- **Retention: keep only the newest 1 or 2 checkpoints (default 2, configurable to 1), and delete an older one only once a newer one is known to be saved:** all ranks finished writing (barrier), DCP's own metadata file present, the file count and total size as expected, then `metadata.json`, the rename and `latest`. For async saves the deletion happens when the background write is confirmed, not when it starts. Log each deletion and how long it took (88 GB may take a while on `/staging`). The README explains the trade-off of keeping only one (a corrupt newest checkpoint has no fallback) and gives the footprint for both settings: kept checkpoints plus one being written.

## Checkpointing specifics

- Use `torch.distributed.checkpoint.state_dict.get_state_dict` / `set_state_dict` to obtain and restore sharded model and optimizer state dicts. Wrap the full training state in an object implementing the DCP `Stateful` protocol, so a single `dcp.save` / `dcp.load` call handles model, optimizer, scheduler, step counters and data position.
- RNG states and other small per-rank state: save alongside (a per-rank file, or included in the stateful object). Explain the choice.
- Atomicity: DCP writes many files. Keep the same contract as the other recipes: write into a `.tmp` directory, have all ranks finish (barrier), then rank 0 writes `metadata.json`, renames the directory and updates `latest`. Confirm DCP's own metadata file is present before treating a checkpoint as complete.
- **Async save:** use `dcp.async_save` for periodic checkpoints. Only one async save may be in flight; wait for the previous one before starting another. On a stop request, wait for any in-flight save before deciding what to do next. Note in comments that async save stages a copy of state in CPU memory, and request enough job memory for it.
- **Periodic in-place async saves** (no exit): every 60 minutes on GPU Lab, 30 minutes on backfill (both configurable). These carry the protection against hard kills: on `/staging` each is durable as soon as it's written. Check the interval against P15's save time and the `/staging` traffic it causes (88 GB per hour is ~2 TB a day; worth telling CHTC before long runs).
- **Timed exit by slot type:**
  - **GPU Lab (open capacity), the default:** one timed exit just before the `+GPUJobLength` window ends (e.g. `mediumlong` = 72 h: `max_runtime_seconds` ≈ 71 h; save, exit 85). The save is planned rather than squeezed into the 600 s window that reaching the limit with `+is_resumable` would give. Derive it from the chosen job length, so changing one line in the submit file is enough. Confirm that longer job lengths can get 4 GPUs as easily as `short`; otherwise use the longest that does.
  - **Backfill:** every 6–10 h (CHTC's guidance), plus the 30-minute in-place saves.
  - **Which applies is decided at every start**, because each execution can land on either kind of slot (the same job may run on backfill, be evicted, and resume on GPU Lab). The job reads `BackfillSlot` from `$_CONDOR_MACHINE_AD` and picks the save interval and the timed exit for this execution, then logs it in plain words, e.g. `running on a BACKFILL slot: saving every 30 min, timed exit after 8 h` (and records `slot_type` in `metrics.jsonl`'s restart marker). The settings are two pairs in `config.yaml` (`save_every_minutes_gpulab/_backfill`, `max_runtime_hours_backfill`), with the GPU Lab timed exit derived from the job length. `htcondor_ckpt/stop.py` provides `slot_kind()` (backfill / glidein / regular / unknown) and `gpu_job_length()` (seconds from `+GPUJobLength`); the recipe maps them to its settings in one small, commented block.
  - The README and config comments explain the difference, so users don't carry a 72 h interval to the OSPool or backfill.

### The time-budget decision (central lesson, part 2)

First, before the recipe exists: probe P15a (`probes/`) measures `/staging` with 1, 4 and 8 parallel writers and readers, using dummy data, so the defaults (files per rank, periodic interval, whether the final save is normally attempted) rest on numbers. Then measure, at full scale and on the real `/staging`:
- `T_save`: wall time of a synchronous DCP save.
- `T_async_block`: how long training is blocked by an async save before continuing.
- Checkpoint size and file count.
- `T_load` and the total restart cost.

Then implement the stop policy in `htcondor_ckpt/stop.py` as an explicit, documented decision. The budget comes from `vacate_budget()` (machine/job ads; 600 s on every slot measured), not a hard-coded constant:
- If an async save is in flight, wait for it to finish (bounded by the deadline), then exit 85.
- Else, if the estimated save time (last measured `T_save` plus a safety margin) fits within the remaining budget, do a final synchronous save, then exit 85.
- Else, skip the final save, log clearly how much work since the last periodic checkpoint will be redone, and exit 85.

Write the measured numbers and the resulting recommendation into the README. If `T_save` is uncomfortably close to the budget, recommend a shorter periodic interval as the real protection, and say so plainly: on large jobs, periodic checkpoints carry the safety; the save made after SIGTERM is a bonus. Do not raise `job_max_vacate_time` above 600 s to make a save fit. It was honored on some slots in testing, but on backfill that time belongs to the GPU's owner.

### Safety features for big jobs

- **Collective timeout longer than the save.** A rank waiting at a barrier while another writes its shard must not time out. Set the timeout from the measured save time (recipe 2's 300 s is too short if a save takes 3–4 min), and keep the separate start-up communication check short.
- **Never save a broken state over a good one.** If the loss (or gradient norm) is NaN or infinite, skip the save and stop with a clear message. Matters most with `keep_checkpoints: 1`.
- **Space check before saving.** Before a save, check that the checkpoint directory has room for one more checkpoint (size of the last one). If not, say so clearly instead of leaving a half-written `.tmp`. P15 records whether free space on `/staging` reflects the user's quota; if it doesn't, document the limitation.
- **Delete old checkpoints only after the new one is complete,** and log how long deleting takes (P15 measures it; ~88 GB may take a while).
- **Load the base model without every rank holding a full copy in host memory** (4 × 15 GB). Load on one rank or on the `meta` device and fill shards from the weights; record peak host memory.
- **Log per-rank save times** and peak host memory at every checkpoint.

## Resharding

- Demonstrate saving on N GPUs and resuming on a different count (e.g. 4 → 2, if the model still fits on 2 GPUs with CPU offload; otherwise 4 → 3). The data position must be stored in a world-size-independent form (global sample index), with each rank deriving its slice on load.
- Global batch size stays constant across resharding by adjusting gradient accumulation. Log the adjustment.

## Exporting the model

- A separate `export.py` loads a DCP checkpoint and writes a consolidated Hugging Face-format model (safetensors) for inference. This runs as its own job, not inside training.
- Document the conversion, so users understand that resumable checkpoints and exported models serve different purposes and have different formats. The export's size also counts toward the `/staging` quota.

## HTCondor files

- `job.sub`, every line commented:
  - `request_gpus = 4` (parameterized) and `request_memory` from the measured peak (with or without async saves; see Decisions);
  - `+WantGPULab = true`, `+GPUJobLength = "mediumlong"` (see Checkpointing specifics), `+is_resumable = true`;
  - `gpus_minimum_memory = 79000M`, `gpus_minimum_capability = 8.0`, `NCCL_P2P_LEVEL=NVL`;
  - no slot-type requirement, so the job runs on GPU Lab or backfill, whichever has 4 GPUs free first; commented-out lines for "backfill only" (`TARGET.BackfillSlot =?= true`) and "GPU Lab only" (`TARGET.BackfillSlot =!= true`), each with a one-line explanation of when to use it;
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
- [ ] A run on a backfill slot and one on a GPU Lab slot: each logs the right slot type, save interval and timed exit; a backfill eviction (real or `condor_vacate_job`) resumes from the last save, wherever the job lands next.
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
