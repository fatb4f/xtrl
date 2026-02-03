---
id: TASK-28
title: >-
  pkt-ops-0022-packet-pipeline-plant — Packet pipeline plant (pre_contract →
  xtrl → git promote → Completed)
status: Done
assignee: []
created_date: '2026-02-02 22:42'
updated_date: '2026-02-03 00:02'
labels:
  - xtrl
  - ops
  - pipeline
  - control
milestone: Packet pipeline plant
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Objective: Implement the Packet-as-a-Plant composite pipeline:
precontract_Plant <> backlog_Plant <> packet_Plant <> git_Plant.
End-to-end: PreContract → PromoGate → PacketGenerator → Exec (ACTION-only) → Git promote (S0–S9) → Backlog move to completed, with Completed predicate tied to GateDecision ALLOW, EvidenceCapsule present, and successful git promote.

Deliverables:
D1 PreContract → PromoGate → PacketGenerator: xtrl packet generate emits gate/decision.json and materializes OUT_DIR/{contract.json,exec-prompt.md,packet.json}.
D2 Exec (ACTION-only) + EvidenceCapsule: xtrl exec uses OUT_DIR/contract.json only and emits binding EvidenceCapsule layout.
D3 Git promote (branchless, patch-based): xtrl git promote runs S0–S9, denies binaries/submodules, produces single promoted commit with trailers, writes git evidence under OUT_DIR.
D4 Backlog completion: move task + pre_contract to completed and annotate with commit/evidence path.

DoD:
- Tests for gate behavior, ACTION-only enforcement, promote-denies
- Docs updated with binding nouns (PlantSpec, TransitionSpec, EvidenceCapsule, ReasonCodes)
- No writes outside allowed paths; no .codex/.quint
- Evidence paths deterministic under $CODEX_STATE/xtrl/out/<repo>/<packet_id>/...

Plan:
1) Implement PromoGate validator.
2) Implement xtrl packet generate materialization.
3) Implement xtrl exec ACTION-only + EvidenceCapsule emission.
4) Implement xtrl git promote per GitPlant.
5) Add composite state check helper.
6) Mark backlog task completed only after promote succeeds.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 xtrl packet generate denies invalid PreContract and still emits gate/decision.json
- [ ] #2 xtrl packet generate on ALLOW materializes contract.json, exec-prompt.md, packet.json in OUT_DIR
- [ ] #3 xtrl exec refuses any non-ACTION execution and stops with a reason code
- [ ] #4 xtrl exec emits full binding EvidenceCapsule layout in OUT_DIR
- [ ] #5 xtrl git promote produces single promoted commit with required trailers and denies binaries/submodules
- [ ] #6 Composite Completed predicate is mechanically checkable and true only when all conditions hold
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Promotion PASS: /home/src404/.local/state/codex/xtrl/out/xtrl/pkt-ops-0022-packet-pipeline-plant/git/promotion.json

Evidence: /home/src404/.local/state/codex/xtrl/out/xtrl/pkt-ops-0022-packet-pipeline-plant/
<!-- SECTION:NOTES:END -->
