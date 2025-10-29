"""Modelo `TicketModel`.

Define la estructura de un ticket de soporte: prioridad, estado,
fechas de creación/resolución y posible agente asignado.
"""

from datetime import datetime
from typing import Optional, Literal
from .base import OMBase

class TicketModel(OMBase):
    ticket_id: Optional[int] = None
    client_id: int
    subject: str
    description: Optional[str] = None
    priority: Literal['alta','media','baja'] = 'media'
    status: Literal['abierto','en_progreso','cerrado'] = 'abierto'
    created_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[int] = None
