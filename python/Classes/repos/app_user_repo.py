from typing import List, Optional
from .base_repo import BaseRepo
from ..models import AppUserModel

"""Repositorio `AppUserRepo`.

Operaciones específicas para la tabla `app_user`.
"""

class AppUserRepo(BaseRepo):
    table = "app_user"
    pk = "user_id"
    model = AppUserModel

    def find_by_username(self, username: str) -> Optional[AppUserModel]:
        rows = self.filter("username=%s", (username,), limit=1)
        return rows[0] if rows else None
