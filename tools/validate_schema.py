#!/usr/bin/env python3
"""Validate JSON files (schema-aware if possible).

Usage:
  python -m tools.validate_schema path/to/file.json [more.json ...]

Behavior:
- Always checks that JSON parses.
- If jsonschema is available and the file looks like a JSON Schema,
  run Draft7 schema validation on itself.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def is_schema(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    return "$schema" in obj or "type" in obj or "properties" in obj


def validate_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if is_schema(data):
        try:
            import jsonschema  # type: ignore
        except Exception:
            return
        jsonschema.Draft7Validator.check_schema(data)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python -m tools.validate_schema <file.json> [more.json ...]", file=sys.stderr)
        return 2
    rc = 0
    for raw in argv[1:]:
        path = Path(raw)
        try:
            validate_file(path)
        except Exception as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
