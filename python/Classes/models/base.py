# -*- coding: utf-8 -*-
"""Base de modelos (OMBase).

Contiene la clase `OMBase` que extiende `pydantic.BaseModel` con
configuraciones comunes para los modelos de la aplicación (modo ORM,
validación en asignación, etc.). Importar desde aquí para crear nuevos
modelos de datos.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr


class OMBase(BaseModel):
    # pydantic v2: replace inner `Config` with `model_config`.
    # `orm_mode = True` is now `from_attributes = True`.
    model_config = {
        "from_attributes": True,
        "validate_assignment": True,
    }
