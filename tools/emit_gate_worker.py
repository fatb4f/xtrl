#!/usr/bin/env python3
"""Gate worker artifact emitter (Phase B)."""
from __future__ import annotations

import fnmatch
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

from reason_codes import is_valid_reason, REASON_CODES_SET


def sh(argv: List[str], cwd: Path | None = None) -> Tuple[int, str, str]:
    proc = subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    out_dir = Path(os.environ.get("XTRL_OUT_DIR") or ".").resolve()
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    meta_path = out_dir / "raw" / "meta.json"
    meta = read_json(meta_path) if meta_path.exists() else {}
    base_sha = meta.get("base_sha") or ""
    repo_root = Path(meta.get("repo_root") or ".").resolve()
    worktree_path = Path(meta.get("worktree_path") or repo_root).resolve()

    contract_path = out_dir / "contract.json"
    contract = read_json(contract_path) if contract_path.exists() else {}
    budgets = contract.get("budgets") or {}
    max_files = int(budgets.get("max_changed_files", 0) or 0)
    max_lines = int(budgets.get("max_changed_lines", 0) or 0)
    forbidden = contract.get("forbidden_outputs") or []

    # Diff metrics
    files_changed = 0
    lines_added = 0
    lines_deleted = 0
    name_only: List[str] = []
    if base_sha:
        rc, out, _ = sh(["git", "diff", "--name-only", f"{base_sha}..HEAD"], cwd=worktree_path)
        if rc == 0 and out:
            name_only = [ln.strip() for ln in out.splitlines() if ln.strip()]
        rc, out, _ = sh(["git", "diff", "--numstat", f"{base_sha}..HEAD"], cwd=worktree_path)
        if rc == 0 and out:
            for ln in out.splitlines():
                parts = ln.split("\t")
                if len(parts) < 2:
                    continue
                a, d = parts[0], parts[1]
                if a.isdigit():
                    lines_added += int(a)
                if d.isdigit():
                    lines_deleted += int(d)
                files_changed += 1

    forbidden_hits: List[str] = []
    if forbidden and name_only:
        for path in name_only:
            if any(fnmatch.fnmatch(path, pat) for pat in forbidden):
                forbidden_hits.append(path)

    decision = "ALLOW"
    reason_code = "OK"
    if forbidden_hits:
        decision = "DENY"
        reason_code = "FORBIDDEN_PATH_TOUCHED"
    elif max_files and files_changed > max_files:
        decision = "DENY"
        reason_code = "DIFF_BUDGET_EXCEEDED"
    elif max_lines and (lines_added + lines_deleted) > max_lines:
        decision = "DENY"
        reason_code = "DIFF_BUDGET_EXCEEDED"

    if not is_valid_reason(reason_code):
        reason_code = "NOT_IMPLEMENTED"

    payload = {
        "schema_version": "xtrl.gate_worker/v0.1",
        "decision": decision,
        "reason_code": reason_code,
        "facts": {
            "base_sha": base_sha,
            "files_changed": files_changed,
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "forbidden_hits": forbidden_hits,
            "max_files": max_files,
            "max_lines": max_lines,
            "reason_code_enum": sorted(REASON_CODES_SET),
        },
    }

    write_json(evidence_dir / "gate_worker.json", payload)
    # Transcript hygiene placeholders (stdout/stderr separated)
    (evidence_dir / "stdout.txt").write_text("", encoding="utf-8")
    (evidence_dir / "stderr.txt").write_text("", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
