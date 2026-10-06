#!/usr/bin/env python3
"""
Recipe 0: the smallest complete checkpointing job for HTCondor.

It trains a one-line model on made-up data. The model is deliberately boring; the
five blocks marked CHECKPOINT are the point. Every long-running job needs them:

  1. Listen for HTCondor's "please stop" signal.
  2. Save the training state so that a crash can never leave a half-written file.
  3. At startup, continue from the saved state if there is one.
  4. After each training step: if HTCondor asked us to stop, or our own time limit
     is up, save and exit with code 85 ("restart me").
  5. When training is done, exit with code 0 ("finished").

Run it the same way every time, whether it's the first start or a restart:
    python3 train.py
"""
import argparse   # reads the command-line options below
import os         # file operations
import random     # Python's random numbers (saved in the checkpoint)
import signal     # lets us react when HTCondor asks the job to stop
import sys        # sys.exit(code) ends the program with an exit code
import time       # clocks, for the time limit

import numpy as np  # NumPy's random numbers are saved in the checkpoint too
import torch


# Settings
parser = argparse.ArgumentParser(description="Recipe 0: a minimal checkpointing job.")
parser.add_argument("--max-runtime-seconds", type=float, default=3600,
                    help="after this long, save and exit 85 (the timed checkpoint)")
parser.add_argument("--epochs", type=int, default=10, help="passes over the data")
parser.add_argument("--log-every", type=int, default=100, help="print the loss every N steps")
parser.add_argument("--step-delay", type=float, default=0.0,
                    help="seconds to sleep after each step, so this tiny job runs long enough to interrupt")
args = parser.parse_args()

CHECKPOINT = "checkpoints/checkpoint.pt"  # the submit file tells HTCondor to keep the "checkpoints" directory
BATCH_SIZE = 64                           # examples per training step
LEARNING_RATE = 0.01
SEED = 0                                  # makes the data and the shuffling the same on every run
EXIT_RESTART = 85                         # the exit code that means "progress saved, restart me"


# ===== CHECKPOINT 1: listen for HTCondor's stop signal =====
# When HTCondor needs the machine back, it sends this program a SIGTERM signal,
# then force-kills it about 600 seconds later. We only make a note that it happened.
# The training loop checks the note after each step and saves at a safe moment.
# (Don't save right here: this function can run in the middle of a training step.)
stop_requested = False


def on_sigterm(signum, frame):
    global stop_requested
    stop_requested = True


signal.signal(signal.SIGTERM, on_sigterm)  # "when SIGTERM arrives, call on_sigterm"
start_time = time.time()                   # for our own time limit


# The training problem
# Make every run do exactly the same arithmetic, so a resumed run can be checked
# against an uninterrupted one (test_local.py does this).
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")  # needed for repeatable GPU math
torch.use_deterministic_algorithms(True)
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
device = "cuda" if torch.cuda.is_available() else "cpu"     # use a GPU if the job has one

# Made-up data: 20,000 examples of 32 numbers each, sorted into 4 classes by a hidden rule.
g = torch.Generator().manual_seed(SEED)
x = torch.randn(20000, 32, generator=g)                       # inputs
y = (x @ torch.randn(32, 4, generator=g)).argmax(1)           # the right answers
x, y = x.to(device), y.to(device)
steps_per_epoch = (len(x) + BATCH_SIZE - 1) // BATCH_SIZE

# The model: 32 inputs -> 4 class scores. One line; this is logistic regression.
model = torch.nn.Linear(32, 4).to(device)
# The optimizer updates the weights. AdamW also keeps running averages of past
# gradients, which is why its state goes into the checkpoint too.
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
# The scheduler lowers the learning rate over the run; it remembers how far along it is.
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs * steps_per_epoch)
loss_fn = torch.nn.CrossEntropyLoss()  # how wrong the class scores are

# Where we are in training. Together with the above, this is everything a checkpoint needs.
step, epoch, batch_index = 0, 0, 0


