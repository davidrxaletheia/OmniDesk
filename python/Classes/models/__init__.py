"""Módulo `classes.models`.

Contiene los modelos Pydantic que representan las tablas principales de la
base de datos (app_user, client, product, catalog, order, ticket, etc.).
Estos modelos se usan como contratos (shapes) para validación y serialización.
"""

from .app_user import AppUserModel
from .client import ClientModel
from .category import CategoryModel
from .product import ProductModel
from .catalog import CatalogModel, CatalogProductModel
from .conversation import ConversationModel
from .message import MessageModel
from .order import CustomerOrderModel, OrderItemModel, InvoiceModel
from .ticket import TicketModel
from .calendar import CalendarEventModel
from .alert import AlertModel
