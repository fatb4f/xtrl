#!/usr/bin/env python3
"""Minimal release tagging CLI (dry-run)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def tag_from_main() -> int:
    out = Path("/tmp/release_tag.txt")
    out.write_text(f"tag=dry-run-{utc_now()}\n", encoding="utf-8")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    tag = sub.add_parser("tag")
    tag.add_argument("--from-main", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.cmd == "tag" and args.from_main:
        return tag_from_main()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
