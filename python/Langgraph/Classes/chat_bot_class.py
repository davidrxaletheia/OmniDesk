from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


class Message(BaseModel):
    role: Literal['IA', 'user', 'assistant']
    content: str

class Alert(BaseModel):
    alert_id: Optional[int] = None
    chat_id: int
    message_index: int
    alert_type: str
    created_at: Optional[date] = None


class Chat(BaseModel):
    chat_id: Optional[int] = None
    user_id: int
    messages: list[Message] = Field(default_factory=list)
    created_at: Optional[date] = None

    