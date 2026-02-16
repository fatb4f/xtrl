# Migration Tracker (Authoritative)

Goal: re-establish xtrlv2 as SSOT for post-pivot features, then align xtrl runtime/emitters.

## Source of Truth
- xtrlv2: SSOT schemas and policies
- xtrl: runtime/emitters/adapters

## Current State
- SSOT catch-up landed in xtrlv2: commit `328806e`
- M1-T01..M1-T05 are complete in xtrlv2 (reason codes, gate bundle decision, helper event, ledger/latest, src snapshots)
- xtrl schema pin + conformance gates implemented locally for M2-T01
- xtrlv2 gap tracker: https://github.com/fatb4f/xtrlv2/issues/1

## Work Items (ordered, blocking-first)
1. **M1-T01** ReasonCodes schema (SSOT) — formalize `reason_codes.json` as a schema-bound artifact.
2. **M1-T02** Gate decision bundle — decide gate_worker vs gate_decision+run_manifest+evidence_capsule.
3. **M1-T03** helper_created event schema — JSONL envelope + payload.
4. **M1-T04** Ledger/latest pointer schemas — if required by runtime.
5. **M1-T05** Phase E snapshot schemas — dep_graph, api_surface, module_manifest.
6. **M2-T01** Align xtrl emitters/validators to SSOT + pin schema hash.

## Work Item Details (executable checklist)
Format: keep entries short and auditable.

### M1-T01 — ReasonCodes schema (SSOT)
- Repo: xtrlv2
- Artifacts: `control/ssot/reason_codes.json`, `control/ssot/schemas/reason_codes.schema.json`
- Schema refs: `reason_codes` v0.1 (new)
- Tests: schema validation; example file validates; negative case for unknown code
- Status: Done (xtrlv2)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence: xtrlv2 commit `328806e` (`feat(ssot): complete M1 schema catch-up (T01-T05)`)
- Blockers: none

### M1-T02 — Gate decision bundle choice
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/gate_decision.schema.json` (and/or gate_worker schema if chosen)
- Schema refs: `gate_decision` v0.1 (+ run_manifest/evidence_capsule if used)
- Tests: schema validation; golden example; negative case for missing reason code
- Status: Done (xtrlv2)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence: xtrlv2 commit `328806e`; decision record in `docs/migration/decisions/M1-T02-gate-bundle.md`
- Blockers: none

### M1-T03 — helper_created event schema
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/helper_event.schema.json` (name TBD), JSONL envelope spec
- Schema refs: helper event v0.1
- Tests: schema validation; example JSONL line validates; negative case for missing required fields
- Status: Done (xtrlv2)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence: xtrlv2 commit `328806e`; schema `control/ssot/schemas/helper_event.schema.json`
- Blockers: none

### M1-T04 — Ledger/latest pointer schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/ledger_entry.schema.json`, `control/ssot/schemas/latest_state.schema.json` (names TBD)
- Schema refs: ledger/latest v0.1
- Tests: schema validation; example validates; negative case for missing base_ref/run_id
- Status: Done (xtrlv2)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence: xtrlv2 commit `328806e`; schemas `control/ssot/schemas/ledger_entry.schema.json`, `control/ssot/schemas/latest_state.schema.json`
- Blockers: none

### M1-T05 — Phase E snapshot schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/dep_graph.schema.json`, `api_surface.schema.json`, `module_manifest.schema.json` (names TBD)
- Schema refs: snapshots v0.1
- Tests: schema validation; example validates; negative case for unstable ordering
- Status: Done (xtrlv2)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence: xtrlv2 commit `328806e`; schemas `dep_graph`, `api_surface`, `module_manifest`
- Blockers: none

### M2-T01 — xtrl alignment + schema pin
- Repo: xtrl
- Artifacts: pinned schema hash file, conformance validator, updated emitters
- Schema refs: all SSOT items above
- Tests: schema pin gate; artifact conformance gate (B–E)
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema pin + artifact conformance
- Evidence: 2026-02-11 Files: `control/ssot_pin.json`, `Justfile`, `tools/ssot_gate.py`, `tests/test_ssot_conformance.py`, `tests/test_ssot_pin_check_m2_t01.py`, `docs/migration/TRACKER.md` Commands: `just ssot-pin-check` (output: `ssot-pin: ok (53b0e967ba58a7e42ed2606b1163de84c89182f5de9562f6bc7c92573c405053)`), `pytest -q tests/test_ssot_pin_check_m2_t01.py tests/test_ssot_conformance.py` (output: `4 passed in 0.39s`) Commit: not committed
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
