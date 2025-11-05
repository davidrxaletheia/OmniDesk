from typing import Optional, List
from fastapi import APIRouter, Header, HTTPException, Body
from ..repos.cart_repo import CartRepo
from ..repos.product_repo import ProductRepo
from ..repos.catalog_product_repo import CatalogProductRepo
from ..repos.catalog_repo import CatalogRepo
from ..repos.order_repo import OrderRepo
from ..utils.serializers import to_jsonable
from ..core.security import decode_token
from ..core.config import settings

router = APIRouter()
repo = CartRepo()
prod_repo = ProductRepo()
cp_repo = CatalogProductRepo()
cat_repo = CatalogRepo()
order_repo = OrderRepo()


def _get_client_id_from_auth(authorization: Optional[str]) -> Optional[int]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        token = parts[1]
        try:
            payload = decode_token(token)
            sub = payload.get('sub', {})
            cid = sub.get('client_id') if isinstance(sub, dict) else None
            return cid
        except Exception:
            return None
    return None


@router.get('/clients/cart')
def get_cart(authorization: Optional[str] = Header(None)):
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')
    cart = repo.get_cart_by_client(client_id)
    if not cart:
        return to_jsonable({'cart': None, 'items': []})
    return to_jsonable(cart)


class AddItemBody:
    product_id: int
    quantity: int = 1
    catalog_id: Optional[int] = None


@router.post('/clients/cart/items')
def add_item(body: dict = Body(...), authorization: Optional[str] = Header(None)):
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')

    product_id = int(body.get('product_id'))
    quantity = int(body.get('quantity', 1))
    catalog_id = body.get('catalog_id')

    # fetch product snapshot
    prod = prod_repo.get(product_id)
    if not prod:
        raise HTTPException(404, 'Product not found')

    unit_price = getattr(prod, 'price', None) if hasattr(prod, 'price') else (prod.get('price') if isinstance(prod, dict) else None)
    sku = getattr(prod, 'sku', None) if hasattr(prod, 'sku') else (prod.get('sku') if isinstance(prod, dict) else None)
    product_name = getattr(prod, 'name', None) if hasattr(prod, 'name') else (prod.get('name') if isinstance(prod, dict) else None)
    tax_rate = getattr(prod, 'tax_rate', None) if hasattr(prod, 'tax_rate') else (prod.get('tax_rate') if isinstance(prod, dict) else None)

    catalog_special_price = None
    applied_catalog_discount_pct = None
    final_price = unit_price

    if catalog_id:
        cp = cp_repo.get(catalog_id, product_id)
        if cp and isinstance(cp, dict):
            catalog_special_price = cp.get('special_price')
        catalog = cat_repo.get(catalog_id)
        if catalog and isinstance(catalog, dict):
            try:
                cat_pct = float(catalog.get('discount_percentage') or 0.0) / 100.0
            except Exception:
                cat_pct = 0.0
        else:
            cat_pct = 0.0
        if catalog_special_price is not None:
            final_price = catalog_special_price
            applied_catalog_discount_pct = round((unit_price - final_price) / unit_price, 4) if unit_price else 0.0
        else:
            if cat_pct and unit_price is not None:
                final_price = round(float(unit_price) * (1.0 - cat_pct), 2)
                applied_catalog_discount_pct = cat_pct

    # get or create cart
    cart_id = repo.get_or_create_cart_for_client(client_id)

    snapshot = {
        'unit_price': unit_price,
        'catalog_special_price': catalog_special_price,
        'applied_catalog_discount_pct': applied_catalog_discount_pct,
        'final_price': final_price,
        'sku': sku,
        'product_name': product_name,
        'tax_rate': tax_rate,
    }

    ci_id = repo.add_or_update_item(cart_id, product_id, quantity, snapshot)
    return to_jsonable({'cart_id': cart_id, 'cart_item_id': ci_id})


@router.put('/clients/cart/items/{product_id}')
def update_item(product_id: int, body: dict = Body(...), authorization: Optional[str] = Header(None)):
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')
    cart = repo.get_cart_by_client(client_id)
    if not cart:
        raise HTTPException(404, 'Cart not found')
    quantity = int(body.get('quantity', 0))
    ok = repo.update_item_quantity(cart['cart_id'], product_id, quantity)
    if not ok:
        raise HTTPException(404, 'Item not found')
    return to_jsonable({'updated': True})


@router.delete('/clients/cart/items/{product_id}')
def delete_item(product_id: int, authorization: Optional[str] = Header(None)):
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')
    cart = repo.get_cart_by_client(client_id)
    if not cart:
        raise HTTPException(404, 'Cart not found')
    ok = repo.remove_item(cart['cart_id'], product_id)
    return to_jsonable({'removed': bool(ok)})


@router.post('/clients/cart/clear')
def clear_cart(authorization: Optional[str] = Header(None)):
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')
    cart = repo.get_cart_by_client(client_id)
    if not cart:
        return to_jsonable({'cleared': True})
    repo.clear_cart(cart['cart_id'])
    return to_jsonable({'cleared': True})


