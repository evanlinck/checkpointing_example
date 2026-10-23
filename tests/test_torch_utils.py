import pytest

torch = pytest.importorskip("torch")
from htcondor_ckpt import torch_utils  # noqa: E402


def test_rng_round_trip():
    state = torch_utils.capture_rng()
    a = torch.rand(3)
    torch_utils.restore_rng(state)
    assert torch.equal(torch.rand(3), a)


def test_rng_round_trip_current_device_only():
    state = torch_utils.capture_rng(all_devices=False)
    assert state["cuda_all_devices"] is False
    a = torch.rand(3)
    torch_utils.restore_rng(state)
    assert torch.equal(torch.rand(3), a)


def test_restore_rng_from_older_checkpoint():
    state = torch_utils.capture_rng()
    del state["cuda_all_devices"]          # checkpoints written before the option existed
    a = torch.rand(3)
    torch_utils.restore_rng(state)
    assert torch.equal(torch.rand(3), a)


def test_unwrap_compiled_and_plain():
    model = torch.nn.Linear(2, 2)
    assert torch_utils.unwrap(model) is model

    class FakeCompiled(torch.nn.Module):  # what torch.compile's wrapper looks like
        def __init__(self, inner):
            super().__init__()
            self._orig_mod = inner

    assert torch_utils.unwrap(FakeCompiled(model)) is model


def test_agree_without_distributed():
    assert torch_utils.agree(True) is True and torch_utils.agree(False) is False
    assert torch_utils.agree_max(3) == 3 and torch_utils.agree_max(0) == 0


def _agree_worker(rank, world, init_file, levels, out):
    import torch.distributed as dist
    dist.init_process_group("gloo", init_method="file://" + init_file, rank=rank, world_size=world)
    out[rank] = (torch_utils.agree_max(levels[rank]), torch_utils.agree(levels[rank] > 0))
    dist.destroy_process_group()


def test_agree_across_ranks(tmp_path):
    """Two processes, one asking for a timed stop (2), one for nothing (0): both get 2."""
    import torch.multiprocessing as mp
    out = mp.Manager().dict()
    mp.spawn(_agree_worker, args=(2, str(tmp_path / "init"), [2, 0], out), nprocs=2)
    assert dict(out) == {0: (2, True), 1: (2, True)}


def test_save_and_load_state(tmp_path):
    torch_utils.save_state(str(tmp_path), {"w": torch.ones(2), "rng": torch_utils.capture_rng()})
    loaded = torch_utils.load_state(str(tmp_path))
    assert torch.equal(loaded["w"], torch.ones(2))
