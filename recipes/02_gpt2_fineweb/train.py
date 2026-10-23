#!/usr/bin/env python3
"""
Recipe 2: train GPT-2 small (124M) on FineWeb-Edu with DDP on one multi-GPU node, and
survive anything HTCondor does to the job.

Under HTCondor, through the stop-file wrapper (see job.sub):
    python3 htcondor_ckpt/launch.py -- torchrun --standalone --nproc_per_node=4 train.py --resume auto
On one GPU or CPU, no launcher needed:
    python3 train.py --config config.yaml --resume auto [--set name=value ...]

Exit codes:  85 = progress saved, please restart me (submit file: checkpoint_exit_code = 85)
              0 = training finished
Under torchrun, a worker's 85 becomes torchrun's 1; launch.py turns it back into 85.

What's new compared with recipe 1 (whose train.py this follows):
  - every rank must stop at the same step: all stop decisions go through agree_max()
  - only rank 0 writes checkpoints and logs; every rank loads the checkpoint
  - the data is ~100 shards read from /staging, and the position is (pass, shard, sequence)
  - gradient accumulation: a stop request is also checked between micro-batches
"""
import time

T_PROCESS_START = time.time()  # to measure how long a restart takes (imports, data, compile...)

import argparse
import contextlib
import datetime
import json
import math
import os
import shutil
import sys
from dataclasses import asdict, dataclass, fields

import numpy as np
import torch
import torch.distributed as dist
import yaml
from torch.nn.parallel import DistributedDataParallel as DDP

try:  # in a job, htcondor_ckpt/ sits next to this file; in the repository it's two levels up
    import htcondor_ckpt  # noqa: F401
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from htcondor_ckpt import meta, torch_utils
from htcondor_ckpt.stop import StopPolicy
from htcondor_ckpt.store import CheckpointStore, load_newest

from model import GPT, GPTConfig


# ============================================================================ settings
@dataclass
class Config:
    data_dir: str = "."
    vocab_size: int = 50304
    block_size: int = 1024
    n_layer: int = 12
    n_head: int = 12
    n_embd: int = 768
    dropout: float = 0.0
    num_passes: int = 1
    total_batch_tokens: int = 524288     # tokens per optimizer step, whatever the GPU count (2**19)
    micro_batch: int = 32                # sequences per GPU per forward/backward
    lr: float = 6e-4
    min_lr: float = 6e-5
    warmup_steps: int = 700
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    seed: int = 1337
    compile: bool = True
    deterministic: bool = False
    eval_every_steps: int = 250
    eval_sequences: int = 512            # validation loss is measured on the same sequences every time
    log_every: int = 10
    ckpt_dir: str = "checkpoints"
    out_dir: str = "outputs"
    keep_checkpoints: int = 2
    max_runtime_seconds: float = 3600
    save_every_minutes: float = 30
    wandb: bool = False
    wandb_project: str = "gpt2-fineweb-checkpointing"
    collective_timeout_seconds: float = 300
    step_delay: float = 0.0
    save_delay: float = 0.0              # tests only: make every save take this much longer
    max_steps: int = 0


# Changing these makes a saved model unusable: refuse to resume. Other changes only warn.
SHAPE_KEYS = ("vocab_size", "block_size", "n_layer", "n_head", "n_embd")

