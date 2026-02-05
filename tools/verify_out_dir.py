#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from verify_utils import current_packet_id, find_out_dir, legacy_out_dir, read_json, resolve_state


def migrate_legacy(packet_id: str, state_root: Path) -> Path | None:
    legacy = legacy_out_dir(packet_id, state_root)
    if not legacy.exists():
        return None
    packet_json = legacy / "packet.json"
    if not packet_json.exists():
        return None
    try:
        data = read_json(packet_json)
    except Exception:
        return None
    repo = data.get("repo") or "unknown"
    if repo == "unknown":
        return None
    namespaced = (state_root / "out" / repo / packet_id).resolve()
    if not namespaced.exists():
        namespaced.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(legacy), str(namespaced))
    return namespaced


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="namespaced")
    args = ap.parse_args()

    state_root = resolve_state()
    repo_root = Path(".").resolve()
    packet_id = current_packet_id(repo_root)

    out_dir = find_out_dir(packet_id, state_root)
    if out_dir and out_dir.exists():
        return 0

    migrated = migrate_legacy(packet_id, state_root)
    if migrated and migrated.exists():
        return 0

    raise SystemExit("namespaced out_dir missing")


if __name__ == "__main__":
    raise SystemExit(main())
