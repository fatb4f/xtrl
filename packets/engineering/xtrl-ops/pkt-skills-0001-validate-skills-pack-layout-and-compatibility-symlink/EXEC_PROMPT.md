# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink/",
  "tasks": [
    "Validate canonical skills-pack layout at runtime.",
    "Support compatibility symlink layer (skills/ -> skills-pack) without breaking canonical paths.",
    "Update docs/help text for skills-pack layout expectations."
  ],
  "acceptance_checks": [
    "Validation passes for canonical and compatibility layouts and fails with actionable errors for invalid layouts."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink/`

## Tasks
1) Validate canonical skills-pack layout at runtime.
2) Support compatibility symlink layer (skills/ -> skills-pack) without breaking canonical paths.
3) Update docs/help text for skills-pack layout expectations.

## Acceptance checks
- Validation passes for canonical and compatibility layouts and fails with actionable errors for invalid layouts.

## Evidence
Required artifacts under `<repo_root>/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
