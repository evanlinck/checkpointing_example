# Checkpointing Recipes for HTCondor GPU Jobs

## Purpose

This repository contains baseline training recipes for users of CHTC (the Center for High Throughput Computing at UW–Madison). Each recipe trains or fine-tunes a text generation model, but **the real subject of every recipe is robust job checkpointing**: saving state, surviving eviction, and resuming correctly. Users will copy these recipes as starting points for their own work, so clarity and correctness matter more than raw performance or cleverness.

The checkpointing logic is **framework-neutral**. The core decides *when* to save and *where* (stop signals, deadlines, atomic directories, exit codes). The framework code decides *what* to save and *how* (state dicts, sharded saves). PyTorch is the worked example throughout. The guide shows how the same core plugs into other frameworks.

There are four recipes, each building on the last:

0. `recipes/00_minimal/`: one short plain-PyTorch script with no dependency on our package. It shows the five blocks every job needs (signal flag, atomic save, resume, exit 85, finish). Spec: `docs/00-minimal.md`.
1. `recipes/01_tinystories/`: small GPT trained from scratch on one GPU. Teaches the full single-GPU contract, checkpointing at epoch boundaries *and* during an epoch, and every storage mode. Spec: `docs/01-tinystories-gpt.md`.
2. `recipes/02_gpt2_fineweb/`: GPT-2 124M trained from scratch with DDP on one multi-GPU node. Teaches distributed stop agreement, launchers, and long multi-execution runs. Spec: `docs/02-gpt2-fineweb-ddp.md`.
3. `recipes/03_fsdp_finetune/`: full fine-tune of a ~7–8B model with FSDP2 and PyTorch Distributed Checkpoint (DCP). Teaches sharded, async and resharding checkpoints under a time and storage budget. Spec: `docs/03-fsdp-dcp-finetune.md`.

Build them in order. Do not start a later recipe until the earlier one passes its acceptance criteria.

## What we already know: `docs/environment.md`

HTCondor's behavior on our pools has been **measured**, not assumed. The probe suite in `probes/` produced those measurements; `docs/environment.md` holds them, each with its source. Treat that file as the source of truth. When code or docs depend on HTCondor behavior, cite the relevant section. If the pool's HTCondor version changes, rerun the relevant probes before trusting old numbers.

The facts that shape everything below:

- **Eviction** (CHTC CPU, GPU Lab, GPU backfill, OSPool) sends **SIGTERM** (or `kill_sig`) within a second of the vacate, then SIGKILL after **600 s** (`MachineMaxVacateTime = 10 * 60`). `condor_hold` behaves the same. `condor_vacate_job -fast` kills at once with no signal.
- **A save made after SIGTERM only survives** with **`/staging`**, or with spool plus **`when_to_transfer_output = ON_EXIT_OR_EVICT`** alongside `checkpoint_exit_code = 85`. With `checkpoint_exit_code` alone, it is lost; the job restarts from its last planned exit-85 checkpoint.
- **A planned exit 85 is cheap:** the job usually restarts in the same sandbox on the same host within seconds (1 GB adds ~5 s). It *can* be rescheduled to another host.
- **HTCondor signals only the top process.** `run.sh` must `exec`; child processes are never signaled.
- **`torchrun` kills workers ~30 s after SIGTERM** and **turns exit 85 into exit 1**. Use the stop-file wrapper (measured to work) or `--shutdown-timeout` plus exit-code mapping.
- **GPU slots:** `+is_resumable = true` turns the GPU Lab runtime limit into an eviction instead of a hold (inferred from policy) and makes backfill eligible. Backfill jobs also need `requirements = TARGET.BackfillSlot =?= true` to be placed there. Backfill evicts only when the owner needs the GPU.
- **OSPool:** HTCondor itself almost never evicts. Real evictions come from glidein ends and may give no SIGTERM, so timed exit-85 checkpoints carry the protection there. No `/staging`.
- **`/staging`:** fast for few large files, slow for many small ones. The default quota is 100 GB and 1,000 files per user; users can ask CHTC to raise it.

