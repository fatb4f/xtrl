#!/usr/bin/env python3
"""Stub linearizer replay (Phase C)."""
from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    out_dir = Path(os.environ.get("XTRL_OUT_DIR") or ".").resolve()
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "candidate_index.json").write_text(
        json.dumps({"considered": [], "stale_filtered": [], "base_ref": "", "base_sha": "", "head_sha_before": ""}, indent=2, sort_keys=True) + "\n"
    )
    (evidence_dir / "promotion_lock.json").write_text(
        json.dumps({"lock": "NOT_IMPLEMENTED", "head_before": "", "head_after": ""}, indent=2, sort_keys=True) + "\n"
    )
    report = {
        "schema_version": "xtrl.replay_report/v0.1",
        "decision": "ALLOW",
        "reason_code": "NOT_IMPLEMENTED",
        "note": "stub linearizer replay",
    }
    (evidence_dir / "replay_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    (evidence_dir / "replay_report.md").write_text("# Replay Report\n\nStatus: NOT_IMPLEMENTED\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