# What the ranks agree on at each step boundary, by urgency (see agree_max). Every rank
# does the most urgent action any rank asked for, so all ranks save and log the same thing.
GO_ON, PERIODIC, TIMED, STOP_FILE, SIGNAL = 0, 1, 2, 3, 4
REASONS = {PERIODIC: "periodic", TIMED: "timed", STOP_FILE: "stop_file", SIGNAL: "signal"}


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
class ShardData:
    """The token shards made by prepare_data.py, listed in its manifest.json.

    Each shard is cut into non-overlapping sequences of block_size + 1 tokens. A training
    step consumes `step_seqs` consecutive sequences of the current shard (all GPUs
    together), so the position in the data is just three numbers, the same on every rank:

        (pass_index, shard_pos, seq)   which pass over the data, which shard in this pass's
                                       order, and the next unread sequence in that shard

    Each pass visits the shards in an order shuffled with (seed, pass_index); after a
    restart we rebuild exactly that order. A shard's last few sequences that don't fill a
    whole step are skipped (at most one step's worth per shard, under 1% of the data), and
    so is a shard too small for even one step (an input file's last, short shard may be).

    The position counts sequences for *all* GPUs, so it doesn't depend on the GPU count.
    Resuming on a different number of GPUs continues at the same place in the data; only
    which GPU gets which sequences within a step changes."""

    def __init__(self, data_dir, block_size, step_seqs, seed):
        with open(os.path.join(data_dir, "manifest.json")) as f:
            manifest = json.load(f)
        if not manifest.get("complete"):
            print("WARNING: %s/manifest.json says the data is incomplete (prepare_data.py hasn't "
                  "finished, or ran with --max-files)" % data_dir, flush=True)
        self.dir, self.T, self.step_seqs, self.seed = data_dir, block_size, step_seqs, seed
        # Shards in a fixed order: by input file, then by number within the file.
        self.shards = [(name, n) for key in sorted(manifest["files"]) for name, n in manifest["files"][key]["shards"]]
        self.val_name, self.val_tokens = manifest["val"][0]
        self.steps_per_shard = [((n - 1) // block_size) // step_seqs for _, n in self.shards]
        self.steps_per_pass = sum(self.steps_per_shard)
        if not self.steps_per_pass:
            sys.exit("no shard in %s holds a whole step (%d sequences)" % (data_dir, step_seqs))
        self._open = (None, None)
        self._order = (None, None)

    def tokens(self, name):
        """A shard, memory-mapped: only the parts we read are loaded from /staging."""
        if self._open[0] != name:
            self._open = (name, np.load(os.path.join(self.dir, name), mmap_mode="r"))
        return self._open[1]

    def order(self, pass_index):
        """The shard order of one pass, rebuilt from (seed, pass_index) whenever needed."""
        if self._order[0] != pass_index:
            rng = np.random.default_rng(self.seed * 1000 + pass_index)
            self._order = (pass_index, rng.permutation(len(self.shards)))
        return self._order[1]

    def shard(self, pos):
        """The name of the shard the position points into."""
        return self.shards[self.order(pos[0])[pos[1]]][0]

    def sequences(self, name, first, count, device):
        """Sequences first .. first+count-1 of a shard, as (inputs, targets). They're
        consecutive in the shard, so this is one contiguous read."""
        chunk = torch.from_numpy(self.tokens(name)[first * self.T:(first + count) * self.T + 1].astype(np.int64))
        x, y = chunk[:-1].view(count, self.T), chunk[1:].view(count, self.T)
        if device.type == "cuda":
            x, y = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device, non_blocking=True)
        return x, y

    def advance(self, pos):
        """The position after one more step."""
        return self.settle((pos[0], pos[1], pos[2] + self.step_seqs))

    def settle(self, pos):
        """Move on until a whole step fits: the next shard if this one has too few sequences
        left, the next pass after the last shard."""
        pass_index, shard_pos, seq = pos
        while seq + self.step_seqs > self.steps_per_shard[self.order(pass_index)[shard_pos]] * self.step_seqs:
            shard_pos, seq = shard_pos + 1, 0
            if shard_pos == len(self.shards):
                pass_index, shard_pos = pass_index + 1, 0
        return (pass_index, shard_pos, seq)


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
    # Create both directories before anything else can fail, so an early crash shows its real
    # error (in spool mode, a missing directory would turn into a hold for a missing file).
    os.makedirs(cfg.ckpt_dir, exist_ok=True)
    os.makedirs(cfg.out_dir, exist_ok=True)

    # ------------------------------------------------------------------ the ranks
    # torchrun sets RANK, LOCAL_RANK and WORLD_SIZE. Without it this is a 1-process run.
    distributed = "RANK" in os.environ
    rank = int(os.environ.get("RANK", 0))
    local_rank = int(os.environ.get("LOCAL_RANK", 0))
    world = int(os.environ.get("WORLD_SIZE", 1))
    if torch.cuda.is_available():
        device = torch.device("cuda", local_rank)
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")
    if distributed:
        # timeout: how long a rank waits in a collective (all-reduce, barrier) for the others
        # before the job aborts. NCCL's default is 10 minutes, all of it GPU time wasted if the
        # GPUs can't reach each other; nothing here legitimately takes more than a few seconds.
        # device_id: tells NCCL which GPU this rank uses (without it, NCCL warns and guesses).
        timeout = datetime.timedelta(seconds=cfg.collective_timeout_seconds)
        if device.type == "cuda":
            dist.init_process_group("nccl", timeout=timeout, device_id=device)
        else:
            dist.init_process_group("gloo", timeout=timeout)
    master = rank == 0

    def say(msg, all_ranks=False):
        """Print from rank 0 only, or from every rank with a [rank N] prefix. One write per
        line: print() writes the text and the newline separately, so two ranks printing at
        the same moment could run their lines together."""
        if all_ranks and world > 1:
            sys.stdout.write("[rank %d] %s\n" % (rank, msg))
            sys.stdout.flush()
        elif master:
            sys.stdout.write(msg + "\n")
            sys.stdout.flush()

    # When to stop: launch.py's stop file (it gets HTCondor's SIGTERM for us), a SIGTERM sent
    # straight to this process (a 1-GPU run without a launcher), or our time limit.
    policy = StopPolicy(max_runtime_seconds=cfg.max_runtime_seconds)
    say("vacate window: %.0f s (from %s); %d rank(s); stop file: %s"
        % (policy.vacate_seconds, policy.vacate_source, world, policy.stop_file or "none (no launch.py)"))
    if distributed:
        # Check that the GPUs can talk to each other before doing anything else. If this is
        # where the log stops (and the job aborts after collective_timeout_seconds), the GPUs
        # couldn't reach each other: on machines without NVLink, try NCCL_P2P_LEVEL=NVL (job.sub).
        say("checking that the %d ranks can communicate (one all-reduce)..." % world)
        t0 = time.time()
        check = torch.ones(1, device=device)
        dist.all_reduce(check)                    # every rank adds 1: the sum must be the rank count
        total, took = check.item(), time.time() - t0
        # A hung all-reduce can still "return" once NCCL's watchdog gives up, with no valid result:
        # check the value and the time, not just that the call came back.
        if total != world or took >= cfg.collective_timeout_seconds:
            sys.exit("the %d ranks could NOT communicate (all-reduce gave %s after %.0f s). On a machine "
                     "without NVLink, try NCCL_P2P_LEVEL=NVL (see job.sub)." % (world, total, took))
        say("communication OK (%s backend, %.1f s)" % (dist.get_backend(), took))

    torch.manual_seed(cfg.seed + rank)   # each rank its own random stream (there's no dropout by default)
    np.random.seed(cfg.seed + rank)
    torch.use_deterministic_algorithms(cfg.deterministic, warn_only=True)
    if cfg.deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
    # bf16 autocast on GPUs: no GradScaler needed. With fp16 (older GPUs) you would also need a
    # GradScaler, and its state would go into the checkpoint too.
    autocast = (torch.autocast("cuda", dtype=torch.bfloat16) if device.type == "cuda" else contextlib.nullcontext())

    # ------------------------------------------------------------------ batch sizes
    # The optimizer step is always total_batch_tokens (about 0.5M tokens), whatever the GPU
    # count: each GPU runs `accum` micro-batches of micro_batch sequences, then the gradients
    # are averaged across GPUs. 4 GPUs need 4x fewer micro-batches than 1.
    T = cfg.block_size
    step_seqs = cfg.total_batch_tokens // T
    per_micro = cfg.micro_batch * world
    if cfg.total_batch_tokens % T or step_seqs % per_micro:
        sys.exit("total_batch_tokens (%d) must be a multiple of block_size x micro_batch x GPUs (%d x %d x %d)"
                 % (cfg.total_batch_tokens, T, cfg.micro_batch, world))
    accum = step_seqs // per_micro

    data = ShardData(cfg.data_dir, T, step_seqs, cfg.seed)
    total_steps = cfg.num_passes * data.steps_per_pass
    if cfg.max_steps:  # a short run (tests, smoke runs): the learning-rate schedule fits the shorter run
        total_steps = min(total_steps, cfg.max_steps)

    model = GPT(GPTConfig(**{k: cfg_dict[k] for k in ("vocab_size", "block_size", "n_layer",
                                                       "n_head", "n_embd", "dropout")})).to(device)
    decay = [p for p in model.parameters() if p.dim() >= 2]      # weight matrices: weight decay
    no_decay = [p for p in model.parameters() if p.dim() < 2]    # biases, LayerNorms: none
    optimizer = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                                   {"params": no_decay, "weight_decay": 0.0}],
                                  lr=cfg.lr, betas=(0.9, 0.95), fused=(device.type == "cuda"))

    # Where we are. Everything below goes into every checkpoint.
    step = tokens_seen = 0
    pos = data.settle((0, 0, 0))   # (pass_index, shard_pos, seq): see ShardData
    best_val = float("inf")
    wandb_id = None

    # ------------------------------------------------------------------ checkpoints
    store = CheckpointStore(cfg.ckpt_dir, keep=cfg.keep_checkpoints)
    if master:
        for name in store.cleanup_stale():
            print("removed an incomplete save: %s" % name, flush=True)
    if distributed:
        dist.barrier()   # nobody looks for checkpoints while rank 0 is still cleaning up

    def log(**event):
        """Append one line to out_dir/metrics.jsonl (rank 0 only): one continuous record
        across all restarts, with a 'resumed' line at each one."""
        if master:
            event["time"] = round(time.time(), 1)
            with open(os.path.join(cfg.out_dir, "metrics.jsonl"), "a") as f:
                f.write(json.dumps(event) + "\n")

    # ------------------------------------------------------------------ resume
    # Every rank loads the same checkpoint (into CPU memory, then into its own GPU's model),
    # so every rank starts from identical weights and optimizer state.
    if args.resume == "auto":
        path, state = load_newest([store], torch_utils.load_state)
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
            say("WARNING: setting changed since the checkpoint: %s %r -> %r" % (k, old, new))
        model.load_state_dict(state["model"])        # into the plain model, before compile and DDP
        optimizer.load_state_dict(state["optimizer"])
        step, tokens_seen, pos = state["step"], state["tokens_seen"], tuple(state["pos"])
        best_val, wandb_id = state["best_val"], state["wandb_id"]
        # Each rank's own random-number state. With a different GPU count there's no match
        # for every rank: then each rank keeps its fresh seed, and we say so.
        if state["world_size"] == world:
            meta.restore_rng(state["rng"][rank])
            torch_utils.restore_rng(state["rng"][rank])
        else:
            say("WARNING: the checkpoint was written by %d GPUs, this run has %d. Training continues "
                "at the same place in the data, but each GPU gets different sequences within a step, "
                "and the random-number states start fresh." % (state["world_size"], world))
        with open(os.path.join(path, "metadata.json")) as f:
            reason = json.load(f)["reason"]
        say("RESUMED from step %d (pass %d, shard %d of %d, sequence %d; saved because: %s) from %s"
            % (step, pos[0], pos[1], len(data.shards), pos[2], reason, path))
        log(event="resumed", step=step, pos=pos, reason=reason, path=path, world_size=world)
        del state
    else:
        say("STARTING fresh: %.1fM parameters, %d GPUs x %d micro-batches x %d sequences x %d tokens "
            "= %d tokens per step; %d steps per pass over %d shards, %d steps in all"
            % (model.num_params() / 1e6, world, accum, cfg.micro_batch, T, cfg.total_batch_tokens,
               data.steps_per_pass, len(data.shards), total_steps))
        log(event="started", params=model.num_params(), world_size=world, accum=accum,
            steps_per_pass=data.steps_per_pass, total_steps=total_steps)

    if cfg.wandb and master:
        import wandb
        wandb_id = wandb_id or wandb.util.generate_id()       # saved in the checkpoint: same W&B run after restarts
        wandb.init(project=cfg.wandb_project, id=wandb_id, resume="allow", config=cfg_dict)

    # Wrapping: torch.compile, then DDP. Both wrappers change the state-dict keys ("_orig_mod.",
    # "module."), so we keep `model` (the plain module) for saving and loading, and train
    # with `ddp`. torch_utils.unwrap() finds the plain module inside any wrapper.
    use_compile = cfg.compile
    if use_compile and device.type == "cuda" and not (os.environ.get("CC") or shutil.which("gcc")
                                                       or shutil.which("cc") or shutil.which("clang")):
        say("WARNING: compile=true but this container has no C compiler (gcc/cc/clang), which "
            "torch.compile needs on GPUs. Training WITHOUT torch.compile (slower).")
        use_compile = False
    compiled = torch.compile(model) if use_compile else model
    ddp = DDP(compiled, device_ids=[local_rank] if device.type == "cuda" else None) if distributed else compiled

    def peak_gpu_gb():
        return round(torch.cuda.max_memory_allocated() / 1e9, 2) if device.type == "cuda" else 0.0

    def save(reason):
        """Save a resumable checkpoint. Every rank calls this; rank 0 writes.

        The random-number states are per rank, so first every rank sends its own to rank 0
        (all_gather_object): one file then holds them all, and the save is still rank 0's
        alone. The barrier at the end keeps the other ranks from exiting while rank 0 is
        still writing: torchrun stops the remaining workers once one of them exits."""
        rng = {**meta.capture_rng(), **torch_utils.capture_rng(all_devices=False)}
        rngs = [None] * world
        if distributed:
            dist.all_gather_object(rngs, rng)
        else:
            rngs = [rng]
        info = None
        if master:
            if cfg.save_delay:      # tests: a slow save, like a large checkpoint on a busy disk
                time.sleep(cfg.save_delay)
            state = {
                "model": torch_utils.unwrap(model).state_dict(),  # weights, without wrapper prefixes
                "optimizer": optimizer.state_dict(),               # AdamW's running averages
                "step": step, "tokens_seen": tokens_seen,          # the LR comes from the step
                "pos": list(pos),                                  # where we are in the data
                "best_val": best_val, "wandb_id": wandb_id,
                "rng": rngs, "world_size": world,
                "config": cfg_dict,
            }
            info = store.save(step, lambda d: torch_utils.save_state(d, state),
                              meta.describe(cfg_dict, reason, pos=list(pos), world_size=world,
                                            torch=torch.__version__))
            print("SAVED step %d (reason: %s) in %.2f s, %.0f MB, %d files"
                  % (step, reason, info["seconds"], info["bytes"] / 1e6, info["files"]), flush=True)
            log(event="checkpoint", step=step, reason=reason, seconds=info["seconds"], bytes=info["bytes"],
                files=info["files"], peak_gpu_gb=peak_gpu_gb())
        if distributed:
            dist.barrier()
        return info

    def evaluate():
        """Validation loss on the same eval_sequences sequences every time, whatever the GPU
        count: the sequences are dealt out to the GPUs in micro-batches, and the losses
        summed across GPUs. Skips the rest if an eviction arrives meanwhile (the vacate window
        is for saving), and then returns None on every rank."""
        compiled.eval()
        total, count, aborted = 0.0, 0, 0
        batches = range(0, cfg.eval_sequences, cfg.micro_batch)
        with torch.no_grad():
            for b in list(batches)[rank::world]:
                if policy.should_stop() and policy.evicting():
                    aborted = 1
                    break
                n = min(cfg.micro_batch, cfg.eval_sequences - b)
                x, y = data.sequences(data.val_name, b, n, device)
                with autocast:
                    loss = compiled(x, y)[1]
                total += loss.item() * n
                count += n
        compiled.train()
        t = torch.tensor([total, count, aborted], dtype=torch.float64, device=device)
        if distributed:
            dist.all_reduce(t)                               # sum over ranks
        return None if t[2] > 0 else (t[0] / t[1]).item()

    def export_best():
        """The best model so far, as plain weights: what you'd keep and use. Not a resumable
        checkpoint (no optimizer, no position)."""
        if master:
            tmp = os.path.join(cfg.out_dir, "best_model.pt.tmp")
            torch.save({"model": torch_utils.unwrap(model).state_dict(),
                        "model_config": asdict(model.cfg), "val_loss": best_val, "step": step}, tmp)
            os.replace(tmp, os.path.join(cfg.out_dir, "best_model.pt"))

    def stop_level():
        """This rank's view: is a stop or a save due? (Each rank sees its own clock, signal
        and stop file; agree_max() turns the views into one decision.)"""
        if policy.should_stop():
            return {"signal": SIGNAL, "stop_file": STOP_FILE, "timed": TIMED}[policy.reason]
        if cfg.save_every_minutes and time.time() - last_save >= cfg.save_every_minutes * 60:
            return PERIODIC
        return GO_ON

    def exit_for_restart(reason):
        """Every rank: exit 85. Under launch.py each also leaves a note in the restart file,
        and the wrapper exits 85 although torchrun itself exits 1."""
        log(event="exit", code=85, step=step, reason=reason)
        if distributed:
            dist.destroy_process_group()
        policy.exit_for_restart()

    def handle_eviction(level, micro=None):
        """Save the state after the last completed step, then exit 85."""
        say("%s; stopping at step %d" % (policy.describe() if policy.evicting() else
                                         "stop: requested by another rank (%s)" % REASONS[level], step),
            all_ranks=True)
        if micro is not None:
            say("(the stop came between micro-batches %d and %d of %d: that partial step is discarded)"
                % (micro, micro + 1, accum))
        save(REASONS[level])
        left = policy.seconds_left()
        if left is not None:
            say("save finished with %.0f s left before SIGKILL" % left)
        exit_for_restart(REASONS[level])

    # ------------------------------------------------------------------ training
    ddp.train()
    first_step_logged = False
    last_save = time.time()
    t_log, step_at_log = time.time(), step
    data_seconds = 0.0       # time spent reading shards (from /staging), shown as a share of each log interval
    while step < total_steps:
        name = data.shard(pos)
        lr = lr_at(step, cfg, total_steps)
        for group in optimizer.param_groups:
            group["lr"] = lr

        # --- one optimizer step: `accum` micro-batches on each GPU ---
        loss_sum = 0.0
        for m in range(accum):
            # An eviction is also checked between micro-batches, so a stop never waits for a
            # whole accumulation cycle. The partial accumulation is thrown away: the checkpoint
            # is the state after the last completed step, and the position still points at
            # this step's data. (Before the first micro-batch, the check at the end of the
            # previous step has just run.)
            if m > 0:
                local = stop_level()
                level = torch_utils.agree_max(local if local >= STOP_FILE else GO_ON)
                if level >= STOP_FILE:
                    optimizer.zero_grad(set_to_none=True)
                    handle_eviction(level, micro=m)
            first = pos[2] + (m * world + rank) * cfg.micro_batch     # this GPU's sequences
            t_data = time.time()
            x, y = data.sequences(name, first, cfg.micro_batch, device)
            data_seconds += time.time() - t_data
            # DDP averages gradients across GPUs during backward. Only the last micro-batch
            # needs that; no_sync() skips it for the others.
            sync = contextlib.nullcontext() if (m == accum - 1 or not distributed) else ddp.no_sync()
            with sync:
                with autocast:
                    _, loss = ddp(x, y)
                (loss / accum).backward()
            loss_sum += loss.detach()
        torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        step, tokens_seen = step + 1, tokens_seen + cfg.total_batch_tokens
        pos = data.advance(pos)

        if not first_step_logged:  # start-up cost of this process: part of every restart's cost
            first_step_logged = True
            if device.type == "cuda":
                torch.cuda.synchronize()
            startup = time.time() - T_PROCESS_START
            gpu = ("on %s, peak GPU memory %.1f GB" % (torch.cuda.get_device_name(device), peak_gpu_gb())
                   if device.type == "cuda" else "on CPU")
            say("first step done %.1f s after the process started, %s" % (startup, gpu), all_ranks=True)
            log(event="first_step", step=step, startup_seconds=round(startup, 1), gpu=gpu, world_size=world)
        if step % cfg.log_every == 0:
            avg = loss_sum / accum
            if distributed:
                dist.all_reduce(avg)                            # the loss over all GPUs, for the log
                avg /= world
            dt = time.time() - t_log
            tps = (step - step_at_log) * cfg.total_batch_tokens / max(dt, 1e-9)
            data_share = data_seconds / max(dt, 1e-9)            # rank 0's; if high, reading the shards limits training
            say("step %d/%d loss %.4f lr %.2e %.0f tok/s, %.0f%% of the time reading data (pass %d, shard %d, seq %d)"
                % (step, total_steps, avg.item(), lr, tps, 100 * data_share, pos[0], pos[1], pos[2]))
            log(event="train", step=step, loss=avg.item(), lr=lr, tokens_per_s=round(tps),
                data_share=round(data_share, 3))
            if cfg.wandb and master:
                wandb.log({"loss": avg.item(), "lr": lr, "tokens_per_s": tps}, step=step)
            t_log, step_at_log, data_seconds = time.time(), step, 0.0
        if cfg.eval_every_steps and step % cfg.eval_every_steps == 0:
            v = evaluate()
            if v is not None:
                say("step %d val_loss %.4f" % (step, v))
                log(event="eval", step=step, val_loss=v)
                if v < best_val:
                    best_val = v
                    export_best()
        if cfg.step_delay:
            time.sleep(cfg.step_delay)

        # --- the stop check, between steps: every rank agrees on what to do ---
        level = torch_utils.agree_max(stop_level())
        if level >= STOP_FILE:
            handle_eviction(level)
        elif level == TIMED:
            say("stop: runtime limit reached at step %d" % step, all_ranks=True)
            save("timed")
            exit_for_restart("timed")
        elif level == PERIODIC:
            save("periodic")                                  # in-place save, no exit
            last_save = time.time()

    # ------------------------------------------------------------------ done
    v = evaluate()
    if v is not None:
        say("final val_loss %.4f" % v)
        log(event="eval", step=step, val_loss=v)
        if v < best_val:
            best_val = v
            export_best()
    save("final")
    log(event="exit", code=0, step=step)
    say("DONE: %d steps, %.2fB tokens, best val_loss %.4f; exit 0" % (step, tokens_seen / 1e9, best_val))
    if distributed:
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    sys.exit(main())
