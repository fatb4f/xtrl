---
id: TASK-9
title: >-
  pkt-evidence-0001-evidencecapsule-minimum — EvidenceCapsule minimum +
  enforcement
status: Done
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-05 17:19'
labels:
  - packet
  - evidence
milestone: Phase
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Emit minimum required evidence files/signals and enforce missing evidence STOP logic per binding rules.
DoD: PASS produces full capsule; FAIL produces capsule + reason codes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PASS run produces full capsule
- [x] #2 FAIL run produces capsule
- [x] #3 Reason codes emitted on failure
<!-- AC:END -->
