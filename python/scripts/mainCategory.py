"""
Helpers for working with categories from the testclient/repo.

Non-interactive helpers (no input()). Mirrors the style of `mainClient.py`.

Functions:
 - list_categories(limit)
 - list_roots()
 - list_children(parent_id)
 - create_category(name, parent_id=None)
 - get_category(category_id)
 - show_category_full(category_id)
 - update_category_params(category_id, updates)
 - update_category_via_api(category_id, data)

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
from python.app.repos.category_repo import CategoryRepo

client = TestClient(app)
repo = CategoryRepo()


def list_categories(limit: int = 50, offset: int = 0):
    rows = repo.list(limit=limit, offset=offset)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows


def list_roots():
    rows = repo.roots()
    print('Roots:')
    for r in rows:
        print(f"({getattr(r,'category_id',None)}) {getattr(r,'name',None)}")
    return rows


def list_children(parent_id: int):
    rows = repo.children(parent_id)
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
        cid = repo.create(data)
        print('Categoria creada! id ->', cid)
        return cid
    except Exception as e:
        print('Error creando categoria:', repr(e))
        return None


def get_category(category_id: int):
    return repo.get(category_id)


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
        rows = repo.update(category_id, updates)
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


if __name__ == '__main__':
    # Example non-interactive block. Edit variables here to perform actions.
    ACTION = 'show'  # options: demo, list, roots, children, create, show, update_api

    if ACTION == 'list':
        list_categories(limit=50)

    elif ACTION == 'roots':
        list_roots()

    elif ACTION == 'children':
        # example: show children of category 1
        list_children(1)

    elif ACTION == 'create':
        create_category('Nueva Categoria Demo', parent_id=None)

    elif ACTION == 'show':
        show_category_full(1)

    elif ACTION == 'update_api':
        update_category_via_api(1, {'name': 'Renombrada desde script'})

    else:
        # demo: list roots, create a category and show it
        list_roots()
        cid = create_category('script-demo-' + str(os.getpid()))
        if cid:
            show_category_full(cid)
