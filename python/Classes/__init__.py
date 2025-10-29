from .db import DB, get_connection
"""
Paquete `classes`.

Agrupa modelos Pydantic (`classes.models`) y repositorios de acceso a datos
(`classes.repos`). Este archivo permite importarlos convenientemente desde
`from classes import models, repos` o `from classes.models import ...`.
"""

from .models import *
from .repos import *
