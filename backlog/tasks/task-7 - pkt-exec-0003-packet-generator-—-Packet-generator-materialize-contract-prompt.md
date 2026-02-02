---
id: TASK-7
title: >-
  pkt-exec-0003-packet-generator — Packet generator (materialize contract +
  prompt)
status: To Do
assignee: []
created_date: '2026-02-02 21:55'
updated_date: '2026-02-02 22:06'
labels:
  - packet
  - exec
milestone: Phase
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
xtrl packet generate <pre_contract.json> materializes contract.json, exec-prompt.md, packet.json into OUT_DIR.
DoD: generator is the only path to a run-ready contract; outputs always written to OUT_DIR.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 packet generate writes contract.json
- [ ] #2 packet generate writes exec-prompt.md
- [ ] #3 packet generate writes packet.json
- [ ] #4 Outputs always in OUT_DIR
<!-- AC:END -->
