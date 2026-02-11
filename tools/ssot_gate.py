#!/usr/bin/env python3
"""SSOT schema pin + conformance gate against xtrlv2 SSOT."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - handled at runtime
    jsonschema = None

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SSOT_ROOT = Path("/home/src404/src/xtrlv2/control/ssot")
DEFAULT_PIN_PATH = REPO_ROOT / "control" / "ssot_pin.json"


@dataclass(frozen=True)
class ValidationTarget:
    name: str
    schema: str
    artifact: str
    format: str = "json"


DEFAULT_VALIDATIONS = [
    ValidationTarget(
        name="latest_state",
        schema="schemas/latest_state.schema.json",
        artifact="tests/fixtures/ssot/latest_state.json",
    ),
    ValidationTarget(
        name="ledger_entry",
        schema="schemas/ledger_entry.schema.json",
        artifact="tests/fixtures/ssot/ledger_entry.json",
    ),
    ValidationTarget(
        name="gate_decision",
        schema="schemas/gate_decision.schema.json",
        artifact="tests/fixtures/ssot/gate_decision.json",
    ),
]


def compute_ssot_hash(root: Path) -> str:
    if not root.exists():
        raise FileNotFoundError(f"SSOT root missing: {root}")
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda p: p.relative_to(root).as_posix(),
    )
    hasher = hashlib.sha256()
    for path in files:
        rel = path.relative_to(root).as_posix()
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def load_pin(pin_path: Path) -> dict:
    if not pin_path.exists():
        raise FileNotFoundError(f"pin file missing: {pin_path}")
    return json.loads(pin_path.read_text(encoding="utf-8"))


def check_pin(ssot_root: Path, pin_path: Path) -> None:
    pin = load_pin(pin_path)
    expected = pin.get("hash")
    if not expected:
        raise SystemExit("ssot-pin: missing hash in pin file")
    actual = compute_ssot_hash(ssot_root)
    if actual != expected:
        raise SystemExit(
            "ssot-pin: mismatch\n"
            f"  expected: {expected}\n"
            f"  actual:   {actual}\n"
            f"  ssot_root: {ssot_root}"
        )
    print(f"ssot-pin: ok ({actual})")


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _type_matches(expected: str, value: object) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def _minimal_validate(schema: dict, instance: object) -> None:
    if schema.get("type") == "object" and not isinstance(instance, dict):
        raise ValueError("instance must be an object")
    required = schema.get("required", [])
    for key in required:
        if not isinstance(instance, dict) or key not in instance:
            raise ValueError(f"missing required field: {key}")
    properties = schema.get("properties", {})
    if isinstance(instance, dict):
        for key, prop in properties.items():
            if key in instance and isinstance(prop, dict) and "type" in prop:
                if not _type_matches(prop["type"], instance[key]):
                    raise ValueError(f"field {key} expected type {prop['type']}")


def _validator(schema_path: Path) -> tuple[str, object]:
    schema = _load_json(schema_path)
    if jsonschema is None:
        return ("minimal", schema)
    resolver = jsonschema.RefResolver(base_uri=schema_path.as_uri(), referrer=schema)
    return ("jsonschema", jsonschema.Draft7Validator(schema, resolver=resolver))


def _validate_json(validator_kind: str, validator: object, payload: object, label: str) -> None:
    if validator_kind == "jsonschema":
        errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            first = errors[0]
            raise SystemExit(f"ssot-conformance: {label}: {first.message}")
        return
    try:
        _minimal_validate(validator, payload)
    except Exception as exc:
        raise SystemExit(f"ssot-conformance: {label}: {exc}") from exc


def _validate_jsonl(validator_kind: str, validator: object, payload: str, label: str) -> None:
    for idx, line in enumerate(payload.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"ssot-conformance: {label} line {idx}: {exc}") from exc
        _validate_json(validator_kind, validator, data, f"{label} line {idx}")


def validate_targets(ssot_root: Path, targets: Iterable[ValidationTarget]) -> None:
    failures = 0
    for target in targets:
        schema_path = ssot_root / target.schema
        artifact_path = REPO_ROOT / target.artifact
        if not schema_path.exists():
            print(f"ssot-conformance: schema missing: {schema_path}")
            failures += 1
            continue
        if not artifact_path.exists():
            print(f"ssot-conformance: artifact missing: {artifact_path}")
            failures += 1
            continue
        validator_kind, validator = _validator(schema_path)
        try:
            if target.format == "jsonl":
                _validate_jsonl(
                    validator_kind,
                    validator,
                    artifact_path.read_text(encoding="utf-8"),
                    str(artifact_path),
                )
            else:
                _validate_json(validator_kind, validator, _load_json(artifact_path), str(artifact_path))
            print(f"ssot-conformance: ok {target.name}")
        except SystemExit as exc:
            print(str(exc))
            failures += 1
    if failures:
        raise SystemExit(f"ssot-conformance: {failures} validation(s) failed")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SSOT schema pin + conformance gate")
    parser.add_argument("command", choices=["pin", "conformance", "all"], nargs="?", default="all")
    parser.add_argument("--ssot-root", default=str(DEFAULT_SSOT_ROOT))
    parser.add_argument("--pin-file", default=str(DEFAULT_PIN_PATH))
    parser.add_argument("--skip-pin", action="store_true", help="skip pin check (conformance only)")
    parser.add_argument("--schema", help="Override schema path for a single conformance check.")
    parser.add_argument("--instance", help="Override instance path for a single conformance check.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ssot_root = Path(args.ssot_root)
    pin_path = Path(args.pin_file)

    if args.command in ("pin", "all"):
        check_pin(ssot_root, pin_path)
    if args.command in ("conformance", "all"):
        if (args.schema is None) != (args.instance is None):
            raise SystemExit("ssot-conformance: both --schema and --instance are required together")
        if args.skip_pin is False and args.command == "conformance":
            check_pin(ssot_root, pin_path)
        if args.schema and args.instance:
            instance_path = Path(args.instance)
            target = ValidationTarget(
                name=instance_path.stem,
                schema=str(Path(args.schema)),
                artifact=str(instance_path),
                format="jsonl" if instance_path.suffix == ".jsonl" else "json",
            )
            validate_targets(ssot_root, [target])
        else:
            validate_targets(ssot_root, DEFAULT_VALIDATIONS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
