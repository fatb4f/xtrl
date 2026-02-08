# Exec Prompt — pkt-git-0003-promote-actuator

## Phase
P0.4

## Title
Patch-based promotion actuator (deny binaries/submodules; test+lint; FF-only push)

## Dependencies
pkt-git-0002-worktree-commands, pkt-evidence-0001-evidencecapsule-minimum

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.git promote --packet-id <packet_id>`
