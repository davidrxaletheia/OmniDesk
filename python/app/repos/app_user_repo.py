# wrapper that reuses existing repo implementation
# import the legacy repo using the package path so imports work
# when the module is loaded as `python.app...`
from python.Classes.repos.app_user_repo import AppUserRepo as LegacyAppUserRepo
from python.Classes.db import DB
from pydantic import BaseModel
from typing import Optional
from pydantic import ValidationError
from ..core.security import hash_password


class _FallbackUser(BaseModel):
    user_id: Optional[int]
    full_name: Optional[str]
    username: str
    email: Optional[str] = None
    password_hash: str
    role: Optional[str] = 'empleado'
    active: bool = True


class AppUserRepo:
    """Wrapper around legacy `Classes.repos.app_user_repo.AppUserRepo`.

    Provides a small, stable interface used by the FastAPI routes. The
    wrapper is defensive: if the legacy repo raises Pydantic validation
    errors (common with legacy/dirty rows), we fall back to a raw DB
    fetch and build a permissive `_FallbackUser` instance.
    """
    def __init__(self):
        self._legacy = LegacyAppUserRepo()

    def get_by_username(self, username):
        # Try the legacy path first (returns AppUserModel). If invalid
        # data triggers a ValidationError, fall back to raw SQL and build
        # a permissive model so routes (login) can still operate.
        try:
            return self._legacy.find_by_username(username)
        except ValidationError:
            # fallback to raw DB read
            with DB() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM app_user WHERE username=%s LIMIT 1", (username,))
                row = cur.fetchone()
                if not row:
                    return None
                cols = [d[0] for d in cur.description]
                data = {cols[i]: row[i] for i in range(len(cols))}
                # Ensure required keys exist for the fallback model
                return _FallbackUser(**data)

    def list(self, limit: int = 50, offset: int = 0, **kwargs):
        try:
            return self._legacy.list(limit=limit, offset=offset)
        except ValidationError:
            # fallback: raw DB scan and build permissive fallback users
            with DB() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM app_user LIMIT %s OFFSET %s", (limit, offset))
                rows = cur.fetchall()
                if not rows:
                    return []
                cols = [d[0] for d in cur.description]
                out = []
                for row in rows:
                    data = {cols[i]: row[i] for i in range(len(cols))}
                    out.append(_FallbackUser(**data))
                return out

    def get(self, user_id: int):
        return self._legacy.get(user_id)

    def create(self, data: dict):
        # Accept either 'password' (plain) or 'password_hash'. Normalize
        payload = dict(data)
        if 'password' in payload and 'password_hash' not in payload:
            payload['password_hash'] = hash_password(payload.pop('password'))
        return self._legacy.create(payload)

    def update(self, user_id: int, data: dict):
        payload = dict(data)
        if 'password' in payload:
            payload['password_hash'] = hash_password(payload.pop('password'))
        return self._legacy.update(user_id, payload)

    def delete(self, user_id: int):
        return self._legacy.delete(user_id)