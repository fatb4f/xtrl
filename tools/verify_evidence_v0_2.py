#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from verify_utils import current_packet_id, find_out_dir, read_json, resolve_state


def main() -> int:
    state_root = resolve_state()
    packet_id = current_packet_id(Path(".").resolve())
    out_dir = find_out_dir(packet_id, state_root)
    if not out_dir:
        raise SystemExit("out_dir not found for packet")

    contract_path = out_dir / "contract.json"
    if not contract_path.exists():
        raise SystemExit("contract.json missing")
    contract = read_json(contract_path)

    required = contract.get("evidence_required") or []
    if not isinstance(required, list) or not required:
        required = [
            "evidence/plan.md",
            "evidence/decision.md",
            "evidence/scope.json",
            "evidence/integrity.json",
            "evidence/tests.junit.xml",
            "evidence/regression.md",
            "commands.log",
            "summary.md",
        ]

    missing = [rel for rel in required if not (out_dir / rel).exists()]
    if missing:
        raise SystemExit(f"missing evidence files: {missing}")

    evidence_path = out_dir / "evidence.json"
    if not evidence_path.exists():
        raise SystemExit("evidence.json missing")
    evidence = read_json(evidence_path)
    if evidence.get("schema_version") != "xtrl.evidence/v0.2":
        raise SystemExit("evidence.json schema_version not v0.2")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
