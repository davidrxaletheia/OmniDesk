"""
Helpers focused on the two tables: `customer_order` and `order_item`.

Functions provided (non-interactive):
 - list_orders(limit, offset)
 - get_order(order_id)
 - show_order_full(order_id)
 - create_order(client_id, notes=None)
 - add_item_from_product(order_id, product_id, quantity=1, discount_pct=None, discount_amount=None)
 - add_item_manual(order_id, product_id, product_name, sku, unit_price, tax_rate, quantity=1, discount_pct=None, discount_amount=None)
 - update_item(order_id, product_id, updates)
 - delete_item(order_id, product_id)
 - recalc_order_totals(order_id)

This mirrors the style of other `main*.py` scripts. Designed for quick, manual testing
of the two tables and their interactions. The functions use the existing legacy
repos (`python.Classes.repos.order_repo`) and the app product/client repos when
needed to obtain snapshots.

Usage: edit ACTION at bottom or import functions from other scripts.
"""
import os
import sys
from pprint import pprint
from typing import Optional, Dict, Any

# Make repo importable when running script directly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.repos.product_repo import ProductRepo
from python.app.repos.client_repo import ClientRepo
from python.app.repos.order_repo import OrderRepo
from python.app.repos.catalog_repo import CatalogRepo
from python.app.repos.catalog_product_repo import CatalogProductRepo
from python.app.repos.category_repo import CategoryRepo

# Legacy/low level repos for direct table operations
from python.Classes.repos.order_repo import (
    CustomerOrderRepo as LegacyCustomerOrderRepo,
    OrderItemRepo as LegacyOrderItemRepo,
)

client_repo = ClientRepo()
product_repo = ProductRepo()
legacy_order = LegacyCustomerOrderRepo()
legacy_items = LegacyOrderItemRepo()
order_repo = OrderRepo()
catalog_repo = CatalogRepo()
catalog_product_repo = CatalogProductRepo()
category_repo = CategoryRepo()


def list_orders(limit: int = 50, offset: int = 0):
    """List orders (raw models) using legacy repo."""
    return legacy_order.list(limit=limit, offset=offset)


def get_order(order_id: int):
    return legacy_order.get(order_id)


def list_items(order_id: int):
    return legacy_items.filter('order_id=%s', (order_id,), limit=100)


def show_order_full(order_id: int):
    h = get_order(order_id)
    if not h:
        print('Order not found:', order_id)
        return None
    print('\n--- Encabezado pedido')
    pprint(h)
    print('\n--- Items')
    items = list_items(order_id)
    for it in items:
        pprint(it)
    return {'header': h, 'items': items}


def create_order(client_id: int, notes: Optional[str] = None) -> Optional[int]:
    data = {'client_id': client_id}
    if notes is not None:
        data['notes'] = notes
    try:
        oid = legacy_order.create(data)
        print('Order created id=', oid)
        return oid
    except Exception as e:
        print('Error creating order:', repr(e))
        return None


def add_item_from_product(order_id: int, product_id: int, quantity: int = 1,
                          discount_pct: Optional[float] = None,
                          discount_amount: Optional[float] = None):
    """Create an order_item using product snapshot from ProductRepo."""
    prod = product_repo.get(product_id)
    if not prod:
        print('Product not found:', product_id)
        return None
    # product model may be pydantic-like or dict
    name = getattr(prod, 'name', None) or (prod.get('name') if isinstance(prod, dict) else None)
    sku = getattr(prod, 'sku', None) or (prod.get('sku') if isinstance(prod, dict) else None)
    unit_price = getattr(prod, 'price', None) or (prod.get('price') if isinstance(prod, dict) else None)
    tax_rate = getattr(prod, 'tax_rate', None) or (prod.get('tax_rate') if isinstance(prod, dict) else 0)

    if unit_price is None:
        print('Product has no price; supply unit_price manually')
        return None

    return add_item_manual(order_id, product_id, name or 'unknown', sku, unit_price, tax_rate,
                           quantity=quantity, discount_pct=discount_pct, discount_amount=discount_amount)


