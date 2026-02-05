#!/usr/bin/env python3
"""Emit and check a minimal EvidenceCapsule for a packet."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from path_utils import resolve_codex_state, resolve_state_root


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_out_dir(state_root: Path, packet_id: str) -> Path:
    out_root = state_root / "out"
    for candidate in out_root.rglob("packet.json"):
        try:
            data = read_json(candidate)
        except Exception:
            continue
        if data.get("packet_id") == packet_id:
            return candidate.parent
    return out_root / "unknown" / packet_id


def emit(packet_id: str, state_root: Path) -> int:
    out_dir = find_out_dir(state_root, packet_id)
    evidence_path = out_dir / "evidence.json"
    refs: List[Dict[str, Any]] = []
    if evidence_path.exists():
        refs.append({"path": str(evidence_path), "sha256": sha256_file(evidence_path), "role": "packet_evidence"})
    manifest = out_dir / "manifest.json"
    if manifest.exists():
        refs.append({"path": str(manifest), "sha256": sha256_file(manifest), "role": "packet_manifest"})

    capsule = {
        "schema_version": "xtrl.evidence_capsule/v0.1",
        "packet_id": packet_id,
        "generated_at": utc_now(),
        "evidence_refs": refs,
    }
    write_json(out_dir / "evidence_capsule.json", capsule)
    return 0


def check(packet_id: str, state_root: Path) -> int:
    out_dir = find_out_dir(state_root, packet_id)
    capsule_path = out_dir / "evidence_capsule.json"
    if not capsule_path.exists():
        raise SystemExit("missing evidence_capsule.json")
    data = read_json(capsule_path)
    if data.get("packet_id") != packet_id:
        raise SystemExit("packet_id mismatch")
    if not isinstance(data.get("evidence_refs"), list):
        raise SystemExit("evidence_refs missing")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ev = sub.add_parser("emit")
    ev.add_argument("--packet-id", required=True)
    ck = sub.add_parser("check")
    ck.add_argument("--packet-id", required=True)
    args = ap.parse_args(argv[1:])

    codex_state = resolve_codex_state(None)
    state_root = resolve_state_root(str(codex_state))

    if args.cmd == "emit":
        return emit(args.packet_id, state_root)
    if args.cmd == "check":
        return check(args.packet_id, state_root)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
