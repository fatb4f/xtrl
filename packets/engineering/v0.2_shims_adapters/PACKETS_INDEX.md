# Packet Set

- Phase: **v0.2_shims_adapters**
- Generated: 2026-02-05
- Owner: TBD
- Source: TBD
- Revision: TBD
- Backlog: `./backlog` (Backlog.md task entries)

## Packets (in order)

1. `[To Do]` `pkt-compat-0001-outdir-compat-migrate` — Implement OUT_DIR legacy detection + optional migrate-to-namespaced shim; ensure all writers target out/<repo>/<packet_id>/
2. `[To Do]` `pkt-compat-0002-contract-v0-2-materializer-compat` — Add legacy→v0.2 contract materializer adapter; always emit v0.2 contract.json for runs
3. `[To Do]` `pkt-compat-0003-evidencecapsule-v0-2-emitter-compat` — Ensure EvidenceCapsule v0.2 directory tree is always emitted; add adapter to map legacy evidence into required v0.2 files
4. `[To Do]` `pkt-compat-0004-skills-symlink-compat` — Convert skills/ into a compatibility symlink layer to skills-pack/; add validation for resolution
5. `[To Do]` `pkt-compat-0005-state-doctor-subtrees` — Centralize state path resolver and ensure required state subtrees (sessions/history/tmp/logs/cache/worktrees/out) exist; add state-doctor command
6. `[To Do]` `pkt-compat-0006-visibility-index-backlog-worktree-out` — Emit deterministic visibility index mapping backlog task ↔ packet_id ↔ worktree ↔ out_dir; write link.json under namespaced OUT_DIR
7. `[To Do]` `pkt-compat-0007-closure-run-verification` — Add a single verification command that asserts namespaced OUT_DIR contains contract.json, packet.json, exec-prompt.md, and full EvidenceCapsule v0.2 tree for a given packet_id
