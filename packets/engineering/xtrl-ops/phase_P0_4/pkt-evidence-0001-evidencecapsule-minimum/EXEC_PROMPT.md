# Exec Prompt — pkt-evidence-0001-evidencecapsule-minimum

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-evidence-0001-evidencecapsule-minimum/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.evidence emit --packet-id <packet_id>",
    "Run: python -m xtrl.evidence check --packet-id <packet_id>"
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
Emit minimum EvidenceCapsule; enforce missing-evidence STOP logic

## Dependencies
pkt-exec-0004-action-only-runner, pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.evidence emit --packet-id <packet_id>`
- `python -m xtrl.evidence check --packet-id <packet_id>`
