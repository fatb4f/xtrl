# Execution DAG (Packet Lifecycle)

This document describes the canonical packet lifecycle stages.

- S0 Preflight: validate contract + repo state
- G0 Enter Work: create isolated worktree
- Work: run actions (regen/test/commands)
- Evidence: collect Packet-002 evidence
- Check/Gate: enforce required evidence + decision
- Promote: patch-based promotion when allowed
