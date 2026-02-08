# Exec Prompt — pkt-git-0002-worktree-commands

## Phase
P0.4

## Title
Git worktree commands: doctor|wt create|wt status

## Dependencies
pkt-git-0001-gitplant-harness-gates-json

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.git doctor`
- `python -m xtrl.git wt create --packet-id <packet_id>`
- `python -m xtrl.git wt status --packet-id <packet_id>`
