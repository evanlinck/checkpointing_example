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


# ------------------------------------------------------------- several stores and backups
from htcondor_ckpt.store import backup, backup_due, load_newest, newest  # noqa: E402


def test_newest_across_stores_prefers_higher_step_then_first_store(tmp_path):
    local = CheckpointStore(str(tmp_path / "local"), keep=1)
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)
    staging.save(100, write_text("backup-100"))
    local.save(250, write_text("local-250"))
    store, path = newest([local, staging])
    assert store is local and path.endswith("step_00000250")
    staging.save(250, write_text("backup-250"))            # same step in both: local wins
    assert newest([local, staging])[0] is local
    assert newest([CheckpointStore(str(tmp_path / "empty"))]) == (None, None)


def test_load_newest_falls_back_across_stores(tmp_path, capsys):
    local = CheckpointStore(str(tmp_path / "local"), keep=1)
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)
    staging.save(100, write_text("good"))
    local.save(250, write_text("corrupt"))

    def strict(d):
        if read_text(d) == "corrupt":
            raise ValueError("damaged")
        return read_text(d)

    path, value = load_newest([local, staging], strict)
    assert value == "good" and path.endswith("step_00000100")
    assert "WARNING" in capsys.readouterr().err


def test_resubmitted_job_resumes_from_backup(tmp_path):
    """After condor_rm + resubmit there is no spool: the new sandbox's store is empty."""
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)
    old_local = CheckpointStore(str(tmp_path / "old_sandbox"), keep=1)
    info = old_local.save(300, write_text("state-300"), {"reason": "timed"})
    backup(info["path"], staging)
    new_local = CheckpointStore(str(tmp_path / "new_sandbox"), keep=1)
    path, value = load_newest([new_local, staging], read_text)
    assert value == "state-300" and path.startswith(str(tmp_path / "staging"))


def test_backup_copies_files_and_metadata(tmp_path):
    local = CheckpointStore(str(tmp_path / "local"), keep=1)
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)

    def write_nested(d):
        os.makedirs(os.path.join(d, "shards"))
        with open(os.path.join(d, "shards", "rank0.bin"), "wb") as f:
            f.write(b"x" * 100)
        write_text("main")(d)

    info = local.save(42, write_nested, {"reason": "timed", "config_hash": "abc"})
    b = backup(info["path"], staging)
    assert read_text(b["path"]) == "main"
    assert os.path.getsize(os.path.join(b["path"], "shards", "rank0.bin")) == 100
    meta = staging.metadata(b["path"])
    assert meta["step"] == 42 and meta["reason"] == "timed" and meta["config_hash"] == "abc"
    assert meta["backup_of"] == info["path"]


def test_backup_retention(tmp_path):
    local = CheckpointStore(str(tmp_path / "local"), keep=1)
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)
    for step in (1, 2, 3):
        backup(local.save(step, write_text(str(step)))["path"], staging)
    assert [s for s, _ in staging.complete()] == [2, 3]


def test_backup_due_uses_saved_time_not_memory(tmp_path):
    local = CheckpointStore(str(tmp_path / "local"), keep=1)
    staging = CheckpointStore(str(tmp_path / "staging"), keep=2)
    assert backup_due(staging, 3600)                         # no backup yet
    backup(local.save(1, write_text("1"))["path"], staging)
    saved_at = staging.metadata(staging.latest())["saved_at"]
    assert not backup_due(staging, 3600, now=saved_at + 600)
    assert backup_due(staging, 3600, now=saved_at + 3600)
