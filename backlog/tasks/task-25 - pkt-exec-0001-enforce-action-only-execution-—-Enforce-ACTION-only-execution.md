---
id: TASK-25
title: pkt-exec-0001-enforce-action-only-execution — Enforce ACTION-only execution
status: Done
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 19:02'
labels:
  - packet
  - exec
milestone: ctrlv2-schema-normalization
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enforce ACTION-only execution with an initial warn-only phase (no hard failure for one release cycle).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Execution detects shell-string usage and emits warnings.
- [ ] #2 Warn-only mode does not block execution during the initial release cycle.
- [ ] #3 Telemetry/logging captures shell-execution warnings for review.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Warnings are surfaced in runner output and recorded in evidence (e.g., evidence.json or evidence.md).
- [ ] #2 A follow-up ticket is created to switch from warn-only to hard enforcement after the initial release cycle.
<!-- DOD:END -->
