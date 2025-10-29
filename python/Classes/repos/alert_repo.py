"""Repositorio `AlertRepo`.

Gestión de alertas/recordatorios asociados a tickets o eventos.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import AlertModel

class AlertRepo(BaseRepo):
    table = "alert"
    pk = "alert_id"
    model = AlertModel

    def pending(self, limit: int=50) -> List[AlertModel]:
        return self.filter("sent=0", tuple(), order_by="alert_time", limit=limit)
