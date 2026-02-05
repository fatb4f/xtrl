# Exec Prompt — pkt-exec-0003-packet-generator

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-exec-0003-packet-generator/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.packet generate --pre-contract <path> --out <out_dir>"
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
PacketGenerator: PreContract -> Contract + exec-prompt in OUT_DIR

## Dependencies
pkt-exec-0002-promogate-evaluator

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.packet generate --pre-contract <path> --out <out_dir>`
