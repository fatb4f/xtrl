# Exec Prompt — pkt-git-0003-promote-actuator

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-git-0003-promote-actuator/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.git promote --packet-id <packet_id>"
  ],
  "acceptance_checks": [
    "true"
  ],
  "evidence": [
    "evidence.json",
    "decision_trace.md",
    "signals.json"
  ]
}
```


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
