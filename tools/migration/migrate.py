#!/usr/bin/env python
import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="xtrlv2 migration tool (skeleton)")
    parser.add_argument("--dry-run", action="store_true", help="no-op; show planned actions")
    args = parser.parse_args()

    if args.dry_run:
        print("migrate.py dry-run: no actions (skeleton)")
        return 0

    print("migrate.py: not implemented (use --dry-run)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
