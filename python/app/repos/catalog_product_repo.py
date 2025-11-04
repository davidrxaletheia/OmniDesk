from typing import List, Optional, Dict, Any
from python.Classes.db import DB


class CatalogProductRepo:
    """Simple repo to manage the catalog_product association table.

    Returns plain dictionaries (not Pydantic models) to avoid issues with
    legacy rows and to keep the interface minimal for admin scripts.
    """
    table = "catalog_product"

    def list_by_catalog(self, catalog_id: int, limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]:
        with DB() as db:
            cur = db.cursor()
            cur.execute('SELECT * FROM catalog_product WHERE catalog_id=%s LIMIT %s OFFSET %s', (catalog_id, limit, offset))
            cols = [d[0] for d in cur.description]
            out = []
            for row in cur.fetchall():
                out.append({cols[i]: row[i] for i in range(len(cols))})
            return out

    def list_by_product(self, product_id: int, limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]:
        with DB() as db:
            cur = db.cursor()
            cur.execute('SELECT * FROM catalog_product WHERE product_id=%s LIMIT %s OFFSET %s', (product_id, limit, offset))
            cols = [d[0] for d in cur.description]
            out = []
            for row in cur.fetchall():
                out.append({cols[i]: row[i] for i in range(len(cols))})
            return out

    def get(self, catalog_id: int, product_id: int) -> Optional[Dict[str, Any]]:
        with DB() as db:
            cur = db.cursor()
            cur.execute('SELECT * FROM catalog_product WHERE catalog_id=%s AND product_id=%s', (catalog_id, product_id))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return {cols[i]: row[i] for i in range(len(cols))}

    def create(self, data: Dict[str, Any]) -> bool:
        # expected keys: catalog_id, product_id, optional special_price, assigned_stock
        keys = []
        vals = []
        for k in ('catalog_id', 'product_id', 'special_price', 'assigned_stock'):
            if k in data:
                keys.append(k)
                vals.append(data[k])
        if not keys:
            raise ValueError('No valid fields to insert for catalog_product')
        placeholders = ','.join(['%s'] * len(vals))
        cols = ','.join(keys)
        sql = f'INSERT INTO catalog_product ({cols}) VALUES ({placeholders})'
        with DB() as db:
            cur = db.cursor()
            cur.execute(sql, tuple(vals))
        return True

    def update(self, catalog_id: int, product_id: int, data: Dict[str, Any]) -> int:
        if not data:
            return 0
        sets = ','.join([f"{k}=%s" for k in data.keys()])
        sql = f'UPDATE catalog_product SET {sets} WHERE catalog_id=%s AND product_id=%s'
        params = tuple(list(data.values()) + [catalog_id, product_id])
        with DB() as db:
            cur = db.cursor()
            cur.execute(sql, params)
            return cur.rowcount

    def delete(self, catalog_id: int, product_id: int) -> int:
        with DB() as db:
            cur = db.cursor()
            cur.execute('DELETE FROM catalog_product WHERE catalog_id=%s AND product_id=%s', (catalog_id, product_id))
            return cur.rowcount