def add_item_manual(order_id: int, product_id: int, product_name: str, sku: Optional[str],
                    unit_price: float, tax_rate: float, quantity: int = 1,
                    discount_pct: Optional[float] = None, discount_amount: Optional[float] = None):
    data: Dict[str, Any] = {
        'order_id': order_id,
        'product_id': product_id,
        'quantity': quantity,
        'product_name': product_name,
        'sku': sku,
        'unit_price': unit_price,
        'tax_rate': tax_rate,
    }
    if discount_pct is not None:
        data['discount_pct'] = discount_pct
    if discount_amount is not None:
        data['discount_amount'] = discount_amount

    try:
        iid = legacy_items.create(data)
        print('Order item inserted (row id):', iid)
        return iid
    except Exception as e:
        print('Error inserting order_item:', repr(e))
        return None


def update_item(order_id: int, product_id: int, updates: Dict[str, Any]) -> int:
    """Update an order_item by (order_id, product_id). Returns rowcount."""
    allowed = {'quantity', 'product_name', 'sku', 'unit_price', 'discount_pct', 'discount_amount', 'tax_rate'}
    to_set = {k: updates[k] for k in updates.keys() if k in allowed}
    if not to_set:
        print('No valid fields to update')
        return 0
    sets = ', '.join([f"{k}=%s" for k in to_set.keys()])
    params = list(to_set.values()) + [order_id, product_id]
    sql = f"UPDATE order_item SET {sets} WHERE order_id=%s AND product_id=%s"
    cur = legacy_items.db.cursor()
    try:
        cur.execute(sql, params)
        if not legacy_items.db.autocommit:
            legacy_items.db.commit()
        print('Rows updated:', cur.rowcount)
        return cur.rowcount
    except Exception as e:
        print('Error updating order_item:', repr(e))
        return 0


def delete_item(order_id: int, product_id: int) -> int:
    sql = "DELETE FROM order_item WHERE order_id=%s AND product_id=%s"
    cur = legacy_items.db.cursor()
    try:
        cur.execute(sql, (order_id, product_id))
        if not legacy_items.db.autocommit:
            legacy_items.db.commit()
        print('Rows deleted:', cur.rowcount)
        return cur.rowcount
    except Exception as e:
        print('Error deleting order_item:', repr(e))
        return 0


def recalc_order_totals(order_id: int) -> bool:
    """Recalculate subtotal, discount_total and tax_total from order_item and
    update customer_order header accordingly.
    Returns True on success.
    """
    cur = legacy_items.db.cursor()
    try:
        cur.execute("SELECT COALESCE(SUM(line_subtotal),0), COALESCE(SUM(line_discount),0), COALESCE(SUM(line_tax),0) FROM order_item WHERE order_id=%s", (order_id,))
        row = cur.fetchone()
        if not row:
            v_sub, v_dis, v_tax = 0.0, 0.0, 0.0
        else:
            v_sub, v_dis, v_tax = row[0] or 0.0, row[1] or 0.0, row[2] or 0.0
        updates = {
            'subtotal': float(v_sub),
            'discount_total': float(v_dis),
            'tax_total': float(v_tax)
        }
        legacy_order.update(order_id, updates)
        print('Order totals recalculated and updated for order_id=', order_id)
        return True
    except Exception as e:
        print('Error recalculating totals:', repr(e))
        return False


def interactive_create_order_for_client(client_id: int):
    """Interactive flow: show products, allow user to pick product ids and quantities,
    then create the order for the given client_id and print a ticket.
    """
    print(f"Creando orden para client_id={client_id}")
    # Show available products
    try:
        products = product_repo.list(limit=200)
    except Exception:
        # fallback to raw SQL via legacy
        legacy = product_repo._legacy
        cur = legacy.db.cursor()
        cur.execute('SELECT * FROM product LIMIT 200')
        cols = [d[0] for d in cur.description]
        products = []
        for row in cur.fetchall():
            data = {cols[i]: row[i] for i in range(len(cols))}
            products.append(data)

    print('\n--- Productos disponibles ---')
    for p in products:
        pid = getattr(p, 'product_id', None) or (p.get('product_id') if isinstance(p, dict) else None)
        name = getattr(p, 'name', None) or (p.get('name') if isinstance(p, dict) else None)
        price = getattr(p, 'price', None) or (p.get('price') if isinstance(p, dict) else None)
        print(f"({pid}) {name} - {price}")

    # selection loop
    items = []
    while True:
        s = input('\nIngrese product_id para agregar (ENTER para terminar): ').strip()
        if s == '':
            break
        try:
            pid = int(s)
        except ValueError:
            print('product_id inválido, intenta de nuevo')
            continue
        # check product exists
        prod = None
        for p in products:
            p_pid = getattr(p, 'product_id', None) or (p.get('product_id') if isinstance(p, dict) else None)
            if p_pid == pid:
                prod = p
                break
        if not prod:
            print('Producto no encontrado en la lista, intenta otro id')
            continue
        q = input('Cantidad (por defecto 1): ').strip()
        try:
            qty = int(q) if q else 1
            if qty <= 0:
                print('Cantidad debe ser mayor que 0')
                continue
        except ValueError:
            print('Cantidad inválida')
            continue
        items.append({'product_id': pid, 'quantity': qty})
        print(f'Agregado: product_id={pid} qty={qty}')

    if not items:
        print('No se seleccionaron productos. Abortando creación de orden.')
        return None

    # create order using app's OrderRepo (it will snapshot products and create items)
    try:
        payload = {'client_id': client_id, 'items': items, 'notes': 'Orden creada interactivamente'}
        created = order_repo.create(payload)
        # created may be model or dict
        order_id = getattr(created, 'order_id', None) or (created.get('order_id') if isinstance(created, dict) else None)
        print('\nOrden creada con order_id=', order_id)
    except Exception as e:
        print('Error creando orden via OrderRepo:', repr(e))
        return None

    # print nicely formatted ticket
    print_ticket(order_id)
    return order_id


