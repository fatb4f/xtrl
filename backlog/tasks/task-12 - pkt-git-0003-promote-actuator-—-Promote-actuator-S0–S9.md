---
id: TASK-12
title: pkt-git-0003-promote-actuator — Promote actuator (S0–S9)
status: To Do
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-02 22:06'
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
- [ ] #1 Promotion DAG implemented
- [ ] #2 End-to-end promotion works
- [ ] #3 Evidence emitted on denial
<!-- AC:END -->
