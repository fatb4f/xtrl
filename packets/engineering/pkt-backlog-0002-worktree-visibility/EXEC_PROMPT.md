# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-backlog-0002-worktree-visibility/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-backlog-0002-worktree-visibility/",
  "tasks": [
    "Map worktrees to backlog tasks deterministically.",
    "Expose mapping via a CLI or report output.",
    "Warn clearly (non-failing) for unmapped worktrees."
  ],
  "acceptance_checks": [
    "CLI/report output shows mappings and emits warnings for unmapped worktrees."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-backlog-0002-worktree-visibility/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-backlog-0002-worktree-visibility/`

## Tasks
1) Map worktrees to backlog tasks deterministically.
2) Expose mapping via a CLI or report output.
3) Warn clearly (non-failing) for unmapped worktrees.

## Acceptance checks
- CLI/report output shows mappings and emits warnings for unmapped worktrees.

## Evidence
Required artifacts under `$CODEX_STATE/xtrl/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