def print_ticket(order_id: int, catalog: Optional[object] = None):
    """Print a nicely formatted ticket for order_id. If `catalog` is provided,
    show catalog discount info in the header.
    """
    header = legacy_order.get(order_id)
    if not header:
        print('Order not found for ticket:', order_id)
        return

    rows = legacy_items.filter('order_id=%s', (order_id,), limit=500)

    # Header
    print('\n' + '=' * 48)
    print(' ' * 12 + 'TICKET DE VENTA'.center(24))
    print('=' * 48)
    client_id_h = getattr(header, 'client_id', None)
    created_at = getattr(header, 'created_at', None)
    status = getattr(header, 'status', None)
    print(f'Order: {order_id}    Cliente: {client_id_h}    Fecha: {created_at}    Estado: {status}')
    if catalog:
        disc_pct = getattr(catalog, 'discount_percentage', None) or (catalog.get('discount_percentage') if isinstance(catalog, dict) else None)
        print(f"Catalogo aplicado: {getattr(catalog,'name',None) or (catalog.get('name') if isinstance(catalog,dict) else '')}  Descuento: {disc_pct}%")

    print('-' * 48)
    # Lines
    print(f"{'Producto':28} {'QTY':>3} {'PU':>8} {'DESC':>7} {'IVA':>6} {'TOTAL':>8}")
    print('-' * 48)
    for r in rows:
        name = getattr(r, 'product_name', None) or (r.get('product_name') if isinstance(r, dict) else '')
        qty = getattr(r, 'quantity', None) or (r.get('quantity') if isinstance(r, dict) else 0)
        up = getattr(r, 'unit_price', None) or (r.get('unit_price') if isinstance(r, dict) else 0)
        ld = getattr(r, 'line_discount', None) or (r.get('line_discount') if isinstance(r, dict) else 0)
        lt = getattr(r, 'line_tax', None) or (r.get('line_tax') if isinstance(r, dict) else 0)
        ltot = getattr(r, 'line_total', None) or (r.get('line_total') if isinstance(r, dict) else 0)
        print(f"{name[:28]:28} {qty:>3} {float(up):8.2f} {float(ld):7.2f} {float(lt):6.2f} {float(ltot):8.2f}")

    print('-' * 48)
    subtotal = getattr(header, 'subtotal', None) or (header.get('subtotal') if isinstance(header, dict) else 0)
    discount_total = getattr(header, 'discount_total', None) or (header.get('discount_total') if isinstance(header, dict) else 0)
    tax_total = getattr(header, 'tax_total', None) or (header.get('tax_total') if isinstance(header, dict) else 0)
    shipping_total = getattr(header, 'shipping_total', None) or (header.get('shipping_total') if isinstance(header, dict) else 0)
    grand_total = getattr(header, 'grand_total', None) or (header.get('grand_total') if isinstance(header, dict) else 0)

    print(f"{'SUBTOTAL:':30} {float(subtotal):18.2f}")
    print(f"{'DESCUENTO:':30} {float(discount_total):18.2f}")
    print(f"{'IMPUESTOS:':30} {float(tax_total):18.2f}")
    print(f"{'ENVIO:':30} {float(shipping_total):18.2f}")
    print('=' * 48)
    print(f"{'GRAND TOTAL:':30} {float(grand_total):18.2f}")
    print('=' * 48)
    return order_id


