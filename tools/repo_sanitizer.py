#!/usr/bin/env python3
"""Repo-local cleanup tool for transient artifacts.

Defaults to dry-run. Use --apply to delete.
Scopes:
- repo root
- worktree root (defaults to <repo_root>/worktrees)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

from path_utils import resolve_repo_root


def iter_paths(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if ".git" in p.parts:
            continue
        yield p


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def collect_cleanup_targets(root: Path) -> List[Path]:
    targets: List[Path] = []
    for p in iter_paths(root):
        name = p.name
        if p.is_dir() and name == "__pycache__":
            targets.append(p)
        elif p.is_file() and name.endswith(".pyc"):
            targets.append(p)
    return targets


def cleanup_paths(paths: List[Path], apply: bool) -> Tuple[int, int]:
    deleted = 0
    skipped = 0
    for p in paths:
        if not apply:
            print(f"DRY-RUN: {p}")
            continue
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            deleted += 1
        except Exception:
            skipped += 1
    return deleted, skipped


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Clean transient artifacts in repo/worktrees.")
    ap.add_argument("--repo-root", default=None, help="Repo root (defaults to git rev-parse).")
    ap.add_argument(
        "--worktree-root",
        default=None,
        help="Worktree root (defaults to <repo_root>/worktrees).",
    )
    ap.add_argument("--apply", action="store_true", help="Apply deletions (default: dry-run).")
    args = ap.parse_args(argv[1:])

    repo_root = resolve_repo_root(args.repo_root)
    worktree_root = Path(args.worktree_root).resolve() if args.worktree_root else (repo_root / "worktrees")

    targets: List[Path] = []
    targets.extend(collect_cleanup_targets(repo_root))
    if worktree_root.exists() and is_under(worktree_root, repo_root):
        targets.extend(collect_cleanup_targets(worktree_root))

    # Deduplicate + keep only paths under repo/worktree roots
    allowed_roots = [repo_root.resolve(), worktree_root.resolve()]
    unique: List[Path] = []
    seen = set()
    for p in targets:
        rp = p.resolve()
        if rp in seen:
            continue
        if any(is_under(rp, r) for r in allowed_roots):
            unique.append(p)
            seen.add(rp)

    deleted, skipped = cleanup_paths(unique, args.apply)
    if not args.apply:
        print(f"Dry-run complete. Candidates: {len(unique)}")
    else:
        print(f"Deleted: {deleted}, Skipped: {skipped}, Total: {len(unique)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
