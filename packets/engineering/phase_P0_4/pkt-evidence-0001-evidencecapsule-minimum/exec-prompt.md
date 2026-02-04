# Exec Prompt — pkt-evidence-0001-evidencecapsule-minimum

## Phase
P0.4

## Title
Emit minimum EvidenceCapsule; enforce missing-evidence STOP logic

## Dependencies
pkt-exec-0004-action-only-runner, pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.evidence emit --packet-id <packet_id>`
- `python -m xtrl.evidence check --packet-id <packet_id>`
