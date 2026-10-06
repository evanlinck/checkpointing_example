"""htcondor_ckpt: shared checkpointing code for jobs running under HTCondor.

Import the modules directly (they don't import each other):
    from htcondor_ckpt.stop import StopPolicy        # when to stop (signal, stop file, time limit)
    from htcondor_ckpt.store import CheckpointStore  # atomic checkpoint directories
    from htcondor_ckpt import meta, torch_utils      # metadata, RNG; PyTorch helpers
This file deliberately imports nothing, so `import htcondor_ckpt` never pulls in PyTorch.
"""
