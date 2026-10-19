#!/usr/bin/env python3
"""
redact.py - remove personal details from probe reports before sharing them.

Replaces:
  - the submitting user's name (from --user, $USER, or the login name)
  - /home/<name> and /staging/<x>/<name> or /staging/<name> paths
  - osdf:///chtc/staging/... paths
  - IPv4 and IPv6 addresses (event-log "Job executing on host: <...>" lines)
  - execute machine names (many CHTC GPU machines are named after their owners; OSPool
    worker nodes name the site). Each becomes <host-1>, <host-2>, ... numbered per file, so
    a report still shows whether a job restarted on the same machine or a different one.
    The access point's name (ap2002 etc.) is kept.

analyze.py applies this to every report it writes. To clean existing reports in place:
    python3 redact.py results/            # all .md and .json files under results/
    python3 redact.py --check results/    # list files that still contain something to redact
"""

import argparse
import getpass
import os
import re
import sys

PATTERNS = [
    # osdf:///chtc/staging/e/name/... or osdf:///chtc/staging/name/...
    (re.compile(r"osdf:///chtc/staging/(?:[a-z]/)?[A-Za-z0-9_][A-Za-z0-9_.-]*"), "osdf:///chtc/staging/<user>"),
    # /staging/e/name or /staging/name. A name starts with a letter or digit, so doc
    # placeholders like "/staging/..." and "/staging/<user>" are left alone.
    (re.compile(r"/staging/(?:[a-z]/)?[A-Za-z0-9_][A-Za-z0-9_.-]*"), "/staging/<user>"),
    (re.compile(r"/home/[A-Za-z0-9_][A-Za-z0-9_.-]*"), "/home/<user>"),
    # IPv6 as HTCondor writes it in sinful strings: [2607-f388-2200-100-...]
    (re.compile(r"\[[0-9a-fA-F]{1,4}(?:-[0-9a-fA-F]{0,4}){2,7}\]"), "[<ipv6>]"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "<ip>"),
]


# Where machine names appear in reports: the alias in sinful strings, SlotName and
# LastRemoteHost (slot@host, glidein_..@host), and the probes' own "saved_on_host".
HOST_SOURCES = [
    re.compile(r"alias=([A-Za-z0-9][A-Za-z0-9.-]*)"),
    # the last @-part of a slot name. A glidein name (glidein_123_456@host) has underscores, which
    # host names never have, so the lookahead skips it.
    re.compile(r"@([A-Za-z][A-Za-z0-9-]*(?:\.[A-Za-z0-9-]+)*)(?![A-Za-z0-9_@-])"),
    re.compile(r'"saved_on_host": "([^"]+)"'),
]
KEEP_HOST = re.compile(r"^(ap\d+|submit-?\d*)(\.|$)")   # access points are public; keep them


def redact_hosts(text):
    """Replace every execute machine name found in text with <host-N>: the full name and
    its first label (tables often show only that), in order of first appearance."""
    names = []
    for pat in HOST_SOURCES:
        for m in pat.finditer(text):
            full = m.group(1).rstrip(".")
            if len(full) >= 4 and not KEEP_HOST.match(full) and not full.startswith("<"):
                if full not in names:
                    names.append(full)
    labels, numbers = {}, {}   # name -> placeholder; short name -> number
    for full in sorted(names, key=lambda n: text.find(n)):
        short = full.split(".")[0]
        n = numbers.setdefault(short, len(numbers) + 1)
        labels[full] = labels[short] = "<host-%d>" % n
    for name in sorted(labels, key=len, reverse=True):   # longest first: full names before labels
        if len(name) >= 4:
            text = re.sub(r"(?<![A-Za-z0-9-])%s(?![A-Za-z0-9-])" % re.escape(name), labels[name], text)
    return text


def default_user():
    for var in ("PROBE_USER", "USER", "LOGNAME"):
        if os.environ.get(var):
            return os.environ[var]
    try:
        return getpass.getuser()
    except Exception:
        return None


def redact(text, user=None):
    for pat, repl in PATTERNS:
        text = pat.sub(repl, text)
    text = redact_hosts(text)
    user = user if user is not None else default_user()
    if user and len(user) >= 3:
        text = re.sub(r"\b%s\b" % re.escape(user), "<user>", text)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="files or directories (directories: all .md and .json inside)")
    ap.add_argument("--user", default=None, help="name to replace (default: $USER)")
    ap.add_argument("--check", action="store_true", help="only report files that would change")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            for root, _dirs, names in os.walk(p):
                files += [os.path.join(root, n) for n in names if n.endswith((".md", ".json"))]
        else:
            files.append(p)

    changed = 0
    for f in sorted(files):
        with open(f, errors="replace") as fh:
            old = fh.read()
        new = redact(old, args.user)
        if new != old:
            changed += 1
            if args.check:
                print("needs redaction: %s" % f)
            else:
                with open(f, "w") as fh:
                    fh.write(new)
    print("%s %d of %d files" % ("would change" if args.check else "redacted", changed, len(files)))
    sys.exit(1 if (args.check and changed) else 0)


if __name__ == "__main__":
    main()
