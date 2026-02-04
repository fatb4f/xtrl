# Exec Prompt — pkt-release-0001-tag-release-on-main

## Phase
P0.4

## Title
Release: tag-based automation on push to main (optional)

## Dependencies
pkt-git-0003-promote-actuator

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.release tag --from-main`
