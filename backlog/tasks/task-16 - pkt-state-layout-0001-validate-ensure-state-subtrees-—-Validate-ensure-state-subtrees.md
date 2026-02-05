---
id: TASK-16
title: >-
  pkt-state-layout-0001-validate-ensure-state-subtrees — Validate/ensure state
  subtrees
status: Done
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 18:28'
labels:
  - packet
  - state-layout
milestone: P2
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create/validate sessions/history/tmp state subtrees when used.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 State subtrees (sessions/history/tmp) are created when first used.
- [x] #2 Validation detects missing or invalid subtrees and repairs or errors deterministically.
- [x] #3 Behavior is consistent across platforms/OS paths.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 State subtree logic covered by tests or scripted checks.
- [ ] #2 No regressions in existing state usage paths.
<!-- DOD:END -->
