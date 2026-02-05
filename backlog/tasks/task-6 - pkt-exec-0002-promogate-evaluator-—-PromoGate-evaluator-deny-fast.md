---
id: TASK-6
title: pkt-exec-0002-promogate-evaluator — PromoGate evaluator (deny-fast)
status: Done
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-05 17:19'
labels:
  - packet
  - exec
milestone: Phase
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement PromoGate checks exactly as listed (required fields, mode/budgets, argv-only, allowed_paths, forbidden roots, etc.).
DoD: deny-fast works; GateDecision emitted to OUT_DIR on ALLOW and DENY.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Deny-fast checks implemented
- [x] #2 GateDecision emitted on ALLOW
- [x] #3 GateDecision emitted on DENY
<!-- AC:END -->
