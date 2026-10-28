#!/usr/bin/env python3
"""
Local tests for recipe 4, on CPU, with a tiny random model of the same kind as Qwen2.5
and made-up token data: no download, no GPU, no HTCondor. A few minutes.

    pip install -r requirements.txt     # torch, transformers, peft
    python3 test_local.py

1. Resume equivalence: a run stopped with SIGTERM three times logs exactly the same
   losses as an uninterrupted run.
2. Timed checkpoint: max_runtime_seconds makes the job save and exit 85.
3. Glidein end: a machine ad with GLIDEIN_ToDie in a few seconds makes the job save and
   exit 85 before then.
4. Hand-off: a job ad whose AllowedJobDuration is nearly used up makes the job save and
   exit 86. handoff.sh (the DAG's script) moves the checkpoint to resume/, and the next
   job continues from it, to the same losses as the uninterrupted run.
5. A different base model is refused.
"""
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEQ, BATCH, N_TRAIN = 32, 8, 240          # 30 steps per epoch
TINY = ["seq_len=%d" % SEQ, "batch_size=%d" % BATCH, "epochs=2", "lora_r=4", "lora_alpha=8",
        "warmup_steps=5", "gradient_checkpointing=false", "deterministic=true",
        "eval_every_steps=0", "eval_batches=2", "log_every=1"]


def make_model(d, layers=2):
    """A tiny Qwen2 model with random weights, saved the way prepare_data.py saves the real one."""
    import torch
    from transformers import AutoModelForCausalLM, Qwen2Config
    torch.manual_seed(0)
    cfg = Qwen2Config(vocab_size=256, hidden_size=32, intermediate_size=64, num_hidden_layers=layers,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=64)
    AutoModelForCausalLM.from_config(cfg).save_pretrained(d)


def make_data(d):
    """Token blocks with some structure, so the loss goes down."""
    rng = np.random.default_rng(0)
    base = rng.integers(0, 256, size=SEQ)
    blocks = np.stack([np.roll(base, k) for k in range(N_TRAIN + 16)]).astype(np.uint32)
    np.save(os.path.join(d, "train.npy"), blocks[:N_TRAIN])
    np.save(os.path.join(d, "val.npy"), blocks[N_TRAIN:])


def run(work, sets=(), env=None, kill_at_step=None):
    """Run train.py in `work`. With kill_at_step, send SIGTERM (what HTCondor does on a
    vacate) as soon as the job prints that step."""
    args = [sys.executable, os.path.join(HERE, "train.py"), "--config", os.path.join(HERE, "config.yaml")]
    for s in TINY + ["model_dir=" + MODEL, "data_dir=" + DATA] + list(sets):
        args += ["--set", s]
    full_env = {k: v for k, v in os.environ.items() if not k.startswith("_CONDOR_")}
    full_env.update(env or {})
    p = subprocess.Popen(args, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=full_env)
    head = ""
    if kill_at_step is not None:
        while True:
            line = p.stdout.readline()
            head += line
            m = re.match(r"step (\d+) ", line)
            if not line or (m and int(m.group(1)) >= kill_at_step):
                break
        p.send_signal(signal.SIGTERM)
    out = head + p.communicate()[0]
    return p.returncode, out


