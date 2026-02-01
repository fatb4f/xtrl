#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


def run(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def expand_path(raw: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(raw)))


def resolve_codex_home(codex_home: str | None) -> Path:
    if codex_home:
        return expand_path(codex_home).resolve()
    env = os.environ.get("CODEX_HOME")
    if env:
        return expand_path(env).resolve()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else (Path.home() / ".config")
    return (base / "codex").resolve()


def resolve_codex_state(codex_state: str | None) -> Path:
    if codex_state:
        return expand_path(codex_state).resolve()
    env = os.environ.get("CODEX_STATE")
    if env:
        return expand_path(env).resolve()
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else (Path.home() / ".local" / "state")
    return (base / "codex").resolve()


def resolve_state_root(codex_state: str | None, codex_home: str | None = None) -> Path:
    base = resolve_codex_state(codex_state)
    xtrl_root = base / "xtrl"
    ctrlex_root = base / "ctrlex"
    plant_root = base / "plant-a"
    if xtrl_root.exists():
        return xtrl_root.resolve()
    if ctrlex_root.exists():
        return ctrlex_root.resolve()
    if plant_root.exists():
        return plant_root.resolve()
    return xtrl_root.resolve()


def resolve_repo_root(repo_root: str | None) -> Path:
    if repo_root:
        return expand_path(repo_root).resolve()
    rc, out, _ = run(["git", "rev-parse", "--show-toplevel"])
    if rc != 0:
        raise SystemExit("must run inside a git repo or pass --repo-root")
    return Path(out.strip()).resolve()


def ensure_git_root(repo_root: Path) -> None:
    rc, out, err = run(["git", "rev-parse", "--show-toplevel"], cwd=repo_root)
    if rc != 0:
        raise SystemExit(f"not a git repository: {repo_root}")
    resolved = Path(out.strip()).resolve()
    if resolved != repo_root.resolve():
        raise SystemExit(f"--repo-root is not a git root: {repo_root}")


def resolve_state_path(path_raw: str | None, state_root: Path, default_subdir: str) -> Path:
    if not path_raw:
        return (state_root / default_subdir).resolve()
    expanded = expand_path(path_raw)
    if expanded.is_absolute():
        return expanded.resolve()
    parts = Path(path_raw).parts
    if parts and parts[0] in (".codex", ".quint"):
        stripped = Path(*parts[1:]) if len(parts) > 1 else Path()
        return (state_root / stripped).resolve()
    return (state_root / expanded).resolve()


def resolve_contract_path(contract_path: str, repo_root: Path) -> Path:
    p = expand_path(contract_path)
    if p.is_absolute():
        return p.resolve()
    cwd_path = (Path.cwd() / p).resolve()
    if cwd_path.exists():
        return cwd_path
    repo_path = (repo_root / p).resolve()
    if repo_path.exists():
        return repo_path
    return cwd_path
