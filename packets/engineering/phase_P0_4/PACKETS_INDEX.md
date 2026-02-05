# Packet Set

- Phase: **P0.4**
- Generated: 2026-02-02
- Owner: TBD
- Source: TBD
- Revision: TBD

## Packets (in order)

1. `[Done]` `pkt-binding-0001-binding-ssot-schemas` — Binding SSOT schemas + seed instances
2. `[Done]` `pkt-binding-0002-gen-derived-views-ci-regen-compare` — Generate derived binding views + CI regen-and-compare
3. `[Done]` `pkt-exec-0001-precontract-schema-examples` — PreContract schema + examples (xtrl.pre_contract/v0.2)
4. `[Done]` `pkt-exec-0002-promogate-evaluator` — Implement PromoGate evaluator (deny-fast) + GateDecision emission
5. `[Done]` `pkt-exec-0003-packet-generator` — PacketGenerator: PreContract -> Contract + exec-prompt in OUT_DIR
6. `[Done]` `pkt-exec-0004-action-only-runner` — ACTION-only runner reading OUT_DIR/contract.json; argv-only execution
7. `[Done]` `pkt-evidence-0001-evidencecapsule-minimum` — Emit minimum EvidenceCapsule; enforce missing-evidence STOP logic
8. `[Done]` `pkt-git-0001-gitplant-harness-gates-json` — GitPlant harness + dry-run gates.json emission
9. `[Done]` `pkt-git-0002-worktree-commands` — Git worktree commands: doctor|wt create|wt status
10. `[Done]` `pkt-git-0003-promote-actuator` — Patch-based promotion actuator (deny binaries/submodules; test+lint; FF-only push)
11. `[Done]` `pkt-release-0001-tag-release-on-main` — Release: tag-based automation on push to main (optional)
