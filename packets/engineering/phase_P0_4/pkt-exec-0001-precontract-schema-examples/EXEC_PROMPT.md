# Exec Prompt — pkt-exec-0001-precontract-schema-examples

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-exec-0001-precontract-schema-examples/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m tools.validate_schema control/spec/pre_contract.schema.json",
    "Run: python -m tools.validate_schema control/spec/examples/pre_contract.example.json"
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
PreContract schema + examples (xtrl.pre_contract/v0.2)

## Dependencies
pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m tools.validate_schema control/spec/pre_contract.schema.json`
- `python -m tools.validate_schema control/spec/examples/pre_contract.example.json`
