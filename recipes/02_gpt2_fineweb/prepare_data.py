#!/usr/bin/env python3
"""
prepare_data.py: download FineWeb-Edu (sample-10BT, ~10B tokens) and turn it into token
shards for training. A CPU job: run it with prepare.sub.

    python3 prepare_data.py --out-dir /staging/<user>/fineweb10B                 # everything
    python3 prepare_data.py --out-dir /staging/<user>/fineweb10B-test --max-files 1   # a quick test

Writes, in --out-dir:
  val_000.npy                  the validation shard: the first --val-tokens tokens of the data
  train_fNN_KKK.npy            training shards, GPT-2 token ids (uint16), --shard-tokens each
                               (the last shard of each input file is shorter). NN is the
                               input file the shard came from, KKK its number within that file.
  manifest.json                which input files are finished, and every shard with its size.
                               Training reads this file to find the shards.

The dataset arrives as a list of large parquet files. They're processed one at a time:
download, tokenize (all CPUs), write that file's shards, record it in manifest.json, delete
the download. So the job needs disk for about one input file, not for the whole dataset.

Resumable: if the job is interrupted (evicted, held, removed and resubmitted), the next run
reads manifest.json and skips every input file recorded there, without downloading it again.
Shards are written under a temporary name and renamed when complete, and an input file is
recorded only after all its shards exist. So a half-finished file is simply redone.
The shards' content depends only on the input files and these settings, never on how
often the job was interrupted.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO = "HuggingFaceFW/fineweb-edu"
SUBSET = "sample/10BT/"         # the ~10B-token sample, as a list of parquet files
MANIFEST = "manifest.json"


# ============================================================================ writing shards
def write_atomic(path, array):
    """np.save to path.tmp, then rename: a shard is either complete or absent."""
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        np.save(f, array)
        f.flush()
        os.fsync(f.fileno())    # on /staging, make sure it's on disk before the rename
    os.replace(tmp, path)


class ShardWriter:
    """Collects token arrays and writes them as shards of exactly `size` tokens
    (the last one shorter). Returns [(shard name, tokens), ...] from close()."""

    def __init__(self, out_dir, prefix, size):
        self.out_dir, self.prefix, self.size = out_dir, prefix, size
        self.buf = np.empty(size, dtype=np.uint16)
        self.fill = 0
        self.written = []

    def add(self, tokens):
        while len(tokens):
            n = min(len(tokens), self.size - self.fill)
            self.buf[self.fill:self.fill + n] = tokens[:n]
            self.fill += n
            tokens = tokens[n:]
            if self.fill == self.size:
                self._flush()

    def _flush(self):
        name = "%s_%03d.npy" % (self.prefix, len(self.written))
        write_atomic(os.path.join(self.out_dir, name), self.buf[:self.fill])
        self.written.append((name, int(self.fill)))
        print("  wrote %s (%d tokens)" % (name, self.fill), flush=True)
        self.fill = 0

    def close(self):
        if self.fill:
            self._flush()
        return self.written


# ============================================================================ the manifest
def load_manifest(out_dir):
    path = os.path.join(out_dir, MANIFEST)
    if not os.path.exists(path):
        return {"files": {}, "val": None, "complete": False}
    with open(path) as f:
        return json.load(f)


def save_manifest(out_dir, manifest):
    """Rewritten after every input file, atomically (a small file: write, then rename)."""
    path = os.path.join(out_dir, MANIFEST)
    with open(path + ".tmp", "w") as f:
        json.dump(manifest, f, indent=1)
        f.flush()
        os.fsync(f.fileno())
    os.replace(path + ".tmp", path)


def shards_present(out_dir, shards):
    """True if every recorded shard exists. (Someone may have deleted files by hand.)"""
    return all(os.path.exists(os.path.join(out_dir, name)) for name, _ in shards)


# ============================================================================ tokenizing
_enc = None


def _init_worker():
    global _enc
    import tiktoken
    _enc = tiktoken.get_encoding("gpt2")


def tokenize(text):
    """One document -> uint16 token ids, ending with <|endoftext|> (id 50256), the marker
    between documents. GPT-2's ids all fit in uint16 (vocabulary 50,257)."""
    ids = _enc.encode_ordinary(text)
    ids.append(_enc.eot_token)
    return np.asarray(ids, dtype=np.uint16)


