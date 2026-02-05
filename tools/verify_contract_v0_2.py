#!/usr/bin/env python3
from __future__ import annotations

import json
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

    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "contract.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = schema.get("required") or []

    missing = [k for k in required if k not in contract]
    if missing:
        raise SystemExit(f"missing required keys: {missing}")

    if not isinstance(contract.get("network_policy"), dict):
        raise SystemExit("network_policy must be object")
    if not isinstance(contract.get("allowed_paths"), list) or not contract.get("allowed_paths"):
        raise SystemExit("allowed_paths must be non-empty list")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
