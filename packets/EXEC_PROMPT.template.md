# EXEC_PROMPT (Template)

Use this template to define the execution contract for a packet. Keep it short and
unambiguous. Replace all placeholders.

```json
{
  "schema_version": "1.0.0",
  "contract_path": "{{contract_path}}",
  "worktree_root": "{{worktree_root}}",
  "tasks": [
    "<task 1>",
    "<task 2>"
  ],
  "acceptance_checks": [
    "<command or check>"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/<area>/<packet_id>/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/<packet_id>/`

## Tasks
1) <task 1>
2) <task 2>

## Acceptance checks
- <command or check> (required)

## Evidence
Required artifacts under `$CODEX_STATE/xtrl/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
- <any additional raw outputs>
