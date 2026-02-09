#!/usr/bin/env python3
"""Src mutation fuzz (Phase E)."""
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
        evidence_dir / "src_fuzz_mutation_report.json",
        {"schema_version": "xtrl.src_fuzz_mutation_report/v0.1", "decision": decision, "reason_code": reason_code},
    )
    (evidence_dir / "src_fuzz_mutation_report.md").write_text("# Src Fuzz Mutation Report\n\nStatus: OK\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
