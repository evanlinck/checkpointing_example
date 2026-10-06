"""
meta.py: what to record alongside a checkpoint, and random-number state.

- describe(config, reason, ...)  the metadata.json contents: config, its hash, why the
                                 save happened, versions, host, world size
- config_changes(saved, current) which config values differ since the checkpoint was saved
- capture_rng() / restore_rng()  Python's and NumPy's random-number generators

Random numbers matter for resuming: dropout, data augmentation and shuffling all draw
them. Restore the generators and a resumed run continues the same random sequence;
skip it and the run quietly behaves differently from an uninterrupted one. (PyTorch's
generators are in torch_utils.py.)

Standard library only (NumPy is used if installed). No imports from the other
htcondor_ckpt modules, so this file can be copied into a project on its own.
"""

import hashlib
import json
import os
import platform
import random
import socket
import time


def config_hash(config):
    """A short, stable fingerprint of a config dict (same values -> same hash)."""
    text = json.dumps(config, sort_keys=True, default=str)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def describe(config, reason, **extra):
    """The metadata to save with a checkpoint.

    reason: why this save happened: "timed", "signal", "stop_file", "periodic",
            "epoch" or "final". It shows up in the "RESUMED from ..." log line.
    extra:  anything else worth recording (step, epoch, world_size, framework version...).
    """
    meta = {
        "reason": reason,
        "config": config,
        "config_hash": config_hash(config),
        "python": platform.python_version(),
        "host": socket.gethostname(),
        "world_size": int(os.environ.get("WORLD_SIZE", "1")),
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    meta.update(extra)
    return meta


def config_changes(saved_config, current_config):
    """Keys whose values differ between the saved and current config: {key: (saved, now)}.

    Resuming with a changed config is sometimes fine (more epochs, a new log interval)
    and sometimes not (a different model size). Warn on any change; refuse only on
    changes that make the saved state unusable. That decision belongs to your code."""
    keys = set(saved_config) | set(current_config)
    return {k: (saved_config.get(k), current_config.get(k))
            for k in sorted(keys) if saved_config.get(k) != current_config.get(k)}


def capture_rng():
    """State of Python's (and NumPy's, if installed) random-number generators."""
    state = {"python": random.getstate()}
    try:
        import numpy as np
        state["numpy"] = np.random.get_state()
    except ImportError:
        pass
    return state


def restore_rng(state):
    """Put the generators back exactly as capture_rng() found them."""
    random.setstate(state["python"])
    if "numpy" in state:
        import numpy as np
        np.random.set_state(state["numpy"])
