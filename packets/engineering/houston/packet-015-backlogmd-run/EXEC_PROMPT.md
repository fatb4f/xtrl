# EXEC_PROMPT — packet-015-backlogmd-run

```json
{
  "schema_version": "1.0.0",
  "contract_path": "packets/engineering/houston/packet-015-backlogmd-run/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Verify Backlog.md command surface in the repo.",
    "Emit evidence artifacts."
  ],
  "acceptance_checks": [
    "backlog --help",
    "backlog list --help",
    "backlog board --help",
    "backlog browser --help"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt",
    "raw/changed_paths.txt",
    "raw/tests.txt"
  ]
}
```
