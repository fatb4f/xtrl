#!/usr/bin/env python3
"""Verify regenerated files match repository state.

Usage:
  python tools/ci_regen_compare.py --paths <path> [<path> ...]

Checks:
- All paths exist
- `git diff -- <paths>` is clean

Exit codes:
- 0: clean
- 2: differences or missing files
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def run(cmd: List[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="+", required=True)
    args = ap.parse_args(argv[1:])

    paths = [Path(p) for p in args.paths]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        print("missing paths:\n" + "\n".join(missing), file=sys.stderr)
        return 2

    proc = run(["git", "diff", "--"] + [str(p) for p in paths])
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        return 2
    if proc.stdout.strip():
        print(proc.stdout, end="", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
