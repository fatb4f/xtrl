#!/usr/bin/env python3
"""Packet runner (canonical).

Responsibilities:
- provision isolated git worktree for the packet
- execute regen/test/commands (if configured)
- always emit Packet-002 evidence bundle via tools/evidence/collect_packet_evidence.py

Notes:
- stdlib only
- evidence is written under the repo root (default: <repo_root>/out/<packet_id>/)
"""

from __future__ import annotations

import argparse
import shlex
import datetime as _dt
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
from typing import Any, Dict, List, Tuple

from path_utils import (
    ensure_git_root,
    resolve_contract_path,
    resolve_repo_root,
    resolve_state_path,
    resolve_state_root,
)

RUNNER_VERSION = "0.1.4"  # Packet-002
PLANT_ROOT = pathlib.Path(__file__).resolve().parents[1]


def sh(cmd: List[str], cwd: str | None = None) -> Tuple[int, str, str]:
    p = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = p.communicate()
    return p.returncode, out, err


def sh_capture(cmd: List[str], cwd: str | None = None) -> Tuple[int, str, str]:
    rc, out, err = sh(cmd, cwd=cwd)
    return rc, out.strip(), err.strip()


def die(msg: str, code: int = 2) -> None:
    raise SystemExit(f"{msg.rstrip()}\n")


def load_json(path: str) -> Dict[str, Any]:
    p = pathlib.Path(path)
    if not p.exists():
        raise SystemExit(f"contract not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"failed to parse contract json: {e}")


def require(d: Dict[str, Any], k: str, typ: type | tuple[type, ...]) -> Any:
    if k not in d:
        raise SystemExit(f"missing required key: {k}")
    v = d[k]
    if not isinstance(v, typ):
        raise SystemExit(f"invalid type for {k}: expected {typ}, got {type(v)}")
    return v


def validate_network_policy(policy: Dict[str, Any]) -> None:
    required = [
        ("internet_access", str),
        ("domain_allowlist_preset", str),
        ("additional_domains", list),
        ("allowed_http_methods", list),
    ]
    for key, typ in required:
        if key not in policy:
            raise SystemExit(f"network_policy missing key: {key}")
        if not isinstance(policy[key], typ):
            raise SystemExit(f"network_policy.{key} must be {typ.__name__}")


def extract_exec_prompt_metadata(text: str) -> Dict[str, Any]:
    marker = "```json"
    start = text.find(marker)
    if start == -1:
        raise SystemExit("exec_prompt missing json metadata block")
    start = text.find("\n", start)
    if start == -1:
        raise SystemExit("exec_prompt json block malformed")
    end = text.find("```", start)
    if end == -1:
        raise SystemExit("exec_prompt json block not terminated")
    payload = text[start:end].strip()
    try:
        return json.loads(payload)
    except Exception as exc:
        raise SystemExit(f"exec_prompt json parse failed: {exc}")


def validate_exec_prompt_metadata(meta: Dict[str, Any]) -> None:
    required = ["schema_version", "contract_path", "worktree_root", "tasks", "acceptance_checks", "evidence"]
    missing = [k for k in required if k not in meta]
    if missing:
        raise SystemExit(f"exec_prompt missing required keys: {missing}")
    extras = [k for k in meta.keys() if k not in required + ["notes"]]
    if extras:
        raise SystemExit(f"exec_prompt unexpected keys: {sorted(extras)}")
    for key in ("schema_version", "contract_path", "worktree_root"):
        if not isinstance(meta.get(key), str):
            raise SystemExit(f"exec_prompt.{key} must be string")
    for key in ("tasks", "acceptance_checks", "evidence"):
        value = meta.get(key)
        if not isinstance(value, list) or not value:
            raise SystemExit(f"exec_prompt.{key} must be non-empty array")
        if any(not isinstance(item, str) for item in value):
            raise SystemExit(f"exec_prompt.{key} must contain only strings")
    if "notes" in meta and not isinstance(meta.get("notes"), str):
        raise SystemExit("exec_prompt.notes must be string")


def resolve_exec_prompt_path(contract_path: pathlib.Path) -> pathlib.Path:
    primary = contract_path.parent / "EXEC_PROMPT.md"
    if primary.exists():
        return primary
    if contract_path.name != "contract.json":
        legacy = contract_path.with_name(f"{contract_path.stem}.EXEC_PROMPT.md")
        if legacy.exists():
            return legacy
    return primary


def validate_exec_prompt(contract_path: pathlib.Path) -> None:
    prompt_path = resolve_exec_prompt_path(contract_path)
    if not prompt_path.exists():
        raise SystemExit(f"exec_prompt missing: {prompt_path}")
    try:
        text = prompt_path.read_text(encoding="utf-8")
    except Exception as exc:
        raise SystemExit(f"exec_prompt unreadable: {exc}")
    meta = extract_exec_prompt_metadata(text)
    validate_exec_prompt_metadata(meta)


def git_porcelain(cwd: str | None = None) -> List[str]:
    rc, out, err = sh(["git", "status", "--porcelain"], cwd=cwd)
    if rc != 0:
        raise SystemExit(f"git status failed: {err.strip()}")
    return [ln.rstrip("\n") for ln in out.splitlines() if ln.strip()]


def git_rev_parse(ref: str, cwd: str | None = None) -> str:
    rc, out, err = sh(["git", "rev-parse", "--verify", ref], cwd=cwd)
    if rc != 0:
        raise SystemExit(f"git rev-parse failed for {ref}: {err.strip()}")
    return out.strip()


def run_repo_sanitizer(repo_root: pathlib.Path, worktree_root: pathlib.Path) -> Tuple[bool, str]:
    sanitizer = repo_root / "tools" / "repo_sanitizer.py"
    if not sanitizer.exists():
        return False, f"missing sanitizer: {sanitizer}"
    argv = [
        sys.executable,
        str(sanitizer),
        "--repo-root",
        str(repo_root),
        "--worktree-root",
        str(worktree_root),
        "--apply",
    ]
    rc, out, err = sh(argv, cwd=str(repo_root))
    if rc != 0:
        return False, (err or out).strip() or "sanitizer failed"
    return True, (out or err).strip() or "sanitizer ok"


def gh_available() -> bool:
    rc, _, _ = sh_capture(["gh", "--version"])
    return rc == 0


def gh_find_issue(repo: str, title: str) -> str | None:
    rc, out, err = sh_capture(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--search",
            f"{title} in:title",
            "--json",
            "number",
            "--jq",
            ".[0].number",
        ]
    )
    if rc != 0 or not out:
        return None
    return out