def interactive_catalog_order_flow():
    """Full interactive flow requested:
    1) List clients and let user choose client
    2) Show client data (client_type)
    3) List catalogs filtered by client_type
    4) Let user choose catalog and show catalog info
    5) List products in that catalog grouped by category
    6) Let user pick products/quantities and create order applying catalog discount
    7) Print ticket with discount applied
    """
    # 1) list clients
    print('Listando clientes (limit 200)')
    try:
        clients = client_repo.list(limit=200)
    except Exception:
        legacy = client_repo._legacy
        cur = legacy.db.cursor()
        cur.execute('SELECT * FROM client LIMIT 200')
        cols = [d[0] for d in cur.description]
        clients = []
        for row in cur.fetchall():
            clients.append({cols[i]: row[i] for i in range(len(cols))})

    for c in clients:
        cid = getattr(c, 'client_id', None) or (c.get('client_id') if isinstance(c, dict) else None)
        name = getattr(c, 'full_name', None) or (c.get('full_name') if isinstance(c, dict) else None)
        ctype = getattr(c, 'client_type', None) or (c.get('client_type') if isinstance(c, dict) else None)
        print(f"({cid}) {name} - type: {ctype}")

    sel = input('\nElige tu client_id: ').strip()
    try:
        client_id = int(sel)
    except Exception:
        print('client_id inválido')
        return
    client = client_repo.get(client_id)
    if not client:
        print('Cliente no encontrado:', client_id)
        return
    client_type = getattr(client, 'client_type', None) or (client.get('client_type') if isinstance(client, dict) else None)
    print('\nCliente elegido:')
    pprint(client)

    # 3) list catalogs filtered by client_type
    cats = catalog_repo.actives()
    filtered = []
    for cat in cats:
        vis = getattr(cat, 'visible_to', None) or (cat.get('visible_to') if isinstance(cat, dict) else None)
        if client_type == 'premium':
            if vis in (None, 'premium', 'todos'):
                filtered.append(cat)
        else:
            # non-premium see only 'todos' (and None)
            if vis in (None, 'todos'):
                filtered.append(cat)

    if not filtered:
        print('No hay catálogos disponibles para tu tipo de cliente')
        return

    print('\nCatálogos disponibles:')
    for c in filtered:
        cid = getattr(c, 'catalog_id', None)
        name = getattr(c, 'name', None)
        disc = getattr(c, 'discount_percentage', None)
        active = getattr(c, 'active', None)
        print(f"({cid}) {name} - discount: {disc} - active: {active}")

    sel = input('\nElige catalog_id: ').strip()
    try:
        catalog_id = int(sel)
    except Exception:
        print('catalog_id inválido')
        return
    catalog = catalog_repo.get(catalog_id)
    if not catalog:
        print('Catalogo no encontrado:', catalog_id)
        return
    print('\nCatalogo elegido:')
    pprint(catalog)

    # 5) list products in catalog grouped by category
    cp_rows = catalog_product_repo.list_by_catalog(catalog_id)
    # gather product details and group
    grouped = {}
    for cp in cp_rows:
        pid = cp.get('product_id') if isinstance(cp, dict) else getattr(cp, 'product_id', None)
        special_price = cp.get('special_price') if isinstance(cp, dict) else getattr(cp, 'special_price', None)
        prod = product_repo.get(pid)
        if not prod:
            continue
        cat_id = getattr(prod, 'category_id', None) or (prod.get('category_id') if isinstance(prod, dict) else None)
        cat_name = 'Sin categoria'
        if cat_id:
            cat = category_repo.get(cat_id)
            if cat:
                cat_name = getattr(cat, 'name', None) or (cat.get('name') if isinstance(cat, dict) else cat_name)
        entry = {
            'product_id': pid,
            'name': getattr(prod, 'name', None) or (prod.get('name') if isinstance(prod, dict) else ''),
            'price': special_price if special_price not in (None, '') else (getattr(prod, 'price', None) or (prod.get('price') if isinstance(prod, dict) else 0)),
            'sku': getattr(prod, 'sku', None) or (prod.get('sku') if isinstance(prod, dict) else None),
            'tax_rate': getattr(prod, 'tax_rate', None) or (prod.get('tax_rate') if isinstance(prod, dict) else 0),
        }
        grouped.setdefault(cat_name, []).append(entry)

    print('\nProductos por categoria:')
    for cat_name, items in grouped.items():
        print('\n==', cat_name, '==')
        for it in items:
            print(f"({it['product_id']}) {it['name']} - {it['price']}")

    # 6) selection
    selections = []
    while True:
        s = input('\nIngrese product_id para agregar (ENTER para terminar): ').strip()
        if s == '':
            break
        try:
            pid = int(s)
        except Exception:
            print('product_id inválido')
            continue
        q = input('Cantidad (por defecto 1): ').strip()
        try:
            qty = int(q) if q else 1
        except Exception:
            print('Cantidad inválida')
            continue
        selections.append({'product_id': pid, 'quantity': qty})
        print('Agregado', pid, qty)

    if not selections:
        print('No seleccionaste productos. Abortando.')
        return

    # 6b) create order header
    oid = create_order(client_id, notes=f'Pedido desde catalogo {catalog_id}')
    if not oid:
        print('No se pudo crear la orden')
        return

    # apply catalog discount_percentage
    disc_pct = float(getattr(catalog, 'discount_percentage', 0) or (catalog.get('discount_percentage') if isinstance(catalog, dict) else 0))
    for sel in selections:
        pid = sel['product_id']
        qty = sel['quantity']
        # find price and tax
        prod = product_repo.get(pid)
        if not prod:
            print('Producto no encontrado al insertar:', pid)
            continue
        price = getattr(prod, 'price', None) or (prod.get('price') if isinstance(prod, dict) else 0)
        tax_rate = getattr(prod, 'tax_rate', None) or (prod.get('tax_rate') if isinstance(prod, dict) else 0)
        # Insert item with discount_pct = catalog discount
        add_item_manual(oid, pid, getattr(prod, 'name', None) or (prod.get('name') if isinstance(prod, dict) else ''), getattr(prod, 'sku', None), price, tax_rate, quantity=qty, discount_pct=disc_pct)

    # recalc totals and print ticket (nicely formatted)
    recalc_order_totals(oid)
    print('\nTicket final:')
    print_ticket(oid, catalog)
    # --- Preguntar por facturación ---
    try:
        prompt_invoice_flow(oid)
    except Exception as e:
        print('Error en flujo de facturación:', repr(e))
    return oid


