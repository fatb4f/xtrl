# Exec Prompt — pkt-exec-0004-action-only-runner

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-exec-0004-action-only-runner/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.exec run --packet-id <packet_id>"
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
ACTION-only runner reading OUT_DIR/contract.json; argv-only execution

## Dependencies
pkt-exec-0003-packet-generator

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.exec run --packet-id <packet_id>`
