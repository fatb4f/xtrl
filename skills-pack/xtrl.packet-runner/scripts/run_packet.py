#!/usr/bin/env python3
"""Codex skill entrypoint wrapper."""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys


def resolve_codex_home(codex_home: str | None) -> str:
    if codex_home:
        return os.path.expandvars(os.path.expanduser(codex_home))
    env = os.environ.get("CODEX_HOME")
    if env:
        return os.path.expandvars(os.path.expanduser(env))
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = xdg if xdg else os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "codex")


def resolve_codex_state(codex_state: str | None) -> str:
    if codex_state:
        return os.path.expandvars(os.path.expanduser(codex_state))
    env = os.environ.get("CODEX_STATE")
    if env:
        return os.path.expandvars(os.path.expanduser(env))
    xdg = os.environ.get("XDG_STATE_HOME")
    base = xdg if xdg else os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "codex")


def resolve_codex_data() -> str:
    env = os.environ.get("CODEX_DATA")
    if env:
        return os.path.expandvars(os.path.expanduser(env))
    xdg = os.environ.get("XDG_DATA_HOME")
    base = xdg if xdg else os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, "codex")


def resolve_repo_root(repo_root: str | None) -> str:
    if repo_root:
        return os.path.expandvars(os.path.expanduser(repo_root))
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    except Exception:
        raise SystemExit("must run inside a git repo or pass --repo-root")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Codex packet runner wrapper.")
    ap.add_argument("contract_path")
    ap.add_argument("--resume", action="store_true", help="Reuse existing worktree on collision.")
    ap.add_argument("--repo-root", help="Target repo root (defaults to git rev-parse).")
    ap.add_argument("--codex-home", help="Override CODEX_HOME config root.")
    ap.add_argument("--codex-state", help="Override CODEX_STATE root.")
    args = ap.parse_args(argv[1:])
    contract_path = args.contract_path
    repo_root = resolve_repo_root(args.repo_root)
    try:
        repo_root = (
            subprocess.check_output(["git", "-C", repo_root, "rev-parse", "--show-toplevel"], text=True).strip()
        )
    except Exception:
        raise SystemExit(f"not a git repository: {repo_root}")
    if subprocess.run(["git", "-C", repo_root, "status", "--porcelain"], text=True, capture_output=True).stdout.strip():
        raise SystemExit(f"target repo not clean: {repo_root}")
    codex_home = resolve_codex_home(args.codex_home)
    codex_state = resolve_codex_state(args.codex_state)
    codex_data = resolve_codex_data()
    xtrl_root = pathlib.Path(codex_data) / "vendor" / "xtrl"
    if not xtrl_root.exists():
        xtrl_root = pathlib.Path(codex_data) / "vendor" / "ctrlex"
    if not xtrl_root.exists():
        xtrl_root = pathlib.Path(codex_home) / "skills" / "vendor" / "xtrl"
    if not xtrl_root.exists():
        xtrl_root = pathlib.Path(codex_home) / "skills" / "vendor" / "ctrlex"
    if not xtrl_root.exists():
        fallback = pathlib.Path(codex_state) / "xtrl"
        if not fallback.exists():
            fallback = pathlib.Path(codex_state) / "ctrlex"
        if not fallback.exists():
            fallback = pathlib.Path(codex_state) / "plant-a"
        xtrl_root = fallback
    runner = xtrl_root / "tools" / "run_packet.py"
    cmd = [
        sys.executable,
        str(runner),
        contract_path,
        "--repo-root",
        repo_root,
        "--codex-home",
        codex_home,
        "--codex-state",
        codex_state,
    ]
    if args.resume:
        cmd.append("--resume")
    p = subprocess.run(cmd)
    return int(p.returncode)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