## Environment

- **Access point:** ap2002 (HTCondor 26.1). Execute points run 25.14.
- **Scheduler:** HTCondor, vanilla universe.
- **Containers:** Apptainer. Images live on `/staging` and are loaded with `container_image = osdf:///chtc/staging/<user>/...sif`, which works on CHTC and OSPool. Give rebuilt images new file names (OSDF caches by name). Build images in an interactive build job, not on the AP.
- **GPUs:** NVIDIA H200 (141 GB) are the target. GPU jobs use `request_gpus`, `+WantGPULab = true`, `+GPUJobLength` (short / medium / mediumlong / long = 12 / 24 / 72 / 168 h guarantee).
- **OSPool:** reached from ap2002 with `want_ospool = true` and `requirements = (Poolname =!= "CHTC")`.
- **Execute points have internet access** (CHTC and OSPool). Large datasets and weights should still be staged ahead of time, for speed and reproducibility.
- **GPUs per node:** up to **4 H200s** per job. Recipes 2–3 default to 4.
- **GPU PyTorch images:** the user has working PyTorch GPU containers. Ask for them when a recipe first needs a GPU image, instead of building one.

## Repository layout

```
CLAUDE.md
docs/
  environment.md              # measured HTCondor behavior (source of truth)
  00-minimal.md  01-tinystories-gpt.md  02-gpt2-fineweb-ddp.md  03-fsdp-dcp-finetune.md
  checkpointing-guide.md      # user-facing guide, written last
probes/                       # maintainer tooling: HTCondor behavior tests (done; rerun when the pool changes). Never used by recipes.
results/                      # probe result summaries cited by docs/environment.md
htcondor_ckpt/                # shared checkpointing modules: written package-ready, NOT packaged yet
  stop.py                     # StopPolicy: signal flag, stop file, runtime limit, deadline, vacate_budget()
  store.py                    # atomic checkpoint dirs, `latest` pointer, discovery + fallback, retention, .tmp cleanup
  meta.py                     # metadata.json, config hash, Python/NumPy RNG
  torch_utils.py              # PyTorch adapter: torch/CUDA RNG, state-dict unwrap, rank agreement, DCP helpers
  launch.py                   # stop-file launcher wrapper (python launch.py -- torchrun ...)
examples/                     # copyable starter files (see below)
tests/                        # unit tests for htcondor_ckpt/
recipes/
  00_minimal/  01_tinystories/  02_gpt2_fineweb/  03_fsdp_finetune/
```

**Shared code: examples now, a package later.** For now there is no `pyproject.toml` and no install step. We first want to learn how these pieces behave in real recipes. But write `htcondor_ckpt/` so that turning it into an installable package later means adding packaging files, not rewriting code:
- **One module per concern,** with the names and boundaries above, and no import side effects.
- **Each module copyable on its own:**
  - the core modules (`stop.py`, `store.py`, `meta.py`) import only the standard library and each other;
  - `torch_utils.py` is the only file that imports PyTorch;
  - `launch.py` is a standalone script.
- **Recipes get the modules** through `transfer_input_files` (or a copy inside the recipe directory, generated from `htcondor_ckpt/`, never edited by hand). Each recipe README says which modules it uses.
- **Readable:** the core stays short enough to read in one sitting (aim for under ~600 lines). It supports Python 3.9+, so it also runs on bare CHTC execute points.
- **`classad`:** an *optional* import in `vacate_budget()`, to evaluate the machine and job ads, with a plain-arithmetic fallback.
- **Keep a short list of what we learn** that would change the package's API (`htcondor_ckpt/NOTES.md`), for when we package it.
- **`probes/` is maintainer tooling** for measuring the pool. It is never part of `htcondor_ckpt/`, `examples/` or the recipes, and nothing outside `probes/` imports from it.

**`examples/`** holds standalone, copyable starter files:
- the recipe-0 script;
- `run.sh`;
- submit templates for each storage mode (CHTC spool, CHTC `/staging`, OSPool);
- the launcher wrapper.

