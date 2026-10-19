"""
store.py: write checkpoints so a crash can never leave a half-written one, and find
the newest good one again.

Layout of a checkpoint directory (the "root"):

    root/
      step_00000250/        a complete checkpoint: your files + metadata.json
      step_00000500/
      latest                names the newest complete checkpoint
      step_00000750.tmp/    a save that was killed half-way: cleaned up at startup

How a save works:
  1. your write_fn writes its files into step_N.tmp/
  2. metadata.json is written last (its presence marks the checkpoint complete)
  3. everything is fsync'ed (forced onto disk: matters on /staging and after crashes)
  4. step_N.tmp/ is renamed to step_N/. A rename happens all at once, so step_N/ is
     either complete or absent, never half-written
  5. 'latest' is replaced the same way, then old checkpoints beyond `keep` are deleted

Typical use (PyTorch shown, but the store doesn't care what you write):

    from store import CheckpointStore

    store = CheckpointStore("checkpoints", keep=2)
    store.cleanup_stale()
    path, state = store.load(lambda d: torch.load(os.path.join(d, "state.pt")))
    ...
    store.save(step, lambda d: torch.save(state, os.path.join(d, "state.pt")),
               metadata={"reason": "timed"})

Backups that outlive the job (spool + /staging):

In spool mode, HTCondor deletes the spooled checkpoint when the job leaves the queue
(condor_rm, a removal policy, resubmitting after a crash). Keep occasional copies in a
second store on /staging, named after the run (not the job id, which changes when you
resubmit), and resume from whichever store has the newest checkpoint:

    local = CheckpointStore("checkpoints", keep=1)                          # spool
    backups = CheckpointStore("/staging/<user>/<run>/backups", keep=2)       # outlives the job
    path, state = load_newest([local, backups], read_fn)
    ...
    info = local.save(step, write_fn, meta)                 # every timed checkpoint
    if backup_due(backups, every_seconds=12 * 3600):        # only now and then
        backup(info["path"], backups)

Standard library only. No imports from the other htcondor_ckpt modules, so this file
can be copied into a project on its own.
"""

import json
import os
import re
import shutil
import sys
import time

METADATA = "metadata.json"
LATEST = "latest"


class CheckpointStore:
    def __init__(self, root, keep=2, prefix="step_"):
        """root: directory holding the checkpoints. keep: complete checkpoints to keep (>= 1)."""
        if keep < 1:
            raise ValueError("keep must be at least 1")
        self.root = root
        self.keep = keep
        self.prefix = prefix
        self._pattern = re.compile(r"^%s(\d+)$" % re.escape(prefix))
        # Create it now: in spool mode HTCondor holds the job if a directory named in
        # transfer_checkpoint_files doesn't exist at the first exit 85.
        os.makedirs(root, exist_ok=True)

    # ----------------------------------------------------------------- finding
    def cleanup_stale(self):
        """Delete *.tmp leftovers from saves that were killed half-way. Returns their names."""
        removed = [n for n in os.listdir(self.root) if n.endswith(".tmp")]
        for name in removed:
            path = os.path.join(self.root, name)
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
        return removed

    def complete(self):
        """Complete checkpoints, oldest first, as (step, path) pairs."""
        found = []
        for name in os.listdir(self.root):
            m = self._pattern.match(name)
            path = os.path.join(self.root, name)
            if m and os.path.isfile(os.path.join(path, METADATA)):
                found.append((int(m.group(1)), path))
        return sorted(found)

    def candidates(self):
        """Paths to try when resuming, best first: the 'latest' pointer, then newest to oldest."""
        paths = [p for _, p in reversed(self.complete())]
        try:
            with open(os.path.join(self.root, LATEST)) as f:
                pointed = os.path.join(self.root, f.read().strip())
            if pointed in paths:
                paths.remove(pointed)
                paths.insert(0, pointed)
        except OSError:
            pass
        return paths

    def latest(self):
        """The best checkpoint to resume from, or None."""
        paths = self.candidates()
        return paths[0] if paths else None

    def metadata(self, path):
        with open(os.path.join(path, METADATA)) as f:
            return json.load(f)

    def load(self, read_fn):
        """Call read_fn(path) on the best checkpoint. If it fails (a damaged file), warn
        loudly and try the next older one. Returns (path, result), or (None, None) if
        there is no usable checkpoint."""
        for path in self.candidates():
            try:
                return path, read_fn(path)
            except Exception as e:  # damaged or incompatible: fall back to an older one
                print("WARNING: could not load checkpoint %s (%s: %s); trying an older one"
                      % (path, type(e).__name__, e), file=sys.stderr, flush=True)
        return None, None

    # ----------------------------------------------------------------- saving
    def save(self, step, write_fn, metadata=None):
        """Save checkpoint `step`. write_fn(directory) writes your files into it.

        Returns a dict with path, seconds, bytes and files, for logging."""
        t0 = time.time()
        name = "%s%08d" % (self.prefix, step)
        tmp = os.path.join(self.root, name + ".tmp")
        final = os.path.join(self.root, name)
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        write_fn(tmp)
        meta = dict(metadata or {})
        meta.update(step=step, saved_at=time.time(), save_seconds=round(time.time() - t0, 3))
        with open(os.path.join(tmp, METADATA), "w") as f:  # written last: marks it complete
            json.dump(meta, f, indent=2, sort_keys=True, default=str)
        nbytes, nfiles = _fsync_tree(tmp)
        shutil.rmtree(final, ignore_errors=True)  # re-saving the same step replaces it
        os.rename(tmp, final)
        _write_atomic(os.path.join(self.root, LATEST), name)
        _fsync(self.root)
        for _, old in self.complete()[:-self.keep]:  # retention: keep the newest `keep`
            shutil.rmtree(old, ignore_errors=True)
        return {"path": final, "seconds": round(time.time() - t0, 3), "bytes": nbytes, "files": nfiles}


