#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo_root = Path(".").resolve()
    skills_dir = repo_root / "skills"
    skills_pack = repo_root / "skills-pack"

    if not skills_dir.exists() or not skills_pack.exists():
        raise SystemExit("skills or skills-pack directory missing")

    # Accept either top-level symlink or compat symlinks inside skills/
    if skills_dir.is_symlink():
        target = skills_dir.resolve()
        if target != skills_pack.resolve():
            raise SystemExit("skills symlink does not target skills-pack")
        return 0

    expected = {
        "packet-runner": "xtrl.packet-runner",
        "packet-template": "xtrl.packet-template",
    }
    for name, target in expected.items():
        link = skills_dir / name
        if not link.is_symlink():
            raise SystemExit(f"missing symlink: {link}")
        if link.resolve() != (skills_pack / target).resolve():
            raise SystemExit(f"symlink target mismatch: {link}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
