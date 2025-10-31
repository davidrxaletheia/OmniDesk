import sys
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from python.app.main import app


def test_client_signup_and_order_flow(client: TestClient = TestClient(app)):
    # Signup a new client
    import uuid
    phone = f"+521{uuid.uuid4().hex[:8]}"
    # use a unique email per test run to avoid duplicate-key collisions in the shared dev DB
    email = f"ana.client+{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post('/api/clients', json={'full_name': 'Ana Cliente', 'email': email, 'phone': phone})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert 'client_token' in data and 'client_id' in data
    token = data['client_token']
    client_id = data['client_id']

    # List products and pick first
    r = client.get('/api/products')
    assert r.status_code == 200
    prods = r.json()
    assert isinstance(prods, list) and len(prods) > 0
    first = prods[0]
    product_id = first.get('product_id') or first.get('product_id') or first.get('product_id')
    # legacy models sometimes name id different; try common keys
    if not product_id:
        # try 'id' or 'product_id'
        product_id = first.get('id') or first.get('product_id')
    assert product_id, 'No product id found'

    # Create order using client token
    order_body = {'items': [{'product_id': product_id, 'quantity': 1}], 'notes': 'Order from test'}
    r2 = client.post('/api/orders', json=order_body, headers={'Authorization': f'Bearer {token}'})
    assert r2.status_code == 200, r2.text
    created = r2.json()
    # should have order_id or similar
    assert isinstance(created, dict)

    # List orders for this client using token
    r3 = client.get('/api/orders', headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200
    orders = r3.json()
    assert isinstance(orders, list)
    # At least one order returned
    assert any(('order_id' in o) or ('id' in o) for o in orders)

    # Client must not be able to create a product (admin endpoint)
    r4 = client.post('/api/products', json={'sku': 'CL-TEST', 'name': 'Bad', 'price': 1, 'stock': 1, 'status': 'active'}, headers={'Authorization': f'Bearer {token}'})
    assert r4.status_code != 200
