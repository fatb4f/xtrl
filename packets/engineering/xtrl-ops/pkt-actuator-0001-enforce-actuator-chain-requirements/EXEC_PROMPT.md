# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-actuator-0001-enforce-actuator-chain-requirements/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-actuator-0001-enforce-actuator-chain-requirements/",
  "tasks": [
    "Enforce invocation path via just -> xtrl with explicit repo/root/state args.",
    "Add tests for allow/deny actuator chain enforcement paths."
  ],
  "acceptance_checks": [
    "Unit tests covering allow/deny enforcement paths pass."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-actuator-0001-enforce-actuator-chain-requirements/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-actuator-0001-enforce-actuator-chain-requirements/`

## Tasks
1) Enforce invocation path via just -> xtrl with explicit repo/root/state args.
2) Add tests for allow/deny actuator chain enforcement paths.

## Acceptance checks
- Unit tests covering allow/deny enforcement paths pass.

## Evidence
Required artifacts under `<repo_root>/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
