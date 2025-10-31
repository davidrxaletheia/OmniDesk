#!/usr/bin/env python3
"""Import `database/init/init.sql` into the configured MySQL database.

Usage:
  python python/scripts/import_init_sql.py [--file PATH] [--dry-run] [--force]

The script uses `python.Classes.db.get_connection()` so it honors the
.env and environment variables used by the project.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys


import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SQL = ROOT / "database" / "init" / "init.sql"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", default=str(DEFAULT_SQL))
    parser.add_argument("--dry-run", action="store_true", help="Print first lines of the SQL and exit")
    parser.add_argument("--force", action="store_true", help="Execute the SQL against the configured DB")
    args = parser.parse_args()

    sql_path = Path(args.file)
    if not sql_path.exists():
        print(f"SQL file not found: {sql_path}")
        sys.exit(2)

    content = sql_path.read_text(encoding='utf-8')
    if args.dry_run:
        print("--- DRY RUN: first 1200 chars of init.sql ---")
        print(content[:1200])
        print("--- end preview ---")
        return

    if not args.force:
        print("Use --force to actually execute the SQL against the DB. Use --dry-run to preview.")
        return

    # Execute against DB using project's DB helper so it uses .env
    try:
        from python.Classes.db import get_connection
    except Exception as exc:
        print("Failed to import DB helper:", exc)
        sys.exit(1)

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        print("Executing SQL (this may take a few seconds)...")
        # mysql.connector cursor.execute supports multi=True
        for result in cur.execute(content, multi=True):
            # result is a MySQLCursor when ok; fetch warnings if any
            pass
        conn.commit()
        print("Finished applying init.sql")
    except Exception as exc:
        print("Error while executing SQL:", exc)
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        sys.exit(1)
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    main()
