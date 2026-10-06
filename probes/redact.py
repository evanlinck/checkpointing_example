#!/usr/bin/env python3
"""
redact.py - remove personal details from probe reports before sharing them.

Replaces:
  - the submitting user's name (from --user, $USER, or the login name)
  - /home/<name> and /staging/<x>/<name> or /staging/<name> paths
  - osdf:///chtc/staging/... paths
  - IPv4 and IPv6 addresses (event-log "Job executing on host: <...>" lines)

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
