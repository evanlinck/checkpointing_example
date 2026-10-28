#!/usr/bin/env python3
"""
ap_survey_summary.py - turn ap_survey.sh's history.txt and glideins.txt into tables.

    python3 ap_survey_summary.py results/ap-survey/<ap>

Writes <dir>/summary.md. Standard library only (runs on the AP or a laptop).

What the history columns can and can't tell (measured in docs/environment.md):
  - NumJobStarts counts executions that started. An exit-85 restart in the same sandbox does NOT
    add one (P1), so NumJobStarts - 1 counts interruptions (evictions, holds then releases,
    rescheduled restarts), not planned checkpoints.
  - RemoteWallClockTime / NumJobStarts is the mean time per execution. For jobs that were
    interrupted it is a rough stand-in for "how long a job runs before it is interrupted".
  - RemoteWallClockTime - CommittedTime is HTCondor's "badput": runtime from executions that
    didn't end well. For self-checkpointing jobs some of it may have been saved by a checkpoint,
    so read it as an upper bound on work lost.
"""

import os
import re
import sys
from collections import Counter, defaultdict

BUCKETS_H = [1, 2, 4, 6, 8, 12, 24]   # hours


def bucket_label(hours):
    lo = 0
    for b in BUCKETS_H:
        if hours < b:
            return "%d–%d h" % (lo, b)
        lo = b
    return "≥ %d h" % BUCKETS_H[-1]


BUCKET_ORDER = ["%d–%d h" % (lo, hi) for lo, hi in zip([0] + BUCKETS_H, BUCKETS_H)] + ["≥ %d h" % BUCKETS_H[-1]]


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# HTCondor counts a transfer failure twice: as TransferOutputError and as TransferOutputErrorCedar
# (or ...Pelican, the protocol). Keep only the generic name.
PROTOCOL_SUFFIX = re.compile(r"^(Transfer(?:Input|Output)Error)\w+$")


def by_reason(s):
    """A ClassAd record like [ JobPolicy = 2; TransferOutputError = 1 ] -> {name: count}."""
    return {k: int(v) for k, v in re.findall(r"(\w+)\s*=\s*(\d+)", s or "")
            if not PROTOCOL_SUFFIX.match(k)}


def read_history(path):
    cols, rows = None, []
    with open(path, errors="replace") as f:
        for line in f:
            if line.startswith("# columns:"):
                cols = line.split(":", 1)[1].split()
            elif line.startswith("#") or not line.strip():
                continue
            elif cols:
                vals = line.rstrip("\n").split("\t")
                if len(vals) == len(cols):
                    rows.append(dict(zip(cols, vals)))
    return rows


def group_of(r):
    gpu = (num(r.get("RequestGPUs")) or 0) > 0
    ckpt = r.get("SuccessCheckpointExitCode", "undefined") != "undefined"
    g = ("GPU" if gpu else "CPU") + (", self-checkpointing" if ckpt else ", not checkpointing")
    # An AP that flocks (ap2002) mixes pools; MachineAttrGLIDEIN_Site0 is set only for glidein (OSPool) runs.
    site = r.get("MachineAttrGLIDEIN_Site0")
    if site is not None:
        g += ", OSPool" if site != "undefined" else ", not OSPool"
    return g


