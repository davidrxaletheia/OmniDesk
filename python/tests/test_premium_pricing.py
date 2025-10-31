import sys
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from python.app.main import app

from python.app.repos.client_repo import ClientRepo
from python.app.core.security import create_access_token


def test_premium_client_sees_discount(client: TestClient = TestClient(app)):
    # create a premium client directly via repo (test helper)
    import uuid
    crepo = ClientRepo()
    unique = uuid.uuid4().hex[:8]
    cid = crepo.create({'full_name': 'Premium Test', 'email': f'prem+{unique}@test.com', 'phone': f'9{unique}', 'client_type': 'premium'})
    token = create_access_token({'client_id': cid, 'type': 'client'})

    # get products for this client
    r = client.get('/api/products/for-client', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    prods = r.json()
    assert isinstance(prods, list) and len(prods) > 0
    p = prods[0]
    assert 'price' in p and 'price_for_client' in p
    # price_for_client must be <= price
    assert float(p['price_for_client']) <= float(p['price'])

    # create order and verify discount stored on items
    order_body = {'items': [{'product_id': p.get('product_id') or p.get('id') or p.get('product_id'), 'quantity': 1}], 'notes': 'Premium order'}
    r2 = client.post('/api/orders', json=order_body, headers={'Authorization': f'Bearer {token}'})
    assert r2.status_code == 200, r2.text
    created = r2.json()
    # check that discount_total or items discount present
    assert (created.get('discount_total') is not None) or any('discount_pct' in (it or {}) for it in created.get('items', []))
