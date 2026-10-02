#!/usr/bin/env python3
"""
trigger.py - evict a probe job at a chosen moment, from the access point (AP).

It never calls condor_q. Instead it re-reads the probe's job event log (a
local file) every --poll seconds, waits until the job has been running for
--after seconds since its first "Job executing" event, then sends ONE of:

  vacate        condor_vacate_job <id>          (graceful: soft-kill signal, then SIGKILL after the vacate time)
  vacate-fast   condor_vacate_job -fast <id>    (immediate hard kill)
  hold-release  condor_hold <id>, wait for the held event, sleep --hold-seconds, condor_release <id>

Every action is appended as a JSON line to --out, with AP-side timestamps.
It always exits 0 so a DAG keeps going; problems are recorded, not raised.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eventlog  # noqa: E402


def record(out, **fields):
    fields["t"] = round(time.time(), 3)
    line = json.dumps(fields, sort_keys=True)
    print(line, flush=True)
    with open(out, "a") as f:
        f.write(line + "\n")


def run(cmd, dry_run, out):
    if dry_run:
        record(out, action="dry_run", cmd=cmd)
        return 0
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = p.communicate()
    record(out, action="command", cmd=cmd, rc=p.returncode, output=output.decode(errors="replace")[-500:])
    return p.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", required=True, help="the probe job's event log (submit file `log =`)")
    ap.add_argument("--action", required=True, choices=["vacate", "vacate-fast", "hold-release"])
    ap.add_argument("--after", type=float, required=True, help="seconds after the FIRST execute event")
    ap.add_argument("--out", default="trigger.jsonl")
    ap.add_argument("--poll", type=float, default=15, help="seconds between log reads")
    ap.add_argument("--hold-seconds", type=float, default=30)
    ap.add_argument("--wait-timeout", type=float, default=6 * 3600,
                    help="give up if the job has not started executing within this long")
    ap.add_argument("--condor-bin", default="", help="directory holding condor_vacate_job etc. (default: PATH)")
    ap.add_argument("--dry-run", action="store_true", help="print commands instead of running them")
    args = ap.parse_args()

    def tool(name):
        if args.condor_bin:
            return os.path.join(args.condor_bin, name)
        return shutil.which(name) or name

    t_begin = time.time()
    record(args.out, action="waiting", log=args.log, trigger=args.action, after=args.after)

    # Phase 1: wait until it is time to fire.
    while True:
        events = eventlog.read_events(args.log)
        job = eventlog.latest_job_id(events)
        mine = eventlog.for_job(events, job) if job else []
        ended = [e for e in mine if e["name"] in ("terminated", "aborted")]
        if ended:
            record(args.out, action="gave_up", reason="job ended before the trigger fired",
                   job=job, end_event=ended[-1]["name"], end_text=ended[-1]["text"])
            return
        execs = [e for e in mine if e["name"] == "executing"]
        # Only fire while the job is actually running: the latest state-changing event
        # must be "executing". (A job can be rescheduled after an exit 85 - seen on CHTC as
        # "reactivating the claim would have failed" - and a vacate sent while it is
        # transferring input to the new host hits nothing useful.)
        state = [e for e in mine if e["name"] in ("executing", "evicted", "held", "released", "terminated", "aborted")]
        running = bool(state) and state[-1]["name"] == "executing"
        if execs and execs[0]["t"] is not None and time.time() >= execs[0]["t"] + args.after and running:
            break
        if not execs and time.time() - t_begin > args.wait_timeout:
            record(args.out, action="gave_up", reason="job never started executing", job=job)
            return
        time.sleep(args.poll)

    record(args.out, action="firing", job=job, trigger=args.action,
           first_execute_t=execs[0]["t"], executions_so_far=len(execs),
           last_event=mine[-1]["name"] if mine else None)

    # Phase 2: fire. Retry a few times if the command fails, e.g. the job was
    # momentarily idle between executions and the schedd refused the vacate.
    if args.action == "hold-release":
        cmd = [tool("condor_hold"), job]
    elif args.action == "vacate-fast":
        cmd = [tool("condor_vacate_job"), "-fast", job]
    else:
        cmd = [tool("condor_vacate_job"), job]
    for attempt in range(4):
        if run(cmd, args.dry_run, args.out) == 0:
            break
        time.sleep(args.poll)
    t_fired = time.time()

    # Phase 3 (hold-release only): wait for the held event, then release.
    if args.action == "hold-release":
        while not args.dry_run:
            events = eventlog.for_job(eventlog.read_events(args.log), job)
            held = [e for e in events if e["name"] == "held" and e["t"] is not None and e["t"] >= t_fired - 60]
            if held:
                record(args.out, action="saw_held", held_text=held[-1]["text"], held_body=held[-1]["body"])
                break
            if time.time() - t_fired > 1800:
                record(args.out, action="gave_up", reason="no held event within 30 min")
                return
            time.sleep(args.poll)
        time.sleep(args.hold_seconds)
        run([tool("condor_release"), job], args.dry_run, args.out)

    record(args.out, action="done")


if __name__ == "__main__":
    main()
