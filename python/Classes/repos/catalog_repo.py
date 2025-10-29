"""Repositorio `CatalogRepo`.

Operaciones para catálogos. Permite listar catálogos activos y
otras consultas relacionadas con campañas.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import CatalogModel

class CatalogRepo(BaseRepo):
    table = "catalog"
    pk = "catalog_id"
    model = CatalogModel

    def actives(self) -> List[CatalogModel]:
        return self.filter("active=1", tuple(), order_by="start_date", desc=True, limit=200)
