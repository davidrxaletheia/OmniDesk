"""
Non-interactive helpers for Catalogs.

Functions:
 - list_catalogs(limit)
 - list_active_catalogs()
 - get_catalog(catalog_id)
 - create_catalog(data)
 - update_catalog_params(catalog_id, updates)
 - update_catalog_via_api(catalog_id, data, token=None)

Usage: edit the ACTION block at the bottom or import functions.
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
from python.app.repos.catalog_repo import CatalogRepo

client = TestClient(app)
repo = CatalogRepo()


def list_catalogs(limit: int = 50, offset: int = 0):
    rows = repo.list(limit=limit, offset=offset)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows


def list_active_catalogs():
    rows = repo.actives()
    for r in rows:
        pprint(r)
    return rows


def get_catalog(catalog_id: int):
    return repo.get(catalog_id)


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
        cid = repo.create(data)
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
        rows = repo.update(catalog_id, updates)
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


if __name__ == '__main__':
    ACTION = 'show'  # options: list, actives, show, create, update_api

    if ACTION == 'list':
        list_catalogs(limit=50)

    elif ACTION == 'actives':
        list_active_catalogs()

    elif ACTION == 'show':
        show_catalog_full(1)

    elif ACTION == 'create':
        create_catalog({'name': 'Buewn Fin', 'description': 'promciones de fin de año', 'discount_percentage': 25.0, 'start_date': '2025-12-10', 'end_date': '2025-12-31'})

    elif ACTION == 'update_api':
        update_catalog_via_api(1, {'name': 'Catalogo actualizado desde script', 'discount_percentage': 15.0, 'end_date': '2025-12-31'})

    else:
        list_catalogs(limit=10)
        cid = create_catalog({'name': 'script-cat-' + str(os.getpid())})
        if cid:
            show_catalog_full(cid)
