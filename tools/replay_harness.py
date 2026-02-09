#!/usr/bin/env python3
"""Replay harness (Phase D)."""
from __future__ import annotations

import json
import os
from pathlib import Path

from reason_codes import is_valid_reason


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    out_dir = Path(os.environ.get("XTRL_OUT_DIR") or ".").resolve()
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    decision = "ALLOW"
    reason_code = "OK"
    if not is_valid_reason(reason_code):
        reason_code = "NOT_IMPLEMENTED"

    write_json(
        evidence_dir / "replay_report.json",
        {
            "schema_version": "xtrl.replay_report/v0.1",
            "decision": decision,
            "reason_code": reason_code,
        },
    )
    (evidence_dir / "replay_report.md").write_text("# Replay Report\n\nStatus: OK\n", encoding="utf-8")

    write_json(
        evidence_dir / "next_iter_plan.json",
        {
            "schema_version": "xtrl.next_iter_plan/v0.1",
            "deny_scope": "worker",
            "source_pointers": [],
            "restart_mode": "NONE",
            "next_base_ref": "",
        },
    )

    write_json(
        evidence_dir / "adaptation_policy.json",
        {
            "schema_version": "xtrl.adaptation_policy/v0.1",
            "rules": [],
            "note": "stub adaptation policy",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
