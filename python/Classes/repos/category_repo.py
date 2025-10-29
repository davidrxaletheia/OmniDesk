"""Repositorio `CategoryRepo`.

Métodos para listar y gestionar categorías de producto.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import CategoryModel

class CategoryRepo(BaseRepo):
    table = "category"
    pk = "category_id"
    model = CategoryModel

    def children(self, parent_id: int) -> List[CategoryModel]:
        return self.filter("parent_id=%s", (parent_id,), order_by="name", limit=100)

    def roots(self) -> List[CategoryModel]:
        return self.filter("parent_id IS NULL", tuple(), order_by="name", limit=100)