Each works on its own when copied into a user's project. The files use `# ===== CHECKPOINT: <name> =====` banners.

Each recipe directory contains: `prepare_data.py` (except recipe 0), `train.py`, `config.yaml`, `run.sh`, submit files, `requirements.txt` (or the container definition), and a user-facing `README.md`.

## The checkpointing contract

Every recipe must satisfy all of the following. `htcondor_ckpt/` implements the reusable parts. Recipe 0 implements them inline.

### 1. What a resumable checkpoint contains

Framework-neutral fields (every recipe, every framework):
- Model weights, optimizer state, LR scheduler state.
- Global step, epoch, tokens seen.
- Data position: enough to resume mid-epoch without repeating or skipping data (sampler epoch + batch offset, shard index + offset, or a `StatefulDataLoader` state dict).
- RNG states: Python `random`, NumPy, the framework's generators (for PyTorch: `torch` and CUDA on every device).
- Best validation metric so far (for best-model tracking).
- Logging identity (e.g. W&B run id) so logging continues the same run.
- A `metadata.json` with: config, a hash of the config, framework version, world size, save timestamp, save duration, and the reason for the save (`timed`, `signal`, `periodic`, `epoch`, `final`). Its presence marks the checkpoint complete.

PyTorch specifics:
- Training uses bf16 autocast on H200s, so no `GradScaler` is needed. Note this in comments: users on older GPUs using fp16 must save scaler state too.
- If `torch.compile` is used, save the underlying module's state dict, not the compiled wrapper's, to avoid the `_orig_mod.` key-prefix problem. Mention this gotcha in a comment.

### 2. When checkpoints are written

The job exits with **85** ("state saved, restart me") on two equal, first-class triggers, through one code path (`should_stop()` → save → exit 85):

