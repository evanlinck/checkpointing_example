#!/usr/bin/env python3
"""
Recipe 4: fine-tune a language model with LoRA on the OSPool, and survive anything
that happens to the job.

    python3 train.py --config config.yaml [--set name=value ...]

The same command works for the first start and every restart: it continues from the
newest checkpoint if there is one.

What happens, in order (each step is a numbered section below):
  1. Settings      config.yaml, plus any --set changes
  2. Time limits   when this run must stop and save: our own timer, the end of the
                   glidein we run in, and the access point's limits
  3. Data          the token blocks made by prepare_data.py
  4. Model         the base model (never changed) plus small LoRA adapters (trained)
  5. Resume        continue from the newest checkpoint, if there is one
  6. Train         one step at a time; after each step, check whether to stop
  7. Stop          save, then exit with a code that tells HTCondor what to do next:
                     85 = "restart me"            (HTCondor restarts this job)
                     86 = "continue in a new job" (the DAG submits the next job)
                      0 = "finished"

The checkpointing helpers come from ../../htcondor_ckpt (the submit file sends that
directory with the job): stop.py decides when to stop, store.py writes checkpoints safely.
"""
import time

T_PROCESS_START = time.time()  # to measure how long a restart takes

import json
import math
import os
import resource
import shutil
import sys
from contextlib import nullcontext
from dataclasses import asdict, dataclass, fields

import numpy as np
import torch
import yaml

try:  # in a job, htcondor_ckpt/ sits next to this file; in the repository it's two levels up
    import htcondor_ckpt  # noqa: F401
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from htcondor_ckpt import meta, torch_utils
from htcondor_ckpt.stop import EXIT_RESTART, StopPolicy, job_time_left, runtime_limit
from htcondor_ckpt.store import CheckpointStore, load_newest

EXIT_HANDOFF = 86   # our own code: "save done, continue in a new job" (the DAG retries the job)
EXIT_DONE = 0       # training finished


# ============================================================================ 1. settings
@dataclass
class Config:
    model_dir: str = "model"
    data_dir: str = "data"
    ckpt_dir: str = "checkpoints"
    resume_dir: str = "resume"
    out_dir: str = "outputs"
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_targets: str = "q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj"
    seq_len: int = 1024
    epochs: int = 2
    batch_size: int = 8
    lr: float = 2e-4
    min_lr: float = 2e-5
    warmup_steps: int = 50
    weight_decay: float = 0.0
    grad_clip: float = 1.0
    seed: int = 1234
    gradient_checkpointing: bool = True
    deterministic: bool = False
    eval_every_steps: int = 200
    eval_batches: int = 20
    log_every: int = 10
    keep_checkpoints: int = 1
    max_runtime_seconds: float = 18000
    limit_margin_seconds: float = 900
    step_delay: float = 0.0
    max_steps: int = 0


# Changing these makes the saved adapters unusable: refuse to resume. Other changes only warn.
SHAPE_KEYS = ("lora_r", "lora_targets", "seq_len")


def load_config(path, overrides):
    """config.yaml, then any --set name=value (converted to the setting's type)."""
    with open(path) as f:
        values = yaml.safe_load(f) or {}
    types = {f.name: f.type for f in fields(Config)}
    for item in overrides:
        name, _, raw = item.partition("=")
        if name not in types:
            sys.exit("unknown setting in --set: %s" % name)
        values[name] = yaml.safe_load(raw) if types[name] is not str else raw
    unknown = set(values) - set(types)
    if unknown:
        sys.exit("unknown settings in %s: %s" % (path, ", ".join(sorted(unknown))))
    return Config(**values)


def lr_at(step, cfg, total_steps):
    """Warm up, then decay along a cosine. It depends only on the step, so the saved step is
    all the learning-rate schedule needs to resume."""
    if step < cfg.warmup_steps:
        return cfg.lr * (step + 1) / cfg.warmup_steps
    progress = min(1.0, (step - cfg.warmup_steps) / max(1, total_steps - cfg.warmup_steps))
    return cfg.min_lr + 0.5 * (cfg.lr - cfg.min_lr) * (1 + math.cos(math.pi * progress))


