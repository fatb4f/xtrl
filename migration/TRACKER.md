# Migration Tracker (Authoritative)

Goal: re-establish xtrlv2 as SSOT for post-pivot features, then align xtrl runtime/emitters.

## Source of Truth
- xtrlv2: SSOT schemas and policies
- xtrl: runtime/emitters/adapters

## Current State
- SSOT update landed in xtrlv2: commit `0fdb685`
- xtrlv2 gap tracker: https://github.com/fatb4f/xtrlv2/issues/1

## Work Items (ordered, blocking-first)
1. ReasonCodes schema (SSOT) — formalize `reason_codes.json` as a schema-bound artifact.
2. Gate decision bundle — decide gate_worker vs gate_decision+run_manifest+evidence_capsule.
3. helper_created event schema — JSONL envelope + payload.
4. Ledger/latest pointer schemas — if required by runtime.
5. Phase E snapshot schemas — dep_graph, api_surface, module_manifest.
6. Align xtrl emitters/validators to SSOT + pin schema hash.

## Definition of Done
- SSOT covers all post-pivot artifacts.
- xtrl emits schema-valid artifacts for B–E.
- Drift checks prevent schema divergence.

## References
- xtrlv2 SSOT catch-up: https://github.com/fatb4f/xtrlv2/issues/1
- xtrl schema gap map: `reports/xtrl_vs_xtrlv2_schema_mapping.md`
- alignment checklist: `reports/xtrlv2-cross-repo-alignment-checklist.md`
- pivot report: `reports/xtrlv2-migration-pivot-report.md`
