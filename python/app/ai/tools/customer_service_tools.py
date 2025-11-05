import os
import sys
from pprint import pprint
from typing import Any, Dict, Optional
from fastapi import requests
from fastapi.testclient import TestClient

# Make repo importable when running this file directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.Classes.models import category
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
    -hacer pedidos
    -ver el estado de sus pedidos
    -editar pedidos existentes
    - eliminar pedidos (con ciertas restricciones)
    -modificar su informacion de contacto
    -solicitar facturas de pedidos
    -hacer un carrito con los productos que quiere comprar (esto no esta en bd, simplemente crearemos una lista en memoria que podemos usar para crar el pedido)

"""
################################################################################################################################################
################################################################################################################################################
# Identify client via API endpoint POST /api/clients/identify.
################################################################################################################################################
################################################################################################################################################

def identify_client(telegram_username: Optional[str] = None, telegram_user_id: Optional[int] = None,
                    phone: Optional[str] = None, create_if_missing: bool = False, full_name: Optional[str] = None):
    """Identify a client by telegram username or id via POST /api/clients/identify.

    If create_if_missing is True and the client is not found, full_name must be
    provided to create the client.
    Returns a dict {'client': client_obj, 'token': client_token} on success or None on failure.
    """
    payload = {
        'telegram_username': telegram_username,
        'telegram_user_id': telegram_user_id,
        'phone': phone,
        'create_if_missing': create_if_missing,
        'full_name': full_name
    }
    # remove None values to keep payload small
    payload = {k: v for k, v in payload.items() if v is not None}

    r = client.post('/api/clients/identify', json=payload)
    if r.status_code != 200:
        print('Identify fallido:', r.status_code, r.text)
        return None
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

#Client auth and identification return the token.
def client_auth(
    telegram_user_id: int | str | None = None,
    telegram_username: str | None = None,
        create_if_missing: bool = False, 
        full_name: Optional[str] = None, 
        phone: Optional[str] = None,
) -> dict:
    """Authenticate a client by telegram_user_id or telegram_username.

    If `create_if_missing` is True and the client is not found, `full_name` must be
    provided to create the client (this is forwarded to the `/clients/identify` endpoint).

    Returns a standardized dict:
      { "ok": True, "data": { "client_token": str, "client": {...} }, "error": None }
      or
      { "ok": False, "data": None, "error": "not_found"|"missing_credentials"|"exception" }
    """
    # need at least one identifier (telegram id, username or phone)
    if telegram_user_id is None and not telegram_username and not phone:
        print('client_auth: telegram_user_id or telegram_username or phone required')
        return {"ok": False, "data": None, "error": "missing_credentials"}

    try:
        # forward create_if_missing and full_name to the identify endpoint
        kwargs = {
            'telegram_user_id': telegram_user_id,
            'telegram_username': telegram_username,
            'create_if_missing': create_if_missing,
            'full_name': full_name,
                'phone': phone,
        }
        # remove None values so payload is minimal
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        res = identify_client(**kwargs)

        if not res:
            return {"ok": False, "data": None, "error": "not_found"}

        # normalize possible shapes
        token = None
        client_obj = None
        if isinstance(res, dict):
            token = res.get('token') or res.get('client_token') or res.get('access_token')
            client_obj = res.get('client') or res.get('client_obj') or res.get('client_data')
            if not token and isinstance(res.get('data'), dict):
                token = res['data'].get('client_token') or res['data'].get('token')
                client_obj = client_obj or res['data'].get('client')

        if not token:
            # still return client info if present but no token (unexpected)
            return {"ok": False, "data": None, "error": "no_token"}

        return {"ok": True, "data": {"client_token": token, "client": client_obj}, "error": None}
    except Exception as e:
        print('Error en client_auth:', repr(e))
        return {"ok": False, "data": None, "error": "exception"}

def get_client_token(
    telegram_user_id: int | str | None = None,
    telegram_username: str | None = None,
    create_if_missing: bool = True,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
) -> Optional[str]:
    """Convenience helper that returns the JWT token string or None on failure.

    Example:
      token = get_client_token(telegram_user_id=952408)
    """
    # Normalize phone for lookup and optional creation
    norm_phone = _normalize_phone(phone) if phone else None

    # First attempt: try to identify without forcing creation unless create_if_missing True
    r = client_auth(
        telegram_user_id=telegram_user_id,
        telegram_username=telegram_username,
        create_if_missing=False,
        full_name=None,
        phone=norm_phone,
    )
    if r.get('ok') and r.get('data'):
        return r['data'].get('client_token')

    # Not found. If allowed, create a client. Use provided full_name or derive a fallback.
    if create_if_missing:
        fallback_name = full_name
        if not fallback_name:
            # derive a sensible default name from available identifiers
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
            create_if_missing=False,
            full_name=fallback_name,
            phone=norm_phone,
        )
        if r2.get('ok') and r2.get('data'):
            return r2['data'].get('client_token')

    return None

def _normalize_phone(phone: str) -> str:
    """Basic phone normalization: keep leading + if present, remove spaces and common separators.

    Note: this does not add country codes. It only strips formatting characters so lookups
    against DB are more consistent.
    """
    if not phone:
        return phone
    phone = phone.strip()
    # keep leading + if present
    keep_plus = phone.startswith('+')
    # remove non-digit characters
    digits = ''.join(ch for ch in phone if ch.isdigit())
    return ('+' + digits) if keep_plus else digits

def ensure_client_and_get_token(phone: Optional[str] = None, full_name: Optional[str] = None,
                                telegram_user_id: Optional[int] = None, telegram_username: Optional[str] = None) -> Optional[str]:
    """Try to get a client token; if the client doesn't exist and `full_name` is provided,
    create the client and return the new token.

    Returns the token string or None on failure.
    """
    # normalize phone for DB lookups
    norm_phone = _normalize_phone(phone) if phone else None

    # first try without creating
    token = get_client_token(telegram_user_id=telegram_user_id, telegram_username=telegram_username,
                             create_if_missing=False, full_name=None, phone=norm_phone)
    if token:
        return token

    # if not found, try to create when we have a full_name
    if full_name:
        token = get_client_token(telegram_user_id=telegram_user_id, telegram_username=telegram_username,
                                 create_if_missing=True, full_name=full_name, phone=norm_phone)
        return token

    return None

################################################################################################################################################
################################################################################################################################################
# funciones para que el cliente pueda explorar todo el inventario del negocio (solo vista)
################################################################################################################################################
################################################################################################################################################

def list_catalogs_for_client(client_token: str) -> Optional[Dict[str, Any]]:
    """List catalogs for a client based on their subscription level.
     premium o normal. si es normal puede ver solo los catalogos visibles para todos. si es premium puede ver todos los catalogos
    """
    if not client_token:
        print('list_catalogs_for_client: client_token is required')
        return None

    # Try to decode token to extract client_id -> subject.sub.client_id
    client_id = None
    try:
        from python.app.core.security import decode_token
        payload = decode_token(client_token)
        sub = payload.get('sub') or {}
        # subject may be a dict with client_id
        client_id = sub.get('client_id') if isinstance(sub, dict) else None
    except Exception:
        # fallback: try unsafe decode without verifying signature
        try:
            import jwt
            payload = jwt.decode(client_token, options={"verify_signature": False})
            sub = payload.get('sub') or {}
            client_id = sub.get('client_id') if isinstance(sub, dict) else None
        except Exception:
            client_id = None

    if not client_id:
        print('list_catalogs_for_client: could not determine client_id from token')
        return None

    # load client from repo and check status/type
    try:
        client_obj = client_repo.get(client_id)
    except Exception as exc:
        print('list_catalogs_for_client: error loading client:', repr(exc))
        return None

    if not client_obj:
        print('list_catalogs_for_client: client not found')
        return None

    if getattr(client_obj, 'status', None) != 'active':
        print('list_catalogs_for_client: client not active')
        return None

    client_type = getattr(client_obj, 'client_type', 'normal')

    # choose endpoint based on client type
    if client_type == 'premium':
        endpoint = '/api/catalogs'
    else:
        endpoint = '/api/catalogs/actives'

    headers = {'Authorization': f'Bearer {client_token}'}
    r = client.get(endpoint, headers=headers)
    if r.status_code != 200:
        print('list_catalogs_for_client: API error', r.status_code, r.text)
        return None
    try:
        catalogs = r.json()
    except Exception:
        return None

    # Enforce visibility rules locally because `/catalogs/actives` returns all active
    # catalogs (including those visible only to 'premium'). For non-premium clients
    # filter out catalogs whose `visible_to` is not 'todos' (or None).
    if client_type != 'premium' and isinstance(catalogs, list):
        filtered = []
        for c in catalogs:
            vis = c.get('visible_to') if isinstance(c, dict) else None
            if vis in (None, 'todos'):
                filtered.append(c)
        return filtered

    return catalogs


def list_categories_by_catalog_id(catalog_id: int, client_token: str) -> Optional[Dict[str, Any]]:
    """List categories for a given catalog based on client token."""
    if not client_token:
        print('list_categories_by_catalog_id: client_token is required')
        return None

    if not catalog_id:
        print('list_categories_by_catalog_id: catalog_id is required')
        return None

    headers = {'Authorization': f'Bearer {client_token}'}

    # 1) Get catalog products
    r = client.get(f'/api/catalogs/{catalog_id}/products', headers=headers)
    if r.status_code != 200:
        print('list_categories_by_catalog_id: API error fetching catalog products', r.status_code, r.text)
        return None
    try:
        catalog_products = r.json()
    except Exception:
        print('list_categories_by_catalog_id: invalid JSON for catalog products')
        return None

    # 2) For each product_id, fetch product and collect category_ids
    product_ids = [cp.get('product_id') for cp in catalog_products if isinstance(cp, dict) and cp.get('product_id')]
    category_ids = []
    for pid in product_ids:
        pr = client.get(f'/api/products/{pid}', headers=headers)
        if pr.status_code != 200:
            # skip missing products
            continue
        try:
            pdata = pr.json()
        except Exception:
            continue
        # pdata expected to contain 'category_id'
        cid = pdata.get('category_id') if isinstance(pdata, dict) else None
        if cid:
            category_ids.append(cid)

    # unique and preserve order
    seen = set()
    uniq_cids = []
    for cid in category_ids:
        if cid not in seen:
            seen.add(cid)
            uniq_cids.append(cid)

    # 3) Fetch category details for each unique id
    categories = []
    for cid in uniq_cids:
        cr = client.get(f'/api/categories/{cid}', headers=headers)
        if cr.status_code != 200:
            continue
        try:
            cdata = cr.json()
        except Exception:
            continue
        categories.append(cdata)

    return categories


def list_products_by_catalog_and_category(catalog_id: int, category_filter: Optional[str | int], client_token: str,
                                          q: Optional[str] = None) -> Optional[list]:
    """List products for a catalog, filtered by a category id or 'A' for all.

    Parameters:
      - catalog_id: catalog to inspect
      - category_filter: int category_id or 'A' (or 'a') to include all categories
      - client_token: JWT token string for auth (used to compute price_for_client)
      - q: optional search string to filter product title/description (applied after fetching)

    Returns list of product dicts or None on error.
    """
    if not client_token:
        print('list_products_by_catalog_and_category: client_token is required')
        return None

    if not catalog_id:
        print('list_products_by_catalog_and_category: catalog_id is required')
        return None

    headers = {'Authorization': f'Bearer {client_token}'}

    # 1) get catalog products
    r = client.get(f'/api/catalogs/{catalog_id}/products', headers=headers)
    if r.status_code != 200:
        print('list_products_by_catalog_and_category: API error fetching catalog products', r.status_code, r.text)
        return None
    try:
        catalog_products = r.json()
    except Exception:
        print('list_products_by_catalog_and_category: invalid JSON for catalog products')
        return None

    # build list of product ids
    product_ids = [cp.get('product_id') for cp in catalog_products if isinstance(cp, dict) and cp.get('product_id')]

    # normalize filter
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
            # skip missing products
            continue
        try:
            pdata = pr.json()
        except Exception:
            continue

        # pdata expected to contain 'category_id'
        cid = pdata.get('category_id') if isinstance(pdata, dict) else None
        if not all_flag:
            if cid != target_cid:
                continue

        # optional text filter
        if q and isinstance(pdata, dict):
            text = ' '.join([str(pdata.get('name','')), str(pdata.get('description',''))]).lower()
            if q.lower() not in text:
                continue

        out.append(pdata)

    return out


def get_product_details_for_client(catalog_id: int, product_id: int, client_token: str) -> Optional[Dict[str, Any]]:
    # Toma en cuenta que el catalogo ofrece descuentos, asi que tambien debes
    # mostrar eso al cliente: el precio normal, el precio especial del catalogo
    # (si existe) y el precio final para el cliente teniendo en cuenta su tipo
    # (premium/normal) y la configuración PREMIUM_DISCOUNT_PCT.
    if not client_token:
        print('get_product_details_for_client: client_token is required')
        return None

    if not catalog_id or not product_id:
        print('get_product_details_for_client: catalog_id and product_id are required')
        return None

    headers = {'Authorization': f'Bearer {client_token}'}

    # fetch product
    pr = client.get(f'/api/products/{product_id}', headers=headers)
    if pr.status_code != 200:
        print('get_product_details_for_client: product not found or API error', pr.status_code, pr.text)
        return None
    try:
        product = pr.json()
    except Exception:
        print('get_product_details_for_client: invalid product JSON')
        return None

    # fetch catalog-product association to get special_price
    cpr = client.get(f'/api/catalogs/{catalog_id}/products/{product_id}', headers=headers)
    catalog_product = None
    if cpr.status_code == 200:
        try:
            catalog_product = cpr.json()
        except Exception:
            catalog_product = None

    # determine client type from token to apply premium discount if any
    client_type = None
    try:
        from python.app.core.security import decode_token
        payload = decode_token(client_token)
        sub = payload.get('sub', {})
        cid = sub.get('client_id') if isinstance(sub, dict) else None
        if cid:
            cobj = client_repo.get(cid)
            client_type = getattr(cobj, 'client_type', None)
    except Exception:
        # best-effort: try unsafe decode
        try:
            import jwt
            payload = jwt.decode(client_token, options={"verify_signature": False})
            sub = payload.get('sub', {})
            cid = sub.get('client_id') if isinstance(sub, dict) else None
            if cid:
                cobj = client_repo.get(cid)
                client_type = getattr(cobj, 'client_type', None)
        except Exception:
            client_type = None

    # compute prices and breakdowns
    def _to_float(v):
        try:
            return float(v)
        except Exception:
            return None

    price_normal = _to_float(product.get('price'))

    # catalog special price (absolute) if assigned
    catalog_special_price = None
    if catalog_product and isinstance(catalog_product, dict):
        catalog_special_price = _to_float(catalog_product.get('special_price'))

    # fetch catalog to read its discount_percentage (stored as percent, e.g. 10.0 == 10%)
    catalog = None
    cr = client.get(f'/api/catalogs/{catalog_id}', headers=headers)
    if cr.status_code == 200:
        try:
            catalog = cr.json()
        except Exception:
            catalog = None

    catalog_discount_pct = 0.0
    if catalog and isinstance(catalog, dict):
        try:
            # DB stores discount_percentage as percentage (10.0 == 10%)
            catalog_discount_pct = float(catalog.get('discount_percentage') or 0.0) / 100.0
        except Exception:
            catalog_discount_pct = 0.0

    # compute effective price due to catalog (special_price wins, otherwise catalog percentage)
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

    # premium discount (global config, fractional e.g. 0.10)
    premium_pct = 0.0
    try:
        from python.app.core.config import settings
        if client_type == 'premium':
            premium_pct = float(getattr(settings, 'PREMIUM_DISCOUNT_PCT', 0.0))
    except Exception:
        premium_pct = 0.0

    # final price after premium discount (applied on top of catalog-effective price)
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

# pruebas
if __name__ == "__main__":
    print('Probando get_client_token...\n')
    token = get_client_token(telegram_username='t_userN')
    print(f'Token obtenido: {token}\n')

    catalogs = list_catalogs_for_client(token)
    print(f'Catálogos obtenidos: {catalogs}\n')

    
    print('Probando get_client_token...\n')
    token = get_client_token(telegram_username='premiumTU')
    print(f'Token obtenido: {token}\n')

    catalogs = list_catalogs_for_client(token)
    print(f'Catálogos obtenidos: {catalogs}\n')

    print("imprimiendo categorias para el catalogo 2\n")
    categories = list_categories_by_catalog_id(catalog_id=2, client_token=token)
    print(f'Categorías obtenidas: {categories}\n')

    print("Menu categorias: ")
    for cat in categories:
        print(f"- (ID: {cat.get('category_id')})\t{cat.get('name')}")
    print("- (ID: A)\tTodos")


    print("imprimiendo productos para el catalogo 1 y categoria 'A' (todas)\n")
    products = list_products_by_catalog_and_category(catalog_id=1, category_filter='A', client_token=token)
    print(f'Productos obtenidos: {products}\n')

        #impresion bonita de los productos
    print("Productos en categoría ALL:")
    for prod in products:
        print(f"- (ID: {prod.get('product_id')})\t{prod.get('name')} - Precio para cliente: {prod.get('price_for_client')}")
    print('\n\n')
    
    print("imprimiendo productos para el catalogo 1 y categoria '17' (todas)\n")
    products = list_products_by_catalog_and_category(catalog_id=1, category_filter='17', client_token=token)
    print(f'Productos obtenidos: {products}\n')
    
    #impresion bonita de los productos
    print("Productos en categoría 17:")
    for prod in products:
        print(f"- (ID: {prod.get('product_id')})\t{prod.get('name')} - Precio para cliente: {prod.get('price_for_client')}")
    print('\n\n')


    # seleccion de un producto especifico y muestra de su informacion completa
    print("imprimiendo detalles del producto 1 en el catalogo 2\n")
    product_details = get_product_details_for_client(catalog_id=2, product_id=1, client_token=token)
    if not product_details:
        print('No se pudieron obtener los detalles del producto')
    else:
        # print raw dict for full visibility
        print('Detalles del producto obtenidos (raw):')
        pprint(product_details)

        # formatted breakdown
        print('\nDetalles del producto seleccionado (formateado):')
        pd = product_details.get('product', {}) or {}
        cp = product_details.get('catalog_product')
        price_normal = product_details.get('price_normal')
        catalog_price = product_details.get('catalog_price')
        price_for_client = product_details.get('price_for_client')
        client_type = product_details.get('client_type')
        discount_pct = float(product_details.get('discount_pct') or 0.0)

        effective_price = product_details.get('effective_catalog_price')
        catalog_special_price = product_details.get('catalog_special_price')
        catalog_discount_pct = float(product_details.get('catalog_discount_pct') or 0.0)
        catalog_discount_amount = product_details.get('catalog_discount_amount')
        premium_pct = float(product_details.get('premium_pct') or 0.0)
        premium_discount_amount = product_details.get('premium_discount_amount')

        print(f"Tipo de cliente: {client_type}")
        print(f"Nombre: {pd.get('name')}")
        print(f"SKU: {pd.get('sku')}")
        print(f"Imagen: {pd.get('image_url')}")
        print(f"Descripción: {pd.get('description')}")
        print(f"Precio normal: {price_normal}")
        print(f"Descuento del catálogo (monto): {catalog_discount_amount}")
        print(f"Descuento premium (monto): {premium_discount_amount}")
        print(f"Precio para cliente (después de descuento premium): {price_for_client}")

        
        print('\nDetalles de la asociación catálogo-producto (catalog_product):')
        if cp:
            pprint(cp)
        else:
            print('No hay asignación de catalog_product para este (catalog_id, product_id)')
    print('\n')

    