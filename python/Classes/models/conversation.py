"""Modelo `ConversationModel`.

Registra metadatos de una conversación con un cliente por canal externo
(Telegram, WhatsApp, web, etc.). Incluye el timestamp del último
mensaje y referencias opcionales al cliente.
"""

from datetime import datetime
from typing import Optional, Literal
from .base import OMBase

class ConversationModel(OMBase):
    conversation_id: Optional[int] = None
    client_id: Optional[int] = None
    channel: Literal['web','telegram','whatsapp','sms','email','other'] = 'web'
    external_chat_id: Optional[str] = None
    active: bool = True
    handled_by_bot: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
