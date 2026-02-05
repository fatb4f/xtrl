---
id: TASK-29
title: >-
  pkt-ops-0023-gate-target-dispatch — Gate target dispatch (not artifact
  ontology)
status: In Progress
assignee: []
created_date: '2026-02-03 00:04'
updated_date: '2026-02-05 19:06'
labels:
  - xtrl
  - ops
  - control
  - schema
milestone: ctrlv2-schema-normalization
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Objective:
Reframe “artifact kind” enums as internal gate dispatch targets (not ontology/taxonomy).
Gate model: gate_fn(gate_target)(input_state) -> GateDecision.
Stability must live in InputState, GateDecision, ReasonCodes, and evidence refs.

Deliverables:
D1 Schema refactor: rename artifact_kind -> gate_target; add input_state with state_kind, paths, facts.
D2 Gate registry + dispatch mapping gate_target -> gate_fn.
D3 Decision outputs: decision ALLOW|DENY, reason_codes, evidence_refs[{path, sha256, role}].
D4 OSCAL alignment: gate_target maps to internal control IDs; artifacts remain back-matter.resources; observations/findings reference resources.
D5 Docs + tests: clarify dispatch vs ontology; tests for dispatch resolution, input_state typing, deny-fast on unknown gate_target.

Acceptance Criteria:
- No remaining usage of “artifact kind == type ontology” language in docs/schemas.
- All gating interfaces accept input_state + gate_target and return GateDecision with reasons + evidence refs.
- OSCAL artifacts validate; only internal control IDs used for gate_target mapping.
- Tests cover unknown gate_target, missing input_state pointers, and reason-code determinism.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 No remaining usage of “artifact kind == type ontology” language in docs/schemas
- [ ] #2 All gating interfaces accept input_state + gate_target and return GateDecision with reasons + evidence refs
- [ ] #3 OSCAL artifacts validate; only internal control IDs used for gate_target mapping
- [ ] #4 Tests cover unknown gate_target, missing input_state pointers, and reason-code determinism
<!-- AC:END -->