# ===== CHECKPOINT 2: save the training state =====
def save_checkpoint(reason):
    """Save everything needed to continue later as if nothing had happened.

    Write to a temporary file first, then rename it over the real one. A rename
    happens all at once, so even if the job is killed mid-save, checkpoint.pt is
    always either the old complete checkpoint or the new one, never half of one."""
    state = {
        "model": model.state_dict(),          # the weights
        "optimizer": optimizer.state_dict(),  # AdamW's running averages
        "scheduler": scheduler.state_dict(),  # where we are in the learning-rate schedule
        "step": step, "epoch": epoch, "batch_index": batch_index,  # where we are in the data
        # Random number generators. This tiny model uses none while training, but most real
        # models do (dropout, data augmentation): without these a resumed run quietly differs.
        "rng": {"python": random.getstate(), "numpy": np.random.get_state(), "torch": torch.get_rng_state(),
                "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None},
        "reason": reason,                     # just for the log: why this save happened
    }
    torch.save(state, CHECKPOINT + ".tmp")
    os.replace(CHECKPOINT + ".tmp", CHECKPOINT)  # the all-at-once step
    print("SAVED step %d (reason: %s)" % (step, reason), flush=True)


# ===== CHECKPOINT 3: continue from the saved state, if there is one =====
# Create the checkpoint directory right away: HTCondor copies it at every exit 85,
# and puts the job on hold if it doesn't exist.
os.makedirs(os.path.dirname(CHECKPOINT), exist_ok=True)
if os.path.exists(CHECKPOINT):
    # weights_only=False: the checkpoint holds Python/NumPy random-number states, which
    # PyTorch's stricter default loader refuses. Only load checkpoints you wrote yourself.
    state = torch.load(CHECKPOINT, map_location=device, weights_only=False)
    model.load_state_dict(state["model"])  # put everything back exactly as it was
    optimizer.load_state_dict(state["optimizer"])
    scheduler.load_state_dict(state["scheduler"])
    step, epoch, batch_index = state["step"], state["epoch"], state["batch_index"]
    random.setstate(state["rng"]["python"])
    np.random.set_state(state["rng"]["numpy"])
    torch.set_rng_state(state["rng"]["torch"])
    if state["rng"]["cuda"] is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(state["rng"]["cuda"])
    print("RESUMED from step %d (epoch %d, batch %d; saved because: %s)"
          % (step, epoch, batch_index, state["reason"]), flush=True)
else:
    print("STARTING fresh", flush=True)


# The training loop
while epoch < args.epochs:
    # This epoch's shuffled order depends only on (SEED, epoch), so after a restart we
    # rebuild exactly the same order and skip the batches already done. That's why
    # (epoch, batch_index) is all the checkpoint needs to know where it is in the data.
    order = torch.randperm(len(x), generator=torch.Generator().manual_seed(SEED * 1000 + epoch))

    while batch_index < steps_per_epoch:  # after a resume, this starts mid-epoch
        idx = order[batch_index * BATCH_SIZE:(batch_index + 1) * BATCH_SIZE].to(device)
        loss = loss_fn(model(x[idx]), y[idx])  # predict, and measure the error
        optimizer.zero_grad()
        loss.backward()                        # compute gradients
        optimizer.step()                       # update the weights
        scheduler.step()                       # update the learning rate
        step += 1
        batch_index += 1
        if step % args.log_every == 0:
            print("step %d epoch %d loss %r" % (step, epoch, loss.item()), flush=True)
        time.sleep(args.step_delay)

        # ===== CHECKPOINT 4: after every step, check whether to stop =====
        # Between steps, everything (weights, optimizer, data position) agrees, so this is
        # a safe moment to save. Stop if HTCondor asked us to, or our own time limit is up.
        if stop_requested or time.time() - start_time >= args.max_runtime_seconds:
            save_checkpoint("signal" if stop_requested else "timed")
            print("EXIT 85: state saved; asking HTCondor to restart the job", flush=True)
            sys.exit(EXIT_RESTART)

    epoch += 1
    batch_index = 0  # the next epoch starts at its first batch


# ===== CHECKPOINT 5: training is done =====
# Save the final state, then exit 0: only now does HTCondor treat the job as finished.
save_checkpoint("final")
print("DONE after %d steps; exit 0" % step, flush=True)
sys.exit(0)
