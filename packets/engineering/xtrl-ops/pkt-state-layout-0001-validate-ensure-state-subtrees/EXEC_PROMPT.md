# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-state-layout-0001-validate-ensure-state-subtrees/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-state-layout-0001-validate-ensure-state-subtrees/",
  "tasks": [
    "Create and validate sessions/history/tmp state subtrees on first use.",
    "Ensure deterministic repair or error behavior for missing/invalid subtrees.",
    "Add tests or scripted checks for state subtree handling."
  ],
  "acceptance_checks": [
    "State subtree creation/validation checks pass on a clean state root."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-state-layout-0001-validate-ensure-state-subtrees/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-state-layout-0001-validate-ensure-state-subtrees/`

## Tasks
1) Create and validate sessions/history/tmp state subtrees on first use.
2) Ensure deterministic repair or error behavior for missing/invalid subtrees.
3) Add tests or scripted checks for state subtree handling.

## Acceptance checks
- State subtree creation/validation checks pass on a clean state root.

## Evidence
Required artifacts under `$CODEX_STATE/xtrl/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
