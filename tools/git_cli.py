#!/usr/bin/env python3
"""Minimal git plant harness CLI."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)


def dry_run(out_dir: Path) -> int:
    payload = {
        "generated_at": utc_now(),
        "dry_run": True,
        "gates": [],
    }
    write_json(out_dir / "gates.json", payload)
    return 0


def doctor() -> int:
    proc = run(["git", "status", "--porcelain"])
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=__import__("sys").stderr)
        return 2
    return 0


def wt_create(packet_id: str) -> int:
    proc = run(["git", "rev-parse", "--show-toplevel"])
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=__import__("sys").stderr)
        return 2
    repo_root = Path(proc.stdout.strip())
    state_root = Path.home() / ".local" / "state" / "codex" / "xtrl"
    wt_root = state_root / "worktrees"
    wt_path = wt_root / f"{packet_id}-wt"
    if wt_path.exists():
        return 0
    wt_root.mkdir(parents=True, exist_ok=True)
    branch = f"packet/{packet_id}-wt"
    proc = run(["git", "worktree", "add", "-b", branch, str(wt_path), "main"], cwd=repo_root)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=__import__("sys").stderr)
        return 2
    return 0


def wt_status(packet_id: str) -> int:
    proc = run(["git", "worktree", "list", "--porcelain"])
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=__import__("sys").stderr)
        return 2
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    dr = sub.add_parser("dry-run")
    dr.add_argument("--out", required=True)
    sub.add_parser("doctor")
    wt = sub.add_parser("wt")
    wt_sub = wt.add_subparsers(dest="wt_cmd", required=True)
    wt_create_p = wt_sub.add_parser("create")
    wt_create_p.add_argument("--packet-id", required=True)
    wt_status_p = wt_sub.add_parser("status")
    wt_status_p.add_argument("--packet-id", required=True)
    args = ap.parse_args(argv[1:])

    if args.cmd == "dry-run":
        return dry_run(Path(args.out))
    if args.cmd == "doctor":
        return doctor()
    if args.cmd == "wt":
        if args.wt_cmd == "create":
            return wt_create(args.packet_id)
        if args.wt_cmd == "status":
            return wt_status(args.packet_id)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
