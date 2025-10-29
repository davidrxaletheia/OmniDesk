"""Repositorio `ConversationRepo`.

Funciones para crear/consultar conversaciones por canal y cliente.
"""

from typing import List
from .base_repo import BaseRepo
from ..models import ConversationModel

class ConversationRepo(BaseRepo):
    table = "conversation"
    pk = "conversation_id"
    model = ConversationModel

    def by_client(self, client_id: int, limit: int=50) -> List[ConversationModel]:
        return self.filter("client_id=%s", (client_id,), limit=limit, order_by="last_message_at", desc=True)
