# Exec Prompt — pkt-binding-0002-gen-derived-views-ci-regen-compare

```json
{
  "schema_version": "1.0.0",
  "contract_path": "/home/src404/src/xtrl_packets_phase_P0_4/pkt-binding-0002-gen-derived-views-ci-regen-compare/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Run: python tools/gen_binding_views.py",
    "Run: python tools/ci_regen_compare.py --paths control/plant/binding_dag.json control/plant/binding_dag.mmd"
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
Generate derived binding views + CI regen-and-compare

## Dependencies
pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python tools/gen_binding_views.py`
- `python tools/ci_regen_compare.py --paths control/plant/binding_dag.json control/plant/binding_dag.mmd`
