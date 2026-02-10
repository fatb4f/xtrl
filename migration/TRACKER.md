# Migration Tracker (Authoritative)

Goal: re-establish xtrlv2 as SSOT for post-pivot features, then align xtrl runtime/emitters.

## Source of Truth
- xtrlv2: SSOT schemas and policies
- xtrl: runtime/emitters/adapters

## Current State
- SSOT update landed in xtrlv2: commit `0fdb685`
- New SSOT schemas now include `control_strategy` and `guardrails_bundle` (registered)
- ReasonCodes exist as `reason_codes.json` but still lack a formal JSON Schema
- xtrlv2 gap tracker: https://github.com/fatb4f/xtrlv2/issues/1

## Work Items (ordered, blocking-first)
1. ReasonCodes schema (SSOT) — formalize `reason_codes.json` as a schema-bound artifact.
2. Gate decision bundle — decide gate_worker vs gate_decision+run_manifest+evidence_capsule.
3. helper_created event schema — JSONL envelope + payload.
4. Ledger/latest pointer schemas — if required by runtime.
5. Phase E snapshot schemas — dep_graph, api_surface, module_manifest.
6. Align xtrl emitters/validators to SSOT + pin schema hash.

## Work Item Details (executable checklist)
Format: keep entries short and auditable.

### 1) ReasonCodes schema (SSOT)
- Repo: xtrlv2
- Artifacts: `control/ssot/reason_codes.json`, `control/ssot/schemas/reason_codes.schema.json`
- Schema refs: `reason_codes` v0.1 (new)
- Tests: schema validation; example file validates; negative case for unknown code
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: none

### 2) Gate decision bundle choice
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/gate_decision.schema.json` (and/or gate_worker schema if chosen)
- Schema refs: `gate_decision` v0.1 (+ run_manifest/evidence_capsule if used)
- Tests: schema validation; golden example; negative case for missing reason code
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: ReasonCodes schema

### 3) helper_created event schema
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/helper_event.schema.json` (name TBD), JSONL envelope spec
- Schema refs: helper event v0.1
- Tests: schema validation; example JSONL line validates; negative case for missing required fields
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: ReasonCodes schema

### 4) Ledger/latest pointer schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/ledger_entry.schema.json`, `control/ssot/schemas/latest_state.schema.json` (names TBD)
- Schema refs: ledger/latest v0.1
- Tests: schema validation; example validates; negative case for missing base_ref/run_id
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: ReasonCodes schema

### 5) Phase E snapshot schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/dep_graph.schema.json`, `api_surface.schema.json`, `module_manifest.schema.json` (names TBD)
- Schema refs: snapshots v0.1
- Tests: schema validation; example validates; negative case for unstable ordering
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: ReasonCodes schema

### 6) xtrl alignment + schema pin
- Repo: xtrl
- Artifacts: pinned schema hash file, conformance validator, updated emitters
- Schema refs: all SSOT items above
- Tests: schema pin gate; artifact conformance gate (B–E)
- Status: Not started
- Owner: TBD
- Links: (PR/commit)
- Evidence: (CI run / validation report)
- Blockers: 1–5 complete

## Definition of Done
- SSOT covers all post-pivot artifacts.
- xtrl emits schema-valid artifacts for B–E.
- Drift checks prevent schema divergence.

## Operational Gates (stop rules)
- xtrl cannot add new artifact shapes unless an xtrlv2 schema exists or an approved temporary extension is recorded.
- Schema pin gate must fail on mismatch between xtrl and xtrlv2 schema hash.
- Artifact conformance gate must fail when emitted artifacts violate SSOT schemas.

## Migration Health Signals
- % of emitted artifacts passing SSOT schema validation (CI).
- Count of remaining SSOT gaps (from Work Items 1–5).
- Schema hash pinned + verified (Yes/No).

## References
- xtrlv2 SSOT catch-up: https://github.com/fatb4f/xtrlv2/issues/1
- xtrl schema gap map: `reports/xtrl_vs_xtrlv2_schema_mapping.md`
- alignment checklist: `reports/xtrlv2-cross-repo-alignment-checklist.md`
- pivot report: `reports/xtrlv2-migration-pivot-report.md`
