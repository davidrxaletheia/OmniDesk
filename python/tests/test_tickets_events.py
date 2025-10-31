import sys
from pathlib import Path
import os

# ensure repo root on path for imports
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Allow iat fallback in tests (local env may have tiny clock skew)
os.environ.setdefault('JWT_ALLOW_IAT_FALLBACK', 'true')

from fastapi.testclient import TestClient
from python.app.main import app
import pytest


@pytest.fixture()
def client():
    return TestClient(app)


def get_token(client):
    r = client.post('/api/login', json={'username':'x0chipa','password':'Holakhace24.'})
    assert r.status_code == 200, r.text
    return r.json()['access_token']


def test_create_ticket_and_event(client):
    token = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    # Ensure we use a valid client_id (legacy DB enforces FK)
    from python.Classes.repos.client_repo import ClientRepo
    client_repo = ClientRepo()
    existing = client_repo.list(limit=1)
    if existing:
        cid = existing[0].client_id
    else:
        cid = client_repo.create({'full_name': 'pytest client', 'email': 'pytest@example.test'})

    # create ticket
    ticket_payload = {
        'client_id': cid,
        'subject': 'Test ticket from pytest',
        'description': 'Created during automated test',
        'priority': 'media'
    }
    r = client.post('/api/tickets', json=ticket_payload, headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get('subject') == ticket_payload['subject']

    # create event
    event_payload = {
        'title': 'Test Event pytest',
        'description': 'Event created during test',
        'start_time': '2025-11-01T09:00:00',
        'end_time': '2025-11-01T10:00:00'
    }
    r2 = client.post('/api/events', json=event_payload, headers=headers)
    assert r2.status_code == 200, r2.text
    body2 = r2.json()
    assert body2.get('title') == event_payload['title']