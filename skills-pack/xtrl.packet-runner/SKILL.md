---
name: xtrl.packet-runner
description: Run a packet contract against a target repo with clean-worktree gates and Packet-002 evidence.
---

## Purpose
Execute a packet contract with:
1) Preflight checks
2) Isolated git worktree provisioning
3) Bounded execution
4) Post-run evidence harness (Packet-002)

## Entrypoints
- `scripts/run_packet.sh`
- `scripts/run_packet.py`

## Inputs
- `contract_path` (required): path to JSON contract.
- Optional: `--repo-root`, `--codex-home`, `--resume`

## Outputs
Evidence bundles are written under the xtrl state root:
- `out/<packet_id>/...`

## Notes
The runner resolves the target repo via `--repo-root` or `git rev-parse`.
Artifacts are stored under the state root derived from `CODEX_STATE` (or `XDG_STATE_HOME/codex`).
