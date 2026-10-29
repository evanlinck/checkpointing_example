# htcondor_ckpt

Shared checkpointing code for training jobs that run under HTCondor. Recipe 0 shows the bare pattern in one file; these modules are the reusable, more complete version that recipes 1–3 build on.

It isn't an installable package yet. Copy the files you need, or send the directory with your job (`transfer_input_files = htcondor_ckpt`). The modules don't import each other, so any single file also works on its own.

| Module | What it does | Needs |
|---|---|---|
| [`stop.py`](stop.py) | `StopPolicy`: when to save and stop (HTCondor's SIGTERM, a stop file from `launch.py`, or a runtime limit); `exit_for_restart()` exits 85; `vacate_budget()` reads the vacate window from the job's ads; `runtime_limit()` / `job_time_left()` shorten the timed exit before glidein ends and access-point limits; `slot_kind()` says whether this execution landed on backfill, an OSPool glidein or a regular slot, and `gpu_job_length()` reads CHTC's `+GPUJobLength`, to pick the save interval and timed exit per execution | standard library (uses the `classad` module if installed) |
| [`store.py`](store.py) | `CheckpointStore`: write-then-rename checkpoint directories, a `latest` pointer, fallback to an older checkpoint if the newest is damaged, retention, `.tmp` cleanup. Plus `backup()` / `backup_due()` / `load_newest()` for copies on `/staging` that outlive the job | standard library |
| [`meta.py`](meta.py) | what to record with a checkpoint (config, its hash, reason, versions), config comparison, Python/NumPy RNG state | standard library (NumPy optional) |
| [`torch_utils.py`](torch_utils.py) | PyTorch pieces: unwrap DDP/`torch.compile` models, torch/CUDA RNG state, `agree()` so all GPUs stop at the same step, save/load a state dict | PyTorch |
| [`launch.py`](launch.py) | wrapper for multi-process launchers (`torchrun` etc.) so the stop signal and exit 85 survive them | standard library |

Python 3.9 or newer.

## A training loop using them

```python
import os
from htcondor_ckpt.stop import StopPolicy
from htcondor_ckpt.store import CheckpointStore
from htcondor_ckpt import meta, torch_utils

policy = StopPolicy(max_runtime_seconds=6 * 3600)   # timed checkpoint; also listens for SIGTERM
store = CheckpointStore("checkpoints", keep=2)
store.cleanup_stale()                                  # leftovers from a killed save

path, state = store.load(torch_utils.load_state)       # newest good checkpoint, or (None, None)
if state:
    model.load_state_dict(state["model"])
    ...                                                # optimizer, scheduler, position, RNG
    print("RESUMED from", path, "saved because:", store.metadata(path)["reason"])

for batch in batches_from(position):
    train_step(batch)
    if policy.should_stop():                           # signal, stop file, or time limit
        print(policy.describe())
        state = {"model": torch_utils.unwrap(model).state_dict(), ...,
                 "rng": {**meta.capture_rng(), **torch_utils.capture_rng()}}
        store.save(step, lambda d: torch_utils.save_state(d, state),
                   meta.describe(config, policy.reason, step=step))
        policy.exit_for_restart()                      # exit 85: "restart me"
```

With several GPUs, replace `policy.should_stop()` with `torch_utils.agree(policy.should_stop())`, so all ranks stop at the same step.

## Backups that outlive the job

In spool mode, HTCondor deletes the spooled checkpoint when the job leaves the queue: `condor_rm`, a policy that removes held jobs, or resubmitting after something went wrong. To survive that, copy a checkpoint to `/staging` now and then, and resume from whichever is newest:

```python
from htcondor_ckpt.store import CheckpointStore, backup, backup_due, load_newest

local = CheckpointStore("checkpoints", keep=1)                          # spool: every timed checkpoint
backups = CheckpointStore("/staging/<user>/<run_name>/backups", keep=2)  # named after the run, not the job id
path, state = load_newest([local, backups], torch_utils.load_state)      # newest of the two

# at each timed checkpoint (never in the SIGTERM path: that time is for the main save)
info = local.save(step, write_fn, metadata)
if backup_due(backups, every_seconds=12 * 3600):
    backup(info["path"], backups)
```

`backup_due` reads the time of the newest backup from its `metadata.json`, so it stays right across restarts and resubmissions. The job needs `requirements = HasCHTCStaging =?= true` (CHTC only; the OSPool has no `/staging`).

### How often to back up

The two intervals protect against different things:
- **Timed checkpoints** (exit 85) bound what a hard kill can take while the job is queued. Evictions with SIGTERM already get their own save. CHTC usually suggests **4–6 hours on the OSPool (up to 8)** and **6–10 hours on CHTC backfill**. Each one costs a save, a transfer and a restart, so measure that cost and keep it small compared with the interval.
- **Backups** cover losing the job itself. That's rare, so back up less often: the interval is how much work you'd accept redoing if you had to resubmit from scratch.

Starting points:

Backups only happen at timed checkpoints, so a backup interval is a whole number of timed intervals (6–10 h on CHTC backfill):

| How long the whole run takes | Backup to `/staging` | Backups kept |
|---|---|---|
| fits in one or two timed intervals (under ~12 hours) | not needed (a resubmit costs at most a few hours) | 0 |
| up to about a day | at every timed checkpoint | 2 |
| 1 – 3 days | about every 12 hours (every other checkpoint) | 2 |
| several days – 2 weeks | every 12–24 hours | 2–3 |

Adjust for:
- **Write time:** a backup should take well under 1% of its interval. 1 GB takes a few seconds on `/staging`; 100 GB takes minutes.
- **Quota:** backups kept × checkpoint size (and file count) must fit your `/staging` quota (default 100 GB, 1,000 files; you can ask CHTC for more).
- **Timing:** `backup_due(backups, every_seconds=...)` is checked at each timed checkpoint, so the real interval rounds up to the next one.

## Tests

From the repository root: `python -m pytest tests`. The `torch_utils` tests are skipped if PyTorch isn't installed.

See [`NOTES.md`](NOTES.md) for open questions and what might change before this becomes a package.
