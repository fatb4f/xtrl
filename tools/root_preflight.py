#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from path_utils import (
    ensure_git_root,
    resolve_contract_path,
    resolve_repo_root,
    resolve_state_path,
    resolve_state_root,
)
from validate_plant import validate_plant_root

PLANT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_XDG_MARKER = "LEGACY_XDG_PATHS_OK"
LEGACY_XDG_PATTERNS = ("$CODEX_HOME/xtrl/out", "$CODEX_HOME/xtrl/worktrees")

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError as e:
        return 127, "", str(e)


def git_dir(repo: Path) -> Optional[Path]:
    rc, out, err = run(["git", "rev-parse", "--git-dir"], cwd=repo)
    if rc != 0:
        return None
    d = out.strip()
    return (repo / d).resolve()


def git_porcelain(repo: Path) -> List[str]:
    rc, out, err = run(["git", "status", "--porcelain"], cwd=repo)
    if rc != 0:
        return []
    return [ln.rstrip("\n") for ln in out.splitlines() if ln.strip()]


def extract_status_path(line: str) -> str:
    # Porcelain lines are "XY path" or "XY old -> new" for renames.
    raw = line[3:] if len(line) > 3 else line
    if " -> " in raw:
        return raw.split(" -> ", 1)[1].strip()
    return raw.strip()


def allowed_dirty_prefixes(contract: Dict[str, Any], repo_root: Path) -> List[str]:
    prefixes: List[str] = []
    evidence_cfg = contract.get("evidence") if isinstance(contract.get("evidence"), dict) else {}
    out_dir_raw = evidence_cfg.get("out_dir")
    if isinstance(out_dir_raw, str) and out_dir_raw:
        p = Path(os.path.expandvars(os.path.expanduser(out_dir_raw)))
        if p.is_absolute():
            try:
                rel = p.relative_to(repo_root)
                prefixes.append(str(rel).split("/")[0])
            except Exception:
                pass
        else:
            prefixes.append(str(Path(out_dir_raw).parts[0]))
    prefixes.extend(["ledger", "state"])
    return [p for p in prefixes if p]


def git_symbolic_ref(repo: Path) -> Tuple[bool, str]:
    rc, out, err = run(["git", "symbolic-ref", "-q", "--short", "HEAD"], cwd=repo)
    if rc != 0:
        return False, ""
    return True, out.strip()


def git_rev_parse(repo: Path, ref: str) -> Optional[str]:
    rc, out, err = run(["git", "rev-parse", "--verify", ref], cwd=repo)
    if rc != 0:
        return None
    return out.strip()


def git_op_in_progress(gitdir: Path) -> bool:
    markers = [
        "rebase-apply",
        "rebase-merge",
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "BISECT_LOG",
        "BISECT_NAMES",
    ]
    for name in markers:
        if (gitdir / name).exists():
            return True
    return False


def find_forbidden_roots(repo_root: Path) -> List[str]:
    forbidden: List[str] = []
    for target in (".codex", ".quint"):
        for path in repo_root.rglob(target):
            if not path.is_dir():
                continue
            try:
                rel = path.relative_to(repo_root)
            except ValueError:
                rel = path
            forbidden.append(str(rel))
    return forbidden


