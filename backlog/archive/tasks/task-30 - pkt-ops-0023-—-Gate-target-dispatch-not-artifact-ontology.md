---
id: TASK-30
title: pkt-ops-0023 — Gate target dispatch (not artifact ontology)
status: To Do
assignee: []
created_date: '2026-02-04 21:52'
labels:
  - xtrl
  - ops
  - control
  - schema
dependencies: []
references:
  - backlog/tasks/pkt-ops-0023-gate-target-dispatch-not-artifact-ontology.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reframe current “artifact kind” enum as internal gate dispatch targets (tags selecting gating functions over an input state), not as an ontology/external taxonomy.

Target mental model:
`gate_fn(gate_target)(input_state) -> GateDecision`

Stability must live in:
- InputState (typed envelope + pointers + computed facts)
- GateDecision (ALLOW|DENY)
- ReasonCodes (small mechanical enum)
- evidence refs (paths + hashes)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 No remaining usage of “artifact kind == type ontology” language in xtrl docs/schemas.
- [ ] #2 All gating interfaces accept input_state + gate_target and return GateDecision with reasons + evidence refs.
- [ ] #3 OSCAL artifacts continue to validate; only internal control IDs are used for gate_target mapping.
- [ ] #4 Tests cover: unknown gate_target, missing required input_state pointers, and reason-code determinism.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Deliverables D1–D5 completed: schema refactor, gate registry/dispatch, stable decision outputs, OSCAL alignment update, docs + tests.
<!-- DOD:END -->
