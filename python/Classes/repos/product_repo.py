"""Repositorio `ProductRepo`.

Provee métodos de búsqueda y acceso para la tabla `product`.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import ProductModel

class ProductRepo(BaseRepo):
    table = "product"
    pk = "product_id"
    model = ProductModel

    def search(self, q: str, limit: int=50) -> List[ProductModel]:
        return self.filter("(name LIKE %s OR sku LIKE %s)", (f"%{q}%", f"%{q}%"),
                           limit=limit, order_by="product_id", desc=True)

    def by_category(self, category_id: int, limit: int=50) -> List[ProductModel]:
        return self.filter("category_id=%s", (category_id,), limit=limit, order_by="name")
