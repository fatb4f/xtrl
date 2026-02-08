# Exec Prompt — pkt-binding-0001-binding-ssot-schemas

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-binding-0001-binding-ssot-schemas/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python -m tools.validate_schema control/spec/binding/plant_spec.json",
    "Run: python -m tools.validate_schema control/spec/binding/ruleset.json"
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
Binding SSOT schemas + seed instances

## Dependencies
(none)

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m tools.validate_schema control/spec/binding/plant_spec.json`
- `python -m tools.validate_schema control/spec/binding/ruleset.json`
