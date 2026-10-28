#!/usr/bin/env python3
"""
Recipe 1: train a small GPT on TinyStories, and survive anything HTCondor does to the job.

    python3 train.py --config config.yaml --resume auto [--set name=value ...]

The same command works for the first start and every restart: --resume auto picks up the
newest complete checkpoint (from checkpoints/, or from backups on /staging), if any.

Exit codes:  85 = progress saved, please restart me (submit file: checkpoint_exit_code = 85)
              0 = training finished

The checkpointing pieces come from ../../htcondor_ckpt (the submit file sends that
directory with the job):
  stop.StopPolicy       when to stop: HTCondor's SIGTERM, a stop file, or our own time limit
  store.CheckpointStore write-then-rename checkpoints, fallback to an older one, retention
  store.backup...       copies on /staging that outlive the job
  meta / torch_utils    what to record with a checkpoint, random-number state, model unwrapping
"""
import time

T_PROCESS_START = time.time()  # to measure how long a restart takes (imports, data, compile...)

import argparse
import contextlib
import json
import math
import os
import resource
import shutil
import sys
from dataclasses import asdict, dataclass, fields

import numpy as np
import torch
import yaml

try:  # in a job, htcondor_ckpt/ sits next to this file; in the repository it's two levels up
    import htcondor_ckpt  # noqa: F401
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from htcondor_ckpt import meta, torch_utils
from htcondor_ckpt.stop import StopPolicy
from htcondor_ckpt.store import CheckpointStore, backup, backup_due, load_newest

from model import GPT, GPTConfig


# ============================================================================ settings
@dataclass
class Config:
    data_dir: str = "."
    vocab_size: int = 50304
    block_size: int = 512
    n_layer: int = 8
    n_head: int = 8
    n_embd: int = 512
    dropout: float = 0.1
    epochs: int = 6
    batch_size: int = 64
    lr: float = 6e-4
    min_lr: float = 6e-5
    warmup_steps: int = 500
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    seed: int = 1337
    compile: bool = True
    deterministic: bool = False
    eval_every_steps: int = 1000
    eval_batches: int = 20
    sample_stories: bool = True
    log_every: int = 50
    checkpoint_at: str = "interval"
    ckpt_dir: str = "checkpoints"
    out_dir: str = "outputs"
    keep_checkpoints: int = 1
    max_runtime_seconds: float = 21600
    save_every_minutes: float = 0
    backup_dir: str = ""
    backup_every_hours: float = 12
    wandb: bool = False
    wandb_project: str = "tinystories-checkpointing"
    step_delay: float = 0.0
    max_steps: int = 0


# Changing these makes a saved model unusable: refuse to resume. Other changes only warn.
SHAPE_KEYS = ("vocab_size", "block_size", "n_layer", "n_head", "n_embd")


def load_config(path, overrides):
    """config.yaml, then any --set name=value (converted to the field's type)."""
    values = {}
    if path:
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


# ============================================================================ data
class TokenData:
    """train.bin / val.bin from prepare_data.py: one long array of GPT-2 token ids.

    Cut into non-overlapping sequences of block_size + 1 tokens (inputs, plus the same
    tokens shifted by one as targets). Each epoch visits every sequence once, in an
    order shuffled with a seed made from (seed, epoch). After a restart we can rebuild
    exactly that order, so the checkpoint only needs (epoch, batch_index) to know
    where it is in the data: nothing repeated, nothing skipped.
    (nanoGPT instead samples random windows; that makes "epoch" and "where was I?"
    meaningless, which is why this recipe doesn't.)"""

    def __init__(self, path, block_size):
        self.tokens = np.memmap(path, dtype=np.uint16, mode="r")
        self.T = block_size
        self.n_seq = (len(self.tokens) - 1) // block_size

    def order(self, seed, epoch):
        return np.random.default_rng(seed * 1000 + epoch).permutation(self.n_seq)

    def batch(self, seq_ids, device):
        rows = np.stack([self.tokens[i * self.T:i * self.T + self.T + 1] for i in seq_ids]).astype(np.int64)
        xy = torch.from_numpy(rows)
        if device == "cuda":
            xy = xy.pin_memory().to(device, non_blocking=True)
        return xy[:, :-1], xy[:, 1:]


