"""Modelos de usuario (AppUser).

Define `AppUserModel`, el contrato Pydantic que representa la tabla
`app_user`. Usar este modelo para validación de entrada/salida.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import EmailStr
from .base import OMBase

class AppUserModel(OMBase):
    user_id: Optional[int] = None
    full_name: str
    username: str
    email: Optional[EmailStr] = None
    password_hash: str
    role: Literal['admin','empleado'] = 'empleado'
    active: bool = True
    last_login_at: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
