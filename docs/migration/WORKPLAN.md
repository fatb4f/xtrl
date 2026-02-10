# Migration Workplan (M0–M6)

Scope SSOT: `docs/migration/TRACKER.md`
Decision log SSOT: https://github.com/fatb4f/xtrlv2/issues/1

## Operating rule
- SSOT for scope: `docs/migration/TRACKER.md` (tasks + status).
- SSOT for decisions/notes: xtrlv2#1 (constraints, discussion log, “why”).
- Every milestone produces: a mechanical artifact, evidence output, and a DoD gate.

## Milestone 0 — Migration Control Plane
Goal: freeze scope and make progress measurable.

Deliverables
- `docs/migration/WORKPLAN.md` (this plan)
- `docs/migration/STATUS.md` (single page: current phase + next 3 actions)
- `tools/migration/migrate.py` (skeleton with `--dry-run`)
- Local gate: `just migrate-check`

DoD
- PR adds above and `just migrate-check` passes.

## Milestone 1 — Inventory + Mapping
Goal: deterministic map of xtrl -> xtrlv2.

Deliverables
- `tools/migration/inventory_xtrl.py` emits:
  - `docs/migration/inventory_xtrl.json`
  - `docs/migration/mapping.md`
- `mapping.md` classifies each item as PORT/REPLACE/DROP/DEFER

DoD
- Mapping covers all top-level xtrl concerns and is reproducible.

## Milestone 2 — Entry-point + CLI parity in v2
Goal: define canonical v2 invocation and compatibility shim.

Deliverables
- Documented v2 invocation path
- Optional wrapper that warns and forwards to v2
- `docs/migration/cli_changes.md` old -> new

DoD
- v2 "hello world" run is observable
- Wrapper does not silently mutate v1

## Milestone 3 — State layout + one-time migration tool
Goal: idempotent state migration.

Deliverables
- `tools/migration/state_migrate.py`
- `migration_report.json` + `.md`
- migration report schema
- `doctor` validator

DoD
- Dry-run is precise
- Real run emits report and is idempotent

## Milestone 4 — Packet/contract migration + execution harness
Goal: v2 runs packets with valid evidence.

Deliverables
- v2 packet contracts
- execution harness
- regression tests for evidence tree

DoD
- At least one golden packet runs end-to-end under v2

## Milestone 5 — Cutover + deprecation
Goal: make v2 default.

Deliverables
- docs updated, v1 deprecated
- `docs/migration/cutover.md`

DoD
- Fresh bootstrap runs v2 without touching v1

## Milestone 6 — Cleanup + post-migration validation
Goal: remove shims and lock invariants.

Deliverables
- remove transitional shims
- CI guard rails
- `docs/migration/final_report.md`

DoD
- Tracker 100% complete or deferred items moved out

## Mapping to TRACKER
Each tracker item should record:
- milestone (M0–M6)
- PR name
- evidence file path
- gate/check name

See `docs/migration/TRACKER.md` for task definitions.