def main():
    args = sys.argv[1:]
    config_path = args[args.index("--config") + 1] if "--config" in args else "config.yaml"
    sets = [args[i + 1] for i, a in enumerate(args) if a == "--set"]
    cfg = load_config(config_path, sets)
    cfg_dict = asdict(cfg)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    # bf16 on GPUs from the A100 on: no GradScaler needed. (fp16 on older GPUs would need one,
    # and its state would have to be saved in the checkpoint too.)
    autocast = torch.autocast("cuda", dtype=torch.bfloat16) if device == "cuda" else nullcontext()
    if cfg.deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        # warn_only: on GPUs, attention's backward pass has no deterministic version; PyTorch
        # warns about it instead of stopping. (Exact on CPU, as the local tests show.)
        torch.use_deterministic_algorithms(True, warn_only=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    # ======================================================================== 2. time limits
    # Three things can end this run. We stop and save before whichever comes first:
    #   - our own timer (max_runtime_seconds): the timed checkpoint, every 5 h by default;
    #   - the glidein's end (GLIDEIN_ToDie): a hard kill without warning;
    #   - the access point's limit per execution (AllowedExecuteDuration, 20 h on ap40).
    # runtime_limit() reads the last two from the job's ads (docs/environment.md §10).
    limit, limit_source = runtime_limit(cfg.max_runtime_seconds, margin=cfg.limit_margin_seconds)
    # And the access point's limit on the whole job (AllowedJobDuration, 14 days on ap40 for
    # checkpointing jobs). Before it, we hand over to a new job instead of restarting this one.
    job_left = job_time_left(margin=cfg.limit_margin_seconds)
    handoff = job_left is not None and (limit is None or job_left <= limit)
    if handoff:
        limit, limit_source = max(job_left, 0.0), "AllowedJobDuration (then hand over to a new job)"
    policy = StopPolicy(max_runtime_seconds=limit)   # also catches HTCondor's SIGTERM
    print("TIME LIMIT for this run: %s (from %s)"
          % ("%.0f s" % limit if limit is not None else "none", limit_source), flush=True)

    # ======================================================================== 3. data
    # prepare_data.py cut the text into blocks of seq_len tokens. Each epoch visits every
    # block once, in an order made from (seed, epoch), so after a restart we can rebuild
    # exactly that order: the checkpoint only needs (epoch, batch_index).
    train = np.load(os.path.join(cfg.data_dir, "train.npy"), mmap_mode="r")
    val = np.load(os.path.join(cfg.data_dir, "val.npy"), mmap_mode="r")
    if train.shape[1] != cfg.seq_len:
        sys.exit("data blocks have %d tokens but seq_len is %d" % (train.shape[1], cfg.seq_len))
    steps_per_epoch = len(train) // cfg.batch_size
    total_steps = cfg.max_steps or cfg.epochs * steps_per_epoch

    def batch(blocks, ids):
        x = torch.from_numpy(np.stack([blocks[i] for i in ids]).astype(np.int64))
        return x.pin_memory().to(device, non_blocking=True) if device == "cuda" else x

    # ======================================================================== 4. model
    from peft import LoraConfig, get_peft_model, get_peft_model_state_dict, set_peft_model_state_dict
    from transformers import AutoModelForCausalLM

    # The base model never changes, so it is not saved in our checkpoints: it comes into the
    # job as input every time. We record which base model it was, so that a resume with a
    # different one is refused (adapters only make sense on the model they were trained on).
    base_model_id = describe_base_model(cfg.model_dir)
    base = AutoModelForCausalLM.from_pretrained(
        cfg.model_dir, torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32)
    if cfg.gradient_checkpointing:
        base.gradient_checkpointing_enable()
        base.enable_input_require_grads()
    model = get_peft_model(base, LoraConfig(
        r=cfg.lora_r, lora_alpha=cfg.lora_alpha, lora_dropout=cfg.lora_dropout,
        target_modules=cfg.lora_targets.split(","), task_type="CAUSAL_LM"))
    for p in model.parameters():          # train the adapters in full precision
        if p.requires_grad:
            p.data = p.data.float()
    model.to(device)
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=cfg.lr, weight_decay=cfg.weight_decay)
    n_train = sum(p.numel() for p in trainable)
    n_all = sum(p.numel() for p in model.parameters())
    print("MODEL %s: %.0fM parameters, %.1fM of them trained (LoRA, %.2f%%)"
          % (base_model_id, n_all / 1e6, n_train / 1e6, 100 * n_train / n_all), flush=True)

    # ======================================================================== 5. resume
    step, epoch, batch_index, tokens_seen, best_val = 0, 0, 0, 0, float("inf")
    local = CheckpointStore(cfg.ckpt_dir, keep=cfg.keep_checkpoints)   # this job's checkpoints
    previous = CheckpointStore(cfg.resume_dir, keep=1)                  # the previous job's (DAG)
    os.makedirs(cfg.out_dir, exist_ok=True)
    for name in local.cleanup_stale():
        print("removed an incomplete save: %s" % name, flush=True)

    metrics_path = os.path.join(cfg.ckpt_dir, "metrics.jsonl")
    old_metrics = os.path.join(cfg.resume_dir, "metrics.jsonl")
    if not os.path.exists(metrics_path) and os.path.exists(old_metrics):
        shutil.copy(old_metrics, metrics_path)   # a new job continues the previous job's log

    def log(**event):
        """Append one line to the training log. It lives in the checkpoint directory, so it
        travels with the checkpoint and becomes one record across all restarts."""
        event["time"] = round(time.time(), 1)
        with open(metrics_path, "a") as f:
            f.write(json.dumps(event) + "\n")

    path, state = load_newest([local, previous], torch_utils.load_state)
    if state is not None:
        if state["base_model"] != base_model_id:
            sys.exit("cannot resume %s: it was trained on base model %s, this job has %s"
                     % (path, state["base_model"], base_model_id))
        changes = meta.config_changes(state["config"], cfg_dict)
        incompatible = sorted(set(changes) & set(SHAPE_KEYS))
        if incompatible:
            sys.exit("cannot resume %s: adapter shape changed (%s). Use a new run directory."
                     % (path, ", ".join(incompatible)))
        for k, (old, new) in changes.items():
            print("WARNING: setting changed since the checkpoint: %s %r -> %r" % (k, old, new), flush=True)
        set_peft_model_state_dict(model, state["adapters"])
        optimizer.load_state_dict(state["optimizer"])
        step, epoch, batch_index = state["step"], state["epoch"], state["batch_index"]
        tokens_seen, best_val = state["tokens_seen"], state["best_val"]
        meta.restore_rng(state["rng"])
        torch_utils.restore_rng(state["rng"])
        with open(os.path.join(path, "metadata.json")) as f:
            reason = json.load(f)["reason"]
        print("RESUMED from step %d (epoch %d, batch %d; saved because: %s) from %s"
              % (step, epoch, batch_index, reason, path), flush=True)
        log(event="resumed", step=step, epoch=epoch, batch_index=batch_index, reason=reason, path=path)
    else:
        print("STARTING fresh: %d steps per epoch, %d epochs" % (steps_per_epoch, cfg.epochs), flush=True)
        log(event="started", steps_per_epoch=steps_per_epoch, trained_params=n_train)

    # ======================================================================== helpers
    def save(reason):
        """Save a checkpoint: only what changes while training. Not the base model."""
        state = {
            "adapters": get_peft_model_state_dict(model),   # the LoRA weights we train
            "optimizer": optimizer.state_dict(),            # AdamW's running averages
            "step": step, "epoch": epoch, "batch_index": batch_index,   # where we are
            "tokens_seen": tokens_seen, "best_val": best_val,
            "rng": {**meta.capture_rng(), **torch_utils.capture_rng()},
            "config": cfg_dict,
            "base_model": base_model_id,
        }
        info = local.save(step, lambda d: torch_utils.save_state(d, state),
                          meta.describe(cfg_dict, reason, epoch=epoch, batch_index=batch_index,
                                        base_model=base_model_id, torch=torch.__version__))
        print("SAVED step %d (reason: %s) in %.2f s, %.0f MB, %d files"
              % (step, reason, info["seconds"], info["bytes"] / 1e6, info["files"]), flush=True)
        print("RESOURCES: %s" % resources(), flush=True)
        log(event="checkpoint", step=step, reason=reason, seconds=info["seconds"],
            bytes=info["bytes"], files=info["files"], **resources())

    def export(name):
        """The trained adapters in Hugging Face's format: what you keep and use (load them on
        top of the base model with peft). Not a resumable checkpoint."""
        final, tmp = os.path.join(cfg.out_dir, name), os.path.join(cfg.out_dir, name + ".tmp")
        shutil.rmtree(tmp, ignore_errors=True)
        model.save_pretrained(tmp)
        shutil.rmtree(final, ignore_errors=True)
        os.rename(tmp, final)

    def evaluate():
        """Validation loss on the same examples every time, so values are comparable.
        Returns None if HTCondor asked us to stop meanwhile (don't spend the time here)."""
        model.eval()
        losses = []
        with torch.no_grad():
            for i in range(min(cfg.eval_batches, len(val) // cfg.batch_size)):
                if policy.evicting():
                    model.train()
                    return None
                x = batch(val, range(i * cfg.batch_size, (i + 1) * cfg.batch_size))
                with autocast:
                    losses.append(model(input_ids=x, labels=x).loss.item())
        model.train()
        return float(np.mean(losses)) if losses else None

    def stop_and_exit():
        """7. Stop: save, then exit with the code that tells HTCondor (or the DAG) what to do."""
        if policy.evicting():                       # HTCondor's SIGTERM: a vacate or a hold
            print(policy.describe(), flush=True)
            save(policy.reason)
            code = EXIT_RESTART
        elif handoff:                               # the job's total time is nearly up
            save("handoff")
            code = EXIT_HANDOFF
        else:                                       # our timer, or the glidein is ending
            save("timed")
            code = EXIT_RESTART
        log(event="exit", code=code, step=step, reason=policy.reason)
        print("EXIT %d (%s)" % (code, {EXIT_RESTART: "restart me", EXIT_HANDOFF: "continue in a new job"}[code]),
              flush=True)
        if code == EXIT_RESTART:
            policy.exit_for_restart()               # exits 85
        sys.exit(code)

    # ======================================================================== 6. train
    model.train()
    first_step_done = False
    t_log = time.time()
    while epoch < cfg.epochs and not (cfg.max_steps and step >= cfg.max_steps):
        order = np.random.default_rng(cfg.seed * 1000 + epoch).permutation(len(train))
        while batch_index < steps_per_epoch:              # starts mid-epoch after a resume
            if cfg.max_steps and step >= cfg.max_steps:
                break
            x = batch(train, order[batch_index * cfg.batch_size:(batch_index + 1) * cfg.batch_size])
            lr = lr_at(step, cfg, total_steps)
            for group in optimizer.param_groups:
                group["lr"] = lr
            with autocast:
                loss = model(input_ids=x, labels=x).loss   # the model shifts labels by one itself
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(trainable, cfg.grad_clip)
            optimizer.step()
            step, batch_index, tokens_seen = step + 1, batch_index + 1, tokens_seen + x.numel()

            if not first_step_done:   # start-up cost: part of what every restart costs
                first_step_done = True
                print("first step done %.1f s after the process started, %s"
                      % (time.time() - T_PROCESS_START, gpu_name()), flush=True)
                log(event="first_step", step=step, startup_seconds=round(time.time() - T_PROCESS_START, 1),
                    gpu=gpu_name())
            if step % cfg.log_every == 0:
                tps = cfg.log_every * x.numel() / max(time.time() - t_log, 1e-9)
                print("step %d epoch %d batch %d/%d loss %.4f lr %.2e %.0f tok/s"
                      % (step, epoch, batch_index, steps_per_epoch, loss.item(), lr, tps), flush=True)
                log(event="train", step=step, epoch=epoch, loss=loss.item(), lr=lr, tokens_per_s=round(tps))
                t_log = time.time()
            if cfg.eval_every_steps and step % cfg.eval_every_steps == 0:
                v = evaluate()
                if v is not None:
                    print("step %d val_loss %.4f" % (step, v), flush=True)
                    log(event="eval", step=step, val_loss=v)
                    if v < best_val:
                        best_val = v
                        export("best_adapter")
            if cfg.step_delay:
                time.sleep(cfg.step_delay)

            # --- the stop check, between steps, where everything is consistent ---
            if policy.should_stop():
                stop_and_exit()

        if batch_index >= steps_per_epoch:                # end of an epoch
            epoch, batch_index = epoch + 1, 0

    # ======================================================================== 7. finished
    v = evaluate()
    if v is not None and v < best_val:
        best_val = v
        export("best_adapter")
    export("final_adapter")
    save("final")
    log(event="exit", code=EXIT_DONE, step=step, val_loss=v)
    print("DONE: %d steps, final val_loss %s; adapters in %s/; exit 0"
          % (step, "%.4f" % v if v is not None else "n/a", cfg.out_dir), flush=True)
    return EXIT_DONE


# ============================================================================ small helpers
def describe_base_model(model_dir):
    """Which base model this is: from prepare_data.py's note, or the model's own config."""
    note = os.path.join(model_dir, "recipe4_model.json")
    if os.path.exists(note):
        with open(note) as f:
            info = json.load(f)
        return "%s@%s" % (info["repo"], info["revision"][:12])
    with open(os.path.join(model_dir, "config.json")) as f:
        return "unnamed-" + meta.config_hash(json.load(f))


def gpu_name():
    if not torch.cuda.is_available():
        return "on CPU"
    return "on %s, peak GPU memory %.1f GB" % (torch.cuda.get_device_name(0),
                                              torch.cuda.max_memory_allocated() / 1e9)


def resources():
    """What this job needs from a machine, for request_memory, request_cpus and
    gpus_minimum_memory in the submit file."""
    me, kids = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
    rss = me.ru_maxrss * (1 if sys.platform == "darwin" else 1024)   # bytes on macOS, KB on Linux
    cpu = me.ru_utime + me.ru_stime + kids.ru_utime + kids.ru_stime
    out = {"peak_memory_gb": round(rss / 1e9, 2),
           "cpus_used": round(cpu / max(time.time() - T_PROCESS_START, 1e-9), 2)}
    if torch.cuda.is_available():
        out["peak_gpu_memory_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 2)
    return out


if __name__ == "__main__":
    sys.exit(main())