# --------------------------------------------------------------------- helpers
def _fsync(path):
    """Force a file or directory onto disk. Some filesystems refuse fsync on directories."""
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def _fsync_tree(top):
    """fsync every file and directory under top. Returns (bytes, files)."""
    nbytes = nfiles = 0
    for dirpath, _dirs, files in os.walk(top):
        for fn in files:
            path = os.path.join(dirpath, fn)
            _fsync(path)
            nbytes += os.path.getsize(path)
            nfiles += 1
        _fsync(dirpath)
    return nbytes, nfiles


def _write_atomic(path, text):
    """Replace a small text file all at once (write a temp file, then rename over)."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


# --------------------------------------------------------------------- several stores, backups
def newest(stores):
    """The newest complete checkpoint across several stores: (store, path), or (None, None).
    On a tie (the same step in two stores), the store listed first wins, so list the
    local one first."""
    best = (None, None, -1)
    for store in stores:
        for step, path in store.complete():
            if step > best[2]:
                best = (store, path, step)
    return best[0], best[1]


def load_newest(stores, read_fn):
    """Like CheckpointStore.load, across several stores: try checkpoints newest step first
    (local store first on ties); if one fails to load, warn and try the next. Returns
    (path, result), or (None, None)."""
    ordered = []
    for rank, store in enumerate(stores):
        ordered += [(-step, rank, path) for step, path in store.complete()]
    for _, _, path in sorted(ordered):
        try:
            return path, read_fn(path)
        except Exception as e:
            print("WARNING: could not load checkpoint %s (%s: %s); trying an older one"
                  % (path, type(e).__name__, e), file=sys.stderr, flush=True)
    return None, None


def backup_due(backup_store, every_seconds, now=None):
    """True if the newest backup is older than `every_seconds` (or there is none yet).

    The answer comes from the newest backup's metadata.json (its "saved_at" wall-clock
    time), not from memory, so it stays right across exit-85 restarts and resubmissions."""
    complete = backup_store.complete()
    if not complete:
        return True
    saved_at = backup_store.metadata(complete[-1][1]).get("saved_at", 0)
    return (now if now is not None else time.time()) - saved_at >= every_seconds


def backup(checkpoint_path, backup_store):
    """Copy a complete checkpoint into another store (e.g. from spool to /staging),
    with the same write-then-rename safety as any save. Returns the save info dict."""
    with open(os.path.join(checkpoint_path, METADATA)) as f:
        meta = json.load(f)
    step = meta["step"]

    def copy_files(dest):
        for name in os.listdir(checkpoint_path):
            if name == METADATA:
                continue  # rewritten by save(), below
            src = os.path.join(checkpoint_path, name)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(dest, name))
            else:
                shutil.copy2(src, dest)

    meta = {k: v for k, v in meta.items() if k not in ("step", "saved_at", "save_seconds")}
    meta["backup_of"] = checkpoint_path
    return backup_store.save(step, copy_files, meta)