def gh_issue_create(
    repo: str,
    title: str,
    template: str | None,
    labels: List[str],
    milestone: str | None,
    body: str | None,
) -> Tuple[bool, str]:
    cmd = ["gh", "issue", "create", "--repo", repo, "--title", title]
    if not template:
        if body is None:
            body = ""
        cmd += ["--body", body]
    if template:
        cmd += ["--template", template]
    if labels:
        cmd += ["--label", ",".join(labels)]
    if milestone:
        cmd += ["--milestone", milestone]
    rc, out, err = sh_capture(cmd)
    return rc == 0, out or err


def gh_issue_comment(repo: str, number: str, body: str) -> Tuple[bool, str]:
    rc, out, err = sh_capture(["gh", "issue", "comment", number, "--repo", repo, "--body", body])
    return rc == 0, out or err


def gh_issue_close(repo: str, number: str, comment: str | None = None) -> Tuple[bool, str]:
    cmd = ["gh", "issue", "close", number, "--repo", repo]
    if comment:
        cmd += ["--comment", comment]
    rc, out, err = sh_capture(cmd)
    return rc == 0, out or err




def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def write_json(path: pathlib.Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_path(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_visibility_index(
    state_root: pathlib.Path,
    packet_id: str,
    repo: str,
    worktree_path: str | None,
    out_dir: pathlib.Path,
    pre_contract_path: str | None,
) -> None:
    visibility_dir = state_root / "visibility"
    visibility_dir.mkdir(parents=True, exist_ok=True)
    index_path = visibility_dir / "index.json"

    entry = {
        "packet_id": packet_id,
        "repo": repo,
        "worktree_path": worktree_path,
        "out_dir": str(out_dir),
        "pre_contract_path": pre_contract_path,
    }

    items: List[Dict[str, Any]] = []
    if index_path.exists():
        try:
            payload = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and isinstance(payload.get("items"), list):
                items = payload["items"]
        except Exception:
            items = []

    by_id = {str(it.get("packet_id")): it for it in items if isinstance(it, dict)}
    by_id[packet_id] = entry
    merged = [by_id[k] for k in sorted(by_id.keys())]
    write_json(index_path, {"items": merged})

    link_path = out_dir / "link.json"
    write_json(link_path, entry)


def gate_evidence_path(out_dir: str, packet_id: str, name: str) -> pathlib.Path:
    return pathlib.Path(out_dir) / packet_id / f"{name}.json"


def run_gate(
    script: pathlib.Path,
    contract_path: str,
    evidence_path: pathlib.Path,
    repo_root: pathlib.Path,
    codex_home: str | None,
    codex_state: str | None,
) -> int:
    argv = [
        sys.executable,
        str(script),
        "--contract",
        contract_path,
        "--evidence-out",
        str(evidence_path),
        "--repo-root",
        str(repo_root),
    ]
    if codex_home:
        argv += ["--codex-home", codex_home]
    if codex_state:
        argv += ["--codex-state", codex_state]
    p = subprocess.run(argv, check=False)
    return p.returncode


def _parse_name_status(lines: List[str]) -> List[str]:
    paths: List[str] = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith("A"):
            path = parts[1]
        elif "->" in ln:
            # e.g. "R100\told -> new"
            path = parts[-1].split("->", 1)[1].strip() if "->" in parts[-1] else parts[-1]
        else:
            continue
        paths.append(path)
    return paths


def maybe_emit_helper_created(
    *,
    repo_root: pathlib.Path,
    wt_path: str,
    base_sha: str,
    packet_id: str,
    base_ref: str,
    out_dir: str,
    out_base: pathlib.Path,
) -> None:
    new_paths: List[str] = []
    if base_sha:
        rc, out, _ = sh(["git", "diff", "--name-status", f"{base_sha}..HEAD"], cwd=wt_path)
        if rc == 0:
            new_paths = _parse_name_status(out.splitlines())
    # Include untracked files (list explicit files, not just directories)
    untracked_files: List[str] = []
    rc_untracked, untracked_out, _ = sh(["git", "ls-files", "--others", "--exclude-standard"], cwd=wt_path)
    if rc_untracked == 0:
        for ln in untracked_out.splitlines():
            ln = ln.strip()
            if ln:
                untracked_files.append(ln)
                new_paths.append(ln)
    helper_roots = ("tools/", "helpers/")
    helper_files = [p for p in new_paths if p.startswith(helper_roots)]
    if not helper_files:
        return

    # Read existing events to avoid duplicates
    events_path = out_base / "evidence" / "events.jsonl"
    events_path.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("event") == "helper_created":
                existing.add(obj.get("helper_path"))

    # Compute diffstat
    rc, numstat, _ = sh(["git", "diff", "--numstat", f"{base_sha}..HEAD"], cwd=wt_path) if base_sha else (1, "", "")
    files_changed = 0
    insertions = 0
    deletions = 0
    if rc == 0:
        for ln in numstat.splitlines():
            parts = ln.split("\t")
            if len(parts) < 2:
                continue
            a, d = parts[0], parts[1]
            if a.isdigit():
                insertions += int(a)
            if d.isdigit():
                deletions += int(d)
            files_changed += 1
    # If only untracked files were added, synthesize diffstat from them.
    if files_changed == 0 and untracked_files:
        files_changed = len(untracked_files)
        for rel_path in untracked_files:
            try:
                data = (pathlib.Path(wt_path) / rel_path).read_text(encoding="utf-8")
                insertions += data.count("\n")
            except Exception:
                continue
    elif rc != 0:
        files_changed = len(touched_paths)

    # touched_paths
    rc, name_only, _ = sh(["git", "diff", "--name-only", f"{base_sha}..HEAD"], cwd=wt_path) if base_sha else (1, "", "")
    touched_paths = [ln.strip() for ln in name_only.splitlines() if ln.strip()] if rc == 0 else []
    touched_paths = sorted(set(touched_paths + [p for p in new_paths if p]))

    gate_ref = gate_evidence_path(out_dir, packet_id, "g0_enter_work")
    prompt_ref = out_base / "exec-prompt.md"

    wt_root = pathlib.Path(wt_path).resolve()
    helper_candidates: List[pathlib.Path] = []
    for rel_path in helper_files:
        helper_abs = (wt_root / rel_path).resolve()
        if helper_abs.is_dir():
            for p in helper_abs.rglob("*"):
                if p.is_file():
                    helper_candidates.append(p)
        else:
            helper_candidates.append(helper_abs)

    for helper_abs in helper_candidates:
        rel_path = helper_abs.relative_to(wt_root).as_posix()
        if rel_path in existing:
            continue
        if not helper_abs.exists() or not helper_abs.is_file():
            continue
        event = {
            "event": "helper_created",
            "packet_id": packet_id,
            "run_id": packet_id,
            "base_ref": base_ref,
            "base_sha": base_sha,
            "helper_path": rel_path,
            "helper_hash": sha256_path(helper_abs),
            "trigger_reason_code": "HELPER_BIRTH_DETECTED",
            "gate_decision_ref": {
                "path": str(gate_ref),
                "sha256": sha256_path(gate_ref) if gate_ref.exists() else "",
            },
            "prompt_ref": {
                "path": str(prompt_ref),
                "sha256": sha256_path(prompt_ref) if prompt_ref.exists() else "",
            },
            "touched_paths": touched_paths,
            "diffstat": {
                "files_changed": files_changed,
                "insertions": insertions,
                "deletions": deletions,
            },
        }
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")


def ensure_required_files(out_dir: pathlib.Path, required: List[str]) -> None:
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


def run_commands(
    run_cfg: Dict[str, Any],
    cwd: str,
    out_log: List[str],
    post_cmd: callable | None = None,
    *,
    out_base: pathlib.Path | None = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Runs regen_cmd, test_cmd, then run.commands (in that order)."""

    cmds: List[Tuple[str, str]] = []  # (kind, cmd)
    regen = run_cfg.get("regen_cmd")
    test = run_cfg.get("test_cmd")
    extra = run_cfg.get("commands") or []

    if regen:
        cmds.append(("regen", regen))
    if test:
        cmds.append(("test", test))
    if isinstance(extra, list):
        cmds.extend([("cmd", x) for x in extra if x])

    results: List[Dict[str, Any]] = []
    test_rc: int | None = None
    tests_output: str | None = None

    for kind, c in cmds:
        argv: List[str] | None = None
        cmd_display = ""
        if isinstance(c, list):
            argv = [str(x) for x in c]
            if out_base and "evidence/tests.junit.xml" in argv:
                idx = argv.index("evidence/tests.junit.xml")
                argv[idx] = str(out_base / "evidence" / "tests.junit.xml")
            cmd_display = " ".join(argv)
            out_log.append(f"$ {cmd_display}")
            rc, out, err = sh(argv, cwd=cwd)
        else:
            cmd_str = str(c)
            if not cmd_str.strip():
                continue
            try:
                argv = shlex.split(cmd_str)
            except ValueError:
                argv = []
            if not argv:
                results.append({"name": kind, "argv": None, "cmd": cmd_str, "rc": 2})
                out_log.append(f"$ {cmd_str}")
                out_log.append("invalid command: failed to parse argv")
                break
            if out_base and "evidence/tests.junit.xml" in argv:
                idx = argv.index("evidence/tests.junit.xml")
                argv[idx] = str(out_base / "evidence" / "tests.junit.xml")
            cmd_display = " ".join(argv)
            out_log.append(f"$ {cmd_display}")
            rc, out, err = sh(argv, cwd=cwd)
        results.append({"name": kind, "argv": argv, "cmd": cmd_display, "rc": rc})
        if out.strip():
            out_log.append(out.rstrip())
        if err.strip():
            out_log.append(err.rstrip())

        if kind == "test":
            test_rc = rc
            tests_output = (out or "") + ("\n" if out and not out.endswith("\n") else "") + (err or "")

        if post_cmd:
            try:
                post_cmd(kind, c, rc)
            except Exception:
                pass

        if rc != 0:
            break

    meta = {"test_rc": test_rc, "tests_output": tests_output}
    return results, meta


def collect_packet_evidence(
    contract_path: str,
    meta_path: pathlib.Path | None,
    repo_root: pathlib.Path,
    codex_home: str | None,
    codex_state: str | None,
) -> None:
    collector = PLANT_ROOT / "tools" / "evidence" / "collect_packet_evidence.py"
    argv = [sys.executable, str(collector), "--contract", contract_path, "--repo-root", str(repo_root)]
    if codex_home:
        argv += ["--codex-home", codex_home]
    if codex_state:
        argv += ["--codex-state", codex_state]
    if meta_path is not None:
        argv += ["--meta", str(meta_path)]
    subprocess.run(argv, check=False)


def required_evidence_missing(out_base: pathlib.Path) -> List[str]:
    required_files = [
        out_base / "contract.json",
        out_base / "exec-prompt.md",
        out_base / "packet.json",
        out_base / "evidence.json",
        out_base / "evidence.md",
        out_base / "manifest.json",
        out_base / "manifest.sha256",
        out_base / "raw" / "head_before.txt",
        out_base / "raw" / "status_before.txt",
        out_base / "raw" / "head_after.txt",
        out_base / "raw" / "status_after.txt",
        out_base / "raw" / "diff_name_only.txt",
        out_base / "raw" / "diffstat.txt",
    ]
    return [str(p) for p in required_files if not p.exists()]


def read_json(path: pathlib.Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_out_root_from_packet_json(
    packet_id: str,
    state_root: pathlib.Path,
    repo_root: pathlib.Path,
) -> pathlib.Path | None:
    out_root = repo_root / "out"
    for candidate in out_root.rglob("packet.json"):
        try:
            data = read_json(candidate)
        except Exception:
            continue
        if data.get("packet_id") == packet_id:
            repo = data.get("repo") or "unknown"
            return (out_root / repo).resolve()
    return None


def parse_args(argv: List[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run a Codex packet.")
    ap.add_argument("contract_path", help="Path to packet contract JSON.")
    ap.add_argument(
        "--resume",
        action="store_true",
        help="Reuse existing worktree if G0 denies due to collision.",
    )
    ap.add_argument("--repo-root", help="Target repo root (defaults to git rev-parse).")
    ap.add_argument("--codex-home", help="Override CODEX_HOME config root.")
    ap.add_argument("--codex-state", help="Override CODEX_STATE root.")
    return ap.parse_args(argv[1:])


def resume_from_collision(
    g0_path: pathlib.Path,
    base_ref: str,
    branch: str,
    repo_root: pathlib.Path,
) -> Tuple[str | None, str | None, List[str]]:
    reasons: List[str] = []
    if not g0_path.exists():
        return None, None, reasons
    try:
        g0 = read_json(g0_path)
    except Exception:
        return None, None, reasons
    if g0.get("deny_code") != "WORKTREE_COLLISION":
        return None, None, reasons
    wt_path = g0.get("worktree_path")
    if not wt_path:
        return None, None, reasons
    wt = pathlib.Path(wt_path)
    if not wt.exists():
        return None, None, reasons
    try:
        head_ref = git_rev_parse("HEAD", cwd=str(wt))
    except Exception:
        head_ref = None
    if head_ref is None:
        return None, None, reasons
    try:
        branch_name = sh_capture(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(wt))[1]
    except Exception:
        branch_name = ""
    if branch_name and branch_name != branch:
        return None, None, reasons
    try:
        base_sha = git_rev_parse(base_ref, cwd=str(repo_root))
    except Exception:
        base_sha = None
    reasons.append("resume_existing_worktree")
    return str(wt), base_sha, reasons


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    repo_root = resolve_repo_root(args.repo_root)
    ensure_git_root(repo_root)
    state_root = resolve_state_root(args.codex_state, args.codex_home)

    contract_path_obj = resolve_contract_path(args.contract_path, repo_root)
    if not contract_path_obj.exists():
        raw = pathlib.Path(args.contract_path)
        if not raw.is_absolute():
            alt = (state_root / raw).resolve()
            if alt.exists():
                contract_path_obj = alt
    contract_path = str(contract_path_obj)
    contract = load_json(contract_path)
    validate_exec_prompt(pathlib.Path(contract_path))

    packet_id = require(contract, "packet_id", str)
    base_ref = require(contract, "base_ref", str)
    branch = require(contract, "branch", str)
    github_ops_required = require(contract, "github_ops_required", bool)
    network_policy = require(contract, "network_policy", dict)
    validate_network_policy(network_policy)
    evidence_cfg = require(contract, "evidence", dict)
    github_cfg = contract.get("github") if isinstance(contract.get("github"), dict) else None

    out_dir_raw = evidence_cfg.get("out_dir")
    if out_dir_raw:
        expanded = pathlib.Path(os.path.expandvars(os.path.expanduser(str(out_dir_raw))))
        out_dir = str(expanded if expanded.is_absolute() else (repo_root / expanded).resolve())
    else:
        resolved_root = resolve_out_root_from_packet_json(packet_id, state_root, repo_root)
        out_dir = str(resolved_root or (repo_root / "out"))
    out_base = pathlib.Path(out_dir) / packet_id
    raw_dir = out_base / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    run_log: List[str] = []
    run_log.append(f"packet_id={packet_id}")
    run_log.append(f"contract_path={contract_path}")
    run_log.append(f"runner_version={RUNNER_VERSION}")
    run_log.append(f"utc_start={_dt.datetime.now(_dt.timezone.utc).isoformat().replace('+00:00', 'Z')}")
    run_log.append(f"network_internet_access={network_policy.get('internet_access')}")

    decision = "DENY"
    reasons: List[str] = []
    final_status = "FAIL"

    meta_path = raw_dir / "meta.json"

    wt_path: str | None = None
    base_sha: str | None = None
    test_rc: int | None = None
    tests_output: str | None = None

    try:
        preflight_path = gate_evidence_path(out_dir, packet_id, "root_preflight")
        g0_path = gate_evidence_path(out_dir, packet_id, "g0_enter_work")

        rc = run_gate(
            PLANT_ROOT / "tools" / "root_preflight.py",
            contract_path,
            preflight_path,
            repo_root,
            args.codex_home,
            args.codex_state,
        )
        if rc != 0:
            raise SystemExit("root preflight denied")

        rc = run_gate(
            PLANT_ROOT / "tools" / "g0_enter_work.py",
            contract_path,
            g0_path,
            repo_root,
            args.codex_home,
            args.codex_state,
        )
        if rc != 0 and args.resume:
            wt_path, base_sha, resume_reasons = resume_from_collision(g0_path, base_ref, branch, repo_root)
            if wt_path:
                reasons.extend(resume_reasons)
            else:
                raise SystemExit("G0 enter work denied")
        elif rc != 0:
            raise SystemExit("G0 enter work denied")
        else:
            g0_evidence = read_json(g0_path)
            wt_path = g0_evidence.get("worktree_path")
            base_sha = g0_evidence.get("base_sha") or git_rev_parse(base_ref, cwd=str(repo_root))
        if not wt_path:
            raise SystemExit("worktree_path not set by G0")

        # Pre-run evidence scaffolding for v0.2 layout
        required_files = contract.get("evidence_required") or []
        if isinstance(required_files, list) and required_files:
            ensure_required_files(out_base, required_files)
            events_path = out_base / "evidence" / "events.jsonl"
            if events_path.exists():
                write_text(events_path, "")
        evidence_path = out_base / "evidence.json"
        seed = {
            "schema_version": "xtrl.evidence/v0.2",
            "packet_id": packet_id,
            "generated_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        if evidence_path.exists():
            try:
                payload = read_json(evidence_path)
            except Exception:
                payload = {}
            if not isinstance(payload, dict):
                payload = {}
            if payload.get("schema_version") != seed["schema_version"]:
                payload.update(seed)
                write_json(evidence_path, payload)
        else:
            write_json(evidence_path, seed)

        # Pre-run visibility index + link.json
        pre_contract_path = None
        try:
            pkt_path = out_base / "packet.json"
            if pkt_path.exists():
                pkt = read_json(pkt_path)
                pre_contract_path = pkt.get("pre_contract_path")
        except Exception:
            pre_contract_path = None
        try:
            write_visibility_index(
                state_root=state_root,
                packet_id=packet_id,
                repo=str(contract.get("repo") or ""),
                worktree_path=wt_path,
                out_dir=out_base,
                pre_contract_path=pre_contract_path,
            )
        except Exception:
            pass


        # Pre-run snapshot inside worktree
        head_before = git_rev_parse("HEAD", cwd=wt_path)
        status_before = git_porcelain(cwd=wt_path)
        write_text(raw_dir / "head_before.txt", head_before + "\n")
        write_text(raw_dir / "status_before.txt", "\n".join(status_before) + ("\n" if status_before else ""))

        run_cfg = contract.get("run", {})
        def _post_cmd(kind: str, cmd: str, rc: int) -> None:
            if rc != 0:
                return
            maybe_emit_helper_created(
                repo_root=repo_root,
                wt_path=wt_path,
                base_sha=base_sha or "",
                packet_id=packet_id,
                base_ref=base_ref,
                out_dir=out_dir,
                out_base=out_base,
            )

        os.environ["XTRL_OUT_DIR"] = str(out_base)
        cmd_results, run_meta = run_commands(
            run_cfg,
            cwd=wt_path,
            out_log=run_log,
            post_cmd=_post_cmd,
            out_base=out_base,
        )

        test_rc = run_meta.get("test_rc")
        tests_output = run_meta.get("tests_output")
        if tests_output is not None:
            write_text(raw_dir / "tests.txt", tests_output)

        # Post-run snapshot inside worktree
        head_after = git_rev_parse("HEAD", cwd=wt_path)
        status_after = git_porcelain(cwd=wt_path)
        write_text(raw_dir / "head_after.txt", head_after + "\n")
        write_text(raw_dir / "status_after.txt", "\n".join(status_after) + ("\n" if status_after else ""))

        final_rc = int(cmd_results[-1]["rc"]) if cmd_results else 0
        non_test_failed = any(item.get("name") != "test" and item.get("rc") != 0 for item in cmd_results)
        if non_test_failed:
            decision = "DENY"
            reasons.append("non_test_failed")
        elif test_rc == 5:
            decision = "ALLOW"
            reasons.append("TESTS_MISSING")
        elif isinstance(test_rc, int) and test_rc != 0:
            decision = "DENY"
            reasons.append("tests_failed")
        else:
            decision = "ALLOW"

        # Keep a compact machine-readable run record (the collector handles canonical evidence.json)
        write_json(raw_dir / "run_commands.json", {"commands": cmd_results, "final_rc": final_rc})

    except SystemExit as e:
        reasons.append(str(e).strip())
    except Exception as e:
        reasons.append(f"unhandled_error: {e}")
    finally:
        run_log.append(f"utc_end={_dt.datetime.now(_dt.timezone.utc).isoformat().replace('+00:00', 'Z')}")
        write_text(raw_dir / "runner.log", "\n".join(run_log) + "\n")

        meta = {
            "runner_version": RUNNER_VERSION,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "repo_root": str(repo_root),
            "packet_id": packet_id,
            "base_ref": base_ref,
            "base_sha": base_sha,
            "branch": branch,
            "github_ops_required": github_ops_required,
            "network_policy": network_policy,
            "worktree_path": wt_path,
            "decision": decision,
            "reasons": reasons,
            "test_rc": test_rc,
            "tests_output": tests_output,
            "resolved": {
                "base_ref": base_ref,
                "base_sha": base_sha,
                "branch": branch,
                "worktree_path": wt_path,
            },
        }
        write_json(meta_path, meta)

        # Always run the Packet-002 collector (even on DENY)
        collect_packet_evidence(
            contract_path=contract_path,
            meta_path=meta_path,
            repo_root=repo_root,
            codex_home=args.codex_home,
            codex_state=args.codex_state,
        )

    missing = required_evidence_missing(out_base)
    evidence_decision = None
    evidence_path = out_base / "evidence.json"
    if evidence_path.exists():
        try:
            evidence = read_json(evidence_path)
            evidence_decision = evidence.get("decision")
        except Exception as e:
            missing.append(f"{evidence_path}: {e}")

    if missing:
        decision = "DENY"
        reasons.append("missing_evidence_outputs")

    if evidence_decision and evidence_decision != "ALLOW":
        decision = "DENY"
        reasons.append("evidence_denied")

    final_status = "PASS" if decision == "ALLOW" else "DENY"
    if any(r.startswith("unhandled_error") for r in reasons):
        final_status = "FAIL"

    meta["decision"] = decision
    meta["reasons"] = reasons
    meta["final_status"] = final_status
    meta["evidence_decision"] = evidence_decision
    meta["missing_evidence_outputs"] = missing

    gh_ops: Dict[str, Any] = {"attempted": False}
    if github_cfg and isinstance(github_cfg.get("issue"), dict):
        issue_cfg = github_cfg["issue"]
        repo = str(github_cfg.get("repo") or "").strip()
        title = str(issue_cfg.get("title") or packet_id).strip()
        template = (issue_cfg.get("template") or "").strip() or None
        body = issue_cfg.get("body")
        labels = issue_cfg.get("labels") or []
        milestone = (issue_cfg.get("milestone") or "").strip() or None
        ensure = bool(issue_cfg.get("ensure", False))
        comment_on_run = bool(issue_cfg.get("comment_on_run", False))
        close_on_success = bool(issue_cfg.get("close_on_success", False))

        gh_ops["attempted"] = True
        gh_ops["repo"] = repo
        gh_ops["title"] = title
        gh_ops["ensure"] = ensure
        gh_ops["comment_on_run"] = comment_on_run
        gh_ops["close_on_success"] = close_on_success

        if not repo:
            gh_ops["error"] = "missing github.repo"
        elif not gh_available():
            gh_ops["error"] = "gh_not_available"
        else:
            issue_number = gh_find_issue(repo, title)
            created = False
            if not issue_number and ensure:
                ok, msg = gh_issue_create(repo, title, template, labels, milestone, body)
                gh_ops["create"] = {"ok": ok, "message": msg}
                if ok:
                    issue_number = gh_find_issue(repo, title)
                    created = True
            gh_ops["issue_number"] = issue_number
            gh_ops["created"] = created

            if issue_number and comment_on_run:
                evidence_dir = str(out_base)
                evidence_md = str(out_base / "evidence.md")
                meta_rel = str(out_base / "raw" / "meta.json")
                comment = "\n".join(
                    [
                        "Packet run evidence (local)",
                        "",
                        f"- status: {final_status}",
                        f"- evidence dir: `{evidence_dir}`",
                        f"- evidence.md: `{evidence_md}`",
                        f"- meta: `{meta_rel}`",
                    ]
                )
                ok, msg = gh_issue_comment(repo, issue_number, comment)
                gh_ops["comment"] = {"ok": ok, "message": msg}

            if issue_number and close_on_success and final_status == "PASS":
                ok, msg = gh_issue_close(repo, issue_number, comment="Closing: packet run PASS with evidence.")
                gh_ops["close"] = {"ok": ok, "message": msg}

        if github_ops_required and gh_ops.get("error"):
            decision = "DENY"
            reasons.append(f"github_ops_failed:{gh_ops['error']}")

    meta["github_ops"] = gh_ops
    meta["sanitizer"] = {"attempted": False}

    # Post-success cleanup: only after PASS and when worktree points at HEAD.
    if final_status == "PASS":
        sanitizer_reason = ""
        try:
            git_rev_parse("HEAD", cwd=wt_path)
            worktree_root = resolve_state_path(None, state_root, "worktrees")
            ok, msg = run_repo_sanitizer(repo_root, worktree_root)
            meta["sanitizer"] = {"attempted": True, "ok": ok, "message": msg}
        except Exception as exc:
            sanitizer_reason = str(exc)
            meta["sanitizer"] = {"attempted": True, "ok": False, "message": sanitizer_reason}

    # Visibility index + link.json (best-effort)
    pre_contract_path = None
    try:
        pkt_path = out_base / "packet.json"
        if pkt_path.exists():
            pkt = read_json(pkt_path)
            pre_contract_path = pkt.get("pre_contract_path")
    except Exception:
        pre_contract_path = None
    try:
        write_visibility_index(
            state_root=state_root,
            packet_id=packet_id,
            repo=str(contract.get("repo") or ""),
            worktree_path=wt_path,
            out_dir=out_base,
            pre_contract_path=pre_contract_path,
        )
    except Exception:
        pass

    # Ledger + latest state pointer (best-effort).
    try:
        ledger_path = repo_root / "ledger" / "ledger.jsonl"
        latest_path = repo_root / "state" / "latest.json"
        promotion_eligible = (
            decision == "ALLOW"
            and "TESTS_MISSING" not in reasons
            and "missing_evidence_outputs" not in reasons
        )
        entry = {
            "schema_version": "xtrl.ledger_entry/v0.1",
            "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z"),
            "packet_id": packet_id,
            "repo": str(contract.get("repo") or ""),
            "base_ref": base_ref,
            "base_sha": base_sha,
            "decision": decision,
            "reason_codes": reasons,
            "final_status": final_status,
            "out_dir": str(out_base),
            "promotion_eligible": promotion_eligible,
            "worktree_path": wt_path,
        }
        append_jsonl(ledger_path, entry)
        latest_payload = {
            "schema_version": "xtrl.latest_state/v0.1",
            "timestamp_utc": entry["timestamp_utc"],
            "packet_id": packet_id,
            "repo": entry["repo"],
            "decision": decision,
            "reason_codes": reasons,
            "final_status": final_status,
            "out_dir": str(out_base),
            "base_ref": base_ref,
            "base_sha": base_sha,
            "promotion_eligible": promotion_eligible,
        }
        write_json(latest_path, latest_payload)
    except Exception:
        pass
    write_json(meta_path, meta)

    return 0 if final_status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
