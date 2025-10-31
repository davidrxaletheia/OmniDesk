import sys
from pathlib import Path
import pytest
import os

# ensure repo root on path for imports
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# For tests we allow a small JWT iat fallback to account for clock skew in
# local environments. This mirrors the development helper flag in Settings.
os.environ.setdefault('JWT_ALLOW_IAT_FALLBACK', 'true')

from fastapi.testclient import TestClient
from python.app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_login_and_summary(client):
    # Use known test user credentials present in the local DB used during development
    r = client.post('/api/login', json={'username':'x0chipa','password':'Holakhace24.'})
    assert r.status_code == 200, r.text
    body = r.json()
    assert 'access_token' in body
    token = body['access_token']

    r2 = client.get('/api/summary', headers={'Authorization': f'Bearer {token}'})
    assert r2.status_code == 200, r2.text
    summary = r2.json()
    assert 'users_count' in summary
    assert 'tickets' in summary
