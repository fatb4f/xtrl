# xtrl -> xtrlv2 Mapping

## Top-level domains
- CLI/Entrypoint
- control/ssot (schemas, policies, registry)
- packets/contracts
- runtime tools
- state/ledger/out/worktrees
- docs/templates/skills

## Golden path (minimum viable cutover)
- v2 entrypoint runs a dry-run or describe-state action
- control/ssot schemas validated (ReasonCodes + gate decision bundle)
- one golden packet executes and emits evidence under v2 state root

Classification: PORT / REPLACE / DROP / DEFER

| Source | Target | Action | Owner | Depends | Notes |
| --- | --- | --- | --- | --- | --- |
| `control/` | `control/ssot/` | **PORT** | TBD | M1-T01 | SSOT exists in v2; align schemas and policies. |
| `schemas/` | `control/ssot/schemas/` | **REPLACE** | TBD | M1-T01 | v2 owns schemas; map/merge as needed. |
| `tools/` | `tools/` | **PORT** | TBD | M2-T01 | Runtime tooling to be ported selectively. |
| `packets/` | `packets/` | **REPLACE** | TBD | M2-T01 | v2 packet formats may differ; normalize then port. |
| `templates/` | `(tbd)` | **DEFER** | TBD |  | Decide if templates live in v2 or tooling. |
| `docs/` | `docs/` | **PORT** | TBD |  | Migration docs should move; keep as sources of truth. |
| `state/` | `(v2 state root)` | **REPLACE** | TBD | M1-T04 | State layout changes handled in migration tool. |
| `ledger/` | `(v2 state root)` | **REPLACE** | TBD | M1-T04 | Ledger schema and location to be finalized. |
| `out/` | `(v2 state root)` | **REPLACE** | TBD | M1-T02 | Out dir layout to be defined by v2 evidence capsule. |
| `skills/` | `(tbd)` | **DEFER** | TBD |  | Decide: keep in v1 only or port. |
| `skills-pack/` | `(tbd)` | **DEFER** | TBD |  | Decide: keep in v1 only or port. |
| `worktrees/` | `(v2 state root)` | **REPLACE** | TBD | M1-T04 | Worktree layout defined in v2 state model. |
| `xtrl (entrypoint)` | `xtrlv2 entrypoint` | **REPLACE** | TBD | M2-T01 | Define new canonical CLI and wrapper. |
