import sys
from pathlib import Path
import time
import pytest
import os

# ensure repo root on path for imports
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Allow small JWT iat fallback like other tests
os.environ.setdefault('JWT_ALLOW_IAT_FALLBACK', 'true')

from fastapi.testclient import TestClient
from python.app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_create_get_list_roots(client):
    # create a unique category name to avoid collisions with seeds
    name = f"test-cat-{int(time.time())}"

    # create
    r = client.post('/api/categories', json={'name': name})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get('name') == name
    cid = body.get('category_id') or body.get('categoryId') or body.get('category_id')
    assert cid is not None

    # get by id
    r2 = client.get(f'/api/categories/{cid}')
    assert r2.status_code == 200, r2.text
    got = r2.json()
    assert got.get('name') == name

    # list roots and assert our category (parent_id=None) is present
    r3 = client.get('/api/categories/roots')
    assert r3.status_code == 200, r3.text
    roots = r3.json()
    names = [c.get('name') for c in roots if isinstance(c, dict)]
    assert name in names
