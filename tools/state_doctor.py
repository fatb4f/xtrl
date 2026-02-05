#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from path_utils import resolve_codex_state, resolve_state_root


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--codex-state", default=None)
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()

    codex_state = resolve_codex_state(args.codex_state)
    state_root = resolve_state_root(str(codex_state))

    required = ["sessions", "history", "tmp", "logs", "cache", "worktrees", "out"]
    results = []
    for name in required:
        path = state_root / name
        existed = path.exists()
        path.mkdir(parents=True, exist_ok=True)
        results.append((name, path, existed))

    if args.print:
        for name, path, existed in results:
            status = "exists" if existed else "created"
            print(f"{name}={path} ({status})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