- **Timed exit** (`max_runtime_seconds`, default ~1 h; the HTCondor manual's suggestion). This is CHTC's documented pattern. It is cheap, because the restart is usually in place. It is also the only protection against hard kills and OSPool glidein ends. In spool mode it is also *the* periodic checkpoint: a save that stays in scratch is lost on a hard kill.
- **Eviction** (SIGTERM from a vacate, a hold, backfill preemption, or reaching the GPU runtime limit with `+is_resumable`). See section 3.

Also:
- **Periodic in-place saves** (no exit) on a wall-clock interval are useful in `/staging` mode, where they are durable immediately.
- **At the end of training:** final save, then exit 0. Exit 0 only when training has actually finished.
- **Epoch boundaries vs. during an epoch:** recipes support both (`checkpoint_at: epoch | interval`). Epoch-only checkpointing is simpler and fine when an epoch is shorter than the work you can afford to redo. Interval checkpointing (with the in-epoch data position) is required when it isn't. Recipe 1 demonstrates both side by side. READMEs explain how to choose.

Resumable checkpoints are distinct from **exported models** (best or final weights in a simple loadable format). Keep the two separate in code and in docs.

### 3. Signal handling

- The SIGTERM handler only sets a flag and records the time. It does no I/O and touches no CUDA state.
- The training loop checks the flag at step boundaries. Also check it between micro-batches of long gradient-accumulation cycles and inside evaluation loops. When it is set: finish the current step (or discard a partial accumulation), save, exit 85. The checkpoint is the state after the last *completed* step, and the data position points at the next batch.
- **Deadline:** derive it from the vacate window. `vacate_budget()` reads `$_CONDOR_MACHINE_AD` / `$_CONDOR_JOB_AD` at startup and logs the result. It falls back to 600 s. Start the final save no later than ~70% into the window (≈420 s of 600). Log the time remaining when the save starts and when it finishes. Do not request `job_max_vacate_time` above 600: on backfill that time belongs to the GPU's owner.
- If SIGTERM arrives during a periodic save, finish that save and exit. Do not start a second save.
- Ignore repeated signals after the first.
- **Never exit 0 because of a signal.** HTCondor requeues anyway (measured), but the code should say what it means.
- Set `kill_sig = SIGTERM` explicitly in submit files, so the signal the code handles is visible.
- **Process tree:** HTCondor signals only the top process. `run.sh` must `exec` Python (or the launcher wrapper). A wrapper that has to do work after training must trap and handle the signal itself. Workers and DataLoader children need no handler of their own, but making DataLoader workers ignore SIGTERM in `worker_init_fn` stays as cheap insurance for other schedulers.
- **Distributed runs:** ranks must agree on when to stop. Use a cheap collective (`all_reduce` with `MAX` on a one-element tensor) each step or every few steps, so all ranks stop at the same step. A rank that stops alone deadlocks the others. The runtime limit goes through the same agreement.
- **Launchers** (`torchrun`, `accelerate`, `deepspeed`, `mpirun`):
  - **Default: the version-independent stop-file wrapper** (`htcondor_ckpt/launch.py`). On SIGTERM it creates a stop file and does *not* forward the signal, so the launcher never starts its own kill timer. Workers treat the file like the signal. After the launcher exits, the wrapper exits 85 if the workers asked for a restart.
  - **Optional convenience on recent PyTorch:** `torchrun --shutdown-timeout` / `TORCH_ELASTIC_SHUTDOWN_TIMEOUT`, with a version note. It still needs the exit-code mapping.

### 4. Atomic writes, storage and retention

- Write each checkpoint to a temporary directory (e.g. `step_00012000.tmp/`), flush and `fsync`, then rename it to its final name. Update a `latest` pointer file last, also atomically.
- On resume, pick the newest *complete* checkpoint. Ignore `.tmp` directories and anything missing `metadata.json`. If the newest fails to load, fall back to the previous one and warn loudly.
- Keep the last N resumable checkpoints (configurable; default 2, and 1 in spool mode to keep transfers small) plus the best exported model.
- Clean up stale `.tmp` directories on startup (a hard kill mid-save leaves them, as measured).
- **Spool mode:** list **one directory** in `transfer_checkpoint_files` and create it before the first possible exit 85. A listed path that doesn't exist puts the job on hold.
- **`/staging` mode:** write few, large files (many small files are 10–40× slower). Every README states the checkpoint footprint: size × checkpoints kept, plus one in progress, and the file count. If it exceeds the default quota (100 GB / 1,000 files), the README tells users to request a larger quota from CHTC.

### 5. Resuming

- `train.py --resume auto` resumes from the latest valid checkpoint if one exists and starts fresh otherwise. This is the default in submit files, so the same command works for the first start and every restart.
- `--resume <path>` resumes from a specific checkpoint.
- Detect "this is a restart" from what is on disk, never from `NumJobStarts` in the sandbox job ad: it is not updated on exit-85 restarts. Never assume the restart is in the same sandbox.
- On resume, compare the saved config hash with the current config. Warn on mismatch; refuse only if the change makes the state incompatible (e.g. model shape).
- Log a clear "RESUMED from step X (saved because: <reason>) at time Y" line.

### 6. HTCondor integration

Storage modes, selected in config and in the submit file:

| Mode | Submit lines | Where | Use for |
|---|---|---|---|
| **Spool** | `checkpoint_exit_code = 85`, `transfer_checkpoint_files = <dir>`, `when_to_transfer_output = ON_EXIT_OR_EVICT` | CHTC and OSPool | Recipes 0–1 (and 2 if the checkpoint stays ~1–2 GB) |
| **Staging** | `checkpoint_exit_code = 85`, checkpoint dir under `/staging/<user>/...` passed as an argument, `requirements = HasCHTCStaging =?= true` | CHTC only | Recipes 2–3, large checkpoints |

- **Not recommended:** `checkpoint_destination`. `file://` fails and holds the job. `osdf://` works but restores slowly, and no SIGTERM save through it has been tested.
- **GPU recipes** set `+is_resumable = true` and `+GPUJobLength`. Submit files document the optional backfill requirement (`TARGET.BackfillSlot =?= true`).
- **Every submit file** has `checkpoint_exit_code = 85`, `kill_sig = SIGTERM`, and a container image loaded via `osdf://`. Every line in user-facing submit files is commented.

### 7. Logging

- Append-only metrics log (JSONL) in the run directory that survives restarts, with an explicit restart marker each time the job resumes. In spool mode the log lives inside the checkpoint directory so it travels with it.
- Per checkpoint, log: step, wall time, save duration, size on disk, file count, and reason.
- Optional W&B support that resumes the same run id. Everything must work with W&B disabled and no network.

### 8. Testing and acceptance

`tests/` must include unit tests for:
- atomic write;
- latest-checkpoint discovery and fallback on a corrupted checkpoint;
- stale `.tmp` cleanup;
- RNG round-trip;
- the stop policy (signal, stop file, runtime limit, deadline);
- `vacate_budget()` on sample ads;
- the launcher wrapper with a fake launcher.

Each recipe must pass:
- **A local signal test:** start a short run, send `kill -TERM` at a random step, confirm it saves and exits 85, then resume and finish.
- **A resume-equivalence test:** run N steps uninterrupted, then the same N steps with several interruptions and resumes, and compare loss curves. With deterministic settings they should match within a small tolerance. Document the tolerance and why exact bitwise equality may not hold (nondeterministic CUDA kernels). The overlaid plot is a key teaching artifact; include it in each README.
- **Save time and checkpoint footprint at full scale,** recorded in the README and compared against the 600 s budget and the `/staging` quota.
- **HTCondor tests on the recipe's target pools:**
  - a timed exit 85;
  - `condor_vacate_job`;
  - `condor_hold` then `condor_release`;
  - `condor_vacate_job -fast` (resumes from the last durable checkpoint).

  Each recipe gets its own small, user-readable way to drive these (e.g. a short `test_eviction.sh` that waits on the job's event log and runs the HTCondor command once). The probes' `trigger.py` shows a working pattern to adapt (event log only, no `condor_q` polling), but recipes must not import from `probes/`.

## Coding conventions

- Recipes: Python 3.11+ in containers. The package core: Python 3.9+. As few dependencies as practical (`numpy`, `tiktoken` or Hugging Face tokenizers, `datasets` for preparation only, `pyyaml`). Pin versions per recipe.
- Configuration in YAML loaded into a dataclass, with CLI overrides for common fields.
- Comments explain *why*, especially around checkpointing decisions. These files are teaching material. When a decision rests on a measurement, say so ("HTCondor signals only the top process; see docs/environment.md §6").
- Mark checkpoint code in recipe 0 and in `examples/` with `# ===== CHECKPOINT: <name> =====` banners so users can find and copy each block. The guide's snippets are taken verbatim from them.
- No hidden magic: a user should be able to trace every saved field from save to restore.
- Ask the user before downloading large datasets or model weights, and before submitting jobs that use more than about one GPU-hour.

## Working order

1. ~~Measure HTCondor behavior (probes) and fill in `docs/environment.md`.~~ Done.
2. Recipe 0 (dependency-free reference), including its local and HTCondor tests on CHTC and OSPool.
3. The `htcondor_ckpt/` core modules, factored out of recipe 0, plus their unit tests and `examples/`. Don't package them yet.
4. Recipe 1, then the PyTorch adapter's distributed parts and the launcher wrapper, then recipe 2, then recipe 3.
5. Write `docs/checkpointing-guide.md` last, using measurements and plots from the real runs. Topics it must cover:
   - **When a SIGTERM save happens and what it contains:** step boundaries, and why not to save inside the handler.
   - **Which storage setups make that save durable.**
   - **Epoch length vs. checkpoint interval.**
   - **Epoch vs. interval checkpointing.**
   - **Graceful shutdown with launchers:** version-independent first.
   - **Plugging the core into other frameworks:** Lightning, Hugging Face Trainer, JAX/Orbax, Keras.
   - **Sizing and requesting `/staging` quota.**
