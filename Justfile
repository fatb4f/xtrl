set quiet := true

migrate-check:
    @python tools/migration/migrate_check.py

migrate-dry:
    @python tools/migration/migrate.py --dry-run

ssot-conformance:
    @python tools/ssot_gate.py conformance

ssot-pin-check:
    @python tools/ssot_gate.py pin