def losses(work):
    """Training loss per step from the log (the last value counts if a step ran twice)."""
    result = {}
    with open(os.path.join(work, "checkpoints", "metrics.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "train":
                result[e["step"]] = e["loss"]
    return result


def check(cond, msg, out=""):
    print(("PASS  " if cond else "FAIL  ") + msg, flush=True)
    if not cond:
        print(out[-3000:])
        sys.exit(1)


def fresh(name):
    d = os.path.join(TMP, name)
    os.makedirs(d)
    return d


def write_ad(path, **attrs):
    with open(path, "w") as f:
        f.write("".join("%s = %s\n" % kv for kv in attrs.items()))
    return path


def main():
    global TMP, MODEL, DATA
    TMP = tempfile.mkdtemp(prefix="recipe4-test-")
    try:
        MODEL, DATA = fresh("model"), fresh("data")
        make_model(MODEL)
        make_data(DATA)

        # 1. resume equivalence
        ref = fresh("reference")
        rc, out = run(ref)
        check(rc == 0 and "DONE" in out, "an uninterrupted run finishes", out)
        reference = losses(ref)
        check(len(reference) == 60 and reference[60] < reference[1],
              "it logs every step, and the loss goes down (%.3f -> %.3f)" % (reference[1], reference[60]))
        check(os.path.exists(os.path.join(ref, "outputs", "final_adapter", "adapter_config.json")),
              "the trained adapters are exported to outputs/final_adapter")

        work = fresh("interrupted")
        for i, target in enumerate((7, 29, 44)):          # mid-epoch, end of epoch 1, mid-epoch 2
            rc, out = run(work, kill_at_step=target)
            check(rc == 85 and "reason: signal" in out, "SIGTERM #%d at step %d: saves and exits 85" % (i + 1, target), out)
        rc, out = run(work)
        check(rc == 0 and "RESUMED" in out, "the last run resumes and finishes", out)
        check(losses(work) == reference, "losses identical to the uninterrupted run at all 60 steps")

        # 2. timed checkpoint
        w = fresh("timed")
        rc, out = run(w, ["max_runtime_seconds=0.5", "limit_margin_seconds=0", "step_delay=0.05"])
        check(rc == 85 and "reason: timed" in out, "max_runtime_seconds: saves and exits 85", out)

        # 3. the glidein's end, from a machine ad
        w = fresh("glidein")
        ad = write_ad(os.path.join(w, "machine.ad"), GLIDEIN_ToDie=int(time.time()) + 12, GLIDEIN_Site='"Test"')
        rc, out = run(w, ["limit_margin_seconds=2", "step_delay=0.3"], env={"_CONDOR_MACHINE_AD": ad})
        check("GLIDEIN_ToDie" in out and rc == 85 and "reason: timed" in out,
              "GLIDEIN_ToDie: saves and exits 85 before the glidein ends", out)

        # 4. hand-off to a new job, as the DAG does it
        w = fresh("handoff")
        ad = write_ad(os.path.join(w, "job.ad"), JobStartDate=int(time.time()), AllowedJobDuration=14)
        rc, out = run(w, ["limit_margin_seconds=2", "step_delay=0.3"], env={"_CONDOR_JOB_AD": ad})
        check(rc == 86 and "reason: handoff" in out, "AllowedJobDuration nearly used up: saves and exits 86", out)
        post = subprocess.run(["bash", os.path.join(HERE, "handoff.sh"), "post", "86"], cwd=w,
                              capture_output=True, text=True)
        check(post.returncode == 1 and os.path.isdir(os.path.join(w, "resume")) and not os.path.exists(os.path.join(w, "checkpoints")),
              "handoff.sh post 86: moves checkpoints/ to resume/ and asks the DAG for a new job", post.stdout + post.stderr)
        rc, out = run(w)                                    # the next job: same directory, fresh job ad
        check(rc == 0 and re.search(r"RESUMED from step \d+ .*handoff\) from resume", out) is not None,
              "the next job resumes from resume/ and finishes", out)
        check(losses(w) == reference, "losses identical to the uninterrupted run, across the hand-off")
        post = subprocess.run(["bash", os.path.join(HERE, "handoff.sh"), "post", "0"], cwd=w, capture_output=True, text=True)
        check(post.returncode == 0, "handoff.sh post 0: the DAG is done", post.stdout + post.stderr)
        post = subprocess.run(["bash", os.path.join(HERE, "handoff.sh"), "post", "1"], cwd=w, capture_output=True, text=True)
        check(post.returncode == 2, "handoff.sh post 1 (an error): the DAG stops instead of retrying")

        # 5. a different base model is refused
        other = fresh("other_model")
        make_model(other, layers=3)
        rc, out = run(work, ["model_dir=" + other])
        check(rc != 0 and "cannot resume" in out and "base model" in out, "a different base model is refused", out)
        print("all tests passed")
    finally:
        shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
