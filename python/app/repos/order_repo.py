from typing import Dict, Any
from python.Classes.repos.order_repo import CustomerOrderRepo as LegacyOrderRepo, OrderItemRepo as LegacyOrderItemRepo
from python.Classes.repos.product_repo import ProductRepo as LegacyProductRepo
from ..core.config import settings
from decimal import Decimal


class OrderRepo:
    """Wrapper that creates an order header and its items.

    The legacy repos provide low-level CRUD; this adapter coordinates
    creating the header then inserting each order_item using a product
    snapshot (name, sku, unit_price, tax_rate).
    """
    def __init__(self):
        self._order = LegacyOrderRepo()
        self._item = LegacyOrderItemRepo()
        self._prod = LegacyProductRepo()

    def create(self, payload: Dict[str, Any]):
        # payload expected: { client_id: int, items: [{product_id, quantity}, ...], notes?: str, client_type?: 'normal'|'premium' }
        header = {k: v for k, v in payload.items() if k in ('client_id', 'notes')}
        order_id = self._order.create(header)
        # insert items
        items = payload.get('items', []) or []
        client_type = payload.get('client_type')
        discount_pct = float(getattr(settings, 'PREMIUM_DISCOUNT_PCT', 0.0)) if client_type == 'premium' else 0.0
        for it in items:
            prod = self._prod.get(it['product_id'])
            if not prod:
                raise ValueError(f"Product {it['product_id']} not found")
            unit_price = float(getattr(prod, 'price', 0))
            qty = int(it.get('quantity', 1))
            disc_pct = discount_pct
            disc_amount = round(unit_price * qty * disc_pct, 2) if disc_pct else 0
            item_data = {
                'order_id': order_id,
                'product_id': it['product_id'],
                'quantity': it.get('quantity', 1),
                'product_name': prod.name,
                'sku': getattr(prod, 'sku', None),
                'unit_price': prod.price,
                'tax_rate': getattr(prod, 'tax_rate', 0) if hasattr(prod, 'tax_rate') else 0,
                'discount_pct': Decimal(str(disc_pct)) if disc_pct else None,
                'discount_amount': Decimal(str(disc_amount)) if disc_amount else None,
            }
            self._item.add_item(item_data)

        return self._order.get(order_id)

    def get(self, order_id: int):
        return self._order.get(order_id)

    def list_by_client(self, client_id: int, limit: int = 50, offset: int = 0):
        return self._order.by_client(client_id, limit=limit)
