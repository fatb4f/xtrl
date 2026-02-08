#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from path_utils import resolve_contract_path, resolve_repo_root, resolve_state_root


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Resolve evidence path for a packet contract."
    )
    ap.add_argument("contract", help="Path to packet contract JSON.")
    ap.add_argument("--repo-root", help="Target repo root (defaults to git rev-parse).")
    ap.add_argument("--codex-state", help="Override CODEX_STATE root.")
    ap.add_argument("--codex-home", help="Override CODEX_HOME config root.")
    ap.add_argument(
        "--ls", action="store_true", help="List evidence directory contents if present."
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    resolve_state_root(args.codex_state, args.codex_home)
    contract_path = resolve_contract_path(args.contract, repo_root)
    if not contract_path.exists():
        raise SystemExit(f"contract not found: {contract_path}")

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    packet_id = str(contract.get("packet_id") or "")
    if not packet_id:
        raise SystemExit("packet_id missing from contract")
    evidence_cfg = contract.get("evidence") or {}
    out_dir_raw = evidence_cfg.get("out_dir")
    if isinstance(out_dir_raw, str) and out_dir_raw:
        expanded = Path(out_dir_raw).expanduser()
        out_dir = expanded if expanded.is_absolute() else (repo_root / expanded).resolve()
    else:
        out_dir = (repo_root / "out").resolve()
    evidence_path = (Path(out_dir) / packet_id).resolve()

    print(evidence_path)
    if args.ls and evidence_path.exists():
        for entry in sorted(evidence_path.iterdir()):
            print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
