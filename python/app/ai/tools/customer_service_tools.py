import os
import sys
from pprint import pprint
from typing import Any, Dict, Optional, List, Tuple, Union
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime
from langchain_core.tools import tool

# Minimal Pydantic models used by the demo tools below. If your project
# already defines equivalent classes, feel free to replace these imports
# with the project's definitions.
class BusinessInfo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    website: Optional[str] = None
    social: Optional[Dict[str, str]] = None


class AdminStatus(BaseModel):
    conversation_id: str
    active: bool = False
    activated_by: Optional[int] = None
    updated_at: Optional[str] = None


# In-memory admin flags (demo only)
_admin_flags: Dict[str, AdminStatus] = {}


def _now_iso() -> str:
    return datetime.utcnow().isoformat()

from fastapi.testclient import TestClient

# Make repo importable when running this file directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.main import app
from python.app.repos.client_repo import ClientRepo

client = TestClient(app)
client_repo = ClientRepo()


"""
la idea es la siguiente
1. Identificar al cliente usando su teléfono, username o user_id de Telegram
2. si el cliente no existe no mostrar nada
3. si el cliente existe pero su status es "inactive" o "blocked", no mostrar nada
4. si el cliente existe y su status es "active", devolver un token JWT para autenticación
5. si se pasa create_if_missing=True y full_name, crear el cliente con los datos minimossi no existe

una vez tenemos esto, podemos acceder a las siguientes funcionalidades

    -ver catalogos y toda su informacion
    -acceder por completo a productos, categorias, subcategorias, catalogos, etc... consultas en general.
    -acciones del carrito. 
    -hacer pedidos
    -ver el estado de sus pedidos
    -editar pedidos existentes
    - eliminar pedidos (con ciertas restricciones)
    -modificar su informacion de contacto
    -solicitar facturas de pedidos
    -hacer un carrito con los productos que quiere comprar (esto no esta en bd, simplemente crearemos una lista en memoria que podemos usar para crar el pedido)

"""


# ------------------------
# Herramientas de negocio
# ------------------------

@tool
def get_business_info_tool(db: Optional[Session] = None) -> BusinessInfo:
    """Obtiene los datos del negocio desde BD. Si no hay BD, retorna valores de ejemplo."""
    if db is None:
        return BusinessInfo(
            name="Aura Idiomas",
            description="Escuela de inglés con IA conversacional.",
            phone="+52 55 9876 5432",
            email="info@auraidiomas.com",
            address="Av. del Aprendizaje 202, CDMX",
            opening_hours={
                "mon": "08:00-20:00",
                "tue": "08:00-20:00",
                "wed": "08:00-20:00",
                "thu": "08:00-20:00",
                "fri": "08:00-18:00",
                "sat": "09:00-14:00",
                "sun": "closed",
            },
            website="https://auraidiomas.com",
            social={"instagram": "@auraidiomas"}
        )

    row = db.execute(
        text("SELECT name, description, phone, email, address, website FROM business LIMIT 1")
    ).mappings().first()
    if not row:
        return get_business_info_tool(None)

    info = BusinessInfo(**row)
    hours = db.execute(text("SELECT day_code, open_close FROM business_hours")).mappings()
    info.opening_hours = {h["day_code"]: h["open_close"] for h in hours}
    return info


# ------------------------
# Herramientas de ADMIN
# ------------------------

@tool
def set_admin_status_tool(conversation_id: str, active: bool, by_user_id: Optional[int] = None) -> AdminStatus:
    """Activa o desactiva el modo ADMIN (toma de control humano) para una conversación."""
    status = AdminStatus(conversation_id=conversation_id, active=active, activated_by=by_user_id, updated_at=_now_iso())
    _admin_flags[conversation_id] = status
    return status


@tool
def get_admin_status_tool(conversation_id: str) -> AdminStatus:
    """Consulta si el modo ADMIN está activo para una conversación."""
    status = _admin_flags.get(conversation_id)
    if status is None:
        status = AdminStatus(conversation_id=conversation_id, active=False, updated_at=_now_iso())
        _admin_flags[conversation_id] = status
    return status

#funciones que definen el estado del cliente 
"""
@tool
def set_admin_status_tool(conversation_id: str, active: bool, by_user_id: Optional[int] = None) -> AdminStatus:
    Activa o desactiva el modo ADMIN (toma de control humano) para una conversación.
@tool
def get_admin_status_tool(conversation_id: str) -> AdminStatus:
    Consulta si el modo ADMIN está activo para una conversación.
"""



# ==============================================================================================
# Helpers internos (sin prints)
# ==============================================================================================

def _json(resp) -> Optional[Dict[str, Any]]:
    try:
        return resp.json()
    except Exception:
        return None

def _auth_headers(token: str) -> Dict[str, str]:
    return {'Authorization': f'Bearer {token}'} if token else {}

def _normalize_phone(phone: str) -> str:
    """Conserva '+' al inicio, quita separadores."""
    if not phone:
        return phone
    phone = phone.strip()
    keep_plus = phone.startswith('+')
    digits = ''.join(ch for ch in phone if ch.isdigit())
    return ('+' + digits) if keep_plus else digits

def _client_id_from_token(token: str) -> Optional[int]:
    if not token:
        return None
    try:
        from python.app.core.security import decode_token
        payload = decode_token(token)
        sub = payload.get('sub') or {}
        return sub.get('client_id') if isinstance(sub, dict) else None
    except Exception:
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            sub = payload.get('sub') or {}
            return sub.get('client_id') if isinstance(sub, dict) else None
        except Exception:
            return None

def _get_client_type(client_id: Optional[int]) -> Optional[str]:
    if not client_id:
        return None
    try:
        cobj = client_repo.get(client_id)
        return getattr(cobj, 'client_type', None)
    except Exception:
        return None

# ==============================================================================================
# Identify client via API endpoint POST /api/clients/identify.
# ==============================================================================================

