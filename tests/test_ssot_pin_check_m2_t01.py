import json
import subprocess
import sys
from pathlib import Path

PIN_CHECK = Path(__file__).resolve().parent.parent / "tools" / "ssot_gate.py"
PIN_FILE = Path(__file__).resolve().parent.parent / "control" / "ssot_pin.json"
SSOT_DIR = Path("/home/src404/src/xtrlv2/control/ssot")


def _load_pinned_hash() -> str:
    data = json.loads(PIN_FILE.read_text(encoding="utf-8"))
    return data["hash"]


def _run_checker(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PIN_CHECK), "pin", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_pin_mismatch_fails(tmp_path: Path) -> None:
    pin_path = tmp_path / "ssot_pin.json"
    pin_path.write_text(
        json.dumps(
            {
                "ssot_root": str(SSOT_DIR),
                "algorithm": "sha256",
                "hash": "deadbeef",
            }
        ),
        encoding="utf-8",
    )

    result = _run_checker("--pin-file", str(pin_path), "--ssot-root", str(SSOT_DIR))

    assert result.returncode != 0
    assert "ssot-pin: mismatch" in result.stderr


def test_pin_match_succeeds(tmp_path: Path) -> None:
    pin_path = tmp_path / "ssot_pin.json"
    pin_path.write_text(
        json.dumps(
            {
                "ssot_root": str(SSOT_DIR),
                "algorithm": "sha256",
                "hash": _load_pinned_hash(),
            }
        ),
        encoding="utf-8",
    )

    result = _run_checker("--pin-file", str(pin_path), "--ssot-root", str(SSOT_DIR))

    assert result.returncode == 0
    assert result.stdout.startswith("ssot-pin: ok")
