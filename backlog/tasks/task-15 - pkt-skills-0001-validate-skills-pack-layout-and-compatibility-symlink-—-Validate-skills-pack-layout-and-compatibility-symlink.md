---
id: TASK-15
title: >-
  pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink —
  Validate skills-pack layout and compatibility symlink
status: In Progress
assignee: []
created_date: '2026-02-02 21:59'
updated_date: '2026-02-05 18:18'
labels:
  - packet
  - skills
milestone: P2
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Verify skills-pack canonical paths and allow skills/ as a compatibility layer.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Skills-pack canonical paths validated at runtime.
- [ ] #2 Compatibility symlink layer supported (skills/ -> skills-pack) without breaking canonical path usage.
- [ ] #3 Failure modes emit actionable error messages.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Validation checks implemented with tests or fixtures.
- [ ] #2 Docs or help text updated to describe layout expectations.
<!-- DOD:END -->
