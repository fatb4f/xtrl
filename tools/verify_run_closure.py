#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from verify_utils import resolve_repo


REQUIRED = [
    "contract.json",
    "packet.json",
    "evidence/plan.md",
    "evidence/decision.md",
    "evidence/scope.json",
    "evidence/integrity.json",
    "evidence/tests.junit.xml",
    "evidence/regression.md",
    "commands.log",
    "summary.md",
]


def find_latest_out_dir(repo_root: Path) -> Path | None:
    out_root = repo_root / "out"
    candidates = []
    for evidence in out_root.rglob("evidence.json"):
        try:
            candidates.append((evidence.stat().st_mtime, evidence.parent))
        except Exception:
            continue
    if not candidates:
        return None
    return sorted(candidates, key=lambda x: x[0], reverse=True)[0][1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--packet-id", default=None)
    args = ap.parse_args()

    repo_root = resolve_repo()
    out_dir: Path | None = None
    if args.latest:
        out_dir = find_latest_out_dir(repo_root)
    if args.packet_id and not out_dir:
        for candidate in (repo_root / "out").rglob(args.packet_id):
            if candidate.is_dir():
                out_dir = candidate
                break
    if not out_dir:
        raise SystemExit("no run found")

    missing = [rel for rel in REQUIRED if not (out_dir / rel).exists()]
    exec_ok = (out_dir / "exec-prompt.md").exists() or (out_dir / "EXEC_PROMPT.md").exists()
    if not exec_ok:
        missing.append("exec-prompt.md (or EXEC_PROMPT.md)")
    if missing:
        raise SystemExit(f"missing closure files: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
