#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo_root = Path(".").resolve()
    helpers_dir = repo_root / "tools" / "helpers"
    helpers_dir.mkdir(parents=True, exist_ok=True)
    target = helpers_dir / "helper_created_stub.py"
    if not target.exists():
        target.write_text("# helper_created_stub\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
