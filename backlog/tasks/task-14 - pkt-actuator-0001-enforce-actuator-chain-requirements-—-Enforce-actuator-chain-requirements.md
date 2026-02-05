---
id: TASK-14
title: >-
  pkt-actuator-0001-enforce-actuator-chain-requirements — Enforce actuator chain
  requirements
status: To Do
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 17:25'
labels:
  - packet
  - actuator
milestone: P2
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ensure invocation paths are via just → xtrl with explicit repo/root/state args.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Invocation path enforced (just -> xtrl) with explicit repo/root/state args.
- [ ] #2 Non-compliant invocation is rejected with clear reason code.
- [ ] #3 Coverage includes at least one positive and one negative path test.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Validation logic implemented and wired into CLI entry points.
- [ ] #2 Tests passing for new enforcement paths.
<!-- DOD:END -->
