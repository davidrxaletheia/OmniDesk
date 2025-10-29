"""Repositorio `MessageRepo`.

Maneja la persistencia de mensajes dentro de conversaciones y
consulta por `conversation_id` o `external_message_id`.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import MessageModel

class MessageRepo(BaseRepo):
    table = "message"
    pk = "message_id"
    model = MessageModel

    def by_conversation(self, conversation_id: int, limit: int=50) -> List[MessageModel]:
        return self.filter("conversation_id=%s", (conversation_id,), limit=limit, order_by="created_at", desc=True)
