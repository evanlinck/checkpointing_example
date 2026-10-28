import os
import signal

import pytest

from htcondor_ckpt import stop
from htcondor_ckpt.stop import StopPolicy, job_time_left, runtime_limit, vacate_budget


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def policy(**kw):
    kw.setdefault("vacate_seconds", 600)
    kw.setdefault("install_handlers", False)
    kw.setdefault("stop_file", "")
    return StopPolicy(**kw)


def test_runtime_limit():
    clock = Clock()
    p = policy(max_runtime_seconds=60, clock=clock)
    assert not p.should_stop()
    clock.t += 61
    assert p.should_stop() and p.reason == "timed" and not p.evicting()
    assert p.seconds_left() is None


def test_signal_sets_reason_and_deadline():
    clock = Clock()
    p = policy(clock=clock)
    p._on_signal(signal.SIGTERM, None)
    p._on_signal(signal.SIGTERM, None)  # repeats are ignored
    assert p.should_stop() and p.reason == "signal" and p.signal_name == "SIGTERM"
    clock.t += 100
    assert p.seconds_left() == pytest.approx(500)
    assert not p.past_deadline()             # 70% of 600 s = 420 s not reached
    clock.t += 330
    assert p.past_deadline()
    assert "SIGTERM" in p.describe()


def test_signal_handler_installed(tmp_path):
    p = StopPolicy(vacate_seconds=600, stop_file="")
    old = signal.getsignal(signal.SIGUSR1)
    try:
        p2 = StopPolicy(vacate_seconds=600, stop_file="", signals=(signal.SIGUSR1,))
        os.kill(os.getpid(), signal.SIGUSR1)
        assert p2.should_stop() and p2.signal_name == "SIGUSR1"
    finally:
        signal.signal(signal.SIGUSR1, old)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)


def test_stop_file(tmp_path):
    f = tmp_path / "STOP"
    p = policy(stop_file=str(f))
    assert not p.should_stop()
    f.write_text("")
    assert p.should_stop() and p.reason == "stop_file" and p.evicting()


def test_stop_file_from_environment(tmp_path, monkeypatch):
    f = tmp_path / "STOP"
    monkeypatch.setenv(stop.STOP_FILE_ENV, str(f))
    p = StopPolicy(vacate_seconds=600, install_handlers=False)
    f.write_text("")
    assert p.should_stop() and p.reason == "stop_file"


def test_exit_for_restart_writes_restart_file(tmp_path, monkeypatch):
    rf = tmp_path / "RESTART"
    monkeypatch.setenv(stop.RESTART_FILE_ENV, str(rf))
    with pytest.raises(SystemExit) as e:
        policy().exit_for_restart()
    assert e.value.code == 85 and rf.read_text().startswith("pid=")


def write_ad(path, **attrs):
    path.write_text("".join("%s = %s\n" % kv for kv in attrs.items()))
    return str(path)


def test_vacate_budget_from_ads(tmp_path):
    m = write_ad(tmp_path / "machine", MachineMaxVacateTime="10 * 60", Name='"slot1@host"')
    j = write_ad(tmp_path / "job", JobMaxVacateTime="60")
    assert vacate_budget(m, j) == (60, "min(MachineMaxVacateTime, JobMaxVacateTime)")
    assert vacate_budget(m, str(tmp_path / "missing")) == (600, "MachineMaxVacateTime")


def test_vacate_budget_unevaluable_falls_back(tmp_path):
    m = write_ad(tmp_path / "machine", MachineMaxVacateTime="SomeOtherAttribute * 2")
    seconds, source = vacate_budget(m, str(tmp_path / "missing"), default=600)
    assert source in ("default", "MachineMaxVacateTime")  # "default" without the classad module
    assert seconds == 600 or source == "MachineMaxVacateTime"


def test_vacate_budget_uses_classad2_when_installed(tmp_path, monkeypatch):
    """HTCondor 25.x's bindings name the module classad2: the expression is evaluated there,
    so an ad value plain arithmetic can't handle still works."""
    import sys
    import types

    class FakeAd:
        def eval(self, attr):
            return 450

    fake = types.ModuleType("classad2")
    fake.parseOne = lambda f: FakeAd()
    monkeypatch.setitem(sys.modules, "classad2", fake)
    m = write_ad(tmp_path / "machine", MachineMaxVacateTime="SomeOtherAttribute * 2")
    assert vacate_budget(m, str(tmp_path / "missing")) == (450, "MachineMaxVacateTime")


