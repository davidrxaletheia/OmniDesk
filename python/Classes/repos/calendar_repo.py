"""Repositorio `CalendarEventRepo`.

Soporta operaciones para eventos de calendario (crear, listar,
filtrar por rango de fecha, etc.).
"""

from typing import List
from .base_repo import BaseRepo
from ..models import CalendarEventModel

class CalendarEventRepo(BaseRepo):
    table = "calendar_event"
    pk = "event_id"
    model = CalendarEventModel

    def upcoming(self, limit: int=20) -> List[CalendarEventModel]:
        return self.filter("start_time >= NOW()", tuple(), order_by="start_time", limit=limit)
