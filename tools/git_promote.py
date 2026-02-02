#!/usr/bin/env python3
"""Git promotion harness (minimal)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from path_utils import resolve_codex_state, resolve_repo_root, resolve_state_root
from subprocess import run


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_cmd(argv: List[str], cwd: Path | None = None) -> str:
    proc = run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if proc.returncode != 0:
        return ""
    return proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet_id")
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--codex-state", default=None)
    args = ap.parse_args()

    repo_root = resolve_repo_root(args.repo_root)
    codex_state = resolve_codex_state(args.codex_state)
    state_root = resolve_state_root(str(codex_state))

    packet_id = args.packet_id
    packet_path = None
    for candidate in (state_root / "out").rglob("packet.json"):
        try:
            data = read_json(candidate)
        except Exception:
            continue
        if data.get("packet_id") == packet_id:
            packet_path = candidate
            packet_meta = data
            break
    if not packet_path:
        raise SystemExit(f"packet.json not found for {packet_id}")

    repo = packet_meta.get("repo") or "unknown"
    out_dir = state_root / "out" / repo / packet_id
    contract = read_json(out_dir / "contract.json")
    base_ref = contract.get("base_ref")
    if not base_ref:
        raise SystemExit("base_ref missing from contract")

    # ensure clean
    status = run_cmd(["git", "status", "--porcelain"], cwd=repo_root)
    if status.strip():
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["DIRTY_REPO_DENIED"],
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        return 2

    # binary diff detection
    numstat = run_cmd(["git", "diff", "--numstat", f"{base_ref}..HEAD"], cwd=repo_root)
    binary = any(line.split("\t")[0] == "-" or line.split("\t")[1] == "-" for line in numstat.splitlines() if line)
    if binary:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["BINARY_DIFF_DENIED"],
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        return 2

    # submodule detection
    raw = run_cmd(["git", "diff", "--raw", f"{base_ref}..HEAD"], cwd=repo_root)
    if "160000" in raw:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["SUBMODULE_DENIED"],
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        return 2

    patch = run_cmd(["git", "diff", "--binary", f"{base_ref}..HEAD"], cwd=repo_root)
    diffstat = run_cmd(["git", "diff", "--stat", f"{base_ref}..HEAD"], cwd=repo_root)

    write_text(out_dir / "git" / "patch.diff", patch)
    write_text(out_dir / "git" / "diffstat.txt", diffstat)

    promotion = {
        "timestamp": utc_now(),
        "packet_id": packet_id,
        "status": "BLOCKED",
        "reason_codes": ["PROMOTE_NOT_IMPLEMENTED"],
        "note": "Promotion DAG not yet implemented; patch captured for review.",
    }
    write_json(out_dir / "git" / "promotion.json", promotion)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
