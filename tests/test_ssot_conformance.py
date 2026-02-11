import json
import subprocess
import sys
from pathlib import Path

SSOT_ROOT = Path("/home/src404/src/xtrlv2/control/ssot")
SCHEMA_PATH = SSOT_ROOT / "schemas/reason_codes.schema.json"
INSTANCE_PATH = SSOT_ROOT / "examples/reason_codes.example.json"


def compute_ssot_hash(root: Path) -> str:
    hasher = __import__("hashlib").sha256()
    files = []
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            files.append((rel, path))
    for rel, path in sorted(files):
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(chunk)
    return hasher.hexdigest()


def write_pin(path: Path, digest: str) -> None:
    payload = {
        "hash": digest,
        "algorithm": "sha256",
        "ssot_root": str(SSOT_ROOT),
        "generated_at_utc": "2026-02-11T00:00:00Z",
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_check(*args: str) -> subprocess.CompletedProcess[str]:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "ssot_gate.py"
    cmd = [sys.executable, str(script), "conformance", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_pin_mismatch_fails(tmp_path: Path) -> None:
    pin_path = tmp_path / "pin.json"
    write_pin(pin_path, "deadbeef")
    result = run_check(
        "--pin-file",
        str(pin_path),
        "--ssot-root",
        str(SSOT_ROOT),
        "--schema",
        str(SCHEMA_PATH),
        "--instance",
        str(INSTANCE_PATH),
    )
    assert result.returncode != 0
    assert "ssot-pin: mismatch" in result.stderr


def test_conformance_failure_fails(tmp_path: Path) -> None:
    pin_path = tmp_path / "pin.json"
    write_pin(pin_path, compute_ssot_hash(SSOT_ROOT))
    bad_instance = tmp_path / "bad_instance.json"
    bad_instance.write_text("{}\n", encoding="utf-8")
    result = run_check(
        "--pin-file",
        str(pin_path),
        "--ssot-root",
        str(SSOT_ROOT),
        "--schema",
        str(SCHEMA_PATH),
        "--instance",
        str(bad_instance),
    )
    assert result.returncode != 0
    assert "ssot-conformance" in result.stdout
