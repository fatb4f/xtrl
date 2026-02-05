# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-evidence-0001-xtrl-ops-v0-2-contract-schema-adoption/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-evidence-0001-xtrl-ops-v0-2-contract-schema-adoption/",
  "tasks": [
    "Extend contract schema to include constraints/actions/evidence.required_files.",
    "Update validators to enforce the new fields.",
    "Provide a backward-compat migration/default path for legacy contracts."
  ],
  "acceptance_checks": [
    "Schema validation passes for v0.2 examples and legacy examples with migration/defaults."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-evidence-0001-xtrl-ops-v0-2-contract-schema-adoption/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-evidence-0001-xtrl-ops-v0-2-contract-schema-adoption/`

## Tasks
1) Extend contract schema to include constraints/actions/evidence.required_files.
2) Update validators to enforce the new fields.
3) Provide a backward-compat migration/default path for legacy contracts.

## Acceptance checks
- Schema validation passes for v0.2 examples and legacy examples with migration/defaults.

## Evidence
Required artifacts under `$CODEX_STATE/xtrl/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
