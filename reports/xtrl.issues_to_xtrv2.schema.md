# xtrl Issue Work-Items → xtrlv2 Schema Mapping

This report maps the current xtrl phase issue work-items (#61–#64) to the xtrlv2 SSOT schemas under `xtrlv2/control/ssot/schemas/`. It highlights direct matches, partial matches, and gaps.

## Summary Fit Table

| Issue | Phase | Primary xtrlv2 Schema Targets | Fit |
| --- | --- | --- | --- |
| #61 | Phase B — gate_worker + sensors | `gate_decision.schema.json`, `run_manifest.schema.json`, `evidence_capsule.schema.json` | Medium |
| #62 | Phase C — candidate queue + linearizer replay | `candidate_set.schema.json`, `patch_proposal.schema.json`, `work_queue.schema.json` | High |
| #63 | Phase D — deny recovery + replay/fuzz + policy | `next_iter_plan.schema.json`, `fuzz_replay_report.schema.json`, `fuzz_mutation_report.schema.json`, `rank_policy.schema.json` | High |
| #64 | Phase E — src lineage + replay/fuzz | `src_conventions.schema.json`, `state_space.schema.json`, `fuzz_replay_report.schema.json`, `fuzz_mutation_report.schema.json` | Medium |

## Phase B (#61) — Worker gate artifact + real sensors

**Goal:** authoritative worker gate artifact with stable reason codes and facts.

**Closest xtrlv2 mappings**
- `gate_decision.schema.json`: decision + reason code payloads.
- `run_manifest.schema.json`: execution metadata and facts (diff metrics, budgets, tool versions).
- `evidence_capsule.schema.json`: evidence pointer aggregation.

**Gaps / deltas**
- xtrl has a dedicated `gate_worker.json` artifact; xtrlv2 has no direct `gate_worker` schema.
- Transcript hygiene (stdout/stderr separation, JSONL-only events) is a validator/policy requirement, not a schema.
- Canonical reason-code enum currently lives in xtrl; xtrlv2 lacks a dedicated reason-code schema.

**Fit:** Medium (conceptual alignment; not 1:1 schema).

## Phase C (#62) — Concurrency-safe candidates + authoritative linearizer replay

**Goal:** deterministic replay/promotion with concurrency-safe candidate handling.

**Direct xtrlv2 mappings**
- `candidate_set.schema.json`: candidate index, stale filtering, base refs.
- `patch_proposal.schema.json`: patch hashes + provenance.
- `work_queue.schema.json`: queueing/linearizer input set (concurrency-safe candidates).

**Secondary mappings**
- `run_manifest.schema.json`: replay metadata, lock status, check results.
- `gate_decision.schema.json`: replay decision + reason code.

**Fit:** High (Phase C maps well to candidate/patch/queue schemas).

## Phase D (#63) — Denied-promo recovery + replay/fuzz + policy

**Goal:** deterministic next-iteration plan + replay/fuzz with stable policy mapping.

**Direct xtrlv2 mappings**
- `next_iter_plan.schema.json`: deny scope, next base ref, carry-forward, stale candidates.
- `fuzz_replay_report.schema.json`: corpus replay outputs.
- `fuzz_mutation_report.schema.json`: mutation fuzz outputs.
- `rank_policy.schema.json`: adaptation policy mapping (signal → strategy).

**Fit:** High (Phase D is nearly a direct mapping).

## Phase E (#64) — src lineage + validation spine

**Goal:** deterministic src snapshots + describe_src + replay/fuzz.

**Direct xtrlv2 mappings**
- `src_conventions.schema.json`: constraints for src layer.
- `state_space.schema.json`: state snapshot container (if src state is modeled as a sub-domain).
- `fuzz_replay_report.schema.json` / `fuzz_mutation_report.schema.json`: replay/fuzz outputs.

**Gaps / deltas**
- No explicit xtrlv2 schemas for `dep_graph.json`, `api_surface.json`, `module_manifest.json`.
- Phase E snapshot artifacts are currently implicit; would benefit from schema additions.

**Fit:** Medium (needs dedicated snapshot schemas to be a tight match).

## Cross-cutting gaps

1) **Canonical ReasonCode enum**
- xtrl now has a single enum + schema; xtrlv2 does not.
- Adding a `reason_codes.schema.json` in xtrlv2 would improve alignment across B/C/D/E.

2) **Snapshot schemas for Phase E**
- Add explicit schemas for dep graph, API surface, and module manifest to match Phase E artifacts.

3) **Transcript hygiene**
- JSONL-only events + stdout/stderr separation are policy/validation concerns, not schema fields.
- Consider a validator spec or policy schema in xtrlv2 if you want strict formalization.

## Recommendation

- **Short term:** treat Phase B/C/D as aligned to xtrlv2 with minor gaps (ReasonCode enum + gate_worker schema).
- **Mid term:** add explicit snapshot schemas in xtrlv2 to align Phase E.
- **Long term:** consider a validator/policy spec to formalize transcript hygiene.
