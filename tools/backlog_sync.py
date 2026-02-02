#!/usr/bin/env python3
"""Backlog sync wrapper for xtrl packets."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence


@dataclass
class SyncResult:
    packet_id: str
    output_dir: Path | None
    dry_run: bool
    packet_returncode: int | None = None
    match_strategy: str | None = None
    matches: list[str] | None = None
    updated_file: str | None = None
    update_status: str | None = None
    errors: list[str] | None = None


def expand_path(raw: str | None) -> Path:
    if raw is None:
        raise ValueError("path not provided")
    return Path(os.path.expanduser(raw)).resolve()


def resolve_codex_state(raw: str | None) -> Path:
    if raw:
        return expand_path(raw)
    env = os.environ.get("CODEX_STATE")
    if env:
        return Path(os.path.expanduser(env)).resolve()
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "state"
    return (base / "codex").resolve()


def resolve_repo_root(raw: str | None) -> Path:
    if raw:
        return expand_path(raw)
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise SystemExit("must run inside a git repo or pass --repo-root")
    return Path(proc.stdout.strip()).resolve()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_contract(contract_path: Path) -> dict:
    return json.loads(contract_path.read_text(encoding="utf-8"))


def backlog_output_dir(codex_state: Path, packet_id: str) -> Path:
    return codex_state / "xtrl" / "out" / packet_id / "backlog"


def list_backlog_files(backlog_root: Path) -> list[dict]:
    files: list[dict] = []
    if not backlog_root.exists():
        return files
    for path in sorted(backlog_root.rglob("*.md")):
        if path.is_file():
            rel = path.relative_to(backlog_root)
            try:
                size = path.stat().st_size
            except OSError:
                size = None
            files.append({"path": str(rel), "size": size})
    return files


def snapshot_backlog(repo_root: Path) -> dict:
    backlog_root = repo_root / "backlog"
    snapshot = {
        "timestamp": now_iso(),
        "repo_root": str(repo_root),
        "backlog_root": str(backlog_root),
        "backlog_root_exists": backlog_root.exists(),
        "backlog_md_exists": (repo_root / "backlog.md").exists(),
        "task_files": list_backlog_files(backlog_root),
    }
    return snapshot


def extract_title(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        if line.lower().startswith("title:"):
            value = line.split(":", 1)[1].strip()
            if (value.startswith("\"") and value.endswith("\"")) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            return value
    return None


def iter_task_files(repo_root: Path) -> Iterable[Path]:
    backlog_root = repo_root / "backlog"
    if not backlog_root.exists():
        return []
    return sorted(p for p in backlog_root.rglob("*.md") if p.is_file())


def find_matches(repo_root: Path, packet_id: str) -> tuple[str, list[Path]]:
    explicit: list[Path] = []
    fallback: list[Path] = []
    pid_lower = packet_id.lower()
    for path in iter_task_files(repo_root):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            if line.strip() == f"Packet: {packet_id}":
                explicit.append(path)
                break
        if path in explicit:
            continue
        title = extract_title(text) or ""
        filename = path.name
        if pid_lower in filename.lower() or pid_lower in title.lower():
            fallback.append(path)
    if explicit:
        return "packet_line", explicit
    return "filename_or_title", fallback


def update_task_file(path: Path, evidence_path: str, result: str) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    found_evidence = False
    found_result = False
    for idx, line in enumerate(lines):
        if line.startswith("Evidence:"):
            lines[idx] = f"Evidence: {evidence_path}"
            found_evidence = True
        if line.startswith("Result:"):
            lines[idx] = f"Result: {result}"
            found_result = True
    if not found_evidence:
        lines.append(f"Evidence: {evidence_path}")
    if not found_result:
        lines.append(f"Result: {result}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_packet(
    xtrl_root: Path,
    repo_root: Path,
    codex_home: Path | None,
    codex_state: Path,
    contract: Path,
) -> int:
    script = xtrl_root / "tools" / "run_packet.py"
    args = [
        sys.executable,
        str(script),
        "--repo-root",
        str(repo_root),
        "--codex-state",
        str(codex_state),
    ]
    if codex_home is not None:
        args.extend(["--codex-home", str(codex_home)])
    args.append(str(contract))
    proc = subprocess.run(args)
    return proc.returncode


def main() -> None:
    parser = argparse.ArgumentParser(prog="backlog_sync")
    parser.add_argument("contract")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--codex-home", default=None)
    parser.add_argument("--codex-state", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    contract_path = expand_path(args.contract)
    repo_root = resolve_repo_root(args.repo_root)
    codex_state = resolve_codex_state(args.codex_state)
    codex_home = expand_path(args.codex_home) if args.codex_home else None
    xtrl_root = Path(__file__).resolve().parent.parent

    contract = load_contract(contract_path)
    packet_id = contract.get("packet_id")
    if not packet_id:
        raise SystemExit("packet_id missing from contract")

    result = SyncResult(packet_id=packet_id, output_dir=None, dry_run=args.dry_run)

    output_dir: Path | None = None
    try:
        output_dir = backlog_output_dir(codex_state, packet_id)
        output_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = output_dir
    except OSError as exc:
        result.errors = [f"output_dir_error: {exc}"]

    snapshot_payload: dict | None = None
    try:
        snapshot_payload = snapshot_backlog(repo_root)
        if output_dir:
            write_json(output_dir / "snapshot.json", snapshot_payload)
    except Exception as exc:  # noqa: BLE001
        result.errors = (result.errors or []) + [f"snapshot_error: {exc}"]

    if args.dry_run:
        if output_dir:
            write_json(
                output_dir / "result.json",
                {
                    "timestamp": now_iso(),
                    "packet_id": packet_id,
                    "dry_run": True,
                    "packet_run": None,
                    "update": None,
                },
            )
        return

    packet_returncode = run_packet(
        xtrl_root=xtrl_root,
        repo_root=repo_root,
        codex_home=codex_home,
        codex_state=codex_state,
        contract=contract_path,
    )
    result.packet_returncode = packet_returncode

    update_result: dict = {
        "timestamp": now_iso(),
        "packet_id": packet_id,
        "match_strategy": None,
        "matches": [],
        "updated_file": None,
        "status": None,
        "result": "PASS" if packet_returncode == 0 else "FAIL",
    }

    try:
        strategy, matches = find_matches(repo_root, packet_id)
        update_result["match_strategy"] = strategy
        update_result["matches"] = [str(p) for p in matches]
        result.match_strategy = strategy
        result.matches = [str(p) for p in matches]
        if len(matches) == 1:
            evidence_path = f"{codex_state / 'xtrl' / 'out' / packet_id}/"
            update_task_file(matches[0], evidence_path, update_result["result"])
            update_result["updated_file"] = str(matches[0])
            update_result["status"] = "updated"
            result.updated_file = str(matches[0])
            result.update_status = "updated"
        elif len(matches) == 0:
            update_result["status"] = "no_match"
            result.update_status = "no_match"
        else:
            update_result["status"] = "multiple_matches"
            result.update_status = "multiple_matches"
    except Exception as exc:  # noqa: BLE001
        update_result["status"] = "error"
        update_result["error"] = str(exc)
        result.update_status = "error"
        result.errors = (result.errors or []) + [f"update_error: {exc}"]

    if output_dir:
        write_json(output_dir / "update_result.json", update_result)
        try:
            post_snapshot = snapshot_backlog(repo_root)
            write_json(output_dir / "post_snapshot.json", post_snapshot)
        except Exception as exc:  # noqa: BLE001
            result.errors = (result.errors or []) + [f"post_snapshot_error: {exc}"]
        write_json(
            output_dir / "result.json",
            {
                "timestamp": now_iso(),
                "packet_id": packet_id,
                "dry_run": False,
                "packet_run": {
                    "returncode": packet_returncode,
                    "result": update_result["result"],
                },
                "update": update_result,
                "errors": result.errors or [],
            },
        )

    if packet_returncode != 0:
        raise SystemExit(packet_returncode)


if __name__ == "__main__":
    main()
