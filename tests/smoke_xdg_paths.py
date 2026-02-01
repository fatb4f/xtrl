#!/usr/bin/env python3
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from path_utils import resolve_state_root
import run_packet


@contextmanager
def with_env(env_updates):
    old = dict(os.environ)
    os.environ.update(env_updates)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old)


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_state_root_uses_xdg_state():
    with tempfile.TemporaryDirectory() as tmp:
        xdg_state = Path(tmp) / "state"
        xdg_config = Path(tmp) / "config"
        codex_home = xdg_config / "codex"
        env = {
            "CODEX_STATE": "",
            "XDG_STATE_HOME": str(xdg_state),
            "XDG_CONFIG_HOME": str(xdg_config),
            "CODEX_HOME": str(codex_home),
        }
        with with_env(env):
            state_root = resolve_state_root(None, str(codex_home))
        expected = (xdg_state / "codex" / "xtrl").resolve()
        assert_true(state_root == expected, f"state_root mismatch: {state_root} != {expected}")
        assert_true(str(codex_home) not in str(state_root), "state_root should not live under CODEX_HOME")


def test_state_root_override_flag():
    with tempfile.TemporaryDirectory() as tmp:
        codex_state = Path(tmp) / "custom_state"
        state_root = resolve_state_root(str(codex_state), None)
        expected = (codex_state / "xtrl").resolve()
        assert_true(state_root == expected, f"state_root override mismatch: {state_root} != {expected}")


def test_run_packet_accepts_codex_state():
    args = run_packet.parse_args(["run_packet.py", "contract.json", "--codex-state", "/tmp/codex-state"])
    assert_true(args.codex_state == "/tmp/codex-state", "run_packet did not accept --codex-state")


def main():
    failures = []
    for test in (test_state_root_uses_xdg_state, test_state_root_override_flag, test_run_packet_accepts_codex_state):
        try:
            test()
        except Exception as exc:
            failures.append(f"{test.__name__}: {exc}")
    if failures:
        print("SMOKE FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("SMOKE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
