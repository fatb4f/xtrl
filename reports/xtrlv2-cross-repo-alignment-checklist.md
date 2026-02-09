# xtrl ⇄ xtrlv2 Cross-Repo Alignment Checklist

Purpose: keep schema and runtime aligned without duplicating work.

## Ownership split
- xtrlv2 repo: schema, canonical enums, validators, contracts, reference spec.
- xtrl repo: runtime/controller, adapters, compatibility shims, evidence emission, execution pipeline.

## Standard workflow
1. Update schema/spec in xtrlv2 first.
2. Tag the xtrlv2 commit that introduced the change.
3. Update xtrl implementation to match.
4. Add/adjust tests in xtrl to validate schema conformance.
5. Record the alignment in xtrl reports (schema commit hash + summary).

## Decision rules
- If a change affects schema structure or meaning: do it in xtrlv2.
- If a change affects runtime behavior but not schema: do it in xtrl.
- If both: schema in xtrlv2 first, then xtrl implementation.

## Branch policy
- Prefer cross-repo (xtrlv2 branch) for schema work.
- Use xtrl branch only for temporary prototype shims.
- Backport finalized changes into xtrlv2 before promotion.

## Alignment artifacts (recommended)
- `reports/xtrlv2-schema-alignment.md` (in xtrl)
- Schema commit pin / hash
- Short diff summary (what changed, where it is enforced)

## Drift checks (optional but valuable)
- Pin schema hash in xtrl and fail precheck if schema drift is detected.
- Add a small audit script to compare required artifacts vs emitted artifacts.
