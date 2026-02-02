#!/usr/bin/env python3
from __future__ import annotations

import argparse

from path_utils import resolve_codex_state, resolve_state_root


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="List available packet contracts under CODEX_STATE."
    )
    ap.add_argument("--codex-state", help="Override CODEX_STATE root.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    codex_state = resolve_codex_state(args.codex_state)
    state_root = resolve_state_root(str(codex_state))
    packets_root = state_root / "packets"

    if not packets_root.exists():
        print(f"no packets directory: {packets_root}")
        return 1

    contracts = []
    contracts.extend(packets_root.rglob("contract.json"))
    examples = packets_root / "examples"
    if examples.exists():
        contracts.extend(examples.glob("*.json"))

    if not contracts:
        print(f"no contracts found under {packets_root}")
        return 0

    for path in sorted({p.resolve() for p in contracts}):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
