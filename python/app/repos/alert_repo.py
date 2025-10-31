from python.Classes.repos.alert_repo import AlertRepo as LegacyAlertRepo


class AlertRepo:
    def __init__(self):
        self._legacy = LegacyAlertRepo()

    def pending(self, limit: int = 50):
        return self._legacy.pending(limit=limit)

    def create(self, data: dict):
        return self._legacy.create(data)

    def list(self, where: str = None, params: tuple = (), limit: int = 50, offset: int = 0):
        if where:
            return self._legacy.filter(where, params, limit=limit, offset=offset)
        return self._legacy.list(limit=limit, offset=offset)

    def get(self, alert_id: int):
        return self._legacy.get(alert_id)

    def update(self, alert_id: int, data: dict):
        return self._legacy.update(alert_id, data)
