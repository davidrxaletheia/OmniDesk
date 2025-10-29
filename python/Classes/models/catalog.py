"""Modelos `CatalogModel` y `CatalogProductModel`.

Representan catálogos (campañas) y la relación N..N entre catálogos
y productos (precios especiales, assigned_stock).
"""

from datetime import date
from typing import Optional, Literal
from decimal import Decimal
from .base import OMBase

class CatalogModel(OMBase):
    catalog_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    discount_percentage: Decimal = Decimal('0.00')
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    visible_to: Literal['todos','premium','interno'] = 'todos'
    active: bool = True

class CatalogProductModel(OMBase):
    catalog_id: int
    product_id: int
    special_price: Optional[Decimal] = None
    assigned_stock: Optional[int] = None
