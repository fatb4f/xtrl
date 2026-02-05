---
id: TASK-4
title: >-
  pkt-binding-0002-gen-derived-views-ci-regen-compare — Generate derived views +
  CI regen-compare gate
status: Done
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-05 17:19'
labels:
  - packet
  - binding
milestone: Phase
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement gen_binding_views.py, generate DAG + PlanCards, add regen-and-compare CI gate.
DoD: CI fails on drift; generated views match SSOT.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 gen_binding_views.py produces DAG + PlanCards
- [x] #2 CI fails on drift
- [x] #3 Generated views match SSOT
<!-- AC:END -->
