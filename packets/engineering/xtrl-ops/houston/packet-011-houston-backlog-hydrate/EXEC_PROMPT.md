# EXEC_PROMPT — packet-011-houston-backlog-hydrate

## Contract
- contract_path: packets/engineering/packet-011-houston-backlog-hydrate/contract.json
- worktree_root: $CODEX_STATE/xtrl/worktrees

## Intent
Add network-enabled backlog hydration for Houston-in-xtrl. Hydrate richer metadata from issue/PR refs referenced by the Houston backlog index packet, store it in $CODEX_STATE cache, and keep the renderer deterministic.

## Requirements (must)
1) Add a hydrator tool:
   - Path: tools/houston/hydrate.py
   - Inputs:
     - data/houston/index.packet.json (SSOT items and refs)
     - optional: targets registry if present (do not require)
   - Outputs (disk state only):
     - $CODEX_STATE/xtrl/cache/houston/refs/<ref_key>.json
     - $CODEX_STATE/xtrl/cache/houston/cache.manifest.json (or equivalent)
   - Modes:
     - --offline (no network; cache-only; never errors if cache missing, but reports misses)
     - --dry-run (no writes; prints what would be fetched/written)
     - --ttl-minutes N (skip fetch if cache fresh; default sensible value)
   - Failure behavior:
     - Soft-fail per-ref (record error in manifest entry), but command exits non-zero only if a strict flag is set (optional).
2) Keep renderer deterministic:
   - tools/houston/render.py must render using:
     - packet + cache (when present)
     - stable sorting and stable formatting
3) Tests:
   - Add/extend tests to validate:
     - ref parsing to canonical ref_key
     - cache schema/manifest shape
     - renderer determinism using fixture cache files (tests must not require network)
4) Docs:
   - Add short usage note in docs/ (or README section):
     - xtrl backlog hydrate (online)
     - xtrl backlog hydrate --offline
     - xtrl backlog render

## Out of scope
- Webhooks/push updates
- Repo-local caching
- Any writes outside $CODEX_STATE/xtrl/cache/houston

## Acceptance checks (must pass)
- python -m pytest -q
- python -m compileall tools
- python tools/houston/hydrate.py --dry-run (should exit 0)
- python tools/houston/hydrate.py --offline (should exit 0 and report misses)
- python tools/houston/render.py (should exit 0; if it needs args, provide --help and keep default safe)

## Evidence to emit (under $CODEX_STATE/xtrl/out/packet-011-houston-backlog-hydrate/)
- summary.md
- raw/diffstat.txt
- raw/changed_paths.txt
- raw/tests.txt
- raw/hydrate_dryrun.txt
- raw/hydrate_offline.txt
