"""Repositorio `ClientRepo`.

Provee métodos especializados para consultar la tabla `client`.
Ejemplo: búsqueda por nombre/email y filtrado por tipo.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import ClientModel

class ClientRepo(BaseRepo):
    table = "client"
    pk = "client_id"
    model = ClientModel

    def search(self, q: str, limit: int=50) -> List[ClientModel]:
        return self.filter("(full_name LIKE %s OR email LIKE %s)", (f"%{q}%", f"%{q}%"),
                           limit=limit, order_by="registered_at", desc=True)

    def by_type(self, client_type: str, limit: int=50) -> List[ClientModel]:
        return self.filter("client_type=%s", (client_type,), limit=limit, order_by="full_name")
