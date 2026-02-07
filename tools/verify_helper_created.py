#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from verify_utils import find_out_dir, read_json, resolve_state


REQUIRED_FIELDS = [
    "packet_id",
    "run_id",
    "base_ref",
    "base_sha",
    "helper_path",
    "helper_hash",
    "trigger_reason_code",
    "gate_decision_ref",
    "prompt_ref",
    "touched_paths",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def require_ref(obj: dict, label: str) -> None:
    if not isinstance(obj, dict):
        raise SystemExit(f"{label} must be object")
    path = obj.get("path")
    digest = obj.get("sha256")
    if not isinstance(path, str) or not path:
        raise SystemExit(f"{label}.path missing")
    if not isinstance(digest, str) or not digest:
        raise SystemExit(f"{label}.sha256 missing")
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"{label} path missing: {path}")
    actual = sha256(p)
    if actual != digest:
        raise SystemExit(f"{label} sha256 mismatch: {path}")


def is_repo_relative(path: str, repo_root: Path) -> bool:
    p = Path(path)
    if p.is_absolute():
        return False
    try:
        (repo_root / p).resolve().relative_to(repo_root.resolve())
    except Exception:
        return False
    return True


def main() -> int:
    state_root = resolve_state()
    # We do not rely on branch -> packet_id; scan latest out_dir for events.jsonl.
    out_root = state_root / "out"
    candidates = []
    for events_path in out_root.rglob("evidence/events.jsonl"):
        try:
            candidates.append((events_path.stat().st_mtime, events_path))
        except Exception:
            continue
    if not candidates:
        raise SystemExit("evidence/events.jsonl not found")
    events_path = sorted(candidates, key=lambda x: x[0], reverse=True)[0][1]
    out_dir = events_path.parents[1]
    evidence_path = out_dir / "evidence.json"
    if not evidence_path.exists():
        raise SystemExit("evidence.json missing for helper_created verification")
    evidence = read_json(evidence_path)
    repo_root = Path(evidence.get("repo", {}).get("root") or ".").resolve()

    lines = [ln for ln in events_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise SystemExit("events.jsonl is empty")

    found = None
    for ln in lines:
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("event") == "helper_created":
            found = obj
            break
    if not found:
        raise SystemExit("helper_created event not found")

    missing = [k for k in REQUIRED_FIELDS if k not in found]
    if missing:
        raise SystemExit(f"missing fields: {missing}")

    touched_paths = found.get("touched_paths")
    if not isinstance(touched_paths, list) or not touched_paths:
        raise SystemExit("touched_paths must be array")
    diffstat = found.get("diffstat")
    if not isinstance(diffstat, dict):
        raise SystemExit("diffstat required")
    files_changed = diffstat.get("files_changed")
    if not isinstance(files_changed, int) or files_changed <= 0:
        raise SystemExit("diffstat.files_changed must be > 0")
    if "patch_hash" not in found and "diffstat" not in found:
        raise SystemExit("diffstat or patch_hash required")

    helper_path = found.get("helper_path")
    helper_hash = found.get("helper_hash")
    if not isinstance(helper_path, str) or not helper_path:
        raise SystemExit("helper_path invalid")
    if not isinstance(helper_hash, str) or not helper_hash:
        raise SystemExit("helper_hash invalid")
    if not is_repo_relative(helper_path, repo_root):
        raise SystemExit("helper_path must be repo-relative")
    if helper_path not in touched_paths:
        raise SystemExit("helper_path must appear in touched_paths")

    hp = (repo_root / helper_path).resolve()
    if not hp.exists():
        raise SystemExit(f"helper_path missing: {helper_path}")
    actual = sha256(hp)
    if actual != helper_hash:
        raise SystemExit("helper_hash mismatch")

    require_ref(found.get("gate_decision_ref"), "gate_decision_ref")
    require_ref(found.get("prompt_ref"), "prompt_ref")

    # Ensure evidence is under the same out_dir
    expected = out_dir / "evidence" / "events.jsonl"
    if expected.resolve() != events_path.resolve():
        raise SystemExit("events.jsonl not under expected out_dir")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