def safe_read_json(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not path.exists():
        return None, f"contract not found: {path}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as e:
        return None, f"failed to parse contract json: {e}"


def ensure_keys(obj: Dict[str, Any], required: List[str]) -> Optional[str]:
    missing = [k for k in required if k not in obj]
    if missing:
        return f"missing required keys: {missing}"
    return None


def ensure_no_extra(obj: Dict[str, Any], allowed: List[str]) -> Optional[str]:
    extras = [k for k in obj.keys() if k not in allowed]
    if extras:
        return f"unexpected keys: {sorted(extras)}"
    return None


def ensure_type(name: str, value: Any, typ: type) -> Optional[str]:
    if not isinstance(value, typ):
        return f"{name} must be {typ.__name__}"
    return None


def ensure_array_of_strings(name: str, value: Any) -> Optional[str]:
    if not isinstance(value, list):
        return f"{name} must be array"
    for item in value:
        if not isinstance(item, str):
            return f"{name} must contain only strings"
    return None


def validate_worktree_policy(policy: Dict[str, Any]) -> Optional[str]:
    required = ["mode", "worktree_root", "deny_if_worktree_exists", "allow_dirty_globs", "allow_untracked_globs"]
    err = ensure_keys(policy, required)
    if err:
        return f"worktree_policy: {err}"
    err = ensure_no_extra(policy, required)
    if err:
        return f"worktree_policy: {err}"
    if policy.get("mode") not in ("strict", "allow_dirty_allowlist"):
        return "worktree_policy.mode must be strict or allow_dirty_allowlist"
    err = ensure_type("worktree_policy.worktree_root", policy.get("worktree_root"), str)
    if err:
        return err
    err = ensure_type("worktree_policy.deny_if_worktree_exists", policy.get("deny_if_worktree_exists"), bool)
    if err:
        return err
    err = ensure_array_of_strings("worktree_policy.allow_dirty_globs", policy.get("allow_dirty_globs"))
    if err:
        return err
    err = ensure_array_of_strings("worktree_policy.allow_untracked_globs", policy.get("allow_untracked_globs"))
    if err:
        return err
    return None


def validate_network_policy(policy: Dict[str, Any]) -> Optional[str]:
    required = ["internet_access", "domain_allowlist_preset", "additional_domains", "allowed_http_methods"]
    err = ensure_keys(policy, required)
    if err:
        return f"network_policy: {err}"
    err = ensure_no_extra(policy, required)
    if err:
        return f"network_policy: {err}"
    if policy.get("internet_access") not in ("off", "on"):
        return "network_policy.internet_access must be off or on"
    err = ensure_type("network_policy.domain_allowlist_preset", policy.get("domain_allowlist_preset"), str)
    if err:
        return err
    err = ensure_array_of_strings("network_policy.additional_domains", policy.get("additional_domains"))
    if err:
        return err
    err = ensure_array_of_strings("network_policy.allowed_http_methods", policy.get("allowed_http_methods"))
    if err:
        return err
    return None


def validate_evidence(evidence: Dict[str, Any]) -> Optional[str]:
    required = ["out_dir", "include_git_diff_patch"]
    err = ensure_keys(evidence, required)
    if err:
        return f"evidence: {err}"
    err = ensure_no_extra(evidence, required)
    if err:
        return f"evidence: {err}"
    err = ensure_type("evidence.out_dir", evidence.get("out_dir"), str)
    if err:
        return err
    err = ensure_type("evidence.include_git_diff_patch", evidence.get("include_git_diff_patch"), bool)
    if err:
        return err
    return None


def validate_exec_prompt_metadata(meta: Dict[str, Any]) -> Optional[str]:
    required = ["schema_version", "contract_path", "worktree_root", "tasks", "acceptance_checks", "evidence"]
    err = ensure_keys(meta, required)
    if err:
        return f"exec_prompt: {err}"
    err = ensure_no_extra(meta, required + ["notes"])
    if err:
        return f"exec_prompt: {err}"
    for key in ("schema_version", "contract_path", "worktree_root"):
        err = ensure_type(f"exec_prompt.{key}", meta.get(key), str)
        if err:
            return err
    for key in ("tasks", "acceptance_checks", "evidence"):
        err = ensure_array_of_strings(f"exec_prompt.{key}", meta.get(key))
        if err:
            return err
        if not meta.get(key):
            return f"exec_prompt.{key} must not be empty"
    if "notes" in meta:
        err = ensure_type("exec_prompt.notes", meta.get("notes"), str)
        if err:
            return err
    return None


def extract_exec_prompt_metadata(text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    marker = "```json"
    start = text.find(marker)
    if start == -1:
        return None, "exec_prompt missing json metadata block"
    start = text.find("\n", start)
    if start == -1:
        return None, "exec_prompt json block malformed"
    end = text.find("```", start)
    if end == -1:
        return None, "exec_prompt json block not terminated"
    payload = text[start:end].strip()
    try:
        return json.loads(payload), None
    except Exception as exc:
        return None, f"exec_prompt json parse failed: {exc}"


def resolve_exec_prompt_path(contract_path: Path) -> Path:
    primary = contract_path.parent / "EXEC_PROMPT.md"
    if primary.exists():
        return primary
    if contract_path.name != "contract.json":
        legacy = contract_path.with_name(f"{contract_path.stem}.EXEC_PROMPT.md")
        if legacy.exists():
            return legacy
    return primary


def validate_contract(contract: Dict[str, Any]) -> Optional[str]:
    required = [
        "packet_id",
        "area",
        "repo",
        "base_ref",
        "branch",
        "github_ops_required",
        "net_ops_required",
        "allowed_paths",
        "forbidden_outputs",
        "worktree_policy",
        "network_policy",
        "evidence",
    ]
    err = ensure_keys(contract, required)
    if err:
        return err

    allowed_keys = [
        "packet_id",
        "area",
        "repo",
        "base_ref",
        "branch",
        "github_ops_required",
        "net_ops_required",
        "mode",
        "actions",
        "allowed_paths",
        "forbidden_outputs",
        "worktree_policy",
        "network_policy",
        "run",
        "budgets",
        "evidence",
        "evidence_required",
        "github",
    ]
    err = ensure_no_extra(contract, allowed_keys)
    if err:
        return err

    for key in ("packet_id", "area", "repo", "base_ref", "branch"):
        err = ensure_type(key, contract.get(key), str)
        if err:
            return err
    err = ensure_type("github_ops_required", contract.get("github_ops_required"), bool)
    if err:
        return err
    err = ensure_type("net_ops_required", contract.get("net_ops_required"), bool)
    if err:
        return err

    err = ensure_array_of_strings("allowed_paths", contract.get("allowed_paths"))
    if err:
        return err
    if not contract.get("allowed_paths"):
        return "allowed_paths must not be empty"
    err = ensure_array_of_strings("forbidden_outputs", contract.get("forbidden_outputs"))
    if err:
        return err

    err = validate_worktree_policy(contract.get("worktree_policy", {}))
    if err:
        return err

    err = validate_network_policy(contract.get("network_policy", {}))
    if err:
        return err

    err = validate_evidence(contract.get("evidence", {}))
    if err:
        return err

    if "evidence_required" in contract:
        err = ensure_array_of_strings("evidence_required", contract.get("evidence_required"))
        if err:
            return err

    if "github" in contract:
        gh = contract.get("github")
        if not isinstance(gh, dict):
            return "github must be an object"
        issue = gh.get("issue")
        if issue is not None and not isinstance(issue, dict):
            return "github.issue must be an object"
        if isinstance(issue, dict):
            for key in ("labels",):
                if key in issue and not isinstance(issue.get(key), list):
                    return f"github.issue.{key} must be array"
            for key in ("title", "template", "milestone"):
                if key in issue and not isinstance(issue.get(key), str):
                    return f"github.issue.{key} must be string"
            if "body" in issue and not isinstance(issue.get("body"), str):
                return "github.issue.body must be string"
            for key in ("ensure", "comment_on_run", "close_on_success"):
                if key in issue and not isinstance(issue.get(key), bool):
                    return f"github.issue.{key} must be bool"

    return None


def find_legacy_xdg_refs(repo_root: Path) -> Dict[str, List[str]]:
    rc, out, err = run(["git", "ls-files"], cwd=repo_root)
    if rc != 0:
        return {}
    hits: Dict[str, List[str]] = {}
    for rel in out.splitlines():
        rel = rel.strip()
        if not rel:
            continue
        path = (repo_root / rel).resolve()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if LEGACY_XDG_MARKER in text:
            continue
        found = [pat for pat in LEGACY_XDG_PATTERNS if pat in text]
        if found:
            hits[rel] = found
    return hits


@dataclass
class Decision:
    allow: bool = True
    deny_code: Optional[str] = None
    message: Optional[str] = None

    def deny(self, code: str, message: str) -> None:
        if self.allow:
            self.allow = False
            self.deny_code = code
            self.message = message


def default_evidence_path(contract: Optional[Dict[str, Any]], state_root: Path) -> Path:
    out_dir = str(resolve_state_path(None, state_root, "out"))
    packet_id = "unknown"
    if contract:
        packet_id = str(contract.get("packet_id") or packet_id)
        evidence = contract.get("evidence") or {}
        out_dir = str(resolve_state_path(evidence.get("out_dir"), state_root, "out"))
    return Path(out_dir) / packet_id / "root_preflight.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Root preflight (S0) gate.")
    parser.add_argument("--contract", required=True, help="Path to packet contract JSON.")
    parser.add_argument("--evidence-out", help="Override evidence output path.")
    parser.add_argument("--repo-root", help="Target repo root (defaults to git rev-parse).")
    parser.add_argument("--codex-home", help="Override CODEX_HOME config root.")
    parser.add_argument("--codex-state", help="Override CODEX_STATE root.")
    args = parser.parse_args()

    repo_root = resolve_repo_root(args.repo_root)
    ensure_git_root(repo_root)
    state_root = resolve_state_root(args.codex_state, args.codex_home)
    decision = Decision()

    contract_path = resolve_contract_path(args.contract, repo_root)
    if not contract_path.exists():
        raw = Path(args.contract)
        if not raw.is_absolute():
            alt = (state_root / raw).resolve()
            if alt.exists():
                contract_path = alt
    contract, contract_err = safe_read_json(contract_path)

    evidence_path = Path(args.evidence_out) if args.evidence_out else default_evidence_path(contract, state_root)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)

    base_ref = None
    github_ops_required = False
    net_ops_required = False
    worktree_root = str(resolve_state_path(None, state_root, "worktrees"))

    if contract is None:
        decision.deny("CONTRACT_INVALID", contract_err or "contract parse failed")
    else:
        base_ref = contract.get("base_ref")
        github_ops_required = bool(contract.get("github_ops_required", False))
        net_ops_required = bool(contract.get("net_ops_required", False))
        policy = contract.get("worktree_policy") or {}
        worktree_root = str(resolve_state_path(policy.get("worktree_root"), state_root, "worktrees"))
        if not isinstance(base_ref, str) or not base_ref.strip():
            decision.deny("BASE_REF_MISSING", "base_ref missing or empty")

    plant_err = validate_plant_root(PLANT_ROOT)
    if plant_err:
        decision.deny("PLANT_INVALID", plant_err)

    if decision.allow:
        forbidden_paths = find_forbidden_roots(repo_root)
        if forbidden_paths:
            sample = ", ".join(forbidden_paths[:3])
            decision.deny("FORBIDDEN_ROOTS", f"forbidden directories present: {sample}")

    if decision.allow:
        legacy_refs = find_legacy_xdg_refs(repo_root)
        if legacy_refs:
            sample = ", ".join(sorted(legacy_refs.keys())[:3])
            decision.deny(
                "LEGACY_XDG_PATHS",
                f"legacy CODEX_HOME state paths in: {sample} (use CODEX_STATE or mark {LEGACY_XDG_MARKER})",
            )

    if decision.allow:
        dirty = git_porcelain(repo_root)
        if dirty:
            allowed_prefixes = allowed_dirty_prefixes(contract, repo_root)
            remaining = []
            for line in dirty:
                path = extract_status_path(line)
                if any(path == p or path.startswith(f"{p}/") for p in allowed_prefixes):
                    continue
                remaining.append(line)
            if remaining:
                decision.deny("DIRTY_ROOT_PRE", "root working tree not clean")

    if decision.allow:
        gdir = git_dir(repo_root)
        if gdir and git_op_in_progress(gdir):
            decision.deny("GIT_OP_IN_PROGRESS", "git operation in progress in root")

    head_ok = False
    head_ref = ""
    if decision.allow:
        head_ok, head_ref = git_symbolic_ref(repo_root)
        if not head_ok:
            decision.deny("HEAD_DETACHED_PRE", "HEAD is detached in root")

    if decision.allow and base_ref:
        if git_rev_parse(repo_root, base_ref) is None:
            decision.deny("BASE_REF_MISSING", f"base_ref not resolvable: {base_ref}")

    if decision.allow and contract is not None:
        err = validate_contract(contract)
        if err:
            decision.deny("CONTRACT_INVALID", err)

    if decision.allow and contract is not None:
        prompt_path = resolve_exec_prompt_path(contract_path)
        if not prompt_path.exists():
            decision.deny("EXEC_PROMPT_MISSING", f"exec_prompt missing: {prompt_path}")
        else:
            try:
                prompt_text = prompt_path.read_text(encoding="utf-8")
            except Exception as exc:
                decision.deny("EXEC_PROMPT_INVALID", f"exec_prompt unreadable: {exc}")
            else:
                meta, meta_err = extract_exec_prompt_metadata(prompt_text)
                if meta_err:
                    decision.deny("EXEC_PROMPT_INVALID", meta_err)
                else:
                    err = validate_exec_prompt_metadata(meta or {})
                    if err:
                        decision.deny("EXEC_PROMPT_INVALID", err)

    if decision.allow:
        if shutil.which("git") is None:
            decision.deny("TOOLS_MISSING", "git not available in PATH")
        if not sys.executable or not Path(sys.executable).exists():
            decision.deny("TOOLS_MISSING", "python interpreter not available")

    if decision.allow:
        if not os.access(repo_root, os.W_OK):
            decision.deny("ENVELOPE_UNAVAILABLE", "repo root is not writable")
        wt_root = Path(worktree_root)
        if wt_root.exists() and not os.access(wt_root, os.W_OK):
            decision.deny("ENVELOPE_UNAVAILABLE", "worktree root is not writable")
        usage = shutil.disk_usage(repo_root)
        if usage.free <= 0:
            decision.deny("ENVELOPE_UNAVAILABLE", "no free disk space available")

    probes: Dict[str, Dict[str, Any]] = {}
    tx_mode = "offline"
    if shutil.which("gh") is None:
        probes["gh_auth_status"] = {"rc": 127, "stdout": "", "stderr": "gh not found"}
        probes["gh_pr_list"] = {"rc": 127, "stdout": "", "stderr": "gh not found"}
        rc = 127
        rc2 = 127
    else:
        rc, out, err = run(["gh", "auth", "status"], cwd=repo_root)
        probes["gh_auth_status"] = {"rc": rc, "stdout": out, "stderr": err}
        rc2, out2, err2 = run(["gh", "pr", "list", "--limit", "1"], cwd=repo_root)
        probes["gh_pr_list"] = {"rc": rc2, "stdout": out2, "stderr": err2}
    rc3, out3, err3 = run(["git", "ls-remote", "origin", "HEAD"], cwd=repo_root)
    probes["git_ls_remote"] = {"rc": rc3, "stdout": out3, "stderr": err3}
    if rc == 0 and rc2 == 0:
        tx_mode = "online"

    if decision.allow and github_ops_required:
        if rc != 0 or rc2 != 0:
            decision.deny("GITHUB_UNAVAILABLE", "GitHub auth/PR API unavailable")

    if decision.allow and contract is not None and net_ops_required:
        net = contract.get("network_policy") or {}
        domains = list(dict.fromkeys((net.get("additional_domains") or [])))
        if not domains:
            decision.deny("NET_UNAVAILABLE", "net_ops_required but no additional_domains configured")
        else:
            failed = []
            for domain in domains:
                rc, out, err = run(["getent", "hosts", domain])
                probes[f"net_dns:{domain}"] = {"rc": rc, "stdout": out, "stderr": err}
                if rc != 0:
                    failed.append(domain)
            if failed:
                decision.deny("NET_UNAVAILABLE", f"DNS resolution failed for: {', '.join(failed)}")

    evidence = {
        "stage": "S0",
        "timestamp_utc": utc_now(),
        "repo_root": str(repo_root),
        "base_ref": base_ref,
        "head_ref": head_ref if head_ok else "DETACHED",
        "github_ops_required": github_ops_required,
        "net_ops_required": net_ops_required,
        "tx_mode": tx_mode,
        "probes": probes,
        "decision": "ALLOW" if decision.allow else "DENY",
        "deny_code": decision.deny_code,
        "message": decision.message,
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if decision.allow else 2


if __name__ == "__main__":
    raise SystemExit(main())
