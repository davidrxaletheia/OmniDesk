"""
Simple CLI for client operations (list, create, login & show).
Mirrors the patterns from `mainAppUser.py` for working with clients.
"""
import os
import sys
from pprint import pprint
from typing import Optional, List, Dict, Any
from fastapi.testclient import TestClient

# Make repo importable when running script directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.main import app
from python.app.repos.client_repo import ClientRepo

client = TestClient(app)
client_repo = ClientRepo()


def list_clients(limit: int = 10):
    """List clients using a raw query (avoids Pydantic validation on dirty rows).

    Prints every column for each client and marks empty/NULL values with '<EMPTY>'.
    """
    try:
        cur = client_repo._legacy.db.cursor()
        cur.execute('SELECT * FROM client LIMIT %s', (limit,))
        cols = [d[0] for d in cur.description]
        for row in cur.fetchall():
            data = {cols[i]: row[i] for i in range(len(cols))}
            # pretty print showing empty markers
            print('-' * 80)
            print(f"Client ID: {data.get('client_id')}")
            for k in cols:
                v = data.get(k)
                display = v if (v is not None and (not isinstance(v, str) or v.strip() != '')) else '<EMPTY>'
                print(f"  {k}: {display}")
        print('-' * 80)
    except Exception as e:
        print('Error listando clientes:', repr(e))

def get_raw_client_by_id(client_id: int) -> Dict[str, Any]:
    """Return a raw DB row (dict) for the given client_id or None."""
    try:
        cur = client_repo._legacy.db.cursor()
        cur.execute('SELECT * FROM client WHERE client_id=%s', (client_id,))
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        return {cols[i]: row[i] for i in range(len(cols))}
    except Exception as e:
        print('Error obteniendo cliente crudo:', repr(e))
        return None
    
def show_client_full(client_id: int):
    """Print all fields (with empty marker) for a single client by id."""
    r = get_raw_client_by_id(client_id)
    if not r:
        print('Cliente no encontrado:', client_id)
        return
    print('-' * 80)
    print(f"Client ID: {r.get('client_id')}")
    for k, v in r.items():
        display = v if (v is not None and (not isinstance(v, str) or v.strip() != '')) else '<EMPTY>'
        print(f"  {k}: {display}")
    print('-' * 80)

def create_client(name: str):
    """Create a client providing only the required `full_name`.

    The client table allows NULL for phone/email and has defaults for the
    other columns, so inserting only `full_name` is valid.
    """
    name = (name or '').strip()
    if not name:
        print('full_name requerido')
        return None

    try:
        cid = client_repo.create({'full_name': name})
        print('Cliente creado! id ->', cid)
        return cid
    except Exception as e:
        print('Error al crear cliente:', repr(e))
        return None

def edit_client_params(client_id: int, updates: Dict[str, Any]):
    """Edit client by id using a dict of updates (no input). Returns rows affected."""
    if not isinstance(updates, dict) or not updates:
        print('No hay actualizaciones proporcionadas')
        return 0
    try:
        rows = client_repo.update(client_id, updates)
        print(f'Actualizados {rows} filas para client_id={client_id}')
        # show result
        show_client_full(client_id)
        return rows
    except Exception as e:
        print('Error actualizando cliente:', repr(e))
        return None

def edit_client(client_id: int, full_name: Optional[str] = None, phone: Optional[str] = None,
                email: Optional[str] = None, client_type: Optional[str] = None):
    """Edita un cliente usando parámetros (no interacción).

    Devuelve el número de filas actualizadas o None en error.
    """
    try:
        c = client_repo.get(client_id)
        if not c:
            print('Cliente no encontrado: id=', client_id)
            return None

        # show current values for context
        print('Cliente actual:')
        pprint(c)

        data = {}
        if full_name:
            data['full_name'] = full_name.strip()
        if phone:
            data['phone'] = phone.strip()
        if email:
            data['email'] = email.strip()
        if client_type:
            data['client_type'] = client_type.strip()

        if not data:
            print('Nada que actualizar')
            return 0

        rows = client_repo.update(client_id, data)
        print(f'Actualizados {rows} filas')
        return rows
    except Exception as e:
        print('Error editando cliente:', repr(e))
        return None


def list_clients_by_type(client_type: str, limit: int = 50):
    try:
        clients = client_repo.by_type(client_type, limit=limit)
        for c in clients:
            cid = getattr(c, 'client_id', None) or (c.get('client_id') if isinstance(c, dict) else None)
            name = getattr(c, 'full_name', None) or (c.get('full_name') if isinstance(c, dict) else None)
            phone = getattr(c, 'phone', None) or (c.get('phone') if isinstance(c, dict) else None)
            email = getattr(c, 'email', None) or (c.get('email') if isinstance(c, dict) else None)
            print(f"({cid}) - {name}\tphone: {phone}\t{email}")
            print(c)
            print('-'*40)
    except Exception as e:
        print('Error filtrando por tipo:', repr(e))


def identify_client(telegram_username: Optional[str] = None, telegram_user_id: Optional[int] = None,
                    create_if_missing: bool = False, full_name: Optional[str] = None):
    """Identify a client by telegram username or id via POST /api/clients/identify.

    If create_if_missing is True and the client is not found, full_name must be
    provided to create the client.
    Returns (client_obj, client_token) or (None, None) on failure.
    """
    payload = {
        'telegram_username': telegram_username,
        'telegram_user_id': telegram_user_id,
        'create_if_missing': create_if_missing,
        'full_name': full_name
    }
    # remove None values to keep payload small
    payload = {k: v for k, v in payload.items() if v is not None}

    r = client.post('/api/clients/identify', json=payload)
    if r.status_code != 200:
        print('Identify fallido:', r.status_code, r.text)
        return None, None
    body = r.json()
    token = body.get('client_token') or body.get('access_token') or body.get('acces_token')
    client_obj = body.get('client')
    print('Client identified:')
    pprint(client_obj)
    print('Token:', token)
    return {'client': client_obj, 'token': token}


def update_client_via_api(client_id: int, data: dict):
    """Patch client via API endpoint PATCH /api/clients/{client_id}.

    Returns the response JSON or None on failure.
    """
    if not data:
        print('No hay datos para actualizar')
        return None
    r = client.patch(f'/api/clients/{client_id}', json=data)
    if r.status_code >= 400:
        print('Error actualizando cliente:', r.status_code, r.text)
        return None
    body = r.json()
    print('Update response:')
    pprint(body)
    return body

if __name__ == '__main__':

    #LIST CLIENTS BY TYPE
    list_clients_by_type('normal', limit=10)

    print('\n\n')

    list_clients_by_type('premium', limit=10)
    update_client_via_api(12, {'client_type': 'premium'})

    """
    ejemplo de como usar update_client_via_api
    data = {'phone': '+521900000000', 'email': 'acme@example.com'}

    """