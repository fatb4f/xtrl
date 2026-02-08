# Exec Prompt — pkt-git-0002-worktree-commands

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-git-0002-worktree-commands/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.git doctor",
    "Run: python -m xtrl.git wt create --packet-id <packet_id>",
    "Run: python -m xtrl.git wt status --packet-id <packet_id>"
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
