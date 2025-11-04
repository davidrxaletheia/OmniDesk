"""Modelos relacionados con pedidos e invoicing.

Contiene `CustomerOrderModel`, `OrderItemModel` y `InvoiceModel`.
Los `OrderItem` contienen snapshots de precio/tasa para preservar
consistencia cuando los productos cambian con el tiempo.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from .base import OMBase

class CustomerOrderModel(OMBase):
    order_id: Optional[int] = None
    client_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Literal['borrador','confirmado','preparando','enviado','entregado','cancelado','devuelto'] = 'borrador'
    payment_status: Literal['pendiente','pagado','reembolsado','fallido'] = 'pendiente'
    subtotal: Decimal = Decimal('0.00')
    discount_total: Decimal = Decimal('0.00')
    tax_total: Decimal = Decimal('0.00')
    shipping_total: Decimal = Decimal('0.00')
    grand_total: Optional[Decimal] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class OrderItemModel(OMBase):
    order_id: int
    product_id: int
    quantity: int
    product_name: str
    sku: str
    unit_price: Decimal
    discount_pct: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    tax_rate: Decimal = Decimal('0.00')
    # line_* son generadas por la BD

class InvoiceModel(OMBase):
    invoice_id: Optional[int] = None
    order_id: int
    invoice_number: str
    series: Optional[str] = None
    issued_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    currency_code: str = 'MXN'
    exchange_rate: Optional[Decimal] = None
    billing_name: Optional[str] = None
    rfc: Optional[str] = None
    regimen_fiscal: Optional[str] = None
    fiscal_postal_code: Optional[str] = None
    billing_address: Optional[str] = None
    uso_cfdi: Optional[str] = None
    forma_pago: Optional[str] = None
    metodo_pago: Optional[str] = None
    status: Literal['emitida','pagada','parcial','cancelada'] = 'emitida'
    notes: Optional[str] = None
