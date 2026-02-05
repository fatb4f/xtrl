#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from verify_utils import current_packet_id, find_out_dir, resolve_state


def main() -> int:
    state_root = resolve_state()
    packet_id = current_packet_id(Path(".").resolve())
    out_dir = find_out_dir(packet_id, state_root)
    if not out_dir:
        raise SystemExit("out_dir not found for packet")

    index_path = state_root / "visibility" / "index.json"
    if not index_path.exists():
        raise SystemExit("visibility index missing")
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        raise SystemExit("visibility index invalid")

    entry = next((it for it in items if isinstance(it, dict) and it.get("packet_id") == packet_id), None)
    if not entry:
        raise SystemExit("visibility index entry missing")

    link_path = out_dir / "link.json"
    if not link_path.exists():
        raise SystemExit("link.json missing")
    link = json.loads(link_path.read_text(encoding="utf-8"))

    if link.get("packet_id") != packet_id:
        raise SystemExit("link.json packet_id mismatch")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
