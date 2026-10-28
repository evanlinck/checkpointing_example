"""
torch_utils.py: the PyTorch-specific pieces of checkpointing.

- unwrap(model)          the plain module inside DDP-wrapped / torch.compile'd models,
                         so saved state-dict keys don't depend on how the model was wrapped
- capture_rng() / restore_rng()  torch's CPU and CUDA random-number generators
- agree(flag)            in multi-GPU runs, make every rank stop at the same step
- agree_max(level)       the same, carrying a number (e.g. which kind of stop), so every
                         rank also acts for the same reason
- save_state / load_state  torch.save / torch.load into a checkpoint directory

The only htcondor_ckpt file that imports PyTorch. No imports from the other modules,
so it can be copied into a project on its own.

Not here yet: sharded (DCP) checkpoint helpers for FSDP; they arrive with recipe 3.
"""

import os

import torch
import torch.distributed as dist

STATE_FILE = "state.pt"


def unwrap(model):
    """The underlying module of a wrapped model.

    - DistributedDataParallel keeps the real model in .module
    - torch.compile returns a wrapper whose state-dict keys all start with "_orig_mod."

    Saving the unwrapped module's state dict means the checkpoint loads into a plain
    model too, whatever wrapping the next run uses."""
    while True:
        if hasattr(model, "_orig_mod"):
            model = model._orig_mod
        elif isinstance(model, torch.nn.parallel.DistributedDataParallel):
            model = model.module
        else:
            return model


def capture_rng(all_devices=True):
    """torch's CPU generator and, if available, CUDA's.

    all_devices=True: every visible GPU's generator (one process driving all its GPUs).
    all_devices=False: only the current GPU's (one process per GPU, as under torchrun).
    Use False there: each worker usually sees all of the job's GPUs, and reading every
    device's generator starts a CUDA context, with its memory, on GPUs the worker
    doesn't otherwise use."""
    cuda = None
    if torch.cuda.is_available():
        cuda = torch.cuda.get_rng_state_all() if all_devices else [torch.cuda.get_rng_state()]
    return {"torch": torch.get_rng_state(), "cuda": cuda, "cuda_all_devices": all_devices}


def restore_rng(state):
    torch.set_rng_state(state["torch"])
    if state.get("cuda") is not None and torch.cuda.is_available():
        if state.get("cuda_all_devices", True):
            torch.cuda.set_rng_state_all(state["cuda"])
        else:
            torch.cuda.set_rng_state(state["cuda"][0])     # the current device


def agree(flag):
    """True on every rank if `flag` is True on ANY rank. Call it at the same point of
    every step on every rank (e.g. agree(policy.should_stop())).

    In a multi-GPU run, each rank sees signals, stop files and clocks on its own. A rank
    that stops alone leaves the others waiting for it in the next collective: a
    deadlock. One tiny all_reduce(MAX) per step makes them stop together. Outside a
    distributed run it simply returns `flag`."""
    return agree_max(1 if flag else 0) > 0


def agree_max(level):
    """The largest `level` (an int) of all ranks, on every rank. Like agree(), but it can
    carry *what* to do: number the possible actions by urgency (e.g. 0 = go on,
    1 = periodic save, 2 = timed stop, 3 = eviction), and every rank does the most urgent
    one any rank asked for, for the same reason."""
    if not (dist.is_available() and dist.is_initialized()):
        return int(level)
    device = torch.device("cuda", torch.cuda.current_device()) if dist.get_backend() == "nccl" else torch.device("cpu")
    t = torch.tensor([int(level)], device=device)
    dist.all_reduce(t, op=dist.ReduceOp.MAX)
    return int(t.item())


def save_state(directory, state):
    """torch.save `state` into a checkpoint directory (use as a CheckpointStore write_fn)."""
    torch.save(state, os.path.join(directory, STATE_FILE))


def load_state(directory, map_location="cpu"):
    """Load what save_state wrote.

    weights_only=False because checkpoints hold Python/NumPy random-number states, which
    PyTorch's stricter default loader refuses. Only load checkpoints you wrote yourself."""
    return torch.load(os.path.join(directory, STATE_FILE), map_location=map_location, weights_only=False)
