#!/usr/bin/env python3
"""Detect and optionally fix invalid emails in `app_user`.

Usage:
  python python/scripts/clean_app_user_emails.py --dry-run
  python python/scripts/clean_app_user_emails.py --apply

By default it runs in dry-run mode and prints the rows that look invalid.
With --apply it will update invalid emails to a safe developer address
`dev+<username>@example.test` (idempotent).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.Classes.db import DB
from pydantic import EmailStr


def is_valid_email(value: str) -> bool:
    if value is None:
        return False
    value = value.strip()
    if value == "":
        return False
    try:
        EmailStr.validate(value)
        return True
    except Exception:
        return False


def find_invalid_emails(db: DB):
    cur = db.cursor()
    cur.execute("SELECT user_id, username, email FROM app_user")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    out = []
    for row in rows:
        data = {cols[i]: row[i] for i in range(len(cols))}
        if not is_valid_email(data.get('email')):
            out.append(data)
    return out


def apply_fixes(db: DB, rows):
    cur = db.cursor()
    changed = []
    for r in rows:
        uid = r['user_id']
        username = r.get('username') or f'user{uid}'
        new_email = f"dev+{username}@example.test"
        cur.execute("UPDATE app_user SET email=%s WHERE user_id=%s", (new_email, uid))
        changed.append((uid, new_email))
    if not db.autocommit:
        db.commit()
    return changed


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--apply', action='store_true', help='Apply fixes (updates DB).')
    args = p.parse_args(argv)

    with DB() as db:
        invalid = find_invalid_emails(db)
        if not invalid:
            print('No invalid emails found. Nothing to do.')
            return 0

        print(f'Found {len(invalid)} rows with invalid or missing email:')
        for r in invalid:
            print(f" - user_id={r['user_id']}, username={r.get('username')!r}, email={r.get('email')!r}")

        if not args.apply:
            print('\nDry-run mode: no changes applied. Re-run with --apply to update emails to dev+<username>@example.test')
            return 0

        changed = apply_fixes(db, invalid)
        print('\nApplied fixes:')
        for uid, email in changed:
            print(f' - user_id={uid} -> {email}')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
