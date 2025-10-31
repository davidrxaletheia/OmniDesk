import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from python.app.main import app
from python.app.repos.client_repo import ClientRepo
from python.app.core.security import create_access_token
import uuid

if __name__ == '__main__':
    crepo = ClientRepo()
    unique = uuid.uuid4().hex[:8]
    try:
        cid = crepo.create({'full_name': 'Premium Test', 'email': f'prem+{unique}@test.com', 'phone': f'9{unique}', 'client_type': 'premium'})
    except Exception as e:
        print('client create error:', repr(e))
        raise
    token = create_access_token({'client_id': cid, 'type': 'client'})
    client = TestClient(app)
    r = client.get('/api/products/for-client', headers={'Authorization': f'Bearer {token}'})
    print('STATUS:', r.status_code)
    print('HEADERS:', dict(r.headers))
    print('TEXT:', r.text)
    try:
        j = r.json()
        print('JSON keys:', list(j[0].keys()) if isinstance(j, list) and j else j.keys() if isinstance(j, dict) else 'other')
    except Exception as e:
        print('json parse error:', repr(e))
