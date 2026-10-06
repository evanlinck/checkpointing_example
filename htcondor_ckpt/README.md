# htcondor_ckpt

Shared checkpointing code for training jobs that run under HTCondor. Recipe 0 shows the bare pattern in one file; these modules are the reusable, more complete version that recipes 1–3 build on.

It isn't an installable package yet. Copy the files you need, or send the directory with your job (`transfer_input_files = htcondor_ckpt`). The modules don't import each other, so any single file also works on its own.

| Module | What it does | Needs |
|---|---|---|
| [`stop.py`](stop.py) | `StopPolicy`: when to save and stop (HTCondor's SIGTERM, a stop file from `launch.py`, or a runtime limit); `exit_for_restart()` exits 85; `vacate_budget()` reads the vacate window from the job's ads | standard library (uses the `classad` module if installed) |
| [`store.py`](store.py) | `CheckpointStore`: write-then-rename checkpoint directories, a `latest` pointer, fallback to an older checkpoint if the newest is damaged, retention, `.tmp` cleanup | standard library |
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

policy = StopPolicy(max_runtime_seconds=3600)        # also listens for SIGTERM
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

## Tests

From the repository root: `python -m pytest tests`. The `torch_utils` tests are skipped if PyTorch isn't installed.

See [`NOTES.md`](NOTES.md) for open questions and what might change before this becomes a package.
