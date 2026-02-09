"""Canonical reason codes for xtrl.

Single source of truth for reason-code strings used across:
- gate_worker.json
- linearizer replay/promotion reports
- replay/fuzz harness reports

Keep this list stable; add new codes only with schema + tests.
"""

from __future__ import annotations

from enum import Enum
from typing import Iterable, Set


class ReasonCode(str, Enum):
    # Success / meta
    OK = "OK"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    INTERNAL_ERROR = "INTERNAL_ERROR"

    # Worker gate
    SCHEMA_VALIDATION_FAILED = "SCHEMA_VALIDATION_FAILED"
    ACTION_NOT_FOUND = "ACTION_NOT_FOUND"
    FORBIDDEN_PATH_HIT = "FORBIDDEN_PATH_HIT"
    DIFF_BUDGET_EXCEEDED = "DIFF_BUDGET_EXCEEDED"

    # Linearizer / promotion
    PATCH_APPLY_FAILED = "PATCH_APPLY_FAILED"
    CHECK_FAILED = "CHECK_FAILED"
    STALE_BASE_REF = "STALE_BASE_REF"
    LOCK_UNAVAILABLE = "LOCK_UNAVAILABLE"


ALL_REASON_CODES: Set[str] = {c.value for c in ReasonCode}


def is_valid_reason_code(code: str) -> bool:
    return code in ALL_REASON_CODES


def require_valid_reason_codes(codes: Iterable[str]) -> None:
    bad = [c for c in codes if c not in ALL_REASON_CODES]
    if bad:
        raise ValueError(f"invalid reason_code(s): {bad}")
