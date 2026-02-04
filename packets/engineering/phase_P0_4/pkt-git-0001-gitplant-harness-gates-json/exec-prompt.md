# Exec Prompt — pkt-git-0001-gitplant-harness-gates-json

## Phase
P0.4

## Title
GitPlant harness + dry-run gates.json emission

## Dependencies
(none)

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.git dry-run --out <out_dir>`
