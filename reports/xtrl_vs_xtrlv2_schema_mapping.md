# xtrl vs xtrlv2 Schema Mapping (Initial)

Generated: 2026-02-09

## Summary
This is a first-pass mapping between xtrl repo schemas and the xtrlv2 SSOT schemas. It highlights
conceptual overlaps, missing SSOT coverage, and candidate consolidation targets.

## xtrl schemas (repo root `schemas/`)
- contract.schema.json
- exec_prompt.schema.json
- plant.schema.json
- gate_worker.schema.json
- reason_codes.schema.json
- xtrl.gate_worker.v0.1.schema.json
- xtrl.reason_codes.v0.1.schema.json

## xtrlv2 SSOT schemas (`control/ssot/schemas/`)
- candidate_set.schema.json
- evidence_capsule.schema.json
- fuzz_mutation_report.schema.json
- fuzz_replay_report.schema.json
- gate_decision.schema.json
- next_iter_plan.schema.json
- patch_proposal.schema.json
- pattern_catalog.schema.json
- plant_spec.schema.json
- rank_policy.schema.json
- run_manifest.schema.json
- src_conventions.schema.json
- state_space.schema.json
- work_queue.schema.json
- _common.json

## Mapping table (conceptual)
| xtrl artifact | Closest xtrlv2 SSOT schema | Notes | Gap status |
| --- | --- | --- | --- |
| plant.schema.json | plant_spec.schema.json | Naming mismatch only; align field naming and IDs. | Align needed |
| gate_worker.schema.json | gate_decision.schema.json + run_manifest.schema.json + evidence_capsule.schema.json | xtrl gate_worker is a worker-specific decision artifact; xtrlv2 splits into gate_decision + run_manifest + evidence capsule. | Needs SSOT decision |
| reason_codes.schema.json | (none) | No SSOT reason code enum yet. | Missing SSOT |
| xtrl.reason_codes.v0.1.schema.json | (none) | Candidate SSOT enum source. | Missing SSOT |
| xtrl.gate_worker.v0.1.schema.json | gate_decision.schema.json | If gate_worker persists, SSOT should include a schema for it. | Missing SSOT |
| contract.schema.json | (none) | xtrlv2 doesn’t currently expose a contract schema. | Missing SSOT |
| exec_prompt.schema.json | (none) | xtrlv2 doesn’t currently expose an exec prompt schema. | Missing SSOT |

## xtrlv2 schemas not represented in xtrl
| xtrlv2 schema | xtrl candidate artifact | Notes |
| --- | --- | --- |
| candidate_set.schema.json | candidate index (Phase C) | xtrl has candidate_index.json in Phase C; needs SSOT match. |
| evidence_capsule.schema.json | evidence JSONL + out dir layout | xtrl evidence is partially aligned but schema not referenced directly. |
| gate_decision.schema.json | decision.md/decision.json | xtrl emits decision.md; needs schema-bound JSON. |
| next_iter_plan.schema.json | next_iter_plan.json | xtrl Phase D requires next_iter_plan.json. |
| patch_proposal.schema.json | patch/commit promotion | xtrl uses patch-based promotion; missing explicit schema. |
| run_manifest.schema.json | run manifest | xtrl has run manifests but not schema-bound. |
| src_conventions.schema.json | src conventions | Phase E requests conventions; SSOT exists in xtrlv2. |
| state_space.schema.json | state_space.json | Phase A describes state; schema exists in xtrlv2. |
| work_queue.schema.json | queue/linearizer | xtrl Phase C should map to this. |
| fuzz_replay_report.schema.json | replay reports | Phase C/D use replay_report.*; should align. |
| fuzz_mutation_report.schema.json | mutation reports | Phase D/E use fuzz reports; should align. |

## SSOT catch-up priority (blocking-first)
1. ReasonCodes enum (add to xtrlv2 SSOT)
2. gate_worker decision artifact OR confirm gate_decision + run_manifest is the replacement
3. helper_created event schema (JSONL envelope + event shape)
4. ledger/latest pointer schemas (if relied on)
5. Phase E snapshots (dep_graph, api_surface, module_manifest)

## Recommended next steps
1. Add a ReasonCodes schema in xtrlv2 and update xtrl to reference it.
2. Decide gate_worker vs gate_decision bundle and encode in SSOT.
3. Align Phase C/D/E report names to SSOT schemas.
4. Pin xtrl to xtrlv2 schema hash once SSOT updates land.
