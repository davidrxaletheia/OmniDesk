"""Modelo `ClientModel`.

Representa la forma de los clientes en la aplicación y coincide con
los campos de la tabla `client` en la base de datos. Usar para validar
datos de entrada y serializar respuestas.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import EmailStr
from .base import OMBase

class ClientModel(OMBase):
    client_id: Optional[int] = None
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    telegram_username: Optional[str] = None
    telegram_user_id: Optional[int] = None
    client_type: Literal['normal','premium'] = 'normal'
    status: Literal['active','inactive','blocked'] = 'active'
    registered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
