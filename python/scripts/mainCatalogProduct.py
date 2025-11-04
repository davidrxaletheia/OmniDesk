"""
Helpers for managing catalog-product assignments (non-interactive).

Functions:
 - list_catalog_products(catalog_id)
 - get_catalog_product(catalog_id, product_id)
 - assign_product_to_catalog(catalog_id, product_id, special_price=None, assigned_stock=None)
 - update_assignment(catalog_id, product_id, updates)
 - remove_assignment(catalog_id, product_id)

Usage: edit ACTION at bottom or import functions.
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
from python.app.repos.catalog_product_repo import CatalogProductRepo

client = TestClient(app)
repo = CatalogProductRepo()


def list_catalog_products(catalog_id: int):
    rows = repo.list_by_catalog(catalog_id)
    for r in rows:
        print('-' * 60)
        pprint(r)
    print('-' * 60)
    return rows


def get_catalog_product(catalog_id: int, product_id: int):
    return repo.get(catalog_id, product_id)


def assign_product_to_catalog(catalog_id: int, product_id: int, special_price: Optional[float] = None, assigned_stock: Optional[int] = None):
    data = {'catalog_id': catalog_id, 'product_id': product_id}
    if special_price is not None:
        data['special_price'] = special_price
    if assigned_stock is not None:
        data['assigned_stock'] = assigned_stock
    try:
        repo.create(data)
        print('Assignment created:', catalog_id, product_id)
        return True
    except Exception as e:
        print('Error creating assignment:', repr(e))
        return False


def update_assignment(catalog_id: int, product_id: int, updates: Dict[str, Any]):
    try:
        rows = repo.update(catalog_id, product_id, updates)
        print('Updated rows:', rows)
        return rows
    except Exception as e:
        print('Error updating assignment:', repr(e))
        return None


def remove_assignment(catalog_id: int, product_id: int):
    try:
        rows = repo.delete(catalog_id, product_id)
        print('Deleted rows:', rows)
        return rows
    except Exception as e:
        print('Error deleting assignment:', repr(e))
        return None


if __name__ == '__main__':
    ACTION = 'assign'  # options: list, get, assign, update, remove

    if ACTION == 'list':
        list_catalog_products(1)

    elif ACTION == 'get':
        pprint(get_catalog_product(1, 1))

    elif ACTION == 'assign':
        assign_product_to_catalog(2, 3, special_price=99.99, assigned_stock=5)
     

    elif ACTION == 'update':
        update_assignment(1, 1, {'special_price': 79.99})

    elif ACTION == 'remove':
        remove_assignment(1, 1)

    else:
        list_catalog_products(1)