def prompt_invoice_flow(order_id: int):
    """Interactive invoice flow:
    - Pregunta si desea factura. Si no, sale.
    - Si sí, pregunta 1 ó 2 facturas (por ahora solo 2 con split 50/50).
    - Pide datos fiscales y crea una o dos filas en `invoice` con esos datos.
    """
    header = legacy_order.get(order_id)
    if not header:
        print('Orden no encontrada para facturar:', order_id)
        return
    grand_total = getattr(header, 'grand_total', None) or (header.get('grand_total') if isinstance(header, dict) else 0) or 0

    resp = input('\n¿Quieres factura? (s/n) [n]: ').strip().lower() or 'n'
    if resp != 's':
        print('No se generarán facturas para esta orden.')
        return

    choice = input('¿Una factura o varias? (1 = una, 2 = dos de 50% cada una) [1]: ').strip() or '1'

    # collect billing/fiscal fields
    print('\nIntroduce datos fiscales (ENTER para dejar vacío o usar valores por defecto):')
    default_name = ''
    try:
        default_name = getattr(client_repo.get(getattr(header,'client_id',None)),'full_name',None) or ''
    except Exception:
        default_name = ''
    billing_name = input(f'Nombre / Razón social [{default_name}]: ').strip() or default_name
    rfc = input('RFC (si aplica): ').strip() or None
    regimen_fiscal = input('Régimen fiscal (CFDI): ').strip() or None
    fiscal_postal_code = input('CP del domicilio fiscal: ').strip() or None
    billing_address = input('Dirección (para logística/comprobante interno): ').strip() or None
    uso_cfdi = input('Uso CFDI (si timbras): ').strip() or None
    forma_pago = input('Forma de pago (si timbras): ').strip() or None
    metodo_pago = input('Método de pago (si timbras): ').strip() or None
    currency_code = input('Moneda [MXN]: ').strip() or 'MXN'
    exchange_rate = input('Tipo de cambio (vacío si no aplica): ').strip() or None
    # normalize exchange_rate
    if exchange_rate in (None, ''):
        exchange_rate_val = None
    else:
        try:
            exchange_rate_val = float(exchange_rate)
        except Exception:
            exchange_rate_val = None

    # Insert invoices
    cur = legacy_order.db.cursor()
    def insert_invoice(inv_number: str, notes: str):
        sql = (
            "INSERT INTO invoice (order_id, invoice_number, billing_name, rfc, regimen_fiscal, fiscal_postal_code, billing_address, uso_cfdi, forma_pago, metodo_pago, series, issued_at, due_at, currency_code, exchange_rate, status, notes) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NULL,%s,%s,%s,%s)"
        )
        params = (
            order_id, inv_number, billing_name, rfc, regimen_fiscal, fiscal_postal_code,
            billing_address, uso_cfdi, forma_pago, metodo_pago, 'A', currency_code, exchange_rate_val,
            'emitida', notes
        )
        cur.execute(sql, params)
        if not legacy_order.db.autocommit:
            legacy_order.db.commit()
        try:
            lastid = cur.lastrowid
        except Exception:
            lastid = None
        return lastid

    if choice == '2':
        # Only support 2 invoices 50/50
        total = float(grand_total)
        half = round(total / 2.0, 2)
        inv1 = input(f'Número de factura 1 [INV-{order_id:04d}-1]: ').strip() or f'INV-{order_id:04d}-1'
        inv2 = input(f'Número de factura 2 [INV-{order_id:04d}-2]: ').strip() or f'INV-{order_id:04d}-2'
        notes1 = f'Factura 1/2 - {half:.2f} de total {total:.2f}'
        notes2 = f'Factura 2/2 - {half:.2f} de total {total:.2f}'
        id1 = insert_invoice(inv1, notes1)
        print(f'Factura 1 creada id={id1} ({inv1}) - {notes1}')
        id2 = insert_invoice(inv2, notes2)
        print(f'Factura 2 creada id={id2} ({inv2}) - {notes2}')
    else:
        inv = input(f'Número de factura [INV-{order_id:04d}-1]: ').strip() or f'INV-{order_id:04d}-1'
        total = float(grand_total)
        notes = f'Factura por total {total:.2f}'
        iid = insert_invoice(inv, notes)
        print(f'Factura creada id={iid} ({inv}) - {notes}')
    print('\nFlujo de facturación completado.')


