"""launch.py with a fake launcher that behaves like torchrun: it starts two workers,
forwards SIGTERM to them and kills them 2 s later, and exits 1 if any worker fails."""
import os
import signal
import subprocess
import sys
import textwrap
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCH = os.path.join(ROOT, "htcondor_ckpt", "launch.py")

WORKER = textwrap.dedent("""
    import os, sys, time
    sys.path.insert(0, %r)
    from htcondor_ckpt.stop import StopPolicy
    policy = StopPolicy(vacate_seconds=600)
    print("worker ready", flush=True)
    for step in range(600):
        time.sleep(0.05)
        if policy.should_stop():
            time.sleep(float(os.environ.get("SAVE_SECONDS", "0")))   # a slow save
            print("worker saved after", policy.reason, flush=True)
            policy.exit_for_restart()
    print("worker finished", flush=True)
""") % ROOT

FAKE_LAUNCHER = textwrap.dedent("""
    import signal, subprocess, sys, time
    procs = [subprocess.Popen([sys.executable, sys.argv[1]], env=dict(__import__("os").environ, RANK=str(r)))
             for r in range(2)]
    def on_term(s, f):
        for p in procs: p.send_signal(signal.SIGTERM)
        time.sleep(2)
        for p in procs: p.kill()
        sys.exit(143)
    signal.signal(signal.SIGTERM, on_term)
    while True:
        codes = [p.poll() for p in procs]
        if any(c not in (None, 0) for c in codes):
            time.sleep(0.5); [p.kill() for p in procs if p.poll() is None]; sys.exit(1)
        if all(c == 0 for c in codes): sys.exit(0)
        time.sleep(0.05)
""")


def start(tmp_path, save_seconds):
    (tmp_path / "worker.py").write_text(WORKER)
    (tmp_path / "fake_launcher.py").write_text(FAKE_LAUNCHER)
    env = dict(os.environ, SAVE_SECONDS=str(save_seconds))
    return subprocess.Popen([sys.executable, LAUNCH, "--", sys.executable, "fake_launcher.py", "worker.py"],
                            cwd=str(tmp_path), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def wait_ready(p, n=2):
    ready = 0
    while ready < n:
        line = p.stdout.readline()
        assert line, "process ended early"
        ready += line.startswith("worker ready")


def test_sigterm_gives_workers_time_and_maps_exit_to_85(tmp_path):
    p = start(tmp_path, save_seconds=4)   # longer than the fake launcher's 2 s kill timer
    wait_ready(p)
    p.send_signal(signal.SIGTERM)         # HTCondor signals only the top process: the wrapper
    out = p.communicate(timeout=60)[0]
    assert p.returncode == 85, out
    assert out.count("worker saved after stop_file") == 2, out
    assert "workers asked for a restart" in out
    assert not (tmp_path / "STOP_REQUESTED").exists() and not (tmp_path / "RESTART_REQUESTED").exists()


def test_normal_finish_passes_exit_code(tmp_path):
    (tmp_path / "worker.py").write_text(WORKER.replace("range(600)", "range(5)"))
    (tmp_path / "fake_launcher.py").write_text(FAKE_LAUNCHER)
    p = subprocess.run([sys.executable, LAUNCH, "--", sys.executable, "fake_launcher.py", "worker.py"],
                       cwd=str(tmp_path), capture_output=True, text=True, timeout=60)
    assert p.returncode == 0 and "launcher exited 0" in p.stdout


def test_usage_error():
    p = subprocess.run([sys.executable, LAUNCH], capture_output=True, text=True)
    assert p.returncode == 2 and "usage" in p.stderr
