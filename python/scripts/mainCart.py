"""
Simple demo script to exercise the cart API endpoints.

Flow executed when run as __main__:
 - obtain a client JWT (create client if missing)
 - pick a product from ProductRepo
 - add item to cart
 - fetch and print cart
 - update item quantity
 - remove item
 - add again and checkout
 - verify cart removed and print created order summary

This uses the in-process TestClient so it talks to the app directly.
"""
import os
import sys
import time
from pprint import pprint
import re
from typing import Optional
from fastapi.testclient import TestClient

# adjust path so repository imports work when running this script directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.main import app
from python.app.repos.product_repo import ProductRepo
from python.app.repos.order_repo import OrderRepo

# reuse helper from mainClient to obtain a client token
from python.scripts.mainClient import get_client_token
from python.app.core.security import create_access_token

# optional color support for nicer final ticket
try:
    from colorama import Fore, Style, init as _colorama_init
    _colorama_init(autoreset=True)
except Exception:
    class _Col:
        RESET_ALL = ''
    Fore = type('F', (), {'CYAN': '', 'GREEN': '', 'YELLOW': '', 'MAGENTA': '', 'RED': '', 'BLUE': '', 'WHITE': ''})
    Style = type('S', (), {'BRIGHT': '', 'RESET_ALL': ''})

# ANSI strike sequence (some terminals support it). If unsupported, it will be ignored
STRIKE = '\x1b[9m'
RST = '\x1b[0m'

client = TestClient(app)
product_repo = ProductRepo()
order_repo = OrderRepo()


def choose_product() -> Optional[int]:
    """Return a product_id to use for the demo or None if none available."""
    try:
        rows = product_repo.list(limit=20)
    except Exception:
        # fallback to legacy SQL query
        try:
            legacy = product_repo._legacy
            cur = legacy.db.cursor()
            cur.execute('SELECT product_id FROM product LIMIT 20')
            rows = [r[0] for r in cur.fetchall()]
            if not rows:
                return None
            return int(rows[0])
        except Exception:
            return None

    if not rows:
        return None
    first = rows[0]
    pid = getattr(first, 'product_id', None) or (first.get('product_id') if isinstance(first, dict) else None)
    return int(pid) if pid is not None else None


def choose_products(n: int = 3) -> list:
    """Return up to `n` distinct product_ids for the demo."""
    out = []
    try:
        rows = product_repo.list(limit=50)
        for r in rows:
            pid = getattr(r, 'product_id', None) or (r.get('product_id') if isinstance(r, dict) else None)
            if pid is not None:
                out.append(int(pid))
            if len(out) >= n:
                break
        return out
    except Exception:
        try:
            legacy = product_repo._legacy
            cur = legacy.db.cursor()
            cur.execute('SELECT product_id FROM product LIMIT %s', (n,))
            rows = cur.fetchall()
            return [int(r[0]) for r in rows]
        except Exception:
            return []


def pretty_resp(r):
    print(f'STATUS: {r.status_code}')
    try:
        pprint(r.json())
    except Exception:
        print(r.text)


def _fmt_money(v):
    try:
        return f"{float(v):.2f}"
    except Exception:
        return str(v)


def _strip_ansi(s: str) -> str:
    """Remove ANSI sequences for visible-length calculations."""
    try:
        return re.sub(r"\x1b\[[0-9;]*m", "", str(s))
    except Exception:
        return str(s)


def _pad_visible(s: str, width: int, align: str = 'left') -> str:
    """Pad a string containing ANSI codes to a given visible width.

    align: 'left' or 'right'
    """
    raw = str(s)
    vis_len = len(_strip_ansi(raw))
    pad = max(0, width - vis_len)
    if align == 'right':
        return ' ' * pad + raw
    return raw + ' ' * pad