@router.post('/clients/cart/checkout')
def checkout(authorization: Optional[str] = Header(None)):
    """Create an order from the current cart and remove the cart on success."""
    client_id = _get_client_id_from_auth(authorization)
    if not client_id:
        raise HTTPException(401, 'Missing or invalid token')
    cart = repo.get_cart_by_client(client_id)
    if not cart or not cart.get('items'):
        raise HTTPException(400, 'Cart empty')

    # Build order payload: include snapshots from cart items so order_items preserve pricing
    items = []
    for it in cart.get('items', []):
        items.append({
            'product_id': int(it.get('product_id')),
            'quantity': int(it.get('quantity', 1)),
            'unit_price': it.get('unit_price'),
            'catalog_special_price': it.get('catalog_special_price'),
            'applied_catalog_discount_pct': it.get('applied_catalog_discount_pct'),
            'final_price': it.get('final_price'),
            'sku': it.get('sku'),
            'product_name': it.get('product_name'),
            'tax_rate': it.get('tax_rate'),
        })

    payload = {'client_id': client_id, 'items': items, 'client_type': None}

    # try to detect client type from client table (OrderRepo expects client_type)
    try:
        from ..repos.client_repo import ClientRepo
        c = ClientRepo().get(client_id)
        payload['client_type'] = getattr(c, 'client_type', None) if c else None
    except Exception:
        payload['client_type'] = None

    try:
        order = order_repo.create(payload)
    except Exception as exc:
        raise HTTPException(400, f'Error creating order: {exc}')
    # Try to enrich response with order items so callers receive full order + items
    order_items = []
    try:
        # order may be header-only; try to extract order_id
        order_id = None
        if isinstance(order, dict):
            order_id = order.get('order_id') or order.get('header', {}).get('order_id')
        else:
            order_id = getattr(order, 'order_id', None)

        if order_id:
            # use legacy repo to fetch order items
            try:
                from python.Classes.repos.order_repo import OrderItemRepo as LegacyOrderItemRepo
                legacy_items = LegacyOrderItemRepo()
                order_items = legacy_items.filter('order_id=%s', (order_id,), limit=1000)
                # convert results to list/dict-friendly if needed (legacy objects may be dict-like)
            except Exception:
                order_items = []
    except Exception:
        order_items = []

    # Build a richer per-line breakdown from the cart snapshots (catalog + premium discounts)
    enriched_items = []
    try:
        # client premium pct
        premium_pct = 0.0
        try:
            premium_pct = float(payload.get('client_type') and (1.0 if payload.get('client_type') == 'premium' else 0.0))
        except Exception:
            premium_pct = 0.0

        # prefer to compute using the original cart items (we still have `cart` variable)
        for it in cart.get('items', []):
            pid = int(it.get('product_id'))
            qty = int(it.get('quantity') or 0)
            unit_price = float(it.get('unit_price') or 0.0)
            final_unit = None
            if it.get('final_price') is not None:
                try:
                    final_unit = float(it.get('final_price'))
                except Exception:
                    final_unit = unit_price
            elif it.get('catalog_special_price') is not None:
                try:
                    final_unit = float(it.get('catalog_special_price'))
                except Exception:
                    final_unit = unit_price
            elif it.get('applied_catalog_discount_pct') is not None:
                try:
                    pct = float(it.get('applied_catalog_discount_pct') or 0.0)
                    final_unit = round(unit_price * (1.0 - pct), 2)
                except Exception:
                    final_unit = unit_price
            else:
                final_unit = unit_price

            catalog_disc = round((unit_price - final_unit) * qty, 2) if unit_price and final_unit is not None else 0.0
            premium_disc = round((final_unit * qty) * (settings.PREMIUM_DISCOUNT_PCT if payload.get('client_type') == 'premium' else 0.0), 2) if payload.get('client_type') == 'premium' else 0.0
            total_disc = round(catalog_disc + premium_disc, 2)
            line_total = round(unit_price * qty - total_disc, 2)

            enriched_items.append({
                'product_id': pid,
                'product_name': it.get('product_name'),
                'quantity': qty,
                'unit_price': unit_price,
                'final_unit': final_unit,
                'catalog_discount_amount': catalog_disc,
                'premium_discount_amount': premium_disc,
                'total_discount_amount': total_disc,
                'line_total': line_total,
            })
    except Exception:
        enriched_items = []

    # remove the cart now that order exists
    try:
        repo.delete_cart(cart['cart_id'])
    except Exception:
        # non-fatal: cart deletion failed, but order was created; include warning
        return to_jsonable({'order': order, 'items': order_items, 'items_detail': enriched_items, 'warning': 'order created but failed to delete cart'})
    return to_jsonable({'order': order, 'items': order_items, 'items_detail': enriched_items})
