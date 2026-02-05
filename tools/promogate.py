#!/usr/bin/env python3
"""PromoGate evaluator (deny-fast) + GateDecision emission."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

REQUIRED_FIELDS = [
    "schema_version",
    "packet_id",
    "repo",
    "base_ref",
    "mode",
    "budgets",
    "constraints",
    "actions",
    "evidence",
]

REQUIRED_CONSTRAINT_FIELDS = [
    "clean_repo_required",
    "deny_repo_local_roots",
    "allowed_paths",
    "forbidden_paths",
    "forbidden_patterns",
]


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


def promo_gate(pre_contract: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    reasons: List[str] = []
    errors: List[str] = []

    for field in REQUIRED_FIELDS:
        if field not in pre_contract:
            errors.append(f"missing_field:{field}")

    if errors:
        return False, ["PRECONTRACT_MISSING_FIELDS"], errors

    mode = pre_contract.get("mode")
    if mode not in {"NORMAL", "REPAIR", "SAFE"}:
        reasons.append("MODE_INVALID")

    budgets = pre_contract.get("budgets") or {}
    if "diff_budget" not in budgets or "time_minutes" not in budgets or "iteration_budget" not in budgets:
        reasons.append("BUDGETS_INVALID")

    constraints = pre_contract.get("constraints") or {}
    for field in REQUIRED_CONSTRAINT_FIELDS:
        if field not in constraints:
            reasons.append("CONSTRAINTS_INVALID")
            break

    deny_roots = constraints.get("deny_repo_local_roots")
    if deny_roots != [".codex", ".quint"]:
        reasons.append("DENY_ROOTS_INVALID")

    allowed_paths = constraints.get("allowed_paths")
    if not isinstance(allowed_paths, list) or not allowed_paths:
        reasons.append("ALLOWED_PATHS_EMPTY")

    diff_budget = budgets.get("diff_budget") if isinstance(budgets, dict) else None
    if not isinstance(diff_budget, dict) or not all(k in diff_budget for k in ("max_files_changed", "max_lines_changed")):
        reasons.append("DIFF_BUDGET_INVALID")

    actions = pre_contract.get("actions") or {}
    if not isinstance(actions, dict) or not actions:
        reasons.append("ACTIONS_MISSING")
    else:
        for name, argv in actions.items():
            if not isinstance(argv, list) or not argv or any(not isinstance(x, str) for x in argv):
                reasons.append("ACTIONS_INVALID")
                break

    evidence = pre_contract.get("evidence") or {}
    req_files = evidence.get("required_files") if isinstance(evidence, dict) else None
    if not isinstance(req_files, list) or not req_files:
        reasons.append("EVIDENCE_REQUIRED_FILES_MISSING")

    base_ref = pre_contract.get("base_ref")
    if not isinstance(base_ref, str) or not base_ref.strip():
        reasons.append("BASE_REF_MISSING")

    return len(reasons) == 0, reasons, errors


def eval_cmd(pre_contract_path: Path, out_dir: Path) -> int:
    pre = read_json(pre_contract_path)
    allow, reasons, errors = promo_gate(pre)
    decision = "ALLOW" if allow else "DENY"

    payload = {
        "gate": "promogate",
        "decision": decision,
        "reasons": reasons,
        "errors": errors,
        "packet_id": pre.get("packet_id"),
        "schema_version": pre.get("schema_version"),
        "pre_contract_path": str(pre_contract_path),
        "pre_contract_sha256": sha256_file(pre_contract_path),
        "timestamp_utc": utc_now(),
    }
    write_json(out_dir / "gate_decision.json", payload)
    return 0 if decision == "ALLOW" else 2


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ev = sub.add_parser("eval")
    ev.add_argument("--pre-contract", required=True)
    ev.add_argument("--out", required=True)
    args = ap.parse_args(argv[1:])

    if args.cmd == "eval":
        return eval_cmd(Path(args.pre_contract), Path(args.out))
    return 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
