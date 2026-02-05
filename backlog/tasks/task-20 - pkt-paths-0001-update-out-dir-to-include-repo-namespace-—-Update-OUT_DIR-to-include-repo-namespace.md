---
id: TASK-20
title: >-
  pkt-paths-0001-update-out-dir-to-include-repo-namespace — Update OUT_DIR to
  include repo namespace
status: In Progress
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 18:25'
labels:
  - packet
  - paths
milestone: P1
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Default OUT_DIR to $CODEX_STATE/xtrl/out/<repo>/<packet_id> with backward-compatible handling if needed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Default OUT_DIR uses $CODEX_STATE/xtrl/out/<repo>/<packet_id>.
- [ ] #2 Backward-compatible handling for legacy OUT_DIR paths exists.
- [ ] #3 Repo namespace correctly derived for local and remote URLs.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Path derivation documented and tested.
- [ ] #2 Existing workflows remain functional or migration is documented.
<!-- DOD:END -->
