#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from path_utils import resolve_codex_state, resolve_state_root


def sh(argv: List[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
    proc = subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    rc, out, err = sh(["git", "rev-parse", "--show-toplevel"])
    if rc != 0 or not out:
        raise SystemExit(f"repo_root unresolved: {err}")
    return Path(out).resolve()


def current_packet_id() -> str:
    rc, out, _ = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if rc != 0 or not out:
        raise SystemExit("unable to resolve current branch")
    if out.startswith("packet/"):
        return out.split("packet/", 1)[1]
    raise SystemExit("current branch is not packet/<packet_id>")


def find_out_dir(packet_id: str, state_root: Path) -> Path:
    out_root = state_root / "out"
    for candidate in out_root.rglob("packet.json"):
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("packet_id") == packet_id:
            repo = data.get("repo") or "unknown"
            return (out_root / repo / packet_id).resolve()
    raise SystemExit(f"out_dir not found for {packet_id}")


def read_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_trailers(message: str) -> Dict[str, List[str]]:
    trailers: Dict[str, List[str]] = {}
    for line in message.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if not key or not val:
            continue
        trailers.setdefault(key, []).append(val)
    return trailers


def git_log_src(base_ref: str, n: int, root: Path) -> List[Dict[str, str]]:
    fmt = "%H%x1f%h%x1f%an%x1f%ad%x1f%s%x1f%b"
    rc, out, err = sh(["git", "log", base_ref, f"-n", str(n), f"--pretty=format:{fmt}", "--date=iso"], cwd=root)
    if rc != 0:
        raise SystemExit(f"git log failed: {err}")
    entries = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) < 6:
            continue
        sha, short, author, date, subject, body = parts[:6]
        trailers = parse_trailers(body)
        entries.append(
            {
                "sha": sha,
                "short": short,
                "author": author,
                "date": date,
                "subject": subject,
                "trailers": trailers,
            }
        )
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ref", default="HEAD")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--plan-path", default=None)
    args = ap.parse_args()

    root = repo_root()
    packet_id = current_packet_id()

    codex_state = resolve_codex_state(None)
    state_root = resolve_state_root(str(codex_state))
    out_dir = find_out_dir(packet_id, state_root)
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    contract_path = out_dir / "contract.json"
    contract = read_json(contract_path) if contract_path.exists() else {}

    rc, status_out, _ = sh(["git", "status", "--porcelain"], cwd=root)
    clean = rc == 0 and not status_out.strip()

    base_ref = contract.get("base_ref") or args.base_ref
    rc, head_sha, _ = sh(["git", "rev-parse", base_ref], cwd=root)
    if rc != 0:
        head_sha = ""

    repo_key = contract.get("repo") or "unknown"

    allowed_paths = contract.get("allowed_paths") if isinstance(contract.get("allowed_paths"), list) else []
    budgets = contract.get("budgets") if isinstance(contract.get("budgets"), dict) else {}
    actions = []
    run_cfg = contract.get("run") if isinstance(contract.get("run"), dict) else {}
    if run_cfg:
        test_cmd = run_cfg.get("test_cmd")
        if isinstance(test_cmd, list) and test_cmd:
            actions.append("test")
        elif isinstance(test_cmd, str) and test_cmd:
            actions.append("test")
        cmds = run_cfg.get("commands")
        if isinstance(cmds, list):
            actions.extend([f"cmd:{i}" for i in range(len(cmds))])

    state_latest = state_root / "state" / "latest.json"
    ledger_path = state_root / "ledger" / "ledger.jsonl"
    ledger_tail = []
    if ledger_path.exists():
        lines = ledger_path.read_text(encoding="utf-8").splitlines()
        ledger_tail = lines[-args.n :]

    decision_digest = None
    evidence_json = out_dir / "evidence.json"
    if evidence_json.exists():
        try:
            ev = read_json(evidence_json)
            decision_digest = {
                "decision": ev.get("decision"),
                "reason_codes": ev.get("reasons") if isinstance(ev.get("reasons"), list) else [],
            }
        except Exception:
            decision_digest = None

    payload = {
        "schema_version": "xtrl.state_space/v0.1",
        "generated_at_utc": utc_now(),
        "repo": {
            "repo_key": repo_key,
            "repo_root": str(root),
            "base_ref": base_ref,
            "head_sha": head_sha,
            "clean": bool(clean),
        },
        "contract": {
            "allowed_paths": allowed_paths,
            "budgets": budgets,
            "actions": actions,
        },
        "latest": {
            "state_latest_path": str(state_latest),
            "ledger_tail": ledger_tail,
        },
    }
    if decision_digest:
        payload["decision_digest"] = decision_digest
    if args.plan_path:
        payload["plan_path"] = args.plan_path

    # Markdown
    lines = [
        f"# State Space — {packet_id}",
        "",
        f"- Generated: `{payload['generated_at_utc']}`",
        f"- Repo key: `{repo_key}`",
        f"- Repo root: `{root}`",
        f"- Base ref: `{base_ref}`",
        f"- Head SHA: `{head_sha}`",
        f"- Clean: `{clean}`",
        "",
        "## Contract summary",
        f"- Allowed paths: {len(allowed_paths)}",
        f"- Budgets: {budgets}",
        f"- Actions: {actions}",
        "",
        "## Latest pointers",
        f"- state/latest.json: `{state_latest}`",
        f"- ledger.jsonl (tail): {len(ledger_tail)} lines",
    ]
    if decision_digest:
        lines += [
            "",
            "## Decision digest",
            f"- Decision: `{decision_digest.get('decision')}`",
            f"- Reason codes: {decision_digest.get('reason_codes')}",
        ]
    if args.plan_path:
        lines += ["", "## Plan pointer", f"- Plan: `{args.plan_path}`"]

    (evidence_dir / "state_space.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evidence_dir / "state_space.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
