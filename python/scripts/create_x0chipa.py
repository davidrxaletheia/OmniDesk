#!/usr/bin/env python3
"""Create test user x0chipa if missing (for pytest)."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.app.repos.app_user_repo import AppUserRepo
from python.app.core.security import hash_password
from python.Classes.db import DB


def main():
    repo = AppUserRepo()
    # Avoid loading full model rows (which may raise Pydantic validation
    # errors for legacy/dirty rows). Check existence with a raw DB query.
    with DB() as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(1) FROM app_user WHERE username=%s", ('x0chipa',))
        cnt = cur.fetchone()[0]
        if cnt and int(cnt) > 0:
            print('user exists')
            return 0

    payload = {
        'full_name': 'Dev Seed x0chipa',
        'username': 'x0chipa',
        'email': 'dev+x0chipa@example.test',
        'password_hash': hash_password('Holakhace24.'),
        'role': 'admin',
        'active': True,
    }
    try:
        uid = repo.create(payload)
        print('created user id=', uid)
        return 0
    except Exception as e:
        print('failed to create user:', e)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
