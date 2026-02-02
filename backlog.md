# xtrl backlog

## P0
- P0.2: Ship Layer 1 ctrl.* control surface (Justfile + MCP)
- P0.3: Align Yazi → just wiring (no logic in Yazi)
- P0.4: HQ backlog topology (hub-and-spoke)

## P1
- P1.5: ComplianceReport is SSOT; gate exec on evidence.ok
- P1.6: Pydantic-authoritative models + controller CLI
- P1.7: ACTION-based exec + {VAR} allowlist substitution

## Backlog.md tool adoption (xtrl)
- P0 READY: Spike Backlog.md in xtrl repo
  - repo: xtrl
  - intent: install + run `backlog init` in xtrl; validate it can be the SSOT
  - decision: how `xtrl/backlog.md` relates to tool’s `backlog/` folder (keep as summary/export vs retire)
  - outputs: created `backlog/` tree; documented conventions; no state outside xtrl + CODEX_STATE
- P0 READY: Define mapping between xtrl packets and Backlog.md tasks
  - intent: decide how a task references a packet contract (packet_id + contract_path) and evidence dir
  - rule: promoted commit includes Packet/Evidence trailers; tasks link to evidence path
- P1 READY: Wire Just/MCP surface to Backlog.md
  - intent: add `ctrl.backlog.*` commands that call the Backlog.md CLI/MCP (start, list/view tasks, export board)
  - constraint: keep writes bounded (repo-local backlog/ + CODEX_STATE caches only)
