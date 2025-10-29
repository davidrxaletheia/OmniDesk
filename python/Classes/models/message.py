"""Modelo `MessageModel`.

Representa un mensaje dentro de una `Conversation`. Contiene el
contenido, remitente y opcionalmente el identificador externo (por
ej. id en Telegram) para evitar duplicados.
"""

from datetime import datetime
from typing import Optional, Literal
from .base import OMBase

class MessageModel(OMBase):
    message_id: Optional[int] = None
    conversation_id: int
    sender: Literal['client','user','bot']
    content: str
    external_message_id: Optional[str] = None
    created_at: Optional[datetime] = None
