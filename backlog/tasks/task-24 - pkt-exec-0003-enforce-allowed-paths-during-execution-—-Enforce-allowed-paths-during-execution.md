---
id: TASK-24
title: >-
  pkt-exec-0003-enforce-allowed-paths-during-execution — Enforce allowed paths
  during execution
status: To Do
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 18:52'
labels:
  - packet
  - exec
milestone: ctrlv2-schema-normalization
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enforce allowed paths during execution with an initial warn-only phase (no hard failure for one release cycle).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Execution checks for allowed paths and emits warnings when violations occur.
- [ ] #2 Warn-only mode does not block execution during the initial release cycle.
- [ ] #3 Telemetry/logging captures path-violation warnings for review.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Warnings are surfaced in runner output and recorded in evidence (e.g., evidence.json or evidence.md).
- [ ] #2 A follow-up ticket is created to switch from warn-only to hard enforcement after the initial release cycle.
<!-- DOD:END -->
