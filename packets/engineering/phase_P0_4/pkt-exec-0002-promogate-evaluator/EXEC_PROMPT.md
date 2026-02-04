# Exec Prompt — pkt-exec-0002-promogate-evaluator

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-exec-0002-promogate-evaluator/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m xtrl.promogate eval --pre-contract <path> --out <out_dir>"
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
Implement PromoGate evaluator (deny-fast) + GateDecision emission

## Dependencies
pkt-exec-0001-precontract-schema-examples, pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m xtrl.promogate eval --pre-contract <path> --out <out_dir>`
