"""
stop.py: decide when a training job should save and stop.

A job running under HTCondor should stop (save, then exit 85 so HTCondor restarts it)
when any of these happens:
  - "signal":    HTCondor sent SIGTERM (a vacate, a hold, a backfill slot reclaimed).
                 The process is killed about 600 s later.
  - "stop_file": a launcher wrapper (launch.py) received SIGTERM on our behalf and
                 created a stop file, because launchers like torchrun don't pass the
                 signal on safely.
  - "timed":     our own runtime limit is up (the timed checkpoint).

Typical use, checked once per training step:

    from stop import StopPolicy, EXIT_RESTART

    policy = StopPolicy(max_runtime_seconds=3600)
    ...
    for batch in loader:
        train_step(batch)
        if policy.should_stop():
            save_checkpoint(reason=policy.reason)
            policy.exit_for_restart()          # exit 85 ("restart me")

Standard library only. No imports from the other htcondor_ckpt modules, so this file
can be copied into a project on its own.
"""

import ast
import os
import signal
import sys
import time

EXIT_RESTART = 85  # "progress saved, please restart me" (submit file: checkpoint_exit_code = 85)

# Environment variables set by launch.py for the processes it starts.
STOP_FILE_ENV = "HTCONDOR_CKPT_STOP_FILE"
RESTART_FILE_ENV = "HTCONDOR_CKPT_RESTART_FILE"

DEFAULT_VACATE_SECONDS = 600  # MachineMaxVacateTime on every CHTC and OSPool slot measured


class StopPolicy:
    """Watches for a stop signal, a stop file and a runtime limit.

    The signal handler only records the time; it does no I/O and touches no GPU state.
    Call should_stop() at step boundaries, where all training state is consistent.
    """

    def __init__(self, max_runtime_seconds=None, stop_file=None, vacate_seconds=None,
                 deadline_fraction=0.7, signals=(signal.SIGTERM,), install_handlers=True,
                 clock=time.monotonic):
        """
        max_runtime_seconds: save and stop after this long (None: no limit).
        stop_file:           path to watch (default: $HTCONDOR_CKPT_STOP_FILE, set by launch.py).
        vacate_seconds:      time between SIGTERM and SIGKILL (default: vacate_budget()).
        deadline_fraction:   start the final save no later than this fraction of the window.
        """
        self.clock = clock
        self.start = clock()
        self.max_runtime_seconds = max_runtime_seconds
        self.stop_file = stop_file if stop_file is not None else os.environ.get(STOP_FILE_ENV)
        if vacate_seconds is None:
            vacate_seconds, self.vacate_source = vacate_budget()
        else:
            self.vacate_source = "given"
        self.vacate_seconds = float(vacate_seconds)
        self.deadline_fraction = deadline_fraction
        self.reason = None          # "signal", "stop_file" or "timed" once a stop is requested
        self.stop_time = None       # clock() when the stop was first requested
        self.signal_name = None
        if install_handlers:
            for sig in signals:
                signal.signal(sig, self._on_signal)

    def _on_signal(self, signum, frame):
        if self.reason is None:  # keep the first request; ignore repeats
            self.reason, self.stop_time = "signal", self.clock()
            self.signal_name = signal.Signals(signum).name

    def should_stop(self):
        """True if the job should save and stop now. Cheap enough to call every step."""
        if self.reason is None and self.stop_file and os.path.exists(self.stop_file):
            self.reason, self.stop_time = "stop_file", self.clock()
        if (self.reason is None and self.max_runtime_seconds is not None
                and self.clock() - self.start >= self.max_runtime_seconds):
            self.reason, self.stop_time = "timed", self.clock()
        return self.reason is not None

    def evicting(self):
        """True if HTCondor is evicting us (as opposed to our own timed stop)."""
        return self.reason in ("signal", "stop_file")

    def seconds_left(self):
        """Seconds until HTCondor's SIGKILL, if we are being evicted; else None."""
        if not self.evicting():
            return None
        return self.vacate_seconds - (self.clock() - self.stop_time)

    def past_deadline(self):
        """True if it is too late to *start* a long save (past deadline_fraction of the window).

        Large jobs use this to decide whether a final save still fits (recipe 3); a save that
        starts after the deadline risks being killed half-way."""
        left = self.seconds_left()
        return left is not None and left < self.vacate_seconds * (1 - self.deadline_fraction)

    def describe(self):
        """One line for the log, e.g. 'stop: signal SIGTERM, 597 s left before SIGKILL'."""
        if self.reason is None:
            return "stop: not requested"
        if self.evicting():
            what = self.signal_name if self.reason == "signal" else "stop file %s" % self.stop_file
            return "stop: %s, %.0f s left before SIGKILL (window %.0f s from %s)" % (
                what, self.seconds_left(), self.vacate_seconds, self.vacate_source)
        return "stop: runtime limit of %.0f s reached" % self.max_runtime_seconds

    def exit_for_restart(self):
        """Exit 85 ("restart me"). Under launch.py, first leave a note in the restart file:
        launchers like torchrun turn a worker's exit 85 into 1, and the wrapper uses the
        note to exit 85 itself. Never exit 0 because of a stop request."""
        mark_restart_requested()
        sys.stdout.flush()
        sys.exit(EXIT_RESTART)


