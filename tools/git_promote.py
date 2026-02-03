#!/usr/bin/env python3
"""Git promotion harness (minimal)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def run_cmd(argv: List[str], cwd: Path | None = None) -> Tuple[int, str, str]:
    proc = run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def run_ok(argv: List[str], cwd: Path | None = None) -> bool:
    rc, _, _ = run_cmd(argv, cwd=cwd)
    return rc == 0


def stdout_or_empty(argv: List[str], cwd: Path | None = None) -> str:
    rc, out, _ = run_cmd(argv, cwd=cwd)
    return out if rc == 0 else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet_id")
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--codex-state", default=None)
    ap.add_argument("--dry-run", action="store_true")
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

    gates = []

    # ensure clean
    status = stdout_or_empty(["git", "status", "--porcelain"], cwd=repo_root)
    clean_ok = not status.strip()
    gates.append({"id": "clean_repo", "status": "PASS" if clean_ok else "FAIL"})
    if not clean_ok:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["DIRTY_REPO_DENIED"],
            "dry_run": args.dry_run,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates})
        return 2

    # binary diff detection
    numstat = stdout_or_empty(["git", "diff", "--numstat", f"{base_ref}..HEAD"], cwd=repo_root)
    binary = any(line.split("\t")[0] == "-" or line.split("\t")[1] == "-" for line in numstat.splitlines() if line)
    gates.append({"id": "no_binary_diffs", "status": "PASS" if not binary else "FAIL"})
    if binary:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["BINARY_DIFF_DENIED"],
            "dry_run": args.dry_run,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates})
        return 2

    # submodule detection
    raw = stdout_or_empty(["git", "diff", "--raw", f"{base_ref}..HEAD"], cwd=repo_root)
    has_submodule = "160000" in raw
    gates.append({"id": "no_submodules", "status": "PASS" if not has_submodule else "FAIL"})
    if has_submodule:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["SUBMODULE_DENIED"],
            "dry_run": args.dry_run,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates})
        return 2

    patch = stdout_or_empty(["git", "diff", "--binary", f"{base_ref}..HEAD"], cwd=repo_root)
    diffstat = stdout_or_empty(["git", "diff", "--stat", f"{base_ref}..HEAD"], cwd=repo_root)

    write_text(out_dir / "git" / "patch.diff", patch)
    write_text(out_dir / "git" / "diffstat.txt", diffstat)

    # empty patch gate
    has_patch = bool(patch.strip())
    gates.append({"id": "has_patch", "status": "PASS" if has_patch else "FAIL"})

    # base ref resolvable
    base_ok = run_ok(["git", "rev-parse", "--verify", base_ref], cwd=repo_root)
    gates.append({"id": "base_ref_resolves", "status": "PASS" if base_ok else "FAIL"})
    if not base_ok:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["BASE_REF_MISSING"],
            "dry_run": args.dry_run,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": args.dry_run})
        return 2

    # patch apply check (skip if empty)
    apply_ok = True
    already_applied = False
    if has_patch:
        apply_ok = run_ok(["git", "apply", "--check", str(out_dir / "git" / "patch.diff")], cwd=repo_root)
        if not apply_ok:
            already_applied = run_ok(
                ["git", "apply", "--check", "--reverse", str(out_dir / "git" / "patch.diff")], cwd=repo_root
            )
            if already_applied:
                apply_ok = True
    gates.append(
        {
            "id": "patch_applies",
            "status": "PASS" if apply_ok else "FAIL",
            "note": "already_applied" if already_applied else None,
        }
    )
    if not apply_ok:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["PATCH_APPLY_FAILED"],
            "dry_run": args.dry_run,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": args.dry_run})
        return 2

    if args.dry_run:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "BLOCKED",
            "reason_codes": ["DRY_RUN_ONLY"],
            "note": "Dry-run: patch applicable or empty; commit/push not performed.",
            "dry_run": True,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": True})
        return 3

    # non-dry-run: if already applied on current branch, push directly
    rc, current_branch, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
    current_branch = current_branch.strip() if rc == 0 else ""
    temp_branch = f"promote/{packet_id}"

    if already_applied and current_branch:
        push_ok = run_ok(["git", "push", "origin", current_branch], cwd=repo_root)
        if push_ok:
            promotion = {
                "timestamp": utc_now(),
                "packet_id": packet_id,
                "status": "PASS",
                "reason_codes": [],
                "note": f"Patch already applied on {current_branch}; pushed.",
                "dry_run": False,
            }
            write_json(out_dir / "git" / "promotion.json", promotion)
            write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": False})
            return 0

    if not run_ok(["git", "checkout", "-B", temp_branch, base_ref], cwd=repo_root):
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["CHECKOUT_FAILED"],
            "dry_run": False,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": False})
        return 2

    if has_patch and not run_ok(["git", "apply", "--index", str(out_dir / "git" / "patch.diff")], cwd=repo_root):
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "DENY",
            "reason_codes": ["PATCH_APPLY_FAILED"],
            "dry_run": False,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": False})
        return 2

    trailer_packet = None
    pre_contract_path = packet_meta.get("pre_contract_path")
    if pre_contract_path:
        try:
            pre = read_json(Path(pre_contract_path))
            trailer_packet = pre.get("inputs", {}).get("promotion_trailer_packet")
        except Exception:
            trailer_packet = None

    trailers = []
    if trailer_packet:
        trailers.append(f"Packet: {trailer_packet}")
    trailers.append(f"Evidence: {out_dir}/")
    message = f"promote({packet_id}): apply patch\n\n" + "\n".join(trailers) + "\n"
    if has_patch:
        run_cmd(["git", "commit", "-m", message], cwd=repo_root)

    # fast-forward main (or current branch) to temp and push
    ff_branch = current_branch or "main"
    ff_ok = run_ok(["git", "checkout", ff_branch], cwd=repo_root) and run_ok(
        ["git", "merge", "--ff-only", temp_branch], cwd=repo_root
    )
    push_ok = False
    if ff_ok:
        push_ok = run_ok(["git", "push", "origin", ff_branch], cwd=repo_root)

    if ff_ok and push_ok:
        promotion = {
            "timestamp": utc_now(),
            "packet_id": packet_id,
            "status": "PASS",
            "reason_codes": [],
            "note": f"FF-only push succeeded to {ff_branch}.",
            "dry_run": False,
        }
        write_json(out_dir / "git" / "promotion.json", promotion)
        write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": False})
        return 0

    # restore branch if FF failed
    if current_branch:
        run_cmd(["git", "checkout", current_branch], cwd=repo_root)

    promotion = {
        "timestamp": utc_now(),
        "packet_id": packet_id,
        "status": "BLOCKED",
        "reason_codes": ["PROMOTE_NOT_PUSHED"],
        "note": "Commit created on temp branch; FF-only push failed or not executed.",
        "dry_run": False,
    }
    write_json(out_dir / "git" / "promotion.json", promotion)
    write_json(out_dir / "git" / "gates.json", {"gates": gates, "dry_run": False})
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
