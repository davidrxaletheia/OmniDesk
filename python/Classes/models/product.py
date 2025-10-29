from datetime import datetime
"""Modelo `ProductModel`.

Modelo maestro para productos: incluye `price`, `stock`, `sku`,
descripción y relación con `category`.
"""

from decimal import Decimal
from typing import Optional, Literal
from .base import OMBase

class ProductModel(OMBase):
    product_id: Optional[int] = None
    sku: str
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    price: Decimal
    stock: int
    status: Literal['active','inactive'] = 'active'
    created_at: Optional[datetime] = None
