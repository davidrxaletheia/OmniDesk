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
        # payload expected: { client_id: int, items: [{product_id, quantity, snapshot...}], notes?: str, client_type?: 'normal'|'premium' }
        header = {k: v for k, v in payload.items() if k in ('client_id', 'notes')}
        order_id = self._order.create(header)
        # insert items
        items = payload.get('items', []) or []
        client_type = payload.get('client_type')
        premium_pct = float(getattr(settings, 'PREMIUM_DISCOUNT_PCT', 0.0)) if client_type == 'premium' else 0.0

        for it in items:
            # try to use snapshot values from cart if provided, otherwise fall back to product repo
            prod = None
            try:
                prod = self._prod.get(it['product_id'])
            except Exception:
                prod = None

            unit_price = None
            prod_name = None
            sku = None
            tax_rate = 0

            # snapshot fields (from cart_item) take precedence
            if it.get('unit_price') is not None:
                try:
                    unit_price = float(it.get('unit_price'))
                except Exception:
                    unit_price = float(getattr(prod, 'price', 0)) if prod else 0.0
            else:
                unit_price = float(getattr(prod, 'price', 0)) if prod else 0.0

            if it.get('product_name'):
                prod_name = it.get('product_name')
            else:
                prod_name = getattr(prod, 'name', None) if prod else None

            if it.get('sku'):
                sku = it.get('sku')
            else:
                sku = getattr(prod, 'sku', None) if prod else None

            if it.get('tax_rate') is not None:
                try:
                    tax_rate = float(it.get('tax_rate') or 0)
                except Exception:
                    tax_rate = getattr(prod, 'tax_rate', 0) if prod else 0
            else:
                tax_rate = getattr(prod, 'tax_rate', 0) if prod else 0

            qty = int(it.get('quantity', 1))

            # compute catalog discount component if snapshot has final_price
            catalog_discount_amount = 0.0
            final_unit = None
            if it.get('final_price') is not None:
                try:
                    final_unit = float(it.get('final_price'))
                except Exception:
                    final_unit = unit_price
            elif it.get('catalog_special_price') is not None:
                try:
                    final_unit = float(it.get('catalog_special_price'))
                except Exception:
                    final_unit = unit_price
            elif it.get('applied_catalog_discount_pct') is not None:
                try:
                    pct = float(it.get('applied_catalog_discount_pct') or 0.0)
                    final_unit = round(unit_price * (1.0 - pct), 2)
                except Exception:
                    final_unit = unit_price
            else:
                final_unit = unit_price

            catalog_discount_amount = round((unit_price - final_unit) * qty, 2) if unit_price and final_unit is not None else 0.0

            # premium discount applies on top of final_unit
            premium_discount_amount = round((final_unit * qty) * premium_pct, 2) if premium_pct else 0.0

            total_discount_amount = round(catalog_discount_amount + premium_discount_amount, 2)

            # compute discount_pct field relative to unit_price * qty (if unit_price is zero, omit)
            discount_pct_field = None
            try:
                if unit_price and qty and total_discount_amount:
                    discount_pct_field = float(total_discount_amount) / (unit_price * qty)
            except Exception:
                discount_pct_field = None

            item_data = {
                'order_id': order_id,
                'product_id': it['product_id'],
                'quantity': qty,
                'product_name': prod_name,
                'sku': sku,
                'unit_price': unit_price,
                'tax_rate': tax_rate,
                'discount_pct': Decimal(str(discount_pct_field)) if discount_pct_field else None,
                'discount_amount': Decimal(str(total_discount_amount)) if total_discount_amount else None,
            }

            self._item.add_item(item_data)

        return self._order.get(order_id)

    def get(self, order_id: int):
        return self._order.get(order_id)

    def list_by_client(self, client_id: int, limit: int = 50, offset: int = 0):
        return self._order.by_client(client_id, limit=limit)
