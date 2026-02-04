# Exec Prompt — pkt-exec-0003-packet-generator

## Phase
P0.4

## Title
PacketGenerator: PreContract -> Contract + exec-prompt in OUT_DIR

## Dependencies
pkt-exec-0002-promogate-evaluator

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.packet generate --pre-contract <path> --out <out_dir>`
