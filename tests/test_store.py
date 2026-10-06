import json
import os

import pytest

from htcondor_ckpt.store import CheckpointStore


def write_text(text):
    def write(d):
        with open(os.path.join(d, "state.txt"), "w") as f:
            f.write(text)
    return write


def read_text(d):
    with open(os.path.join(d, "state.txt")) as f:
        return f.read()


def test_save_creates_complete_checkpoint_and_pointer(tmp_path):
    store = CheckpointStore(str(tmp_path / "ck"), keep=2)
    info = store.save(10, write_text("ten"), {"reason": "timed"})
    assert os.path.basename(info["path"]) == "step_00000010"
    assert info["files"] == 2 and info["bytes"] > 0
    assert open(tmp_path / "ck" / "latest").read() == "step_00000010"
    meta = store.metadata(info["path"])
    assert meta["step"] == 10 and meta["reason"] == "timed"
    assert not any(n.endswith(".tmp") for n in os.listdir(tmp_path / "ck"))


def test_retention_keeps_newest(tmp_path):
    store = CheckpointStore(str(tmp_path), keep=2)
    for step in (1, 2, 3, 4):
        store.save(step, write_text(str(step)))
    assert [s for s, _ in store.complete()] == [3, 4]


def test_incomplete_and_stale_are_ignored_and_cleaned(tmp_path):
    store = CheckpointStore(str(tmp_path), keep=3)
    store.save(5, write_text("five"))
    os.makedirs(tmp_path / "step_00000009.tmp")          # killed mid-save
    os.makedirs(tmp_path / "step_00000008")              # no metadata.json: not complete
    assert store.latest().endswith("step_00000005")
    assert store.cleanup_stale() == ["step_00000009.tmp"]
    assert not (tmp_path / "step_00000009.tmp").exists()


def test_load_falls_back_when_newest_is_corrupt(tmp_path, capsys):
    store = CheckpointStore(str(tmp_path), keep=2)
    store.save(1, write_text("one"))
    store.save(2, write_text("two"))

    def strict_read(d):
        text = read_text(d)
        if text != "one" and text != "two":
            raise ValueError("corrupt")
        return text

    with open(tmp_path / "step_00000002" / "state.txt", "w") as f:  # damage the newest
        f.write("garbage")
    path, value = store.load(strict_read)
    assert path.endswith("step_00000001") and value == "one"
    assert "WARNING: could not load checkpoint" in capsys.readouterr().err


def test_load_with_no_checkpoint(tmp_path):
    assert CheckpointStore(str(tmp_path)).load(read_text) == (None, None)


def test_latest_pointer_wins_over_numbering(tmp_path):
    store = CheckpointStore(str(tmp_path), keep=3)
    store.save(1, write_text("one"))
    store.save(2, write_text("two"))
    with open(tmp_path / "latest", "w") as f:
        f.write("step_00000001")
    assert store.latest().endswith("step_00000001")


def test_resave_same_step_replaces(tmp_path):
    store = CheckpointStore(str(tmp_path))
    store.save(7, write_text("a"))
    store.save(7, write_text("b"))
    assert read_text(store.latest()) == "b"


def test_keep_must_be_positive(tmp_path):
    with pytest.raises(ValueError):
        CheckpointStore(str(tmp_path), keep=0)
