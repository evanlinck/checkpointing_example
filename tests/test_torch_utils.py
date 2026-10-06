import pytest

torch = pytest.importorskip("torch")
from htcondor_ckpt import torch_utils  # noqa: E402


def test_rng_round_trip():
    state = torch_utils.capture_rng()
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


def test_save_and_load_state(tmp_path):
    torch_utils.save_state(str(tmp_path), {"w": torch.ones(2), "rng": torch_utils.capture_rng()})
    loaded = torch_utils.load_state(str(tmp_path))
    assert torch.equal(loaded["w"], torch.ones(2))
