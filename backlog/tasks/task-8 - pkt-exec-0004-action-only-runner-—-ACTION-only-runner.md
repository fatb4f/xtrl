---
id: TASK-8
title: pkt-exec-0004-action-only-runner — ACTION-only runner
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
xtrl exec <packet_id> reads OUT_DIR/contract.json and executes argv arrays only.
DoD: shell strings rejected; only declared actions runnable.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Reads OUT_DIR/contract.json
- [x] #2 Rejects shell strings
- [x] #3 Runs only declared actions
<!-- AC:END -->