if __name__ == '__main__':
    # Entry point. Edit ACTION to choose behavior or run the script and follow prompts.
    ACTION = 'interactive_catalog'  # options: list, show, create, add_item, add_item_from_product, update_item, delete_item, recalc, demo, interactive_catalog

    if ACTION == 'interactive_catalog':
        interactive_catalog_order_flow()
    elif ACTION == 'interactive':
        # legacy interactive for single client id
        interactive_create_order_for_client(3)
    elif ACTION == 'list':
        rows = list_orders(limit=20)
        for r in rows:
            print('-' * 60)
            pprint(r)
    elif ACTION == 'show':
        oid = 1
        show_order_full(oid)
    elif ACTION == 'create':
        # create an order for client_id 1 (adjust to your DB)
        create_order(1, notes='Creado desde script')
    elif ACTION == 'add_item':
        # add manually (provide snapshot values)
        add_item_manual(1, 1, 'Manual product', 'SKU-M', 9.99, 16.0, quantity=2)
    elif ACTION == 'add_item_from_product':
        add_item_from_product(1, 1, quantity=2)
    elif ACTION == 'update_item':
        update_item(1, 1, {'quantity': 5, 'unit_price': 11.0})
    elif ACTION == 'delete_item':
        delete_item(1, 1)
    elif ACTION == 'recalc':
        recalc_order_totals(1)
    else:
        # demo: create client/product, create order, add item via product snapshot,
        # show order, recalc totals, show again
        print('Demo flow: creating client/product/order/item (IDs will be printed)')
        try:
            # create minimal client/product if repos accept it
            try:
                cid = client_repo.create({'full_name': 'Cliente-Demo'})
            except Exception:
                cid = 1
            try:
                pid = product_repo.create({'name': 'Producto-Demo', 'price': 100.0})
            except Exception:
                pid = 1

            print('Using client_id=', cid, ' product_id=', pid)
            oid = create_order(cid, notes='Demo order')
            if oid:
                add_item_from_product(oid, pid, quantity=2)
                show_order_full(oid)
                recalc_order_totals(oid)
                print('\nAfter recalc:')
                show_order_full(oid)
        except Exception as e:
            print('Demo error:', repr(e))