"""
Helpers for working with products from the testclient/repo.

Non-interactive helpers (no input()). Mirrors the style of `mainClient.py` and `mainCategory.py`.

Functions:
 - list_products(limit)
 - get_product(product_id)
 - show_product_full(product_id)
 - create_product(data)
 - update_product_params(product_id, updates)
 - update_product_via_api(product_id, data)
 - list_by_category(category_id, limit)

Usage: edit the bottom `ACTION` block or import functions from other scripts.
"""
import os
import sys
from pprint import pprint
from typing import Optional, Dict, Any
from fastapi.testclient import TestClient

# Make repo importable when running script directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.main import app
from python.app.repos.product_repo import ProductRepo

client = TestClient(app)
repo = ProductRepo()


def list_products(limit: int = 50, offset: int = 0):
    try:
        rows = repo.list(limit=limit, offset=offset)
        for r in rows:
            print('-' * 60)
            pprint(r)
        print('-' * 60)
        return rows
    except Exception as e:
        # Legacy DB may contain rows that fail Pydantic validation (e.g. NULL in
        # non-optional fields like `sku`). In that case, fallback to a raw SQL
        # fetch and return dictionaries so the admin script can still inspect
        # data without crashing.
        print('Falling back to raw SQL list_products due to:', repr(e))
        try:
            legacy = repo._legacy
            cur = legacy.db.cursor()
            cur.execute('SELECT * FROM product LIMIT %s OFFSET %s', (limit, offset))
            cols = [d[0] for d in cur.description]
            out = []
            for row in cur.fetchall():
                data = {cols[i]: row[i] for i in range(len(cols))}
                out.append(data)
                print('-' * 60)
                pprint(data)
            print('-' * 60)
            return out
        except Exception as e2:
            print('Error during raw SQL fallback:', repr(e2))
            return []


def get_product(product_id: int):
    return repo.get(product_id)


def show_product_full(product_id: int):
    p = get_product(product_id)
    if not p:
        print('Product not found:', product_id)
        return None
    pprint(p)
    return p


def create_product(data: Dict[str, Any]) -> Optional[int]:
    # minimal validation
    if not isinstance(data, dict) or not data.get('name'):
        print('data must be a dict and include at least a `name`')
        return None
    try:
        pid = repo.create(data)
        print('Producto creado! id ->', pid)
        return pid
    except Exception as e:
        print('Error creando producto:', repr(e))
        return None


def update_product_params(product_id: int, updates: Dict[str, Any]):
    if not updates:
        print('No hay actualizaciones proporcionadas')
        return 0
    try:
        rows = repo.update(product_id, updates)
        print(f'Actualizados {rows} filas para product_id={product_id}')
        show_product_full(product_id)
        return rows
    except Exception as e:
        print('Error actualizando producto:', repr(e))
        return None


def update_product_via_api(product_id: int, data: Dict[str, Any], token: Optional[str] = None):
    """Update a product via the API. If `token` is not provided, the function
    will try to log in using the demo admin credentials from `seed_data`.

    Returns the parsed JSON response on success or None on failure.
    """
    if not data:
        print('No hay datos para actualizar')
        return None

    # Obtain a token if none provided by attempting to log in with seed admin creds
    headers = {}
    if not token:
        try:
            # Try to import the seed admin credentials defined in the project
            from python.scripts.seed_data import ADMIN_CREDENTIALS
            uname = ADMIN_CREDENTIALS.get('username')
            pwd = ADMIN_CREDENTIALS.get('password')
            if uname and pwd:
                r_token = client.post('/api/login', json={'username': uname, 'password': pwd})
                if r_token.status_code == 200:
                    token = r_token.json().get('access_token')
                else:
                    print('Login with admin creds failed:', r_token.status_code, r_token.text)
        except Exception:
            # If import or login fails, we'll proceed without token and let the API return 401
            token = None

    if token:
        headers = {'Authorization': f'Bearer {token}'}

    # Use PUT because the API exposes PUT /products/{product_id}
    r = client.put(f'/api/products/{product_id}', json=data, headers=headers)
    if r.status_code >= 400:
        print('Error actualizando producto via API:', r.status_code, r.text)
        return None
    body = r.json()
    print('Update response:')
    pprint(body)
    return body


def list_by_category(category_id: int, limit: int = 50):
    # Legacy repo may not have by_category; try a search/filter via repo.list and raw SQL as fallback
    try:
        # Try to call a hypothetical method
        if hasattr(repo, 'by_category'):
            rows = repo.by_category(category_id, limit=limit)
            for r in rows:
                pprint(r)
            return rows
    except Exception:
        pass

    # Fallback: raw SQL through legacy product repo
    try:
        legacy = repo._legacy
        cur = legacy.db.cursor()
        cur.execute('SELECT * FROM product WHERE category_id=%s LIMIT %s', (category_id, limit))
        cols = [d[0] for d in cur.description]
        out = []
        for row in cur.fetchall():
            data = {cols[i]: row[i] for i in range(len(cols))}
            out.append(data)
            pprint(data)
        return out
    except Exception as e:
        print('Error listando por categoria:', repr(e))
        return None


if __name__ == '__main__':
    # Example non-interactive block. Edit variables here to perform actions.
    ACTION = 'by_category'  # options: demo, list, show, create, update_api, by_category

    if ACTION == 'list':
        list_products(limit=50)

    elif ACTION == 'show':
        show_product_full(1)

    elif ACTION == 'create':
        create_product({'name': 'Producto Demo', 'price': 10.0, 'category_id': 1})

    elif ACTION == 'update_api':
        update_product_via_api(13, {'image_url': 'http://example.com/new_image.jpg','name': 'nuevo nombre'})

    elif ACTION == 'by_category':
        list_by_category(1, limit=50)

    else:
        # demo: list, create and show
        list_products(limit=10)
        pid = create_product({'name': 'script-prod-' + str(os.getpid()), 'price': 1.0, 'category_id': 1})
        if pid:
            show_product_full(pid)
