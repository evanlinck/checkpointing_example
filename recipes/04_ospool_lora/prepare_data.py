#!/usr/bin/env python3
"""
Recipe 4, run once before training: download the base model and the dataset, and turn
the dataset into blocks of tokens.

    python3 prepare_data.py --out-model model --out-data data

Writes:
  model/   the base model (~3 GB), plus recipe4_model.json: which model and which version.
           Large, used by every job: it belongs in your access point's OSDF area.
  data/    train.npy and val.npy (blocks of --seq-len tokens) and meta.json. A few MB:
           it can live next to your submit file.

prepare.sub runs this as a job (it needs internet, ~4 GB of memory and ~10 GB of disk).

The dataset is databricks-dolly-15k (CC BY-SA 3.0): 15,000 instruction/response pairs
written by people. Each one becomes a text like

    ### Instruction:
    <instruction>
    ### Context:          (only if there is one)
    <context>
    ### Response:
    <response><end of text>

All texts are joined and cut into blocks of --seq-len tokens. The model learns from every
token, including the instruction. (A refinement: learn only from the responses.)
"""
import argparse
import json
import os

import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B", help="base model on Hugging Face")
    ap.add_argument("--revision", default="main", help="model version (a branch, tag or commit)")
    ap.add_argument("--dataset", default="databricks/databricks-dolly-15k")
    ap.add_argument("--seq-len", type=int, default=1024, help="tokens per block (config.yaml: seq_len)")
    ap.add_argument("--val-fraction", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--out-model", default="model")
    ap.add_argument("--out-data", default="data")
    args = ap.parse_args()

    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer
    from datasets import load_dataset

    # --- 1. the base model: only the files training and later use need ---
    path = snapshot_download(args.model, revision=args.revision, local_dir=args.out_model,
                             allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"])
    from huggingface_hub import HfApi
    commit = HfApi().model_info(args.model, revision=args.revision).sha
    with open(os.path.join(args.out_model, "recipe4_model.json"), "w") as f:
        json.dump({"repo": args.model, "revision": commit}, f, indent=2)
    size = sum(os.path.getsize(os.path.join(r, n)) for r, _, ns in os.walk(path) for n in ns)
    print("model: %s at %s, %.1f GB in %s/" % (args.model, commit[:12], size / 1e9, args.out_model))

    # --- 2. the dataset, as text ---
    tok = AutoTokenizer.from_pretrained(args.out_model)
    rows = load_dataset(args.dataset, split="train")
    texts = []
    for r in rows:
        t = "### Instruction:\n%s\n" % r["instruction"].strip()
        if r.get("context", "").strip():
            t += "### Context:\n%s\n" % r["context"].strip()
        t += "### Response:\n%s" % r["response"].strip()
        texts.append(t)

    # --- 3. tokens, joined and cut into blocks ---
    ids = []
    for t in texts:
        ids.extend(tok(t)["input_ids"] + [tok.eos_token_id])
    n_blocks = len(ids) // args.seq_len
    blocks = np.array(ids[:n_blocks * args.seq_len], dtype=np.uint32).reshape(n_blocks, args.seq_len)
    order = np.random.default_rng(args.seed).permutation(n_blocks)
    n_val = max(1, int(n_blocks * args.val_fraction))
    os.makedirs(args.out_data, exist_ok=True)
    np.save(os.path.join(args.out_data, "val.npy"), blocks[order[:n_val]])
    np.save(os.path.join(args.out_data, "train.npy"), blocks[order[n_val:]])
    info = {"dataset": args.dataset, "model": args.model, "model_revision": commit,
            "seq_len": args.seq_len, "examples": len(texts), "tokens": len(ids),
            "train_blocks": int(n_blocks - n_val), "val_blocks": int(n_val)}
    with open(os.path.join(args.out_data, "meta.json"), "w") as f:
        json.dump(info, f, indent=2)
    print("data: %d examples, %.1fM tokens -> %d training and %d validation blocks of %d tokens in %s/"
          % (len(texts), len(ids) / 1e6, n_blocks - n_val, n_val, args.seq_len, args.out_data))


if __name__ == "__main__":
    main()
