from typing import Optional
"""Modelo `CategoryModel`.

Representa una categoría de producto; soporta jerarquía mediante
`parent_id` (self-FK) para crear árboles de categorías.
"""

from .base import OMBase

class CategoryModel(OMBase):
    category_id: Optional[int] = None
    name: str
    parent_id: Optional[int] = None
