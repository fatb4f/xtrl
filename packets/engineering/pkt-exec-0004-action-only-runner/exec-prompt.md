# Exec Prompt — pkt-exec-0004-action-only-runner

## Phase
P0.4

## Title
ACTION-only runner reading OUT_DIR/contract.json; argv-only execution

## Dependencies
pkt-exec-0003-packet-generator

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.exec run --packet-id <packet_id>`
