#!/usr/bin/env python3
"""Stub gate_worker emitter (Phase B)."""
from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    out_dir = Path(os.environ.get("XTRL_OUT_DIR") or ".").resolve()
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "xtrl.gate_worker/v0.1",
        "decision": "ALLOW",
        "reason_code": "NOT_IMPLEMENTED",
        "facts": {"note": "stub gate_worker emitter"},
    }
    (evidence_dir / "gate_worker.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (evidence_dir / "stdout.txt").write_text("", encoding="utf-8")
    (evidence_dir / "stderr.txt").write_text("", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
