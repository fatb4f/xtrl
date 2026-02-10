# Migration Dependency Matrix

Legend: X depends on Y.

| Work Item | Depends On |
| --- | --- |
| ReasonCodes schema (SSOT) | none |
| Gate decision bundle (SSOT) | ReasonCodes schema |
| helper_created schema | ReasonCodes schema |
| Ledger/latest schemas | ReasonCodes schema |
| Phase E snapshot schemas | ReasonCodes schema |
| xtrl alignment + schema pin | all SSOT schemas above |

## Rationale (short)
- ReasonCodes are referenced by gate decisions, guardrails, and replay/fuzz outcomes.
- Gate decision bundle defines the core decision artifacts B/C/D rely on.
- helper_created / ledger / snapshots are downstream artifacts but should reference SSOT.
- xtrl alignment requires stable SSOT contracts to avoid rework.
