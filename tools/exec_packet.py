#!/usr/bin/env python3
"""ACTION-only packet executor against OUT_DIR/contract.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from path_utils import resolve_codex_state, resolve_repo_root, resolve_state_root


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(argv: List[str], cwd: Path | None = None) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError as exc:
        return 127, "", f"{exc}"


def ensure_required_files(out_dir: Path, required: List[str]) -> None:
    for rel in required:
        path = out_dir / rel
        if path.exists():
            continue
        if path.suffix in {".json"}:
            write_json(path, {})
        elif path.suffix in {".md", ".txt", ".log", ".xml"}:
            write_text(path, "")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet_id")
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--codex-state", default=None)
    ap.add_argument(
        "--action", default=None, help="Run a single action from contract actions."
    )
    args = ap.parse_args()

    repo_root = resolve_repo_root(args.repo_root)
    codex_state = resolve_codex_state(args.codex_state)
    state_root = resolve_state_root(str(codex_state))

    packet_id = args.packet_id
    # packet.json carries repo key
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
    contract_path = out_dir / "contract.json"
    contract = read_json(contract_path)

    actions = contract.get("actions") or {}
    if not isinstance(actions, dict) or not actions:
        raise SystemExit("contract actions missing or invalid")

    action_names = [args.action] if args.action else list(actions.keys())
    commands_log = out_dir / "commands.log"
    commands_log.parent.mkdir(parents=True, exist_ok=True)

    checks = []
    reason_codes: List[str] = []
    all_ok = True

    with commands_log.open("a", encoding="utf-8") as handle:
        for name in action_names:
            argv = actions.get(name)
            if not isinstance(argv, list) or any(not isinstance(x, str) for x in argv):
                raise SystemExit(f"action {name} is not argv array")
            handle.write(f"[{utc_now()}] {name}: {argv}\n")
            rc, out, err = run_cmd(argv, cwd=repo_root)
            handle.write(f"rc={rc}\n")
            if out:
                handle.write(out)
                if not out.endswith("\n"):
                    handle.write("\n")
            if err:
                handle.write(err)
                if not err.endswith("\n"):
                    handle.write("\n")
            checks.append({"name": name, "status": "PASS" if rc == 0 else "FAIL"})
            if rc != 0:
                all_ok = False
        handle.write("\n")

    status = "PASS" if all_ok else "FAIL"
    if not all_ok:
        reason_codes.append("ACTION_FAILED")

    # evidence scaffolding
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # plan.md from pre_contract if available
    plan_md = evidence_dir / "plan.md"
    pre_contract_path = packet_meta.get("pre_contract_path")
    if pre_contract_path:
        try:
            pre = read_json(Path(pre_contract_path))
            plan = pre.get("plan_card") or {}
            plan_lines = ["# PlanCard", ""]
            for key in ("who", "what", "why", "where", "when", "how"):
                if key in plan:
                    plan_lines.append(f"- {key}: {plan[key]}")
            write_text(plan_md, "\n".join(plan_lines) + "\n")
        except Exception:
            pass

    write_text(
        evidence_dir / "decision.md",
        f"Status: {status}\nReasonCodes: {', '.join(reason_codes) if reason_codes else 'NONE'}\n",
    )

    # scope
    rc, diffstat, _ = run_cmd(["git", "diff", "--stat"], cwd=repo_root)
    rc, status_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=repo_root)
    scope = {
        "diffstat": diffstat.strip(),
        "touched_files": [
            ln[3:].strip() for ln in status_out.splitlines() if ln.strip()
        ],
    }
    write_json(evidence_dir / "scope.json", scope)

    write_json(evidence_dir / "integrity.json", {"status": "unknown"})
    write_text(evidence_dir / "regression.md", "")
    write_text(evidence_dir / "tests.junit.xml", "<testsuite></testsuite>\n")

    write_text(out_dir / "summary.md", f"Status: {status}\n")

    # evidence.json
    evidence = {
        "schema_version": "xtrl.evidence/v0.2",
        "packet_id": packet_id,
        "repo": repo,
        "timestamp": utc_now(),
        "status": status,
        "reason_codes": reason_codes,
        "commands_run": action_names,
        "checks": checks,
        "diffstat": scope["diffstat"],
        "touched_files": scope["touched_files"],
        "artifacts": [],
    }

    required_files = (contract.get("evidence") or {}).get("required_files") or []
    if isinstance(required_files, list) and required_files:
        ensure_required_files(out_dir, required_files)
        for rel in required_files:
            path = out_dir / rel
            if path.exists() and path.is_file():
                evidence["artifacts"].append({"path": rel, "sha256": sha256_file(path)})

    write_json(out_dir / "evidence.json", evidence)

    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
