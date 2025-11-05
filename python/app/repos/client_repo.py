from python.Classes.repos.client_repo import ClientRepo as LegacyClientRepo


class ClientRepo:
    """Wrapper around legacy `Classes.repos.client_repo.ClientRepo`."""
    def __init__(self):
        self._legacy = LegacyClientRepo()

    def create(self, data: dict):
        return self._legacy.create(data)

    def get(self, client_id: int):
        return self._legacy.get(client_id)

    def list(self, limit: int = 50, offset: int = 0, **kwargs):
        return self._legacy.list(limit=limit, offset=offset)

    def search(self, q: str, limit: int = 50):
        return self._legacy.search(q, limit=limit)

    def update(self, client_id: int, data: dict):
        return self._legacy.update(client_id, data)

    def by_type(self, client_type: str, limit: int = 50):
        # Legacy repo provides by_type; delegate to it for convenience.
        return self._legacy.by_type(client_type, limit=limit)

    def get_by_telegram_id(self, telegram_user_id: int):
        """Return a single client model matching telegram_user_id or None."""
        rows = self._legacy.filter("telegram_user_id=%s", (telegram_user_id,), limit=1)
        return rows[0] if rows else None

    def get_by_telegram_username(self, telegram_username: str):
        """Return a single client model matching telegram_username or None."""
        rows = self._legacy.filter("telegram_username=%s", (telegram_username,), limit=1)
        return rows[0] if rows else None

    def get_by_phone(self, phone: str):
        """Return a single client model matching phone or None."""
        rows = self._legacy.filter("phone=%s", (phone,), limit=1)
        return rows[0] if rows else None