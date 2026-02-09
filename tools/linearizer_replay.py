#!/usr/bin/env python3
"""Linearizer replay report (Phase C)."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import List, Tuple

from reason_codes import is_valid_reason


def sh(argv: List[str], cwd: Path | None = None) -> Tuple[int, str, str]:
    proc = subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    out_dir = Path(os.environ.get("XTRL_OUT_DIR") or ".").resolve()
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    meta_path = out_dir / "raw" / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    base_ref = meta.get("base_ref") or ""
    base_sha = meta.get("base_sha") or ""
    worktree_path = Path(meta.get("worktree_path") or ".").resolve()

    head_sha_before = ""
    rc, out, _ = sh(["git", "rev-parse", "HEAD"], cwd=worktree_path)
    if rc == 0:
        head_sha_before = out

    candidate_index = {
        "base_ref": base_ref,
        "base_sha": base_sha,
        "head_sha_before": head_sha_before,
        "considered": [],
        "stale_filtered": [],
    }
    write_json(evidence_dir / "candidate_index.json", candidate_index)

    promotion_lock = {
        "lock_acquired": False,
        "head_before": head_sha_before,
        "head_after": head_sha_before,
    }
    write_json(evidence_dir / "promotion_lock.json", promotion_lock)

    decision = "ALLOW"
    reason_code = "OK"
    if not is_valid_reason(reason_code):
        reason_code = "NOT_IMPLEMENTED"
    report = {
        "schema_version": "xtrl.replay_report/v0.1",
        "decision": decision,
        "reason_code": reason_code,
        "note": "linearizer replay stub (no candidates)",
    }
    write_json(evidence_dir / "replay_report.json", report)
    (evidence_dir / "replay_report.md").write_text("# Replay Report\n\nStatus: OK\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
