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
