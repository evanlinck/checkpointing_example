"""
eventlog.py - read an HTCondor job event log (the submit file's `log =` file).

Reading this file is free for the schedd: it is a plain local file the schedd
already writes. trigger.py and analyze.py use it instead of polling condor_q.

Standard library only. No dependency on the htcondor Python bindings.
"""

import datetime
import re
import time

# First line of every event: "001 (1234.000.000) 10/01 12:34:56 Job executing on host: <...>"
# Newer pools may use ISO dates: "001 (1234.000.000) 2026-10-01 12:34:56 Job executing ..."
HEADER = re.compile(r"^(\d{3}) \((\d+)\.(\d+)\.(\d+)\) (.*)$")

EVENT_NAMES = {
    0: "submitted", 1: "executing", 2: "executable_error", 4: "evicted", 5: "terminated",
    6: "image_size", 7: "shadow_exception", 9: "aborted", 12: "held", 13: "released",
    21: "remote_error", 22: "disconnected", 23: "reconnected", 24: "reconnect_failed",
    28: "job_ad_info", 33: "attribute_update", 35: "cluster_submit", 36: "cluster_remove",
    40: "file_transfer",
}


def _parse_time(rest):
    """Return (epoch_seconds, remaining_text) from the text after the job id."""
    parts = rest.split(" ", 2)
    now = datetime.datetime.now()
    candidates = []
    if len(parts) >= 2:
        candidates.append((parts[0] + " " + parts[1], parts[2] if len(parts) > 2 else ""))
    if parts:
        candidates.append((parts[0], " ".join(parts[1:])))
    for stamp, remaining in candidates:
        s = stamp.rstrip("Z")
        s = re.sub(r"\.\d+$", "", s)             # drop fractional seconds
        s = re.sub(r"[+-]\d\d:?\d\d$", "", s)    # drop a UTC offset (treat as local)
        for fmt in ("%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.datetime.strptime(s, fmt)
            except ValueError:
                continue
            if fmt.startswith("%m/%d"):
                # The old format has no year. Assume this year, or last year if that's in the future.
                dt = dt.replace(year=now.year)
                if dt > now + datetime.timedelta(days=1):
                    dt = dt.replace(year=now.year - 1)
            return time.mktime(dt.timetuple()), remaining
    return None, rest


def read_events(path):
    """Parse the whole log. Returns a list of dicts: code, name, job, t, text, body."""
    events = []
    try:
        with open(path, errors="replace") as f:
            lines = f.read().splitlines()
    except OSError:
        return events
    current = None
    for line in lines:
        if current is None:
            m = HEADER.match(line)
            if not m:
                continue
            code = int(m.group(1))
            t, text = _parse_time(m.group(5))
            current = {
                "code": code,
                "name": EVENT_NAMES.get(code, "event_%03d" % code),
                "job": "%d.%d" % (int(m.group(2)), int(m.group(3))),
                "t": t,
                "text": text.strip(),
                "body": [],
            }
        elif line.startswith("..."):
            events.append(current)
            current = None
        else:
            current["body"].append(line.strip())
    return events  # an unterminated last event (still being written) is skipped


def latest_job_id(events):
    """The job id of the most recent submit event (a DAG retry creates a new cluster)."""
    ids = [e["job"] for e in events if e["code"] == 0]
    return ids[-1] if ids else None


def for_job(events, job):
    return [e for e in events if e["job"] == job]
