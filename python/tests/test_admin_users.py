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


def test_admin_users_crud(client: TestClient = TestClient(app)):
    import uuid
    unique = uuid.uuid4().hex[:8]
    username = f"testadmin_{unique}"
    # admin token
    token_admin = login(client, 'admin', 'adminpass')

    # create user
    r = client.post('/api/admin/users', json={'full_name': 'T Admin', 'username': username, 'email': f'{username}@example.com', 'password': 'Secret123', 'role': 'empleado'}, headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 200, r.text
    uid = r.json()['user_id']

    # get user
    r = client.get(f'/api/admin/users/{uid}', headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 200
    data = r.json()
    assert data['username'] == username

    # update user
    r = client.put(f'/api/admin/users/{uid}', json={'full_name': 'T Admin Updated'}, headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 200

    # delete user
    r = client.delete(f'/api/admin/users/{uid}', headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 200

    # ensure deleted
    r = client.get(f'/api/admin/users/{uid}', headers={'Authorization': f'Bearer {token_admin}'})
    assert r.status_code == 404
