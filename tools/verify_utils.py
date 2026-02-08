#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from path_utils import resolve_codex_state, resolve_repo_root, resolve_state_root


def sh(cmd: list[str], cwd: Path | None = None) -> Tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_state() -> Path:
    codex_state = resolve_codex_state(None)
    return resolve_state_root(str(codex_state))


def resolve_repo() -> Path:
    return resolve_repo_root(None)


def current_packet_id(repo_root: Path) -> str:
    rc, out, _ = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
    if rc != 0 or not out:
        raise SystemExit("unable to resolve current branch")
    if out.startswith("packet/"):
        return out.split("packet/", 1)[1]
    raise SystemExit("current branch is not packet/<packet_id>")


def find_out_dir(packet_id: str, repo_root: Path) -> Optional[Path]:
    out_root = repo_root / "out"
    for candidate in out_root.rglob("packet.json"):
        try:
            data = read_json(candidate)
        except Exception:
            continue
        if data.get("packet_id") == packet_id:
            repo = data.get("repo") or "unknown"
            return (out_root / repo / packet_id).resolve()
    return None


def legacy_out_dir(packet_id: str, repo_root: Path) -> Path:
    return (repo_root / "out" / packet_id).resolve()
