"""Modelo `AlertModel`.

Representa alertas/recordatorios que pueden referenciar tickets o eventos.
Incluye `alert_time` y un flag `sent`.
"""

from datetime import datetime
from typing import Optional, Literal
from .base import OMBase

class AlertModel(OMBase):
    alert_id: Optional[int] = None
    alert_time: datetime
    message: str
    kind: Literal['ticket','event','incident'] = 'incident'
    ticket_id: Optional[int] = None
    event_id: Optional[int] = None
    sent: bool = False
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
