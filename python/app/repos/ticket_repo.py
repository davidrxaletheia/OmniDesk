from python.Classes.repos.ticket_repo import TicketRepo as LegacyTicketRepo


class TicketRepo:
    def __init__(self):
        self._legacy = LegacyTicketRepo()

    def list(self, status: str = None, priority: str = None, client_id: int = None, limit: int = 50, offset: int = 0):
        # Basic filtering mapping to legacy filter / helpers
        if client_id is not None:
            return self._legacy.by_client(client_id, limit=limit)
        if status in (None, ''):
            # default: open or in progress
            return self._legacy.open_or_wip(limit=limit)
        # fallback to generic filter
        where = "status=%s"
        params = (status,)
        return self._legacy.filter(where, params, limit=limit, offset=offset)

    def get(self, ticket_id: int):
        return self._legacy.get(ticket_id)

    def create(self, data: dict):
        return self._legacy.create(data)

    def update(self, ticket_id: int, data: dict):
        return self._legacy.update(ticket_id, data)
