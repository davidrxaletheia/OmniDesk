from typing import Optional, List, Dict
from python.Classes.db import DB


class CartRepo:
    """Simple Cart repository backed by the project's DB helper.

    Methods operate on `cart` and `cart_item` tables created in the
    project's init.sql. This is intentionally small and transactional.
    """

    def create_cart(self, client_id: Optional[int] = None, metadata: Optional[dict] = None) -> int:
        with DB() as db:
            cur = db.cursor()
            sql = "INSERT INTO cart (client_id, metadata) VALUES (%s, %s)"
            cur.execute(sql, (client_id, json_or_null(metadata)))
            return cur.lastrowid

    def get_cart_by_client(self, client_id: int) -> Optional[Dict]:
        with DB() as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM cart WHERE client_id = %s AND status = 'active' LIMIT 1", (client_id,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            cart = {cols[i]: row[i] for i in range(len(cols))}
            cur.execute("SELECT * FROM cart_item WHERE cart_id = %s", (cart['cart_id'],))
            items_rows = cur.fetchall()
            items = []
            if items_rows:
                cols2 = [d[0] for d in cur.description]
                for r in items_rows:
                    items.append({cols2[i]: r[i] for i in range(len(cols2))})
            cart['items'] = items
            return cart

    def get_cart(self, cart_id: int) -> Optional[Dict]:
        with DB() as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM cart WHERE cart_id = %s", (cart_id,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            cart = {cols[i]: row[i] for i in range(len(cols))}
            cur.execute("SELECT * FROM cart_item WHERE cart_id = %s", (cart_id,))
            items_rows = cur.fetchall()
            items = []
            if items_rows:
                cols2 = [d[0] for d in cur.description]
                for r in items_rows:
                    items.append({cols2[i]: r[i] for i in range(len(cols2))})
            cart['items'] = items
            return cart

    def get_or_create_cart_for_client(self, client_id: int) -> int:
        existing = self.get_cart_by_client(client_id)
        if existing:
            return existing['cart_id']
        return self.create_cart(client_id=client_id)

    def add_or_update_item(self, cart_id: int, product_id: int, quantity: int, snapshot: Dict) -> int:
        """Insert or update cart_item: if exists, set quantity = existing + quantity."""
        with DB() as db:
            cur = db.cursor()
            # check existing
            cur.execute("SELECT cart_item_id, quantity FROM cart_item WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            row = cur.fetchone()
            if row:
                ci_id, existing_qty = row[0], row[1]
                new_qty = existing_qty + quantity
                cur.execute(
                    "UPDATE cart_item SET quantity = %s, updated_at = CURRENT_TIMESTAMP WHERE cart_item_id = %s",
                    (new_qty, ci_id),
                )
                return ci_id
            else:
                cur.execute(
                    "INSERT INTO cart_item (cart_id, product_id, quantity, unit_price, catalog_special_price, applied_catalog_discount_pct, final_price, sku, product_name, tax_rate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        cart_id,
                        product_id,
                        quantity,
                        snapshot.get('unit_price'),
                        snapshot.get('catalog_special_price'),
                        snapshot.get('applied_catalog_discount_pct'),
                        snapshot.get('final_price'),
                        snapshot.get('sku'),
                        snapshot.get('product_name'),
                        snapshot.get('tax_rate'),
                    ),
                )
                return cur.lastrowid

    def update_item_quantity(self, cart_id: int, product_id: int, quantity: int) -> bool:
        with DB() as db:
            cur = db.cursor()
            cur.execute("UPDATE cart_item SET quantity = %s, updated_at = CURRENT_TIMESTAMP WHERE cart_id = %s AND product_id = %s", (quantity, cart_id, product_id))
            return cur.rowcount > 0

    def remove_item(self, cart_id: int, product_id: int) -> bool:
        with DB() as db:
            cur = db.cursor()
            cur.execute("DELETE FROM cart_item WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            return cur.rowcount > 0

    def clear_cart(self, cart_id: int) -> None:
        with DB() as db:
            cur = db.cursor()
            cur.execute("DELETE FROM cart_item WHERE cart_id = %s", (cart_id,))

    def delete_cart(self, cart_id: int) -> None:
        with DB() as db:
            cur = db.cursor()
            cur.execute("DELETE FROM cart_item WHERE cart_id = %s", (cart_id,))
            cur.execute("DELETE FROM cart WHERE cart_id = %s", (cart_id,))


def json_or_null(v):
    import json
    if v is None:
        return None
    return json.dumps(v)
