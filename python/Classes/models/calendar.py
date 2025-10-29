"""Modelo `CalendarEventModel`.

Representa eventos de calendario que pueden estar vinculados a tickets
u otras entidades. Contiene fecha/hora de inicio y fin.
"""

from datetime import datetime
from typing import Optional
from .base import OMBase

class CalendarEventModel(OMBase):
    event_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    created_by: Optional[int] = None
    ticket_id: Optional[int] = None