def token_stream(parquet_path, pool, batch_rows=8192):
    """Token arrays for every document in one parquet file, in file order.
    The file is read a batch of rows at a time (the files are large: never load one whole),
    and each batch is tokenized in parallel. pool.map returns results in input order, so the
    shards are the same on every run, whatever the number of processes. (pool.imap over all
    documents would be smoother, but it reads its whole input ahead, into memory.)"""
    import pyarrow.parquet as pq
    for batch in pq.ParquetFile(parquet_path).iter_batches(batch_size=batch_rows, columns=["text"]):
        yield from pool.map(tokenize, batch.column(0).to_pylist(), chunksize=64)


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--shard-tokens", type=int, default=100_000_000,
                    help="tokens per shard (default 100M = 200 MB: few, large files suit /staging)")
    ap.add_argument("--val-tokens", type=int, default=10_000_000,
                    help="size of the validation shard, taken from the start of the first input file")
    ap.add_argument("--max-files", type=int, default=0, help="process only the first N input files (tests)")
    ap.add_argument("--num-proc", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--download-dir", default="hf_download", help="scratch space for one input file at a time")
    args = ap.parse_args()

    import multiprocessing
    from huggingface_hub import hf_hub_download, list_repo_files

    os.makedirs(args.out_dir, exist_ok=True)
    for name in os.listdir(args.out_dir):           # a shard cut off by an earlier interruption
        if name.endswith(".tmp"):
            os.remove(os.path.join(args.out_dir, name))
            print("removed an incomplete file: %s" % name)

    manifest = load_manifest(args.out_dir)
    for key in ("shard_tokens", "val_tokens"):      # the same settings, or the shards don't fit together
        old = manifest.get(key)
        if old is not None and old != getattr(args, key):
            sys.exit("%s already holds shards made with %s=%d (now %d). Use a new --out-dir."
                     % (args.out_dir, key, old, getattr(args, key)))
    manifest.update(shard_tokens=args.shard_tokens, val_tokens=args.val_tokens,
                    tokenizer="gpt2 (tiktoken)", dtype="uint16", source=REPO + "/" + SUBSET)

    inputs = sorted(f for f in list_repo_files(REPO, repo_type="dataset")
                    if f.startswith(SUBSET) and f.endswith(".parquet"))
    if args.max_files:
        inputs = inputs[:args.max_files]
    print("%d input files in %s%s; %d already done" % (len(inputs), REPO, "/" + SUBSET,
          sum(1 for f in inputs if f in manifest["files"])), flush=True)

    with multiprocessing.Pool(args.num_proc, initializer=_init_worker) as pool:
        for i, remote in enumerate(inputs):
            done = manifest["files"].get(remote)
            if done and shards_present(args.out_dir, done["shards"]) and (i > 0 or manifest["val"]):
                continue
            t0 = time.time()
            print("[%d/%d] %s: downloading" % (i + 1, len(inputs), remote), flush=True)
            local = hf_hub_download(REPO, remote, repo_type="dataset", local_dir=args.download_dir)
            t1 = time.time()

            train = ShardWriter(args.out_dir, "train_f%02d" % i, args.shard_tokens)
            # The validation shard: the first documents of the first input file, up to
            # val_tokens. Whole documents only, so no document is split between val and train.
            val = ShardWriter(args.out_dir, "val", args.val_tokens) if i == 0 else None
            val_open = val is not None
            docs = tokens = 0
            for ids in token_stream(local, pool):
                if val_open and val.fill + len(ids) <= args.val_tokens:
                    val.add(ids)
                else:
                    val_open = False      # the first document that doesn't fit ends validation
                    train.add(ids)
                docs += 1
                tokens += len(ids)
            if val is not None:
                manifest["val"] = val.close()
            shards = train.close()
            manifest["files"][remote] = {"shards": shards, "documents": docs, "tokens": tokens}
            save_manifest(args.out_dir, manifest)     # only now is this input file "done"
            os.remove(local)
            t2 = time.time()
            print("[%d/%d] %s: %d documents, %.2fB tokens, %d shards; download %.0f s, tokenize %.0f s "
                  "(%.1fM tokens/s)" % (i + 1, len(inputs), remote, docs, tokens / 1e9, len(shards),
                                        t1 - t0, t2 - t1, tokens / max(t2 - t1, 1e-9) / 1e6), flush=True)

    # "complete": every input file is in. A --max-files test run is complete for its subset only.
    manifest["complete"] = all(f in manifest["files"] for f in inputs)
    manifest["max_files"] = args.max_files
    save_manifest(args.out_dir, manifest)
    n_train = sum(t for f in manifest["files"].values() for _, t in f["shards"])
    n_files = sum(len(f["shards"]) for f in manifest["files"].values()) + len(manifest["val"] or [])
    print("DONE: %.2fB training tokens, %d validation tokens, %d shard files (%.1f GB) in %s"
          % (n_train / 1e9, sum(t for _, t in manifest["val"] or []), n_files,
             (n_train + sum(t for _, t in manifest["val"] or [])) * 2 / 1e9, args.out_dir))


if __name__ == "__main__":
    main()
