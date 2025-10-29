"""Repositorio `TicketRepo`.

Operaciones para gestionar tickets de soporte (crear, asignar,
filtrar por estado/prioridad).
"""

from typing import List
from .base_repo import BaseRepo
from ..models import TicketModel

class TicketRepo(BaseRepo):
    table = "ticket"
    pk = "ticket_id"
    model = TicketModel

    def open_or_wip(self, limit: int=50) -> List[TicketModel]:
        return self.filter("status IN ('abierto','en_progreso')", tuple(), order_by="priority", limit=limit)

    def by_client(self, client_id: int, limit: int=50) -> List[TicketModel]:
        return self.filter("client_id=%s", (client_id,), order_by="created_at", desc=True, limit=limit)
