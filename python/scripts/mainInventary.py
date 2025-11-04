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
from python.app.repos.catalog_repo import CatalogRepo
from python.app.repos.category_repo import CategoryRepo
from python.app.repos.catalog_product_repo import CatalogProductRepo

client = TestClient(app)
repoProd = ProductRepo()
repoCat = CatalogRepo()
repoCategory = CategoryRepo()
repoCP = CatalogProductRepo()

####################################################################################################
####################################################################################################
# Product functions 
####################################################################################################
####################################################################################################

def list_products(limit: int = 50, offset: int = 0):
    try:
        rows = repoProd.list(limit=limit, offset=offset)
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
            legacy = repoProd._legacy
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
    return repoProd.get(product_id)

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
        pid = repoProd.create(data)
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
        rows = repoProd.update(product_id, updates)
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
        if hasattr(repoProd, 'by_category'):
            rows = repoProd.by_category(category_id, limit=limit)
            for r in rows:
                pprint(r)
            return rows
    except Exception:
        pass

    # Fallback: raw SQL through legacy product repo
    try:
        legacy = repoProd._legacy
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
    
####################################################################################################
####################################################################################################
# Catalog functions
####################################################################################################
####################################################################################################
def list_catalogs(limit: int = 50, offset: int = 0):
    rows = repoCat.list(limit=limit, offset=offset)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows

def list_active_catalogs():
    rows = repoCat.actives()
    for r in rows:
        pprint(r)
    return rows

def get_catalog(catalog_id: int):
    return repoCat.get(catalog_id)

def show_catalog_full(catalog_id: int):
    c = get_catalog(catalog_id)
    if not c:
        print('Catalog not found:', catalog_id)
        return None
    pprint(c)
    return c

def create_catalog(data: Dict[str, Any]) -> Optional[int]:
    if not isinstance(data, dict) or not data.get('name'):
        print('data must be a dict and include at least a `name`')
        return None
    try:
        cid = repoCat.create(data)
        print('Catalog creado! id ->', cid)
        return cid
    except Exception as e:
        print('Error creando catalog:', repr(e))
        return None

def update_catalog_params(catalog_id: int, updates: Dict[str, Any]):
    if not updates:
        print('No hay actualizaciones proporcionadas')
        return 0
    try:
        rows = repoCat.update(catalog_id, updates)
        print(f'Actualizados {rows} filas para catalog_id={catalog_id}')
        show_catalog_full(catalog_id)
        return rows
    except Exception as e:
        print('Error actualizando catalog:', repr(e))
        return None

def update_catalog_via_api(catalog_id: int, data: Dict[str, Any], token: Optional[str] = None):
    headers = {}
    # If no token provided, try to login with seed admin credentials
    if not token:
        try:
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
            token = None

    if token:
        headers = {'Authorization': f'Bearer {token}'}

    r = client.put(f'/api/catalogs/{catalog_id}', json=data, headers=headers)
    if r.status_code >= 400:
        print('Error actualizando catalog via API:', r.status_code, r.text)
        return None
    body = r.json()
    print('Update response:')
    pprint(body)
    return body


####################################################################################################
####################################################################################################
# Category functions
####################################################################################################
####################################################################################################

def list_categories(limit: int = 50, offset: int = 0):
    rows = repoCategory.list(limit=limit, offset=offset)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows

def list_roots():
    rows = repoCategory.roots()
    print('Roots:')
    for r in rows:
        print(f"({getattr(r,'category_id',None)}) {getattr(r,'name',None)}")
    return rows

def list_children(parent_id: int):
    rows = repoCategory.children(parent_id)
    print(f'Children of {parent_id}:')
    for r in rows:
        print(f"({getattr(r,'category_id',None)}) {getattr(r,'name',None)}")
    return rows

def create_category(name: str, parent_id: Optional[int] = None) -> Optional[int]:
    name = (name or '').strip()
    if not name:
        print('name requerido')
        return None
    data: Dict[str, Any] = {'name': name}
    if parent_id is not None:
        data['parent_id'] = parent_id
    try:
        cid = repoCategory.create(data)
        print('Categoria creada! id ->', cid)
        return cid
    except Exception as e:
        print('Error creando categoria:', repr(e))
        return None

def get_category(category_id: int):
    return repoCategory.get(category_id)

def show_category_full(category_id: int):
    c = get_category(category_id)
    if not c:
        print('Category not found:', category_id)
        return None
    pprint(c)
    return c

def update_category_params(category_id: int, updates: Dict[str, Any]):
    if not updates:
        print('No hay actualizaciones proporcionadas')
        return 0
    try:
        rows = repoCategory.update(category_id, updates)
        print(f'Actualizados {rows} filas para category_id={category_id}')
        show_category_full(category_id)
        return rows
    except Exception as e:
        print('Error actualizando categoria:', repr(e))
        return None

def update_category_via_api(category_id: int, data: Dict[str, Any]):
    if not data:
        print('No hay datos para actualizar')
        return None
    r = client.patch(f'/api/categories/{category_id}', json=data)
    if r.status_code >= 400:
        print('Error actualizando categoria via API:', r.status_code, r.text)
        return None
    body = r.json()
    print('Update response:')
    pprint(body)
    return body

####################################################################################################
####################################################################################################
# Category functions
####################################################################################################
####################################################################################################

def list_catalog_products(catalog_id: int):
    rows = repoCP.list_by_catalog(catalog_id)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows

def get_catalog_product(catalog_id: int, product_id: int):
    return repoCP.get(catalog_id, product_id)

def assign_product_to_catalog(catalog_id: int, product_id: int, special_price: Optional[float] = None, assigned_stock: Optional[int] = None):
    data = {'catalog_id': catalog_id, 'product_id': product_id}
    if special_price is not None:
        data['special_price'] = special_price
    if assigned_stock is not None:
        data['assigned_stock'] = assigned_stock
    try:
        repoCP.create(data)
        print('Assignment created:', catalog_id, product_id)
        return True
    except Exception as e:
        print('Error creating assignment:', repr(e))
        return False

def update_assignment(catalog_id: int, product_id: int, updates: Dict[str, Any]):
    try:
        rows = repoCP.update(catalog_id, product_id, updates)
        print('Updated rows:', rows)
        return rows
    except Exception as e:
        print('Error updating assignment:', repr(e))
        return None

def remove_assignment(catalog_id: int, product_id: int):
    try:
        rows = repoCP.delete(catalog_id, product_id)
        print('Deleted rows:', rows)
        return rows
    except Exception as e:
        print('Error deleting assignment:', repr(e))
        return None


#main

if __name__ == '__main__':
    print("hola mundo")
    #muestra un catalogo y toos los productos de ese catalogo y la informacion de cada producto de ese catalogo
    catalog_id = 1
    show_catalog_full(catalog_id)
    list_catalog_products(catalog_id)
    for cp in list_catalog_products(catalog_id):
        product_id = cp.get('product_id')
        if product_id:
            show_product_full(product_id)
