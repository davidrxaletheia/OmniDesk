from typing import List, Optional
from .base_repo import BaseRepo
from ..models import CustomerOrderModel, OrderItemModel, InvoiceModel
from ..db import DB

"""Repositorios para pedidos, items y facturas.

Contiene `CustomerOrderRepo`, `OrderItemRepo` e `InvoiceRepo` con
operaciones específicas como búsquedas por cliente y manejo de totales.
"""

class CustomerOrderRepo(BaseRepo):
    table = "customer_order"
    pk = "order_id"
    model = CustomerOrderModel

    def by_client(self, client_id: int, limit: int=50) -> List[CustomerOrderModel]:
        return self.filter("client_id=%s", (client_id,), limit=limit, order_by="created_at", desc=True)

class OrderItemRepo(BaseRepo):
    table = "order_item"
    pk = None
    model = OrderItemModel

    def add_item(self, data: dict) -> int:
        return self.create(data)

class InvoiceRepo(BaseRepo):
    table = "invoice"
    pk = "invoice_id"
    model = InvoiceModel

    def by_order(self, order_id: int) -> List[InvoiceModel]:
        return self.filter("order_id=%s", (order_id,), order_by="issued_at", desc=True, limit=20)
