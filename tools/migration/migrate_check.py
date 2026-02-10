#!/usr/bin/env python
import pathlib
import subprocess
from datetime import date, datetime, timedelta

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

REQUIRED = [
    REPO_ROOT / "docs/migration/README.md",
    REPO_ROOT / "docs/migration/TRACKER.md",
    REPO_ROOT / "docs/migration/WORKPLAN.md",
    REPO_ROOT / "docs/migration/STATUS.md",
]


def fail(msg: str) -> int:
    print(f"migrate-check: {msg}")
    return 1


def file_contains(path: pathlib.Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")

def require_headings(path: pathlib.Path, headings: list[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    return all(h in text for h in headings)

def parse_status_date(path: pathlib.Path) -> date | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Last updated:"):
            value = line.split(":", 1)[1].strip()
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return None
    return None


def main() -> int:
    for path in REQUIRED:
        if not path.exists():
            return fail(f"missing required file: {path}")

    workplan = REPO_ROOT / "docs/migration/WORKPLAN.md"
    tracker = REPO_ROOT / "docs/migration/TRACKER.md"
    status = REPO_ROOT / "docs/migration/STATUS.md"

    if not file_contains(workplan, "TRACKER.md"):
        return fail("WORKPLAN.md must reference TRACKER.md")
    if not require_headings(workplan, ["Milestone 0", "Milestone 1"]):
        return fail("WORKPLAN.md must include Milestone sections")

    if not require_headings(tracker, ["Work Items", "Work Item Details", "Operational Gates"]):
        return fail("TRACKER.md missing required headings")
    if not file_contains(tracker, "M1-T01"):
        return fail("TRACKER.md must include tracker IDs (e.g., M1-T01)")

    if not require_headings(status, ["Current phase:", "Last updated:", "Next 3 actions:", "Blockers:"]):
        return fail("STATUS.md must include required dashboard fields")
    status_date = parse_status_date(status)
    if status_date is None:
        return fail("STATUS.md must include Last updated: YYYY-MM-DD")
    if date.today() - status_date > timedelta(days=7):
        return fail("STATUS.md is stale (older than 7 days)")

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
