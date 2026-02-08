# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/pkt-evidence-0002-implement-evidencecapsule-v0-2-layout/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/pkt-evidence-0002-implement-evidencecapsule-v0-2-layout/",
  "tasks": [
    "Emit EvidenceCapsule v0.2 directory layout under OUT_DIR.",
    "Always emit minimum required signals for PASS and FAIL.",
    "Align emitted layout with v0.2 schema expectations."
  ],
  "acceptance_checks": [
    "Sample PASS and FAIL runs produce v0.2 layout with required files present."
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Contract
- Contract path: `$CODEX_STATE/xtrl/packets/engineering/pkt-evidence-0002-implement-evidencecapsule-v0-2-layout/contract.json`

## Execution location
- Worktree root: `$CODEX_STATE/xtrl/worktrees/pkt-evidence-0002-implement-evidencecapsule-v0-2-layout/`

## Tasks
1) Emit EvidenceCapsule v0.2 directory layout under OUT_DIR.
2) Always emit minimum required signals for PASS and FAIL.
3) Align emitted layout with v0.2 schema expectations.

## Acceptance checks
- Sample PASS and FAIL runs produce v0.2 layout with required files present.

## Evidence
Required artifacts under `<repo_root>/out/<packet_id>/`:
- `summary.md`
- `raw/diffstat.txt`
