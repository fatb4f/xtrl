# xtrl → xtrlv2 Migration Pivot Report

Generated: 2026-02-09

## Summary
Based on the ctrlv2 normalization audit and subsequent commit history, the pivot away from strict migration work occurred immediately after the 2026-02-05 ctrlv2 normalization packet set. The first clear non‑migration feature series is the **helper_created telemetry** work.

## Migration anchor (ctrlv2 normalization)
The audit report lists the following packets as completed on 2026-02-05:
- pkt-exec-0001-enforce-action-only-execution
- pkt-exec-0002-enforce-budgets-time-diff-iteration
- pkt-exec-0003-enforce-allowed-paths-during-execution
- pkt-evidence-0003-align-evidence-json-with-v0-2-schema
- pkt-policy-0001-normalize-modes-and-reasoncodes
- pkt-ops-0023-gate-target-dispatch

This corresponds to the ctrlv2 normalization phase captured in:
`reports/ctrlv2-schema-normalization-audit.md`

## Pivot boundary
**First clear post‑migration commit:**
- `9078a54` — *Add helper_created event packet and verifier*

This marks the transition from normalization tasks to new telemetry/loop features not defined in xtrlv2’s current schema set.

## First non‑xtrlv2 feature series (post‑pivot)
The commits immediately after the pivot focus on helper‑created telemetry and v0.2 runtime loop behaviors:

1. **helper_created event telemetry**
   - Add helper_created packet + verifier
   - Emit helper birth events from diffs and tighten verification
   - Worktree‑relative hashing + diffstat fixes

2. **v0.2 runtime loop pre‑contracts / flow changes**
   - New loop packets (pkt‑loop‑0001…0006)
   - Test handling / promotion gating changes
   - argv‑only enforcement adjustments

3. **Ledger / out‑dir / evidence layout changes**
   - Evidence output moved to repo root `out/`
   - Ledger + latest state pointer writes

4. **Reason code enum + schemas**
   - Canonical ReasonCode schema + gate_worker schema
   - New phase tools referencing the enum

These items are not direct translations of the existing xtrlv2 schemas and represent **new behavior** rather than normalization against ctrlv2.

## Implication
If the goal is to keep xtrl aligned with xtrlv2, the post‑pivot feature work should either:
- be back‑ported into xtrlv2 schemas (e.g., helper_created telemetry, ledger model), or
- be explicitly marked as xtrl‑only extensions until xtrlv2 is updated.

## Evidence
- Commit log (post‑2026‑02‑05): helper_created series begins at `9078a54`.
- Audit anchor: `reports/ctrlv2-schema-normalization-audit.md`.