@tool
def identify_client(telegram_username: Optional[str] = None, telegram_user_id: Optional[int] = None,
                    phone: Optional[str] = None, create_if_missing: bool = False, full_name: Optional[str] = None):
    """Identify a client via POST /api/clients/identify. Returns {'client':..., 'token':...} o None."""
    payload = {
        'telegram_username': telegram_username,
        'telegram_user_id': telegram_user_id,
        'phone': phone,
        'create_if_missing': create_if_missing,
        'full_name': full_name
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    r = client.post('/api/clients/identify', json=payload)  
    if r.status_code != 200:
        return None
    body = _json(r) or {}
    token = body.get('client_token') or body.get('access_token') or body.get('acces_token')
    client_obj = body.get('client')
    return {'client': client_obj, 'token': token}

@tool
def update_client_via_api(client_id: int, data: dict):
    """PATCH /api/clients/{client_id}. Devuelve JSON o None."""
    if not data:
        return None
    r = client.patch(f'/api/clients/{client_id}', json=data)
    if r.status_code >= 400:
        return None
    return _json(r)

# Client auth and identification return the token.
@tool
def client_auth(
    telegram_user_id: int | str | None = None,
    telegram_username: str | None = None,
    create_if_missing: bool = False,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
) -> dict:
    """Autentica por telegram_user_id/telegram_username. Sin prints; retorna dict estándar."""
    if telegram_user_id is None and not telegram_username and not phone:
        return {"ok": False, "data": None, "error": "missing_credentials"}

    try:
        kwargs = {
            'telegram_user_id': telegram_user_id,
            'telegram_username': telegram_username,
            'create_if_missing': create_if_missing,
            'full_name': full_name,
            'phone': phone,
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        res = identify_client(**kwargs)
        if not res:
            return {"ok": False, "data": None, "error": "not_found"}

        token = None
        client_obj = None
        if isinstance(res, dict):
            token = res.get('token') or res.get('client_token') or res.get('access_token')
            client_obj = res.get('client') or res.get('client_obj') or res.get('client_data')
            if not token and isinstance(res.get('data'), dict):
                token = res['data'].get('client_token') or res['data'].get('token')
                client_obj = client_obj or res['data'].get('client')

        if not token:
            return {"ok": False, "data": None, "error": "no_token"}

        return {"ok": True, "data": {"client_token": token, "client": client_obj}, "error": None}
    except Exception:
        return {"ok": False, "data": None, "error": "exception"}

@tool
def get_client_token(
    telegram_user_id: int | str | None = None,
    telegram_username: str | None = None,
    create_if_missing: bool = True,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
) -> Optional[str]:
    """Devuelve el token JWT o None. Sin impresiones internas."""
    norm_phone = _normalize_phone(phone) if phone else None

    r = client_auth(
        telegram_user_id=telegram_user_id,
        telegram_username=telegram_username,
        create_if_missing=False,
        full_name=None,
        phone=norm_phone,
    )
    if r.get('ok') and r.get('data'):
        return r['data'].get('client_token')

    if create_if_missing:
        fallback_name = full_name
        if not fallback_name:
            if telegram_username:
                fallback_name = f"Client {telegram_username}"
            elif norm_phone:
                fallback_name = f"Client {norm_phone}"
            elif telegram_user_id:
                fallback_name = f"Client {telegram_user_id}"
            else:
                fallback_name = "Client (auto)"

        r2 = client_auth(
            telegram_user_id=telegram_user_id,
            telegram_username=telegram_username,
            create_if_missing=True,  # aquí sí debe crear
            full_name=fallback_name,
            phone=norm_phone,
        )
        if r2.get('ok') and r2.get('data'):
            return r2['data'].get('client_token')

    return None

# Provide a plain-python callable pointing to the original function implementation.
# When `@tool` from langchain_core is used the decorator returns a Tool object
# which may not accept keyword args in __call__. For local interactive use we
# prefer to call the original wrapped function directly if available.
try:
    _get_client_token_plain = get_client_token.__wrapped__  # original function when decorated
except Exception:
    _get_client_token_plain = getattr(get_client_token, "func", get_client_token)

@tool
def ensure_client_and_get_token(phone: Optional[str] = None, full_name: Optional[str] = None,
                                telegram_user_id: Optional[int] = None, telegram_username: Optional[str] = None) -> Optional[str]:
    """Obtiene token; si no existe y hay full_name, crea y devuelve token. Sin prints."""
    norm_phone = _normalize_phone(phone) if phone else None

    token = _get_client_token_plain(telegram_user_id=telegram_user_id, telegram_username=telegram_username,
                                    create_if_missing=False, full_name=None, phone=norm_phone)
    if token:
        return token

    if full_name:
        token = _get_client_token_plain(telegram_user_id=telegram_user_id, telegram_username=telegram_username,
                                        create_if_missing=True, full_name=full_name, phone=norm_phone)
        return token

    return None

# ==============================================================================================
# Explorar inventario (solo vista) — sin impresiones internas
# ==============================================================================================

@tool
def list_catalogs_for_client(client_token: str) -> Optional[Dict[str, Any]]:
    """Lista catálogos según tipo de cliente. Premium ve todos; normal sólo visibles para todos."""
    if not client_token:
        return None

    client_id = _client_id_from_token(client_token)
    if not client_id:
        return None

    try:
        client_obj = client_repo.get(client_id)
    except Exception:
        return None

    if not client_obj:
        return None

    if getattr(client_obj, 'status', None) != 'active':
        return None

    client_type = getattr(client_obj, 'client_type', 'normal')
    endpoint = '/api/catalogs' if client_type == 'premium' else '/api/catalogs/actives'

    r = client.get(endpoint, headers=_auth_headers(client_token))
    if r.status_code != 200:
        return None

    catalogs = _json(r)
    if catalogs is None:
        return None

    if client_type != 'premium' and isinstance(catalogs, list):
        return [c for c in catalogs if (isinstance(c, dict) and (c.get('visible_to') in (None, 'todos')))]
    return catalogs

@tool
def list_categories_by_catalog_id(catalog_id: int, client_token: str) -> Optional[Dict[str, Any]]:
    """Lista categorías para un catálogo según token."""
    if not client_token or not catalog_id:
        return None

    headers = _auth_headers(client_token)
    r = client.get(f'/api/catalogs/{catalog_id}/products', headers=headers)
    if r.status_code != 200:
        return None
    catalog_products = _json(r)
    if catalog_products is None:
        return None

    product_ids = [cp.get('product_id') for cp in catalog_products if isinstance(cp, dict) and cp.get('product_id')]
    category_ids: List[int] = []
    for pid in product_ids:
        pr = client.get(f'/api/products/{pid}', headers=headers)
        if pr.status_code != 200:
            continue
        pdata = _json(pr) or {}
        cid = pdata.get('category_id') if isinstance(pdata, dict) else None
        if cid:
            category_ids.append(cid)

    seen, uniq_cids = set(), []
    for cid in category_ids:
        if cid not in seen:
            seen.add(cid)
            uniq_cids.append(cid)

    categories = []
    for cid in uniq_cids:
        cr = client.get(f'/api/categories/{cid}', headers=headers)
        if cr.status_code != 200:
            continue
        cdata = _json(cr)
        if cdata is not None:
            categories.append(cdata)

    return categories

@tool
def list_products_by_catalog_and_category(catalog_id: int, category_filter: Optional[str | int], client_token: str,
                                          q: Optional[str] = None) -> Optional[list]:
    """Lista productos de un catálogo, filtrando por categoría id o 'A'/'a' = todas."""
    if not client_token or not catalog_id:
        return None

    headers = _auth_headers(client_token)
    r = client.get(f'/api/catalogs/{catalog_id}/products', headers=headers)
    if r.status_code != 200:
        return None
    catalog_products = _json(r)
    if catalog_products is None:
        return None

    product_ids = [cp.get('product_id') for cp in catalog_products if isinstance(cp, dict) and cp.get('product_id')]

    all_flag = False
    target_cid = None
    if category_filter is None:
        all_flag = True
    elif isinstance(category_filter, str) and category_filter.lower() == 'a':
        all_flag = True
    else:
        try:
            target_cid = int(category_filter)
        except Exception:
            all_flag = True

    out = []
    for pid in product_ids:
        pr = client.get(f'/api/products/{pid}', headers=headers)
        if pr.status_code != 200:
            continue
        pdata = _json(pr)
        if not isinstance(pdata, dict):
            continue

        cid = pdata.get('category_id')
        if not all_flag and cid != target_cid:
            continue

        if q:
            text = f"{pdata.get('name', '')} {pdata.get('description', '')}".lower()
            if q.lower() not in text:
                continue

        out.append(pdata)

    return out

@tool
def get_product_details_for_client(catalog_id: int, product_id: int, client_token: str) -> Optional[Dict[str, Any]]:
    """Calcula precios/desc. según catálogo y tipo de cliente. Sin impresiones."""
    if not client_token or not catalog_id or not product_id:
        return None

    headers = _auth_headers(client_token)

    pr = client.get(f'/api/products/{product_id}', headers=headers)
    if pr.status_code != 200:
        return None
    product = _json(pr) or {}

    cpr = client.get(f'/api/catalogs/{catalog_id}/products/{product_id}', headers=headers)
    catalog_product = _json(cpr) if cpr.status_code == 200 else None

    client_id = _client_id_from_token(client_token)
    client_type = _get_client_type(client_id)

    def _to_float(v):
        try:
            return float(v)
        except Exception:
            return None

    price_normal = _to_float(product.get('price'))

    catalog_special_price = None
    if isinstance(catalog_product, dict):
        catalog_special_price = _to_float(catalog_product.get('special_price'))

    cr = client.get(f'/api/catalogs/{catalog_id}', headers=headers)
    catalog = _json(cr) if cr.status_code == 200 else None

    catalog_discount_pct = 0.0
    if isinstance(catalog, dict):
        try:
            catalog_discount_pct = float(catalog.get('discount_percentage') or 0.0) / 100.0
        except Exception:
            catalog_discount_pct = 0.0

    effective_catalog_price = None
    catalog_discount_amount = None
    if catalog_special_price is not None:
        effective_catalog_price = catalog_special_price
        if isinstance(price_normal, (int, float)):
            catalog_discount_amount = round(price_normal - effective_catalog_price, 2)
    else:
        if catalog_discount_pct and isinstance(price_normal, (int, float)):
            effective_catalog_price = round(price_normal * (1.0 - catalog_discount_pct), 2)
            catalog_discount_amount = round(price_normal - effective_catalog_price, 2)
        else:
            effective_catalog_price = price_normal
            catalog_discount_amount = 0.0

    premium_pct = 0.0
    try:
        from python.app.core.config import settings
        if client_type == 'premium':
            premium_pct = float(getattr(settings, 'PREMIUM_DISCOUNT_PCT', 0.0))
    except Exception:
        premium_pct = 0.0

    price_for_client = None
    premium_discount_amount = None
    if effective_catalog_price is not None:
        try:
            if premium_pct and client_type == 'premium':
                price_for_client = round(effective_catalog_price * (1.0 - premium_pct), 2)
                premium_discount_amount = round(effective_catalog_price - price_for_client, 2)
            else:
                price_for_client = round(effective_catalog_price, 2) if isinstance(effective_catalog_price, (int, float)) else effective_catalog_price
                premium_discount_amount = 0.0
        except Exception:
            price_for_client = effective_catalog_price
            premium_discount_amount = None

    result = {
        'product': product,
        'catalog_product': catalog_product,
        'catalog': catalog,
        'price_normal': price_normal,
        'catalog_special_price': catalog_special_price,
        'catalog_discount_pct': catalog_discount_pct,
        'effective_catalog_price': effective_catalog_price,
        'catalog_discount_amount': catalog_discount_amount,
        'premium_pct': premium_pct,
        'premium_discount_amount': premium_discount_amount,
        'price_for_client': price_for_client,
        'client_type': client_type,
    }
    return result

# ==============================================================================================
# Cart helper tools — sin impresiones internas
# ==============================================================================================

@tool
def find_catalog_for_product(client_token: str, product_id: int) -> Optional[int]:
    """Busca un catálogo (visible para el cliente) que contenga product_id."""
    if not client_token:
        return None         
    try:
        catalogs = list_catalogs_for_client(client_token)
    except Exception:
        catalogs = None
    if not catalogs:
        try:
            r = client.get('/api/catalogs')
            if r.status_code == 200:
                catalogs = _json(r)
        except Exception:
            catalogs = None

    if not catalogs:
        return None

    for c in catalogs:
        try:
            cid = c.get('catalog_id') if isinstance(c, dict) else None
            if cid is None:
                continue
            r = client.get(f'/api/catalogs/{cid}/products/{int(product_id)}', headers=_auth_headers(client_token))
            if r.status_code == 200:
                return int(cid)
        except Exception:
            continue
    return None

@tool
def format_order_ticket(order_payload: Dict[str, Any]) -> str:
    """Devuelve un ticket de pedido en texto plano (sin imprimir)."""
    def _fmt_money(v):
        try:
            return f"{float(v):.2f}"
        except Exception:
            return str(v)

    lines: List[str] = []
    header = None
    items = []
    if isinstance(order_payload, dict):
        header = order_payload.get('order') or order_payload.get('header') or order_payload
        items = order_payload.get('items') or order_payload.get('items_detail') or (header.get('items') if isinstance(header, dict) else None) or []
    else:
        header = order_payload

    lines.append('=' * 60)
    lines.append('ORDER SUMMARY')
    lines.append('-' * 60)
    if header and isinstance(header, dict):
        oid = header.get('order_id')
        client_id = header.get('client_id')
        created_at = header.get('created_at')
        grand = header.get('grand_total')
        lines.append(f"Order id: {oid}    client_id: {client_id}    created_at: {created_at}")
        lines.append(f"Grand total: { _fmt_money(grand) if grand is not None else 'N/A'}")
    lines.append('-' * 60)

    if items:
        lines.append('')
        lines.append('=' * 60)
        lines.append('    OMNIDESK - ORDER TICKET'.center(60))
        lines.append('-' * 60)
        if header and isinstance(header, dict):
            lines.append(f"Order: {header.get('order_id') or '<id?>'}    Date: {header.get('created_at') or ''}    Client: {header.get('client_id') or ''}")
        lines.append('-' * 60)
        lines.append(f"{'PID':>4} {'PRODUCT':30} {'QTY':>3} {'PU':>8} {'FINAL':>8} {'LINE':>10}")
        lines.append('-' * 60)
        total = 0.0
        for it in items:
            pid = it.get('product_id')
            name = it.get('product_name') or ''
            qty = int(it.get('quantity') or 0)
            pu = it.get('unit_price')
            final = it.get('final_unit') if it.get('final_unit') is not None else it.get('final_price') if it.get('final_price') is not None else pu
            try:
                line_total = float(final or 0) * qty
            except Exception:
                line_total = 0.0
            total += line_total
            lines.append(f"{str(pid):>4} {name[:30]:30} {qty:>3} { _fmt_money(pu):>8} { _fmt_money(final):>8} { _fmt_money(line_total):>10}")
        lines.append('-' * 60)
        lines.append(f"{'CALC TOTAL:':>56} { _fmt_money(total):>10}")
        lines.append('=' * 60)
    else:
        lines.append('(no items)')

    return '\n'.join(lines)

@tool
def add_to_cart(client_token: str, product_id: int, quantity: int = 1, catalog_id: Optional[int] = None,
                verify_price: bool = False) -> Dict[str, Any]:
    """Agrega un producto al carrito. Devuelve estructura con verificación opcional."""
    result = {'ok': False, 'resp': None, 'final_price': None, 'expected_price': None, 'mismatch': False, 'error': None}

    if not client_token:
        result['error'] = 'client_token required'
        return result

    headers = _auth_headers(client_token)
    payload = {'product_id': int(product_id), 'quantity': int(quantity)}
    try:
        r = client.post('/api/clients/cart/items', json=payload, headers=headers)
    except Exception as exc:
        result['error'] = f'post failed: {exc!r}'
        return result

    if r.status_code >= 400:
        result['error'] = f'add_to_cart failed: {r.status_code} {r.text}'
        return result

    result['resp'] = _json(r)

    cart = get_cart(client_token)
    final_price = None
    if isinstance(cart, dict):
        items = cart.get('items') or cart.get('cart_items') or (cart.get('cart') or {}).get('items') or []
        for it in items:
            if int(it.get('product_id') or 0) == int(product_id):
                final_price = it.get('final_price') if it.get('final_price') is not None else it.get('unit_price')
                break
    result['final_price'] = float(final_price) if final_price is not None else None

    expected = None
    if verify_price and catalog_id is not None:
        det = get_product_details_for_client(catalog_id=catalog_id, product_id=product_id, client_token=client_token)
        if det and isinstance(det, dict):
            expected = det.get('price_for_client')
    result['expected_price'] = float(expected) if expected is not None else None

    if result['expected_price'] is not None and result['final_price'] is not None:
        mismatch = round(float(result['expected_price']) - float(result['final_price']), 2) != 0.0
        result['mismatch'] = mismatch
        if mismatch:
            result['error'] = f"price_mismatch expected={result['expected_price']} got={result['final_price']}"

    result['ok'] = True
    return result

@tool
def add_multiple_products_to_cart(client_token: str, items: List[Tuple[int, int]], stop_on_error: bool = True,
                                  verify_price: bool = False, catalog_id: Optional[int] = None) -> Dict[str, Any]:
    """Agrega múltiples (product_id, quantity). Sin impresiones."""
    results: List[Dict[str, Any]] = []
    failed: List[Tuple[int, str]] = []
    for pid, qty in items:
        try:
            res = add_to_cart(client_token, pid, qty, catalog_id=catalog_id, verify_price=verify_price)
        except Exception as exc:
            res = {'ok': False, 'error': f'exception during add: {exc!r}'}

        results.append({'product_id': pid, 'quantity': qty, 'result': res})
        if not res.get('ok'):
            failed.append((pid, res.get('error') or 'failed'))
            if stop_on_error:
                break

    return {'results': results, 'failed': failed}

@tool
def get_cart(client_token: str) -> Optional[Dict[str, Any]]:
    """Obtiene el carrito actual del cliente. Sin impresiones."""
    if not client_token:
        return None
    r = client.get('/api/clients/cart', headers=_auth_headers(client_token))
    if r.status_code >= 400:
        return None
    return _json(r) or {'status_code': r.status_code, 'text': r.text}

@tool
def update_cart_item(client_token: str, product_id: int, quantity: int) -> Optional[Dict[str, Any]]:
    """Actualiza cantidad de un producto en el carrito. Sin impresiones."""
    if not client_token:
        return None
    r = client.put(f'/api/clients/cart/items/{int(product_id)}', json={'quantity': int(quantity)}, headers=_auth_headers(client_token))
    if r.status_code >= 400:
        return None
    return _json(r) or {'status_code': r.status_code, 'text': r.text}

@tool
def remove_cart_item(client_token: str, product_id: int) -> bool:
    """Elimina un ítem del carrito. Sin impresiones."""
    if not client_token:
        return False
    r = client.delete(f'/api/clients/cart/items/{int(product_id)}', headers=_auth_headers(client_token))
    if r.status_code >= 400:
        return False
    return True

@tool
def clear_cart(client_token: str) -> bool:
    """Vacía el carrito del cliente. Sin impresiones."""
    if not client_token:
        return False
    r = client.post('/api/clients/cart/clear', headers=_auth_headers(client_token))
    if r.status_code >= 400:
        return False
    return True

@tool
def checkout_cart(client_token: str) -> Optional[Dict[str, Any]]:
    """Realiza checkout y regresa el pedido creado. Sin impresiones."""
    if not client_token:
        return None
    r = client.post('/api/clients/cart/checkout', headers=_auth_headers(client_token))
    if r.status_code >= 400:
        return None
    return _json(r) or {'status_code': r.status_code, 'text': r.text}

@tool
def create_order_from_cart(client_token: str, fail_if_empty: bool = True) -> Optional[Dict[str, Any]]:
    """Asegura carrito con items y hace checkout; retorna el pedido. Sin impresiones."""
    cart = get_cart(client_token)
    if cart is None:
        return None

    items = None
    if isinstance(cart, dict):
        items = cart.get('items') or cart.get('cart_items') or (cart.get('cart') or {}).get('items')
    if not items and fail_if_empty:
        return None

    return checkout_cart(client_token)

@tool
def purchase_items_for_client(
    client_token: str,
    items: List[Dict[str, Any]],
    clear_first: bool = False,
    verify_price: bool = True,
    stop_on_error: bool = True,
) -> Dict[str, Any]:
    """Flujo alto nivel: agrega ítems al carrito y hace checkout. Sin impresiones internas."""
    report: Dict[str, Any] = {'ok': False, 'cart': None, 'order': None, 'added': [], 'mismatches': [], 'errors': []}

    if not client_token:
        report['errors'].append('client_token required')
        return report

    if clear_first:
        try:
            clear_ok = clear_cart(client_token)
            if not clear_ok:
                report['errors'].append('failed to clear cart')
                if stop_on_error:
                    return report
        except Exception as exc:
            report['errors'].append(f'clear_cart exception: {exc!r}')
            if stop_on_error:
                return report

    normalized: List[Tuple[int, int, Optional[int]]] = []
    for it in items:
        if isinstance(it, dict):
            pid = int(it.get('product_id'))
            qty = int(it.get('quantity', 1))
            cid = it.get('catalog_id') if it.get('catalog_id') is not None else None
            normalized.append((pid, qty, cid))
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            pid = int(it[0]); qty = int(it[1]); cid = it[2] if len(it) > 2 else None
            normalized.append((pid, qty, cid))
        else:
            report['errors'].append(f'invalid item spec: {it!r}')
            if stop_on_error:
                return report

    for pid, qty, cid in normalized:
        try:
            res = add_to_cart(client_token, pid, qty, catalog_id=cid, verify_price=verify_price)
        except Exception as exc:
            res = {'ok': False, 'error': f'exception: {exc!r}'}
        report['added'].append({'product_id': pid, 'quantity': qty, 'catalog_id': cid, 'result': res})
        if not res.get('ok'):
            report['errors'].append(f'add failed for {pid}: {res.get("error")}')
            if stop_on_error:
                return report
        if res.get('mismatch'):
            report['mismatches'].append({'product_id': pid, 'expected': res.get('expected_price'), 'got': res.get('final_price')})
            if stop_on_error:
                return report

    cart = get_cart(client_token)
    report['cart'] = cart

    order = checkout_cart(client_token)
    if order is None:
        report['errors'].append('checkout failed')
        return report
    report['order'] = order

    try:
        items_detail = order.get('items_detail') if isinstance(order, dict) else None
        if items_detail and verify_price:
            for it in items_detail:
                pid = int(it.get('product_id') or 0)
                final_unit = it.get('final_unit') if it.get('final_unit') is not None else it.get('final_price')
                expected = None
                for a in report['added']:
                    if int(a['product_id']) == pid:
                        expected = a['result'].get('expected_price')
                        break
                if expected is not None and final_unit is not None and round(float(expected) - float(final_unit), 2) != 0.0:
                    report['mismatches'].append({'product_id': pid, 'expected': expected, 'got': final_unit})
    except Exception:
        pass

    report['ok'] = True
    return report

# ==============================================================================================
# Order helpers (client-facing order operations)
# ==============================================================================================

@tool
def list_orders_for_client(client_token: str) -> Optional[List[Dict[str, Any]]]:
    """Lista los pedidos del cliente autenticado.

    Retorna la lista JSON de pedidos o None en caso de error / no token.
    """
    if not client_token:
        return None
    # The server exposes GET /api/orders which inspects the token to return client orders when
    # the token contains a client_id claim. Use that endpoint rather than a non-existent
    # /api/clients/orders route.
    r = client.get('/api/orders', headers=_auth_headers(client_token))
    if r.status_code != 200:
        return None
    return _json(r)


@tool
def get_order_details(client_token: str, order_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene detalles de un pedido. Intenta endpoints públicos y scoped al cliente.

    Retorna el JSON del pedido o None si no se encuentra / error.
    """
    if not client_token or not order_id:
        return None

    r = client.get(f'/api/orders/{int(order_id)}', headers=_auth_headers(client_token))
    if r.status_code == 200:
        return _json(r)

    # Fallback a endpoint scoped al cliente
    r2 = client.get(f'/api/clients/orders/{int(order_id)}', headers=_auth_headers(client_token))
    if r2.status_code == 200:
        return _json(r2)
    return None


@tool
def update_order(client_token: str, order_id: int, data: dict) -> Optional[Dict[str, Any]]:
    """Actualiza un pedido (PATCH). Devuelve JSON actualizado o None en falla."""
    if not client_token or not order_id or not data:
        return None

    r = client.patch(f'/api/orders/{int(order_id)}', json=data, headers=_auth_headers(client_token))
    if r.status_code < 400:
        return _json(r)

    # Intento fallback scoped
    r2 = client.patch(f'/api/clients/orders/{int(order_id)}', json=data, headers=_auth_headers(client_token))
    if r2.status_code < 400:
        return _json(r2)
    return None


def cancel_order(client_token: str, order_id: int) -> bool:
    """Cancela o elimina un pedido. Devuelve True si la operación tuvo éxito."""
    if not client_token or not order_id:
        return False

    # Preferir endpoint de cancelación si existe
    try:
        r = client.post(f'/api/orders/{int(order_id)}/cancel', headers=_auth_headers(client_token))
        if r.status_code == 200:
            return True
    except Exception:
        pass

    try:
        r2 = client.post(f'/api/clients/orders/{int(order_id)}/cancel', headers=_auth_headers(client_token))
        if r2.status_code == 200:
            return True
    except Exception:
        pass

    # Como último recurso intentar DELETE en el recurso
    try:
        r3 = client.delete(f'/api/orders/{int(order_id)}', headers=_auth_headers(client_token))
        if r3.status_code < 400:
            return True
    except Exception:
        pass

    return False


@tool
def request_invoice_for_order(client_token: str, order_id: int, payload_or_email: Optional[Union[Dict[str, Any], str]] = None) -> Optional[Dict[str, Any]]:
    """Solicita la generación / envío de factura para un pedido.

    `payload_or_email` puede ser un dict con campos fiscales o un email (str).
    Devuelve el JSON de respuesta del endpoint o None en falla.
    """
    if not client_token or not order_id:
        return None

    if isinstance(payload_or_email, dict):
        payload = payload_or_email
    elif isinstance(payload_or_email, str):
        payload = {'email': payload_or_email}
    else:
        payload = {}

    diagnostic: Dict[str, Any] = {'attempts': []}

    # Try primary endpoint
    try:
        url1 = f'/api/orders/{int(order_id)}/invoice'
        r = client.post(url1, json=payload, headers=_auth_headers(client_token))
        diagnostic['attempts'].append({'url': url1, 'status_code': r.status_code, 'text': r.text})
        if r.status_code == 200:
            return {'ok': True, 'source': 'api', 'url': url1, 'body': _json(r)}
    except Exception as exc:
        diagnostic['attempts'].append({'url': url1, 'error': repr(exc)})

    # Try client-scoped endpoint
    try:
        url2 = f'/api/clients/orders/{int(order_id)}/invoice'
        r2 = client.post(url2, json=payload, headers=_auth_headers(client_token))
        diagnostic['attempts'].append({'url': url2, 'status_code': r2.status_code, 'text': r2.text})
        if r2.status_code == 200:
            return {'ok': True, 'source': 'api', 'url': url2, 'body': _json(r2)}
    except Exception as exc:
        diagnostic['attempts'].append({'url': url2, 'error': repr(exc)})

    # If API endpoints are not available, try local DB insertion as a fallback
    try:
        from python.Classes.repos.order_repo import CustomerOrderRepo as LegacyCustomerOrderRepo
        legacy_order = LegacyCustomerOrderRepo()
        cur = legacy_order.db.cursor()
        inv_number = payload.get('invoice_number') or f'INV-{int(order_id):04d}-1'
        notes = payload.get('notes') or f'Factura por total {order_id}'
        currency_code = payload.get('currency_code') or 'MXN'
        exchange_rate = payload.get('exchange_rate')
        sql = (
            "INSERT INTO invoice (order_id, invoice_number, billing_name, rfc, regimen_fiscal, fiscal_postal_code, billing_address, uso_cfdi, forma_pago, metodo_pago, series, issued_at, due_at, currency_code, exchange_rate, status, notes) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NULL,%s,%s,%s,%s)"
        )
        params = (
            int(order_id), inv_number, payload.get('billing_name'), payload.get('rfc'), payload.get('regimen_fiscal'), payload.get('fiscal_postal_code'),
            payload.get('billing_address'), payload.get('uso_cfdi'), payload.get('forma_pago'), payload.get('metodo_pago'), 'A', currency_code, exchange_rate,
            'emitida', notes
        )
        cur.execute(sql, params)
        if not legacy_order.db.autocommit:
            legacy_order.db.commit()
        try:
            lastid = cur.lastrowid
        except Exception:
            lastid = None
        return {'ok': True, 'source': 'local_db', 'lastrowid': lastid, 'invoice_number': inv_number, 'diagnostic': diagnostic}
    except Exception as exc:
        diagnostic['fallback_error'] = repr(exc)
        return {'ok': False, 'source': 'none', 'diagnostic': diagnostic}


@tool
def create_invoice_for_order(client_token: str, order_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Wrapper explícito para enviar una solicitud de factura para un pedido.
    Devuelve la respuesta JSON o un dict diagnóstico en fallo.
    """
    return request_invoice_for_order(client_token, order_id, payload)


def _suggest_invoice_numbers(order_id: int) -> tuple[str, str]:
    """Sugerir dos folios simples basados en order_id (INV-0003-1, INV-0003-2)."""
    base = f"INV-{int(order_id):04d}"
    return f"{base}-1", f"{base}-2"


@tool
def build_invoice_payload(client_token: str, order_id: int, email: Optional[str] = None, interactive: bool = False) -> Optional[Dict[str, Any]]:
    """Construye un payload razonable para solicitar factura usando datos del pedido y cliente.

    Si `interactive` es True y la entrada es tty, permite al usuario modificar valores.
    """
    if not client_token or not order_id:
        return None

    payload: Dict[str, Any] = {}
    if email:
        payload['email'] = email

    # Intentar obtener información del pedido y cliente para rellenar campos
    header = get_order_details(client_token, order_id) or {}
    client_id = header.get('client_id') if isinstance(header, dict) else None

    client_obj = None
    if client_id:
        try:
            client_obj = client_repo.get(client_id)
        except Exception:
            client_obj = None

    # Valores por defecto razonables
    default_name = None
    if client_obj:
        default_name = getattr(client_obj, 'full_name', None) or (client_obj.get('full_name') if isinstance(client_obj, dict) else None)
    default_name = default_name or f'Cliente {client_id or "?"}'

    payload.setdefault('billing_name', default_name)
    payload.setdefault('rfc', None)
    payload.setdefault('regimen_fiscal', None)
    payload.setdefault('fiscal_postal_code', None)
    payload.setdefault('billing_address', None)
    payload.setdefault('uso_cfdi', None)
    payload.setdefault('forma_pago', None)
    payload.setdefault('metodo_pago', None)
    payload.setdefault('currency_code', 'MXN')
    payload.setdefault('exchange_rate', None)

    # Interactive override
    if interactive:
        try:
            if sys.stdin and sys.stdin.isatty():
                print('\nValores por defecto para la factura (deja vacío para mantener):')
                for k in list(payload.keys()):
                    cur = payload.get(k)
                    val = input(f"{k} [{cur}]: ").strip()
                    if val != '':
                        # normalize some types
                        if k == 'exchange_rate':
                            try:
                                payload[k] = float(val)
                            except Exception:
                                payload[k] = val
                        else:
                            payload[k] = val
        except Exception:
            pass

    return payload

# ==============================================================================================
# Interactive cyclic menu for manual testing and realistic usage
# ==============================================================================================

def _choose_or_create_user() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Interactively choose an existing user or create a new one.

    Returns (client_obj, client_token) where client_obj may be None on failure.
    """
    print('\nUsuario: elegir o crear')
    print('  1) Elegir usuario existente (por telegram_username / phone / telegram_user_id)')
    print('  2) Crear nuevo usuario')
    choice = input('Elige 1 o 2 [1]: ').strip() or '1'

    if choice == '2':
        full_name = input('Nombre completo (requerido para crear): ').strip()
        phone = input('Teléfono (opcional): ').strip() or None
        telegram_username = input('Telegram username (opcional): ').strip() or None
        tok = _get_client_token_plain(telegram_user_id=None, telegram_username=telegram_username, create_if_missing=True, full_name=full_name, phone=phone)
        if not tok:
            print('No se pudo crear/obtener token para el usuario.')
            return None, None
        # try to fetch client object via token
        cid = _client_id_from_token(tok)
        client_obj = None
        try:
            if cid:
                client_obj = client_repo.get(cid)
        except Exception:
            client_obj = None
        return client_obj, tok

    # choose existing
    telegram_username = input('Telegram username (ENTER para omitir): ').strip() or None
    phone = input('Teléfono (ENTER para omitir): ').strip() or None
    tid = input('Telegram user id (ENTER para omitir): ').strip() or None
    try:
        tid_val = int(tid) if tid else None
    except Exception:
        tid_val = None

    tok = _get_client_token_plain(telegram_user_id=tid_val, telegram_username=telegram_username, create_if_missing=False, full_name=None, phone=phone)
    if not tok:
        print('Usuario no encontrado con esos datos. Puedes crear uno nuevo desde el menú.')
        return None, None

    cid = _client_id_from_token(tok)
    client_obj = None
    try:
        if cid:
            client_obj = client_repo.get(cid)
    except Exception:
        client_obj = None

    return client_obj, tok


def _print_help():
    print('\nComandos disponibles:')
    print('  u - cambiar usuario (elegir/crear)')
    print('  info - mostrar info del usuario actual')
    print('  catalogs - listar catálogos visibles')
    print('  categories - listar categorías de un catálogo')
    print('  products - listar productos de un catálogo/categoría')
    print('  product - ver detalles de un producto')
    print('  cart - ver carrito actual')
    print('  add - agregar producto al carrito')
    print('  update - actualizar cantidad en carrito')
    print('  remove - eliminar item del carrito')
    print('  clear - vaciar carrito')
    print('  checkout - realizar checkout y crear pedido')
    print('  orders - listar pedidos del cliente')
    print('  order - ver detalles de un pedido')
    print('  invoice - crear / solicitar factura para un pedido')
    print('  purchase - flujo rápido: agregar lista y checkout')
    print('  help - mostrar este mensaje')
    print('  q - salir')


if __name__ == '__main__':
    print('\n=== OmniDesk - Interactive tools menu ===')
    current_token: Optional[str] = None
    current_client: Optional[Dict[str, Any]] = None

    # initial choose/create
    cli_obj, tok = _choose_or_create_user()
    current_client = cli_obj
    current_token = tok

    while True:
        if current_client:
            cid = getattr(current_client, 'client_id', None) or (current_client.get('client_id') if isinstance(current_client, dict) else None)
            name = getattr(current_client, 'full_name', None) or (current_client.get('full_name') if isinstance(current_client, dict) else str(cid))
            prompt = f"[{name} (id={cid})] > "
        else:
            prompt = '[sin usuario] > '

        try:
            cmd = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print('\nSaliendo...')
            break

        if not cmd:
            continue
        cmd = cmd.lower()

        if cmd in ('q', 'quit', 'exit'):
            print('Saliendo...')
            break
        if cmd in ('h', 'help'):
            _print_help()
            continue
        if cmd in ('u', 'user'):
            cli_obj, tok = _choose_or_create_user()
            current_client = cli_obj
            current_token = tok
            continue

        if cmd == 'info':
            if not current_token:
                print('No hay usuario seleccionado.')
                continue
            print('\nToken:', current_token)
            print('Client object:')
            pprint(current_client)
            continue

        if cmd == 'catalogs':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            cats = list_catalogs_for_client(current_token) or []
            pprint(cats)
            continue

        if cmd == 'categories':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            cid_in = input('Catalog id: ').strip()
            try:
                catid = int(cid_in)
            except Exception:
                print('catalog id inválido')
                continue
            cats = list_categories_by_catalog_id(catalog_id=catid, client_token=current_token) or []
            pprint(cats)
            continue

        if cmd == 'products':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            catalog_in = input('Catalog id: ').strip()
            catfilter = input("Categoria id or 'A' para todas [A]: ").strip() or 'A'
            try:
                catalog_id = int(catalog_in)
            except Exception:
                print('catalog id inválido')
                continue
            prods = list_products_by_catalog_and_category(catalog_id=catalog_id, category_filter=catfilter, client_token=current_token) or []
            for p in prods:
                print(f"- (ID: {p.get('product_id')}) {p.get('name')} | $ {p.get('price_for_client') or p.get('price')}")
            continue

        if cmd == 'product':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            catalog_in = input('Catalog id: ').strip()
            pid_in = input('Product id: ').strip()
            try:
                catalog_id = int(catalog_in); pid = int(pid_in)
            except Exception:
                print('IDs inválidos')
                continue
            det = get_product_details_for_client(catalog_id=catalog_id, product_id=pid, client_token=current_token)
            pprint(det)
            continue

        if cmd == 'cart':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            c = get_cart(current_token)
            pprint(c)
            continue

        if cmd == 'add':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            pid = input('product_id: ').strip()
            qty = input('quantity [1]: ').strip() or '1'
            cid = input('catalog_id (opcional): ').strip() or None
            try:
                pidv = int(pid); qtyv = int(qty)
                cidv = int(cid) if cid else None
            except Exception:
                print('Valores inválidos')
                continue
            res = add_to_cart(current_token, pidv, qtyv, catalog_id=cidv, verify_price=True)
            pprint(res)
            continue

        if cmd == 'update':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            pid = input('product_id to update: ').strip()
            qty = input('new quantity: ').strip()
            try:
                pidv = int(pid); qtyv = int(qty)
            except Exception:
                print('Valores inválidos')
                continue
            res = update_cart_item(current_token, pidv, qtyv)
            pprint(res)
            continue

        if cmd == 'remove':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            pid = input('product_id to remove: ').strip()
            try:
                pidv = int(pid)
            except Exception:
                print('product_id inválido')
                continue
            ok = remove_cart_item(current_token, pidv)
            print('removed ->', ok)
            continue

        if cmd == 'clear':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            ok = clear_cart(current_token)
            print('clear ->', ok)
            continue

        if cmd == 'checkout':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            order = checkout_cart(current_token)
            print('Order result:')
            pprint(order)
            if order:
                print('\nTicket:')
                print(format_order_ticket(order))
            continue

        if cmd == 'orders':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            ords = list_orders_for_client(current_token) or []
            pprint(ords)
            continue

        if cmd == 'order':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            oid = input('order_id: ').strip()
            try:
                oidv = int(oid)
            except Exception:
                print('order id inválido')
                continue
            od = get_order_details(current_token, oidv)
            pprint(od)
            continue

        if cmd == 'invoice':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            oid = input('order_id to invoice (ENTER = latest): ').strip() or None
            if not oid:
                ords = list_orders_for_client(current_token) or []
                if not ords:
                    print('No hay pedidos para facturar')
                    continue
                first = ords[0]
                oidv = first.get('order_id') or first.get('id')
            else:
                try:
                    oidv = int(oid)
                except Exception:
                    print('order id inválido')
                    continue

            p = build_invoice_payload(current_token, oidv, interactive=True) or {}
            p.setdefault('invoice_number', _suggest_invoice_numbers(oidv)[0])
            print('Payload para factura:')
            pprint(p)
            send = input('Enviar ahora? (s/n) [n]: ').strip().lower() or 'n'
            if send == 's':
                resp = create_invoice_for_order(current_token, oidv, p)
                pprint(resp)
            continue

        if cmd == 'purchase':
            if not current_token:
                print('Elige primero un usuario.')
                continue
            print('Introduce items como product_id:quantity separados por comas, e.g. 1:2,3:1')
            s = input('items: ').strip()
            if not s:
                print('Nada ingresado')
                continue
            items = []
            for part in s.split(','):
                try:
                    pid_s, qty_s = part.split(':')
                    items.append({'product_id': int(pid_s.strip()), 'quantity': int(qty_s.strip())})
                except Exception:
                    print('Formato inválido para', part)
            report = purchase_items_for_client(current_token, items, clear_first=False, verify_price=True, stop_on_error=False)
            pprint(report)
            continue

        print('Comando no reconocido. Escribe "help" para ver las opciones.')

    