def test_vacate_budget_no_ads(monkeypatch):
    monkeypatch.delenv("_CONDOR_MACHINE_AD", raising=False)
    monkeypatch.delenv("_CONDOR_JOB_AD", raising=False)
    assert vacate_budget() == (600, "default")


@pytest.mark.parametrize("expr,value", [("10 * 60", 600), ("600", 600), ("(5 + 5) * 6", 60), ("-1", -1)])
def test_arithmetic(expr, value):
    assert stop._arithmetic(expr) == value


@pytest.mark.parametrize("expr", ["JobRuntimeGuarantee", "__import__('os')", "1 / 0", "true", ""])
def test_arithmetic_rejects(expr):
    assert stop._arithmetic(expr) is None


def test_eviction_replaces_a_pending_timed_stop(tmp_path):
    """A job waiting for the end of an epoch before its timed checkpoint must still
    notice HTCondor's SIGTERM (and its deadline)."""
    clock = Clock()
    f = tmp_path / "STOP"
    p = policy(max_runtime_seconds=60, stop_file=str(f), clock=clock)
    clock.t += 61
    assert p.should_stop() and p.reason == "timed" and not p.evicting()
    clock.t += 30
    p._on_signal(signal.SIGTERM, None)
    assert p.reason == "signal" and p.evicting() and p.seconds_left() == pytest.approx(600)
    f.write_text("")                      # a later stop file doesn't replace the signal
    p.should_stop()
    assert p.reason == "signal"


def test_runtime_limit_shortened_by_glidein_end(tmp_path):
    m = write_ad(tmp_path / "machine", GLIDEIN_ToDie="100000", GLIDEIN_Site='"UChicago"')
    j = str(tmp_path / "no-job-ad")
    # 10 h of glidein left, minus the 900 s margin, is less than a 12 h limit
    assert runtime_limit(12 * 3600, m, j, now=100000 - 36000) == (36000 - 900, "GLIDEIN_ToDie - 900 s")
    # ... but more than a 5 h limit, which is kept
    assert runtime_limit(5 * 3600, m, j, now=100000 - 36000) == (5 * 3600, "max_runtime_seconds")
    # no limit of our own: the glidein's
    assert runtime_limit(None, m, j, margin=600, now=99000) == (400, "GLIDEIN_ToDie - 600 s")
    # already past the deadline: stop at the first step
    assert runtime_limit(3600, m, j, now=99950)[0] == 0


def test_runtime_limit_from_allowed_execute_duration(tmp_path):
    m = str(tmp_path / "no-machine-ad")
    j = write_ad(tmp_path / "job", AllowedExecuteDuration="20 * 3600")       # ap40 Medium
    assert runtime_limit(24 * 3600, m, j) == (20 * 3600 - 900, "AllowedExecuteDuration - 900 s")
    assert runtime_limit(6 * 3600, m, j) == (6 * 3600, "max_runtime_seconds")


def test_runtime_limit_without_limits(tmp_path, monkeypatch):
    m = write_ad(tmp_path / "machine", MachineMaxVacateTime="600")      # CHTC: no GLIDEIN_ToDie
    j = write_ad(tmp_path / "job", JobStartDate="1000")
    assert runtime_limit(3600, m, j) == (3600, "max_runtime_seconds")
    assert runtime_limit(None, m, j) == (None, "none")
    monkeypatch.delenv("_CONDOR_MACHINE_AD", raising=False)
    monkeypatch.delenv("_CONDOR_JOB_AD", raising=False)
    assert runtime_limit(3600) == (3600, "max_runtime_seconds")


def test_job_time_left(tmp_path):
    j = write_ad(tmp_path / "job", JobStartDate="1000", AllowedJobDuration="14 * 24 * 3600")
    assert job_time_left(j, margin=0, now=1000 + 86400) == 13 * 86400
    assert job_time_left(j, now=1000) == 14 * 86400 - 900
    assert job_time_left(write_ad(tmp_path / "j2", JobStartDate="1000")) is None
