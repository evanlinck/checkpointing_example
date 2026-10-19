#!/usr/bin/env python3
"""
prepare_data.py: download TinyStories once and turn it into token files for training.

    python3 prepare_data.py --out-dir /staging/<user>/tinystories            # the whole dataset
    python3 prepare_data.py --out-dir /staging/<user>/tinystories --fraction 0.1

Writes, in --out-dir:
  train.bin, val.bin   every story as GPT-2 token ids (uint16), one after another,
                       with an end-of-text token between stories
  meta.json            token and story counts

Run it once (on the access point, or with prepare.sub as a CPU job); every training job
then reads the same files. Each file is written under a temporary name and renamed at
the end, so an interrupted run never leaves a half-written train.bin behind.
"""
import argparse
import json
import os

import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fraction", type=float, default=1.0, help="use only this fraction of each split")
    ap.add_argument("--num-proc", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    args = ap.parse_args()

    import tiktoken
    from datasets import load_dataset

    enc = tiktoken.get_encoding("gpt2")
    eot = enc.eot_token  # <|endoftext|>, id 50256: marks where one story ends

    def tokenize(batch):
        ids = [enc.encode_ordinary(text) + [eot] for text in batch["text"]]
        return {"ids": ids, "n": [len(x) for x in ids]}

    os.makedirs(args.out_dir, exist_ok=True)
    ds = load_dataset("roneneldan/TinyStories")
    counts = {}
    for split, name in (("train", "train"), ("validation", "val")):
        data = ds[split]
        if args.fraction < 1.0:
            data = data.select(range(int(len(data) * args.fraction)))
        data = data.map(tokenize, batched=True, remove_columns=data.column_names, num_proc=args.num_proc,
                        desc="tokenizing %s" % split)
        total = int(np.sum(data["n"], dtype=np.int64))
        final = os.path.join(args.out_dir, name + ".bin")
        tmp = final + ".tmp"
        out = np.memmap(tmp, dtype=np.uint16, mode="w+", shape=(total,))
        pos = 0
        for shard in range(64):  # write in pieces to keep memory use low
            part = data.shard(64, shard, contiguous=True).with_format("numpy")
            arr = np.concatenate(part["ids"]).astype(np.uint16) if len(part) else np.zeros(0, np.uint16)
            out[pos:pos + len(arr)] = arr
            pos += len(arr)
        out.flush()
        del out
        os.replace(tmp, final)
        counts[name] = {"stories": len(data), "tokens": total}
        print("%s: %d stories, %d tokens -> %s (%.0f MB)" % (name, len(data), total, final, total * 2 / 1e6))

    with open(os.path.join(args.out_dir, "meta.json"), "w") as f:
        json.dump({"tokenizer": "gpt2 (tiktoken)", "dtype": "uint16", "fraction": args.fraction, **counts}, f, indent=2)
    print("wrote", os.path.join(args.out_dir, "meta.json"))


if __name__ == "__main__":
    main()
