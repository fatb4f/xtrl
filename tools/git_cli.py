#!/usr/bin/env python3
"""Minimal git plant harness CLI."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dry_run(out_dir: Path) -> int:
    payload = {
        "generated_at": utc_now(),
        "dry_run": True,
        "gates": [],
    }
    write_json(out_dir / "gates.json", payload)
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    dr = sub.add_parser("dry-run")
    dr.add_argument("--out", required=True)
    args = ap.parse_args(argv[1:])

    if args.cmd == "dry-run":
        return dry_run(Path(args.out))
    return 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
