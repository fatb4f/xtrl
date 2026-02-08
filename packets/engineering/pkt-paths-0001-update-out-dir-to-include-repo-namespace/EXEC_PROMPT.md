# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-paths-0001-update-out-dir-to-include-repo-namespace/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-paths-0001-update-out-dir-to-include-repo-namespace/",
  "tasks": [
    "Default OUT_DIR to <repo_root>/out/<repo>/<packet_id>.",
    "Maintain backward compatibility for legacy OUT_DIR paths.",
    "Derive repo namespace correctly for local and remote URLs."
  ],
  "acceptance_checks": [
    "OUT_DIR derivation matches the new scheme and legacy path handling remains functional."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-paths-0001-update-out-dir-to-include-repo-namespace/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-paths-0001-update-out-dir-to-include-repo-namespace/`

## Tasks
1) Default OUT_DIR to <repo_root>/out/<repo>/<packet_id>.
2) Maintain backward compatibility for legacy OUT_DIR paths.
3) Derive repo namespace correctly for local and remote URLs.

## Acceptance checks
- OUT_DIR derivation matches the new scheme and legacy path handling remains functional.

## Evidence
Required artifacts under `<repo_root>/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
