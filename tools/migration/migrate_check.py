#!/usr/bin/env python
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

REQUIRED = [
    REPO_ROOT / "docs/migration/TRACKER.md",
    REPO_ROOT / "docs/migration/WORKPLAN.md",
    REPO_ROOT / "docs/migration/STATUS.md",
]


def fail(msg: str) -> int:
    print(f"migrate-check: {msg}")
    return 1


def file_contains(path: pathlib.Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")


def main() -> int:
    for path in REQUIRED:
        if not path.exists():
            return fail(f"missing required file: {path}")

    workplan = REPO_ROOT / "docs/migration/WORKPLAN.md"
    if not file_contains(workplan, "TRACKER.md"):
        return fail("WORKPLAN.md must reference TRACKER.md")

    # If last commit touched migration docs/tools, require STATUS.md change in that commit.
    try:
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1"], cwd=REPO_ROOT
        ).decode("utf-8").splitlines()
    except Exception:
        changed = []

    touched_migration = any(
        p.startswith("docs/migration/") or p.startswith("tools/migration/")
        for p in changed
    )
    if touched_migration and "docs/migration/STATUS.md" not in changed:
        return fail("STATUS.md must be updated when migration docs/tools change")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
