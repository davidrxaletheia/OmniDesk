# -*- coding: utf-8 -*-
"""Repositorio base (CRUD genérico).

`BaseRepo` implementa operaciones CRUD comunes (create, get, update,
delete, list, filter) y utilidades para convertir filas DB a modelos
Pydantic. Los repos específicos heredan y definen `table`, `pk` y
`model`.
"""

from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar
from pydantic import BaseModel
from ..db import DB

ModelT = TypeVar('ModelT', bound=BaseModel)

class BaseRepo:
    table: str = ""
    pk: str = "id"
    model: Type[ModelT]

    def __init__(self, db: Optional[DB]=None):
        self._own = False
        if db is None:
            self.db = DB()
            self._own = True
        else:
            self.db = db

    def close(self):
        if self._own:
            self.db.close()

    # ------- helpers -------
    @staticmethod
    def _rows_to_models(model: Type[ModelT], cur) -> List[ModelT]:
        cols = [d[0] for d in cur.description]
        out: List[ModelT] = []
        for row in cur.fetchall():
            data = {cols[i]: row[i] for i in range(len(cols))}
            out.append(model(**data))
        return out

    @staticmethod
    def _row_to_model(model: Type[ModelT], cur) -> Optional[ModelT]:
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        data = {cols[i]: row[i] for i in range(len(cols))}
        return model(**data)

    # ------- CRUD -------
    def create(self, data: Dict[str, Any]) -> int:
        # Filter data to actual table columns to avoid INSERT errors when
        # callers pass extra keys not present in the legacy schema.
        cur = self.db.cursor()
        try:
            cur.execute(f"SHOW COLUMNS FROM {self.table}")
            table_cols = [r[0] for r in cur.fetchall()]
        except Exception:
            # If SHOW COLUMNS fails (permissions or DB differences), fall back
            # to attempting the insert with provided keys.
            table_cols = None

        if table_cols is not None:
            filtered = {k: v for k, v in data.items() if k in table_cols}
        else:
            filtered = data

        if not filtered:
            raise ValueError("No valid columns to insert for table %s" % self.table)

        cols = ", ".join(filtered.keys())
        placeholders = ", ".join(["%s"] * len(filtered))
        sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
        cur.execute(sql, list(filtered.values()))
        if not self.db.autocommit: self.db.commit()
        return getattr(cur, "lastrowid", None)

    def get(self, id_: int) -> Optional[ModelT]:
        sql = f"SELECT * FROM {self.table} WHERE {self.pk}=%s"
        cur = self.db.cursor()
        cur.execute(sql, (id_,))
        return self._row_to_model(self.model, cur)

    def update(self, id_: int, data: Dict[str, Any]) -> int:
        sets = ", ".join([f"{k}=%s" for k in data.keys()])
        sql = f"UPDATE {self.table} SET {sets} WHERE {self.pk}=%s"
        cur = self.db.cursor()
        cur.execute(sql, list(data.values()) + [id_])
        if not self.db.autocommit: self.db.commit()
        return cur.rowcount

    def delete(self, id_: int) -> int:
        sql = f"DELETE FROM {self.table} WHERE {self.pk}=%s"
        cur = self.db.cursor()
        cur.execute(sql, (id_,))
        if not self.db.autocommit: self.db.commit()
        return cur.rowcount

    def list(self, limit: int=50, offset: int=0, order_by: Optional[str]=None, desc: bool=False) -> List[ModelT]:
        ob = f"ORDER BY {order_by} {'DESC' if desc else 'ASC'}" if order_by else ''
        sql = f"SELECT * FROM {self.table} {ob} LIMIT %s OFFSET %s"
        cur = self.db.cursor()
        cur.execute(sql, (limit, offset))
        return self._rows_to_models(self.model, cur)

    def filter(self, where: str, params: Tuple, limit: int=50, offset: int=0, order_by: Optional[str]=None, desc: bool=False) -> List[ModelT]:
        ob = f"ORDER BY {order_by} {'DESC' if desc else 'ASC'}" if order_by else ''
        sql = f"SELECT * FROM {self.table} WHERE {where} {ob} LIMIT %s OFFSET %s"
        cur = self.db.cursor()
        cur.execute(sql, params + (limit, offset))
        return self._rows_to_models(self.model, cur)
