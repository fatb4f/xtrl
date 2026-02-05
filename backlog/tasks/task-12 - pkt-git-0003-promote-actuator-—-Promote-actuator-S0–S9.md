---
id: TASK-12
title: pkt-git-0003-promote-actuator — Promote actuator (S0–S9)
status: Done
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-05 17:19'
labels:
  - packet
  - git
milestone: Phase
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement S0–S9 promotion DAG (rebase, deny binaries/submodules, patch build/apply, commit, test+lint, FF-only push).
DoD: promotion works end-to-end; evidence emitted even on denial.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Promotion DAG implemented
- [x] #2 End-to-end promotion works
- [x] #3 Evidence emitted on denial
<!-- AC:END -->
