set quiet := true

migrate-check:
    @python tools/migration/migrate_check.py

migrate-dry:
    @python tools/migration/migrate.py --dry-run