def lr_at(step, cfg, total_steps):
    """Linear warmup, then cosine decay to min_lr. A pure function of the step, so the
    saved step is all the learning-rate schedule needs to resume."""
    if step < cfg.warmup_steps:
        return cfg.lr * (step + 1) / cfg.warmup_steps
    progress = min(1.0, (step - cfg.warmup_steps) / max(1, total_steps - cfg.warmup_steps))
    return cfg.min_lr + 0.5 * (cfg.lr - cfg.min_lr) * (1 + math.cos(math.pi * progress))


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--resume", default="auto", help="auto (newest checkpoint, if any), none, or a checkpoint path")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE", help="override a config setting")
    args = ap.parse_args()
    cfg = load_config(args.config, args.set)
    cfg_dict = asdict(cfg)
    # Create both directories before anything else can fail. In spool mode HTCondor transfers them
    # back at every exit; if a crash happened before they existed, the job would go on hold for a
    # missing file and hide the real error.
    os.makedirs(cfg.ckpt_dir, exist_ok=True)
    os.makedirs(cfg.out_dir, exist_ok=True)

    # When to stop: HTCondor's SIGTERM, a stop file (under launch.py), or our time limit.
    # The handler only records the request; we act on it between steps.
    policy = StopPolicy(max_runtime_seconds=cfg.max_runtime_seconds)
    print("vacate window: %.0f s (from %s)" % (policy.vacate_seconds, policy.vacate_source), flush=True)

    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)
    torch.use_deterministic_algorithms(cfg.deterministic, warn_only=True)
    if cfg.deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
    # bf16 autocast on GPUs. No GradScaler is needed with bf16; with fp16 (older GPUs)
    # you would also need a GradScaler, and its state would go into the checkpoint too.
    autocast = (torch.autocast("cuda", dtype=torch.bfloat16) if device == "cuda" else contextlib.nullcontext())

    train = TokenData(os.path.join(cfg.data_dir, "train.bin"), cfg.block_size)
    val = TokenData(os.path.join(cfg.data_dir, "val.bin"), cfg.block_size)
    steps_per_epoch = train.n_seq // cfg.batch_size   # the last partial batch is dropped
    total_steps = cfg.epochs * steps_per_epoch
    if cfg.max_steps:  # a short run (tests): the learning-rate schedule fits the shorter run
        total_steps = min(total_steps, cfg.max_steps)

    model = GPT(GPTConfig(**{k: cfg_dict[k] for k in ("vocab_size", "block_size", "n_layer",
                                                       "n_head", "n_embd", "dropout")})).to(device)
    decay = [p for p in model.parameters() if p.dim() >= 2]      # weight matrices: weight decay
    no_decay = [p for p in model.parameters() if p.dim() < 2]    # biases, LayerNorms: none
    optimizer = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                                   {"params": no_decay, "weight_decay": 0.0}],
                                  lr=cfg.lr, betas=(0.9, 0.95), fused=(device == "cuda"))

    # Where we are. Everything below goes into every checkpoint.
    step = epoch = batch_index = tokens_seen = 0
    best_val = float("inf")
    wandb_id = None

    # ------------------------------------------------------------------ checkpoints
    local = CheckpointStore(cfg.ckpt_dir, keep=cfg.keep_checkpoints)
    stores = [local]
    backups = None
    if cfg.backup_dir:
        backups = CheckpointStore(cfg.backup_dir, keep=2)
        stores.append(backups)
    for s in stores:
        for name in s.cleanup_stale():
            print("removed an incomplete save: %s" % name, flush=True)

    def log(**event):
        """Append one line to outputs/metrics.jsonl. The file travels with the job, so it
        becomes one continuous record across all restarts."""
        event["time"] = round(time.time(), 1)
        with open(os.path.join(cfg.out_dir, "metrics.jsonl"), "a") as f:
            f.write(json.dumps(event) + "\n")

    # ------------------------------------------------------------------ resume
    if args.resume == "auto":
        path, state = load_newest(stores, torch_utils.load_state)
    elif args.resume == "none":
        path, state = None, None
    else:
        path, state = args.resume, torch_utils.load_state(args.resume)
    if state is not None:
        changes = meta.config_changes(state["config"], cfg_dict)
        incompatible = sorted(set(changes) & set(SHAPE_KEYS))
        if incompatible:
            sys.exit("cannot resume %s: model shape changed (%s). Use a new ckpt_dir or --resume none."
                     % (path, ", ".join(incompatible)))
        for k, (old, new) in changes.items():
            print("WARNING: setting changed since the checkpoint: %s %r -> %r" % (k, old, new), flush=True)
        model.load_state_dict(state["model"])        # load into the plain model, before torch.compile
        optimizer.load_state_dict(state["optimizer"])
        step, epoch, batch_index = state["step"], state["epoch"], state["batch_index"]
        tokens_seen, best_val, wandb_id = state["tokens_seen"], state["best_val"], state["wandb_id"]
        meta.restore_rng(state["rng"])
        torch_utils.restore_rng(state["rng"])
        with open(os.path.join(path, "metadata.json")) as f:
            reason = json.load(f)["reason"]                # why that checkpoint was saved
        print("RESUMED from step %d (epoch %d, batch %d; saved because: %s) from %s"
              % (step, epoch, batch_index, reason, path), flush=True)
        log(event="resumed", step=step, epoch=epoch, batch_index=batch_index, reason=reason, path=path)
    else:
        print("STARTING fresh: %.1fM parameters, %d steps per epoch, %d epochs"
              % (model.num_params() / 1e6, steps_per_epoch, cfg.epochs), flush=True)
        log(event="started", params=model.num_params(), steps_per_epoch=steps_per_epoch)

    if cfg.wandb:
        import wandb
        wandb_id = wandb_id or wandb.util.generate_id()       # saved in the checkpoint: same W&B run after restarts
        wandb.init(project=cfg.wandb_project, id=wandb_id, resume="allow", config=cfg_dict)

    # torch.compile wraps the model; its state-dict keys gain a "_orig_mod." prefix. We keep
    # `model` (the plain module) for saving and loading, and train with `compiled`.
    use_compile = cfg.compile
    if use_compile and device == "cuda" and not (os.environ.get("CC") or shutil.which("gcc")
                                                  or shutil.which("cc") or shutil.which("clang")):
        # On GPUs, torch.compile (through Triton) builds small C helpers at run time and fails
        # on the first step without a C compiler (many "runtime" container images have none).
        print("WARNING: compile=true but this container has no C compiler (gcc/cc/clang), which "
              "torch.compile needs on GPUs. Training WITHOUT torch.compile (slower). Install gcc "
              "in the container (see container.def) or set compile=false.", flush=True)
        use_compile = False
    compiled = torch.compile(model) if use_compile else model

    # CPU threads. Some access points hold a job that uses more CPUs than it requested (an OSPool
    # one does after an hour above 1.8 x request_cpus; see docs/environment.md §10). HTCondor sets
    # OMP_NUM_THREADS to request_cpus, which PyTorch's main thread pool follows; os.cpu_count()
    # is the whole machine's. cpus_used() below measures what the job really uses.
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    print("CPU threads: torch %d, interop %d, OMP_NUM_THREADS=%s, machine has %s cores (%s usable)"
          % (torch.get_num_threads(), torch.get_num_interop_threads(), os.environ.get("OMP_NUM_THREADS"),
             os.cpu_count(), affinity), flush=True)

    def save(reason):
        """Save a resumable checkpoint. Returns the CheckpointStore save info."""
        state = {
            "model": torch_utils.unwrap(model).state_dict(),  # weights, without wrapper prefixes
            "optimizer": optimizer.state_dict(),               # AdamW's running averages
            "step": step, "epoch": epoch, "batch_index": batch_index,  # where we are; the LR comes from step
            "tokens_seen": tokens_seen, "best_val": best_val,
            "wandb_id": wandb_id,
            "rng": {**meta.capture_rng(), **torch_utils.capture_rng()},
            "config": cfg_dict,
        }
        info = local.save(step, lambda d: torch_utils.save_state(d, state),
                          meta.describe(cfg_dict, reason, epoch=epoch, batch_index=batch_index,
                                        torch=torch.__version__))
        print("SAVED step %d (reason: %s) in %.2f s, %.0f MB, %d files"
              % (step, reason, info["seconds"], info["bytes"] / 1e6, info["files"]), flush=True)
        # CPUs used: over the whole process (start-up and compiling included), and since the first
        # step (steady training, which is what a CPU-usage policy sees over hours).
        cpus = {"cpus_used": cpus_used((0.0, T_PROCESS_START)),
                "cpus_used_training": cpus_used(training_start) if training_start else None}
        print("CPUs used: %.2f on average since the process started, %s while training"
              % (cpus["cpus_used"], cpus["cpus_used_training"]), flush=True)
        log(event="checkpoint", step=step, reason=reason, seconds=info["seconds"], bytes=info["bytes"],
            files=info["files"], peak_gpu_gb=peak_gpu_gb(), **cpus)
        # Backups only at timed checkpoints: never in the SIGTERM path, where time is short.
        if backups and reason == "timed" and backup_due(backups, cfg.backup_every_hours * 3600):
            b = backup(info["path"], backups)
            print("BACKUP of step %d to %s in %.2f s" % (step, b["path"], b["seconds"]), flush=True)
            log(event="backup", step=step, seconds=b["seconds"], path=b["path"])
        return info

    def cpu_seconds():
        """CPU time of this process and its finished children (torch.compile's workers)."""
        me, kids = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
        return me.ru_utime + me.ru_stime + kids.ru_utime + kids.ru_stime

    def cpus_used(since):
        """Average number of CPUs busy since `since` = (cpu seconds, wall time)."""
        cpu0, t0 = since
        return round((cpu_seconds() - cpu0) / max(time.time() - t0, 1e-9), 2)

    def peak_gpu_gb():
        """Most GPU memory this process has used so far: what a GPU needs to run this config."""
        return round(torch.cuda.max_memory_allocated() / 1e9, 2) if device == "cuda" else 0.0

    def evaluate():
        """Validation loss on the same sequences every time, so values are comparable.
        Returns None if a stop was requested meanwhile (don't spend the vacate window here)."""
        compiled.eval()
        losses = []
        with torch.no_grad():
            for i in range(cfg.eval_batches):
                if policy.evicting():
                    compiled.train()
                    return None
                ids = range(i * cfg.batch_size, min((i + 1) * cfg.batch_size, val.n_seq))
                x, y = val.batch(ids, device)
                with autocast:
                    losses.append(compiled(x, y)[1].item())
        compiled.train()
        return float(np.mean(losses))

    def sample_stories():
        """A few stories from fixed prompts, appended to outputs/samples.txt. Uses its own
        random generator, so it never changes the training run."""
        try:
            import tiktoken
        except ImportError:
            return
        enc = tiktoken.get_encoding("gpt2")
        gen = torch.Generator().manual_seed(epoch)
        model.eval()
        with open(os.path.join(cfg.out_dir, "samples.txt"), "a") as f:
            f.write("=== after epoch %d (step %d) ===\n" % (epoch, step))
            for prompt in ("Once upon a time", "One day, a little girl named Lily", "The dog wanted to"):
                idx = torch.tensor([enc.encode_ordinary(prompt)], device=device)
                with autocast:
                    out = model.generate(idx, 120, generator=gen)
                f.write(enc.decode(out[0].tolist()).split("<|endoftext|>")[0].strip() + "\n\n")
        model.train()

    def export_best():
        """The best model so far, as plain weights: what you'd keep and use. Not a
        resumable checkpoint (no optimizer, no position)."""
        tmp = os.path.join(cfg.out_dir, "best_model.pt.tmp")
        torch.save({"model": torch_utils.unwrap(model).state_dict(),
                    "model_config": asdict(model.cfg), "val_loss": best_val, "step": step}, tmp)
        os.replace(tmp, os.path.join(cfg.out_dir, "best_model.pt"))

    def exit_for_restart():
        log(event="exit", code=85, step=step, reason=policy.reason)
        policy.exit_for_restart()

    # ------------------------------------------------------------------ training
    compiled.train()
    first_step_logged = False
    training_start = None   # (cpu seconds, time) at the first step, for cpus_used()
    last_save = time.time()
    t_log, tokens_at_log = time.time(), tokens_seen
    while epoch < cfg.epochs and not (cfg.max_steps and step >= cfg.max_steps):
        order = train.order(cfg.seed, epoch)
        while batch_index < steps_per_epoch:              # starts mid-epoch after a resume
            if cfg.max_steps and step >= cfg.max_steps:
                break                                     # a short run is done
            x, y = train.batch(order[batch_index * cfg.batch_size:(batch_index + 1) * cfg.batch_size], device)
            lr = lr_at(step, cfg, total_steps)
            for group in optimizer.param_groups:
                group["lr"] = lr
            with autocast:
                _, loss = compiled(x, y)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            optimizer.step()
            step, batch_index, tokens_seen = step + 1, batch_index + 1, tokens_seen + x.numel()

            if not first_step_logged:  # start-up cost of this process: part of every restart's cost
                first_step_logged = True
                if device == "cuda":
                    torch.cuda.synchronize()
                startup = time.time() - T_PROCESS_START
                gpu = ("on %s, peak GPU memory %.1f GB" % (torch.cuda.get_device_name(0), peak_gpu_gb())
                       if device == "cuda" else "on CPU")
                print("first step done %.1f s after the process started, %s" % (startup, gpu), flush=True)
                log(event="first_step", step=step, startup_seconds=round(startup, 1), gpu=gpu)
                training_start = (cpu_seconds(), time.time())
            if step % cfg.log_every == 0:
                dt = time.time() - t_log
                tps = (tokens_seen - tokens_at_log) / max(dt, 1e-9)
                print("step %d epoch %d batch %d/%d loss %.4f lr %.2e %.0f tok/s"
                      % (step, epoch, batch_index, steps_per_epoch, loss.item(), lr, tps), flush=True)
                log(event="train", step=step, epoch=epoch, loss=loss.item(), lr=lr, tokens_per_s=round(tps))
                if cfg.wandb:
                    wandb.log({"loss": loss.item(), "lr": lr, "tokens_per_s": tps}, step=step)
                t_log, tokens_at_log = time.time(), tokens_seen
            if cfg.eval_every_steps and step % cfg.eval_every_steps == 0:
                v = evaluate()
                if v is not None:
                    print("step %d val_loss %.4f" % (step, v), flush=True)
                    log(event="eval", step=step, val_loss=v)
            if cfg.step_delay:
                time.sleep(cfg.step_delay)

            # --- the stop check, between steps: all state agrees here ---
            if policy.should_stop():
                if policy.evicting():
                    print(policy.describe(), flush=True)
                    if cfg.checkpoint_at == "epoch":
                        # Epoch mode keeps no mid-epoch position: the restart redoes this epoch.
                        print("epoch mode: not saving mid-epoch; epoch %d will be redone" % epoch, flush=True)
                    else:
                        save(policy.reason)
                        left = policy.seconds_left()
                        print("save finished with %.0f s left before SIGKILL" % left, flush=True)
                    exit_for_restart()
                if cfg.checkpoint_at == "interval":   # timed: save now, mid-epoch if need be
                    save("timed")
                    exit_for_restart()
                # epoch mode, timed stop: keep going to the end of this epoch (below). A SIGTERM
                # meanwhile replaces the timed stop and is handled above.
            elif (cfg.checkpoint_at == "interval" and cfg.save_every_minutes
                  and time.time() - last_save >= cfg.save_every_minutes * 60):
                save("periodic")                      # in-place save, no exit
                last_save = time.time()

        if batch_index < steps_per_epoch:
            break                                         # max_steps reached mid-epoch: no end-of-epoch work
        # ---------------- end of an epoch ----------------
        epoch, batch_index = epoch + 1, 0
        v = evaluate()
        if v is not None:
            print("epoch %d done: val_loss %.4f" % (epoch - 1, v), flush=True)
            log(event="eval", step=step, epoch=epoch - 1, val_loss=v)
            if v < best_val:
                best_val = v
                export_best()
                print("new best model (val_loss %.4f) -> %s/best_model.pt" % (v, cfg.out_dir), flush=True)
        if cfg.sample_stories and not policy.evicting():
            sample_stories()
        # At an epoch boundary any pending stop (timed, or a SIGTERM that arrived during the
        # evaluation) can be saved in either mode: the position is simply "start of next epoch".
        if policy.should_stop():
            save(policy.reason)
            exit_for_restart()
        if cfg.checkpoint_at == "epoch":
            save("epoch")
        last_save = time.time()

    # ------------------------------------------------------------------ done
    save("final")
    log(event="exit", code=0, step=step)
    best = "%.4f" % best_val if best_val < float("inf") else "none yet (no epoch finished)"
    print("DONE: %d steps, %d epochs, best val_loss %s; exit 0" % (step, epoch, best), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
