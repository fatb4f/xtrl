# xtrl -> xtrlv2 Mapping

Classification: PORT / REPLACE / DROP / DEFER

| Source | Target | Action | Notes |
| --- | --- | --- | --- |
| `control/` | `control/ssot/` | **PORT** | SSOT already exists in v2; align schemas and policies. |
| `schemas/` | `control/ssot/schemas/` | **REPLACE** | v2 owns schemas; map/merge as needed. |
| `tools/` | `tools/` | **PORT** | Runtime tooling to be ported selectively. |
| `packets/` | `packets/` | **REPLACE** | v2 packet formats may differ; normalize then port. |
| `templates/` | `(tbd)` | **DEFER** | Decide if templates live in v2 or tooling. |
| `docs/` | `docs/` | **PORT** | Migration docs should move; keep as sources of truth. |
| `state/` | `(v2 state root)` | **REPLACE** | State layout changes handled in migration tool. |
| `ledger/` | `(v2 state root)` | **REPLACE** | Ledger schema and location to be finalized. |
| `out/` | `(v2 state root)` | **REPLACE** | Out dir layout to be defined by v2 evidence capsule. |
| `skills/` | `(tbd)` | **DEFER** | Decide: keep in v1 only or port. |
| `skills-pack/` | `(tbd)` | **DEFER** | Decide: keep in v1 only or port. |
| `worktrees/` | `(v2 state root)` | **REPLACE** | Worktree layout defined in v2 state model. |
| `xtrl (entrypoint)` | `xtrlv2 entrypoint` | **REPLACE** | Define new canonical CLI and wrapper. |
