import random

from htcondor_ckpt import meta


def test_config_hash_is_stable_and_order_independent():
    assert meta.config_hash({"a": 1, "b": 2}) == meta.config_hash({"b": 2, "a": 1})
    assert meta.config_hash({"a": 1}) != meta.config_hash({"a": 2})


def test_describe():
    d = meta.describe({"lr": 0.1}, "signal", step=5)
    assert d["reason"] == "signal" and d["step"] == 5 and d["config_hash"] == meta.config_hash({"lr": 0.1})


def test_config_changes():
    assert meta.config_changes({"lr": 0.1, "epochs": 5}, {"lr": 0.1, "epochs": 8, "new": 1}) == \
        {"epochs": (5, 8), "new": (None, 1)}


def test_rng_round_trip():
    random.seed(1)
    state = meta.capture_rng()
    first = [random.random() for _ in range(3)]
    np_first = None
    if "numpy" in state:
        import numpy as np
        np_first = np.random.rand(3).tolist()
    meta.restore_rng(state)
    assert [random.random() for _ in range(3)] == first
    if np_first is not None:
        assert np.random.rand(3).tolist() == np_first
