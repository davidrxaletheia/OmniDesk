from python.Classes.repos.calendar_repo import CalendarEventRepo as LegacyCalendarRepo


class CalendarRepo:
    def __init__(self):
        self._legacy = LegacyCalendarRepo()

    def upcoming(self, limit: int = 50):
        return self._legacy.upcoming(limit=limit)

    def list_range(self, start=None, end=None, limit: int = 50, offset: int = 0):
        # If no range provided, return upcoming
        if not start and not end:
            return self.upcoming(limit=limit)
        # Build simple filter conditions
        conds = []
        params = []
        if start:
            conds.append("start_time >= %s")
            params.append(start)
        if end:
            conds.append("end_time <= %s")
            params.append(end)
        where = " AND ".join(conds)
        return self._legacy.filter(where, tuple(params), limit=limit, offset=offset)

    def create(self, data: dict):
        """Create a calendar event using the legacy repo's create method."""
        return self._legacy.create(data)

    def get(self, event_id: int):
        """Return a single calendar event by id using the legacy repo."""
        return self._legacy.get(event_id)
