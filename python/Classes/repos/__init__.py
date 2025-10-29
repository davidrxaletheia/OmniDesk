"""Paquete `classes.repos`.

Exporta los repositorios disponibles para acceso a datos. Cada repo
hereda de `BaseRepo` y mapea una tabla de la base de datos.
"""

from .base_repo import BaseRepo
from .app_user_repo import AppUserRepo
from .client_repo import ClientRepo
from .category_repo import CategoryRepo
from .product_repo import ProductRepo
from .catalog_repo import CatalogRepo
from .conversation_repo import ConversationRepo
from .message_repo import MessageRepo
from .order_repo import CustomerOrderRepo, OrderItemRepo, InvoiceRepo
from .ticket_repo import TicketRepo
from .calendar_repo import CalendarEventRepo
from .alert_repo import AlertRepo