def print_cart_json(cart_payload):
    """Nicely print a cart payload returned by the API.

    Accepts the common shapes:
      - {'cart': None, 'items': []}
      - {'cart_id':..., 'items': [...]}
      - direct cart dict with 'items'
    """
    if not cart_payload:
        print('\n[CART] <empty payload>')
        return

    # normalize
    if isinstance(cart_payload, dict) and 'cart' in cart_payload and 'items' in cart_payload:
        cart = cart_payload.get('cart')
        items = cart_payload.get('items') or []
    elif isinstance(cart_payload, dict) and 'items' in cart_payload:
        cart = cart_payload
        items = cart_payload.get('items') or []
    else:
        print('\n[CART] Unrecognized payload:')
        pprint(cart_payload)
        return

    cart_id = None
    client_id = None
    if cart and isinstance(cart, dict):
        cart_id = cart.get('cart_id')
        client_id = cart.get('client_id') or cart.get('owner_id')

    # header ticket (colored)
    print('\n' + '=' * 60)
    print(Fore.CYAN + Style.BRIGHT + '    OMNIDESK - SHOP TICKET'.center(60) + Style.RESET_ALL)
    print('-' * 60)
    print(f"Cart: {cart_id or '<no cart>'}    Client: {client_id or '<unknown>'}    Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print('-' * 60)
    if not items:
        print('  (empty)')
        print('=' * 60)
        return

    total = 0.0
    print(f"{'ID':>4} {'PRODUCT':30} {'QTY':>3} {'PU':>8} {'FINAL':>8} {'LINE':>10}")
    print('-' * 60)
    for it in items:
        pid = it.get('product_id')
        name = it.get('product_name') or ''
        qty = int(it.get('quantity') or 0)
        pu = it.get('unit_price')
        final = it.get('final_price') if it.get('final_price') is not None else pu
        try:
            line = float(final or 0) * qty
        except Exception:
            line = 0.0
        total += line
        print(f"{str(pid):>4} {name[:30]:30} {qty:>3} { _fmt_money(pu):>8} { _fmt_money(final):>8} { _fmt_money(line):>10}")

    print('-' * 60)
    print('-' * 60)
    # subtotal highlighted
    print(Fore.GREEN + Style.BRIGHT + f"{'SUBTOTAL:':>56} { _fmt_money(total):>10}" + Style.RESET_ALL)
    print('=' * 60)


def print_order_json(order_payload):
    """Nicely print basic order information returned by the checkout endpoint."""
    if not order_payload:
        print('\n[ORDER] <empty payload>')
        return
    # Accept either:
    #  - {'order': {...}, 'items': [...]}
    #  - {'order': {...}} (header-only)
    #  - direct header dict with items inside
    header = None
    items = []
    if isinstance(order_payload, dict) and 'items' in order_payload:
        items = order_payload.get('items') or []
        header = order_payload.get('order') or order_payload.get('header') or None
    else:
        # fallback: payload may be header or {'order': header}
        if isinstance(order_payload, dict) and 'order' in order_payload:
            header = order_payload.get('order')
        else:
            header = order_payload
        # try extracting items from header if present
        if isinstance(header, dict):
            items = header.get('items') or header.get('order_items') or []

    print('\n' + '=' * 60)
    print('ORDER SUMMARY')
    print('-' * 60)
    if header:
        oid = header.get('order_id') if isinstance(header, dict) else getattr(header, 'order_id', None)
        client_id = header.get('client_id') if isinstance(header, dict) else getattr(header, 'client_id', None)
        grand = header.get('grand_total') if isinstance(header, dict) else getattr(header, 'grand_total', None)
        created_at = header.get('created_at') if isinstance(header, dict) else getattr(header, 'created_at', None)
        print(f"Order id: {oid}    client_id: {client_id}    created_at: {created_at or '<unknown>'}")
        print(f"Grand total: { _fmt_money(grand) if grand is not None else 'N/A'}")
    print('-' * 60)

    # print ticket style header
    print('\n' + '=' * 60)
    print(Fore.CYAN + Style.BRIGHT + '    OMNIDESK - ORDER TICKET'.center(60) + Style.RESET_ALL)
    print('-' * 60)
    if header:
        print(f"Order: {oid or '<id?>'}    Date: {created_at or time.strftime('%Y-%m-%d %H:%M:%S')}    Client: {client_id or '<unknown>'}")
    print('-' * 60)

    # prefer enriched items (items_detail) if present
    if isinstance(order_payload, dict) and 'items_detail' in order_payload:
        items = order_payload.get('items_detail') or []

    if items:
        total = 0.0
        # new header: show original PU struck-through, total discount for the line, final unit and line total
        print(f"{'PID':>4} {'PRODUCT':30} {'QTY':>3} {'PU(before)':>14} {'-DISCOUNT':>12} {'FINAL':>10} {'LINE':>12}")
        print('-' * 90)
        for it in items:
            pid = it.get('product_id')
            name = it.get('product_name') or ''
            qty = int(it.get('quantity') or 0)
            pu = it.get('unit_price')
            # determine final unit price (after discounts)
            final_unit = None
            if it.get('final_unit') is not None:
                final_unit = float(it.get('final_unit'))
            elif it.get('final_price') is not None:
                final_unit = float(it.get('final_price'))
            elif pu is not None:
                final_unit = float(pu)

            # estimate per-unit discount: prefer pu - final_unit when possible
            per_unit_discount = 0.0
            try:
                if pu is not None and final_unit is not None:
                    per_unit_discount = float(pu) - float(final_unit)
                else:
                    # fallback to explicit fields
                    per_unit_discount = float(it.get('catalog_discount_amount') or 0) + float(it.get('premium_discount_amount') or 0)
            except Exception:
                per_unit_discount = float(it.get('catalog_discount_amount') or 0) + float(it.get('premium_discount_amount') or 0)

            # compute totals
            line_discount = round(per_unit_discount * qty, 2)
            if it.get('line_total') is not None:
                line_total = float(it.get('line_total'))
            else:
                line_total = round((final_unit or 0) * qty, 2)
            total += line_total

            # format pieces: struck original PU, discount (negative), final unit and line total
            pu_raw = (STRIKE + _fmt_money(pu) + RST) if pu is not None else '<n/a>'
            disc_raw = (Fore.RED + '-' + _fmt_money(line_discount) + Style.RESET_ALL) if line_discount else _fmt_money(0)
            final_raw = Fore.GREEN + Style.BRIGHT + _fmt_money(final_unit) + Style.RESET_ALL
            line_raw = Fore.GREEN + Style.BRIGHT + _fmt_money(line_total) + Style.RESET_ALL

            # pad using visible widths so ANSI codes don't break alignment
            pid_s = f"{str(pid):>4}"
            name_s = _pad_visible(name[:30], 30)
            qty_s = f"{qty:>3}"
            pu_s = _pad_visible(pu_raw, 14, align='right')
            disc_s = _pad_visible(disc_raw, 12, align='right')
            final_s = _pad_visible(final_raw, 10, align='right')
            line_s = _pad_visible(line_raw, 12, align='right')

            print(f"{pid_s} {name_s} {qty_s} {pu_s} {disc_s} {final_s} {line_s}")
        print('-' * 90)
        print(Fore.CYAN + Style.BRIGHT + f"{'CALC TOTAL:':>78} { _fmt_money(total):>10}" + Style.RESET_ALL)
    else:
        print('  (no items included in payload)')
    print('=' * 60)


def run_demo(phone: str = '+5215512345678', full_name: str = 'Cliente Cart Demo', products_to_add: int = 3, client_id: Optional[int] = None):
    """Demo flow that adds multiple products to the cart and checks out once.

    products_to_add: how many distinct products to add (tries to pick that many).
    """
    # obtain token: either create a token for the given client_id (convenient for demos),
    # or fall back to identifying by phone
    if client_id is not None:
        print(f'Using provided client_id={client_id} to create a demo token (useful for premium clients)')
        try:
            token = create_access_token({'client_id': int(client_id), 'type': 'client'})
        except Exception as e:
            print('Failed to create token from client_id:', repr(e))
            return
    else:
        print('Obtaining client token (will create client if missing)')
        token = get_client_token(phone=phone, create_if_missing=True, full_name=full_name)
        if not token:
            print('Failed to obtain token. Aborting demo.')
            return

    headers = {'Authorization': f'Bearer {token}'}
    print('Token obtained (truncated):', (token[:40] + '...') if isinstance(token, str) else str(token))

    # pick multiple products
    pids = choose_products(products_to_add)
    if not pids:
        print('No products found in DB. Populate products first and retry.')
        return
    print('Selected product_ids=', pids)

    # Ensure cart is empty/visible
    print('\n-- GET /api/clients/cart (initial)')
    r = client.get('/api/clients/cart', headers=headers)
    # pretty_resp(r)  # commented to keep output clean, show only ticket-style prints
    try:
        print_cart_json(r.json())
    except Exception:
        pass

    # Add each product to the cart
    for i, pid in enumerate(pids, start=1):
        qty = 1 if i < len(pids) else 2  # make last item quantity 2 for demo
        print(f"\n-- POST /api/clients/cart/items (add product {pid} qty={qty})")
        payload = {'product_id': pid, 'quantity': qty}
        r = client.post('/api/clients/cart/items', json=payload, headers=headers)
        # pretty_resp(r)  # commented to keep output clean
        if r.status_code >= 400:
            print('Add item failed; aborting')
            return

    # Fetch cart
    print('\n-- GET /api/clients/cart (after adds)')
    r = client.get('/api/clients/cart', headers=headers)
    # pretty_resp(r)  # commented to keep output clean
    try:
        print_cart_json(r.json())
    except Exception:
        pass

    # Update quantity of the first product if present
    first_pid = pids[0]
    print(f"\n-- PUT /api/clients/cart/items/{first_pid} (update quantity to 3)")
    r = client.put(f'/api/clients/cart/items/{first_pid}', json={'quantity': 3}, headers=headers)
    # pretty_resp(r)  # commented to keep output clean

    # Fetch cart again
    print('\n-- GET /api/clients/cart (after update)')
    r = client.get('/api/clients/cart', headers=headers)
    # pretty_resp(r)  # commented to keep output clean
    try:
        print_cart_json(r.json())
    except Exception:
        pass

    # Checkout once with everything in the cart
    print('\n-- POST /api/clients/cart/checkout (checkout all items)')
    r = client.post('/api/clients/cart/checkout', headers=headers)
    # pretty_resp(r)  # commented to keep output clean
    if r.status_code >= 400:
        print('Checkout failed; aborting')
        return

    # If order created, try to print a nice ticket and fetch via repo
    try:
        body = r.json()
    # pretty + ticket
    # pretty_resp(r)  # commented to keep output clean
        try:
            print_order_json(body)
        except Exception:
            pass

        order = body.get('order') or body.get('data') or body
        order_id = None
        if isinstance(order, dict):
            order_id = order.get('order_id') or order.get('header', {}).get('order_id')
        elif hasattr(order, 'order_id'):
            order_id = getattr(order, 'order_id')
        if order_id:
            print('\nOrder created, fetching canonical order via OrderRepo:')
            try:
                o = order_repo.get(order_id)
                # order_repo.get may return a header; try to present it nicely
                try:
                    # attempt to fetch canonical order items from legacy repo
                    try:
                        from python.Classes.repos.order_repo import OrderItemRepo as LegacyOrderItemRepo
                        legacy_items = LegacyOrderItemRepo()
                        canonical_items = legacy_items.filter('order_id=%s', (order_id,), limit=1000)
                    except Exception:
                        canonical_items = []
                    print_order_json({'order': o, 'items': canonical_items})
                except Exception:
                    # pprint(o)  # commented to keep output clean
                    pass
            except Exception:
                print('Could not fetch order via repo; raw order payload:')
                pprint(order)
        else:
            print('\nOrder payload returned (no numeric order_id found):')
            pprint(order)
    except Exception:
        print('Error parsing checkout response')

    # Final check: cart should be deleted/empty
    print('\n-- GET /api/clients/cart (final check)')
    r = client.get('/api/clients/cart', headers=headers)
    # pretty_resp(r)  # commented to keep output clean
    try:
        print_cart_json(r.json())
    except Exception:
        pass



    

if __name__ == '__main__':
    # Run demo with defaults; edit phone/full_name if desired
    # Use premium client id=7 for demo (adjust if needed)
    run_demo(client_id=7)