def history_tables(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[group_of(r)].append(r)
    md = ["## Jobs that finished in the period", "",
          "| Group | Jobs | Removed | Interrupted ≥ 1× | Interruptions per interrupted job | Badput share |",
          "|---|---|---|---|---|---|"]
    per_exec = {}
    vacates, holds = defaultdict(Counter), defaultdict(Counter)
    for g in sorted(groups):
        rs = groups[g]
        removed = sum(1 for r in rs if r.get("JobStatus") == "3")
        starts = [num(r.get("NumJobStarts")) or 0 for r in rs]
        hit = [s for s in starts if s > 1]
        wall = sum(num(r.get("RemoteWallClockTime")) or 0 for r in rs)
        good = sum(num(r.get("CommittedTime")) or 0 for r in rs
                   if num(r.get("RemoteWallClockTime")) is not None)
        md.append("| %s | %d | %.1f%% | %.1f%% | %s | %s |" % (
            g, len(rs), 100.0 * removed / len(rs), 100.0 * len(hit) / len(rs),
            "%.1f" % (sum(s - 1 for s in hit) / len(hit)) if hit else "–",
            "%.1f%%" % (100.0 * (wall - good) / wall) if wall else "–"))
        c = Counter()
        for r in rs:
            n, w = num(r.get("NumJobStarts")) or 0, num(r.get("RemoteWallClockTime"))
            if n > 1 and w:
                c[bucket_label(w / n / 3600)] += 1
            vacates[g].update(by_reason(r.get("NumVacatesByReason")))
            holds[g].update(by_reason(r.get("NumHoldsByReason")))
        per_exec[g] = c

    md += ["", "## Mean time per execution, interrupted jobs only", "",
           "A rough stand-in for how long jobs run before an interruption (see the notes at the top of",
           "`ap_survey_summary.py`). Share of interrupted jobs in each range.", "",
           "| Group | n | " + " | ".join(BUCKET_ORDER) + " |",
           "|---|---|" + "---|" * len(BUCKET_ORDER)]
    for g in sorted(per_exec):
        c, n = per_exec[g], sum(per_exec[g].values())
        if n:
            md.append("| %s | %d | " % (g, n) + " | ".join("%.0f%%" % (100.0 * c[b] / n) for b in BUCKET_ORDER) + " |")

    for title, table in (("Vacates by reason (`NumVacatesByReason`)", vacates),
                         ("Holds by reason (`NumHoldsByReason`)", holds)):
        md += ["", "## " + title, ""]
        if not any(table.values()):
            md.append("None recorded (or the attribute isn't in this HTCondor version's history).")
            continue
        md += ["| Group | Reason | Count |", "|---|---|---|"]
        for g in sorted(table):
            for reason, n in table[g].most_common(8):
                md.append("| %s | %s | %d |" % (g, reason, n))
    return md


def glidein_tables(path):
    """glideins.txt's 'count, site, hours to retire, hours to die' block -> distribution over slots."""
    retire, die, sites = Counter(), Counter(), set()
    in_block = False
    with open(path, errors="replace") as f:
        for line in f:
            if line.startswith("# count, site, hours until"):
                in_block = True
                continue
            if in_block and (line.startswith("#") or not line.strip()):
                break
            if in_block:
                parts = line.split()
                if len(parts) >= 4:
                    n = int(parts[0])
                    sites.add(parts[1])
                    for counter, val in ((retire, parts[2]), (die, parts[3])):
                        v = num(val)
                        counter["undefined" if v is None else ("already past" if v < 0 else bucket_label(v))] += n
    if not retire:
        return ["## Glidein lifetimes", "", "No glidein slots found (not an OSPool collector?)."]
    md = ["## Glidein lifetimes left, over all slots now", "",
          "Hours from now until each slot's glidein stops taking jobs (`GLIDEIN_ToRetire`) and is",
          "killed (`GLIDEIN_ToDie`), over %d sites. A snapshot: it shows how much runway a job starting" % len(sites),
          "now would get, not the full lifetime of a glidein.", "",
          "| Range | Slots, to retire | Slots, to die |", "|---|---|---|"]
    for b in ["already past"] + BUCKET_ORDER + ["undefined"]:
        if retire[b] or die[b]:
            md.append("| %s | %d | %d |" % (b, retire[b], die[b]))
    return md


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = sys.argv[1]
    md = ["# Access point survey: %s" % os.path.basename(os.path.normpath(d)), "",
          "From `ap_survey.sh`. The raw files next to this one hold the config, spool, held jobs, GPUs",
          "and hold reasons; this page summarises the job history and glidein lifetimes.", ""]
    hist = os.path.join(d, "history.txt")
    if os.path.exists(hist):
        rows = read_history(hist)
        md += ["%d finished jobs in `history.txt`." % len(rows), ""] + history_tables(rows) + [""]
    gl = os.path.join(d, "glideins.txt")
    if os.path.exists(gl):
        md += glidein_tables(gl) + [""]
    out = os.path.join(d, "summary.md")
    with open(out, "w") as f:
        f.write("\n".join(md))
    print("wrote", out)


if __name__ == "__main__":
    main()