def mark_restart_requested(note=""):
    """Append a line to $HTCONDOR_CKPT_RESTART_FILE, if launch.py set it."""
    path = os.environ.get(RESTART_FILE_ENV)
    if path:
        with open(path, "a") as f:
            f.write("pid=%d rank=%s %s\n" % (os.getpid(), os.environ.get("RANK", "-"), note))


# --------------------------------------------------------------------- vacate window
def vacate_budget(machine_ad=None, job_ad=None, default=DEFAULT_VACATE_SECONDS):
    """Seconds between HTCondor's SIGTERM and its SIGKILL, from the job's ads.

    Reads MachineMaxVacateTime from $_CONDOR_MACHINE_AD and JobMaxVacateTime (set by
    job_max_vacate_time) from $_CONDOR_JOB_AD. Returns (seconds, source).

    Conservative on purpose: if both are set, the smaller one. Our probes saw a job's
    larger request honored on slots with long retirement time, but not everywhere
    (docs/environment.md section 3). Falls back to `default` when nothing can be read.
    """
    machine_ad = machine_ad or os.environ.get("_CONDOR_MACHINE_AD")
    job_ad = job_ad or os.environ.get("_CONDOR_JOB_AD")
    machine = _ad_number(machine_ad, "MachineMaxVacateTime")
    job = _ad_number(job_ad, "JobMaxVacateTime")
    if machine is not None and job is not None:
        return (min(machine, job), "min(MachineMaxVacateTime, JobMaxVacateTime)")
    if machine is not None:
        return (machine, "MachineMaxVacateTime")
    if job is not None:
        return (job, "JobMaxVacateTime")
    return (float(default), "default")


def _ad_number(path, attr):
    """Value of `attr` in the ClassAd file at `path`, as a number, or None."""
    if not path or not os.path.exists(path):
        return None
    try:  # with the HTCondor Python bindings, evaluate the expression in the ad's context
        import classad
        with open(path) as f:
            value = classad.parseOne(f).eval(attr)
        return float(value) if isinstance(value, (int, float)) else None
    except Exception:
        pass
    expr = None
    with open(path) as f:
        for line in f:
            name, sep, value = line.partition(" = ")
            if sep and name.strip().lower() == attr.lower():
                expr = value.strip()
    return _arithmetic(expr) if expr else None


def _arithmetic(expr):
    """Evaluate plain arithmetic like '10 * 60'; None for anything else (e.g. attribute names)."""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        return None
    ops = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
           ast.Div: lambda a, b: a / b, ast.FloorDiv: lambda a, b: a // b}

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -ev(node.operand)
        raise ValueError("not plain arithmetic")

    try:
        return float(ev(tree))
    except (ValueError, ZeroDivisionError):
        return None
