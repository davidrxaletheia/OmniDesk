import sys
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from python.app.main import app


def login(client: TestClient, username: str, password: str) -> str:
    r = client.post('/api/login', json={'username': username, 'password': password})
    assert r.status_code == 200, r.text
    return r.json()['access_token']


def test_products_rbac(client: TestClient = TestClient(app)):
    # unauthenticated
    r = client.post('/api/products', json={'sku': 'RB-1', 'name': 'RB Product', 'price': 10, 'stock': 1, 'status': 'active'})
    assert r.status_code == 401

    # employee should be forbidden
    token_emp = login(client, 'employee', 'employeepass')
    r = client.post('/api/products', json={'sku': 'RB-2', 'name': 'RB Product 2', 'price': 20, 'stock': 1, 'status': 'active'}, headers={'Authorization': f'Bearer {token_emp}'})
    assert r.status_code == 403

    # admin can create (use a unique SKU so test is idempotent)
    import uuid
    sku = f"RB-{uuid.uuid4().hex[:8]}"
    token_admin = login(client, 'admin', 'adminpass')
    r = client.post('/api/products', json={'sku': sku, 'name': 'RB Product 3', 'price': 30, 'stock': 2, 'status': 'active'}, headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 200, r.text
    body = r.json()
    assert 'product_id' in body
