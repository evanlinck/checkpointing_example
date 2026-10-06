"""
torch_utils.py: the PyTorch-specific pieces of checkpointing.

- unwrap(model)          the plain module inside DDP-wrapped / torch.compile'd models,
                         so saved state-dict keys don't depend on how the model was wrapped
- capture_rng() / restore_rng()  torch's CPU and CUDA random-number generators
- agree(flag)            in multi-GPU runs, make every rank stop at the same step
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


def capture_rng():
    """torch's CPU generator and, if available, every CUDA device's generator."""
    return {"torch": torch.get_rng_state(),
            "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None}


def restore_rng(state):
    torch.set_rng_state(state["torch"])
    if state.get("cuda") is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(state["cuda"])


def agree(flag):
    """True on every rank if `flag` is True on ANY rank. Call it at the same point of
    every step on every rank (e.g. agree(policy.should_stop())).

    In a multi-GPU run, each rank sees signals, stop files and clocks on its own. A rank
    that stops alone leaves the others waiting for it in the next collective: a
    deadlock. One tiny all_reduce(MAX) per step makes them stop together. Outside a
    distributed run it simply returns `flag`."""
    if not (dist.is_available() and dist.is_initialized()):
        return bool(flag)
    device = torch.device("cuda", torch.cuda.current_device()) if dist.get_backend() == "nccl" else torch.device("cpu")
    t = torch.tensor([1 if flag else 0], device=device)
    dist.all_reduce(t, op=dist.ReduceOp.MAX)
    return bool(t.item())


def save_state(directory, state):
    """torch.save `state` into a checkpoint directory (use as a CheckpointStore write_fn)."""
    torch.save(state, os.path.join(directory, STATE_FILE))


def load_state(directory, map_location="cpu"):
    """Load what save_state wrote.

    weights_only=False because checkpoints hold Python/NumPy random-number states, which
    PyTorch's stricter default loader refuses. Only load checkpoints you wrote yourself."""
    return torch.load(os.path.join(directory, STATE_FILE), map_location=map_location, weights_only=False)
