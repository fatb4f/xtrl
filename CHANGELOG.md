# Changelog

## Unreleased - 2026-02-05
- Completed P0.4 packet set and added xtrl-ops packet set scaffold with contracts, prompts, and pre-contracts.
- Added required packet contract policy keys for runner compatibility (worktree and network policies, allowed paths, forbidden outputs).
- Added packet runner quality-of-life updates in repo (ignore worktrees, xtrl-ops audit report).
- Expanded exec/promogate/evidence/git/release tooling (pre_contract schema + example, promogate evaluator, packet generator, action-only runner, evidence capsule minimums, gitplant dry-run, worktree commands, promote actuator wiring, release dry-run tag CLI).
- Backlog.md updates for xtrl-ops packets (task lifecycle + acceptance tracking, milestone archive).

## v0.2.0 - 2026-01-30
- Added `agents.md` runbook and execution DAG reference.
- Added plant manifest and schemas to prevent drift.
- Added EXEC_PROMPT template and schema with validation in preflight and runner.
- Expanded packet generator to create contracts and prompts (dir layout by default).
- Added tools for plant validation and flat-packet migration.
