# -*- coding: utf-8 -*-
"""
main.py
-------
Ejecutable simple que usa los **Modelos Pydantic (BaseModel)** y **Repos CRUD**
del paquete `Classes` que te compartí.

Requisitos:
  pip install pydantic mysql-connector-python

Variables de entorno MySQL:
  MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD

Uso:
  python main.py --help
  python main.py demo             # flujo completo
  python main.py list clients     # listar clientes
  python main.py list products    # listar productos
  python main.py order create     # crear pedido rápido
  python main.py chat create      # conversación+mensajes
  python main.py ticket create    # crear ticket y cerrarlo

Coloca la carpeta `Classes` (la del zip) junto a este archivo main.py.
"""

import os
import sys
import argparse
from decimal import Decimal
from datetime import datetime, timedelta

# Asegura que podamos importar 'Classes' si está junto a main.py
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
if CUR_DIR not in sys.path:
    sys.path.append(CUR_DIR)

try:
    from Classes import DB
    from Classes.models import (
        ClientModel, ProductModel, CustomerOrderModel, OrderItemModel, InvoiceModel,
        ConversationModel, MessageModel, TicketModel, CalendarEventModel, AlertModel
    )
    from Classes.repos import (
        ClientRepo, ProductRepo, CustomerOrderRepo, OrderItemRepo, InvoiceRepo,
        ConversationRepo, MessageRepo, TicketRepo, CalendarEventRepo, AlertRepo
    )
except Exception as e:
    print("No se pudo importar el paquete 'Classes'. Asegúrate de descomprimir el ZIP junto a main.py.")
    raise

# ------------------------------------------------------------------
# Helpers de impresión
# ------------------------------------------------------------------
def print_header(title: str):
    print("\n" + "="*80)
    print(title)
    print("="*80)

def short(s, n=60):
    s = str(s) if s is not None else ""
    return (s[:n-3] + "...") if len(s) > n else s

# ------------------------------------------------------------------
# Operaciones de lista
# ------------------------------------------------------------------
def list_clients(limit: int = 10):
    with DB() as db:
        repo = ClientRepo(db)
        clients = repo.list(limit=limit, order_by="registered_at", desc=True)
        print_header(f"Clientes (limit={limit})")
        for c in clients:
            print(f"{c.client_id:>4} | {short(c.full_name,40):40} | {c.client_type:7} | {c.email or ''}")

def list_products(limit: int = 10):
    with DB() as db:
        repo = ProductRepo(db)
        products = repo.list(limit=limit, order_by="product_id", desc=True)
        print_header(f"Productos (limit={limit})")
        for p in products:
            print(f"{p.product_id:>4} | {short(p.sku,12):12} | {short(p.name,40):40} | ${p.price} | stock={p.stock}")

def list_orders(limit: int = 10):
    with DB() as db:
        repo = CustomerOrderRepo(db)
        orders = repo.list(limit=limit, order_by="created_at", desc=True)
        print_header(f"Pedidos (limit={limit})")
        for o in orders:
            print(f"{o.order_id:>4} | cliente={o.client_id:<4} | {o.status:12} | pago={o.payment_status:9} | {o.created_at} | total={o.grand_total}")

# ------------------------------------------------------------------
# Flujo: crear pedido con items e invoice
# ------------------------------------------------------------------
def create_order_flow(search_product: str = "Router", qty: int = 1):
    with DB() as db:
        client_repo = ClientRepo(db)
        prod_repo = ProductRepo(db)
        order_repo = CustomerOrderRepo(db)
        item_repo = OrderItemRepo(db)
        invoice_repo = InvoiceRepo(db)

        # Tomar o crear cliente rápido
        clients = client_repo.search("", limit=1)
        if clients:
            client = clients[0]
        else:
            cm = ClientModel(full_name="Cliente CLI", email="cli@example.com", client_type="normal")
            client_id = client_repo.create(cm.dict(exclude_none=True, exclude_unset=True))
            client = client_repo.get(client_id)

        # Producto por texto
        prods = prod_repo.search(search_product, limit=1)
        if not prods:
            raise RuntimeError(f"No encontré productos que coincidan con '{search_product}'")

        prod = prods[0]

        # Crear pedido
        order_id = order_repo.create({"client_id": client.client_id, "created_at": "NOW()", "notes": "Pedido creado desde main.py"})
        print_header(f"Pedido creado: {order_id} para cliente {client.client_id} - {client.full_name}")

        # Agregar ítem (snapshot de datos del producto)
        item_repo.add_item({
            "order_id": order_id,
            "product_id": prod.product_id,
            "quantity": qty,
            "product_name": prod.name,
            "sku": prod.sku,
            "unit_price": Decimal(prod.price),
            "tax_rate": Decimal("16.00")
        })
        print(f" + Item agregado: {prod.name} x{qty}")

        # Crear factura (emitida ahora)
        invoice_id = invoice_repo.create({
            "order_id": order_id,
            "invoice_number": f"INV-MAIN-{order_id:04d}",
            "series": "A",
            "issued_at": "NOW()",
            "currency_code": "MXN",
            "status": "emitida",
            "notes": "Factura generada desde main.py"
        })
        print(f" + Factura creada: id={invoice_id}")

        # Avanzar estado a confirmado/pagado
        order_repo.update(order_id, {"status": "confirmado", "payment_status": "pagado"})
        print(" + Pedido actualizado: confirmado / pagado")

# ------------------------------------------------------------------
# Flujo: conversación y mensajes
# ------------------------------------------------------------------
def chat_flow():
    with DB() as db:
        conv_repo = ConversationRepo(db)
        msg_repo = MessageRepo(db)
        client_repo = ClientRepo(db)

        cli = client_repo.search("", limit=1)[0]
        conv_id = conv_repo.create({
            "client_id": cli.client_id,
            "channel": "web",
            "active": True,
            "handled_by_bot": True
        })
        msg_repo.create({"conversation_id": conv_id, "sender": "client", "content": "Hola, ¿tienen stock del router?"})
        msg_repo.create({"conversation_id": conv_id, "sender": "user",   "content": "Sí, hay disponibilidad."})

        print_header(f"Conversación {conv_id} creada con cliente {cli.client_id}")
        for m in msg_repo.by_conversation(conv_id, limit=10):
            print(f"[{m.created_at}] {m.sender}: {m.content}")

# ------------------------------------------------------------------
# Flujo: tickets, calendario y alertas
# ------------------------------------------------------------------
def support_flow():
    from random import randint
    with DB() as db:
        ticket_repo = TicketRepo(db)
        cal_repo = CalendarEventRepo(db)
        alert_repo = AlertRepo(db)
        client_repo = ClientRepo(db)

        cli = client_repo.search("", limit=1)[0]
        # Crear ticket
        tid = ticket_repo.create({
            "client_id": cli.client_id,
            "subject": "Intermitencia Wi-Fi",
            "description": "Cortes frecuentes en horas pico",
            "priority": "alta",
            "status": "abierto",
            "created_at": "NOW()",
            "due_at": "DATE_ADD(NOW(), INTERVAL 2 DAY)",
            "assigned_to": randint(1, 3)
        })
        print_header(f"Ticket {tid} creado para cliente {cli.client_id}")

        # Crear evento de calendario asociado
        start = datetime.now() + timedelta(hours=2)
        end = start + timedelta(hours=1)
        eid = cal_repo.create({
            "title": "Visita técnica",
            "description": "Optimización APs y canales",
            "start_time": start,
            "end_time": end,
            "created_by": 1,
            "ticket_id": tid
        })
        print(f" + Evento calendario {eid} creado para ticket {tid}")

        # Alerta del evento
        alert_repo.create({
            "alert_time": start - timedelta(minutes=30),
            "message": "Recordatorio: visita técnica en 30min",
            "kind": "event",
            "event_id": eid,
            "sent": 0,
            "created_by": 1,
            "created_at": datetime.now()
        })
        print(" + Alerta programada")

        # Cerrar ticket (tu trigger debería poner resolved_at)
        ticket_repo.update(tid, {"status": "cerrado"})
        t = ticket_repo.get(tid)
        print(f" + Ticket cerrado. resolved_at={t.resolved_at}")

# ------------------------------------------------------------------
# DEMO end-to-end
# ------------------------------------------------------------------
def run_demo():
    list_clients(5)
    list_products(5)
    create_order_flow(search_product="Impresora", qty=1)
    chat_flow()
    support_flow()
    list_orders(5)
    print_header("DEMO OK")

# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="OmniDesk main.py (Modelos Pydantic + Repos CRUD)")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("demo", help="Ejecuta un flujo completo de demo")

    p_list = sub.add_parser("list", help="Listados rápidos")
    p_list.add_argument("what", choices=["clients","products","orders"], help="Qué listar")
    p_list.add_argument("--limit", type=int, default=10)

    p_order = sub.add_parser("order", help="Operaciones de pedido")
    p_order_sub = p_order.add_subparsers(dest="action")
    p_order_create = p_order_sub.add_parser("create", help="Crear pedido rápido")
    p_order_create.add_argument("--q", default="Router", help="Texto de producto a buscar")
    p_order_create.add_argument("--qty", type=int, default=1)

    p_chat = sub.add_parser("chat", help="Conversaciones")
    p_chat.add_subparsers(dest="action").add_parser("create", help="Crear conversación y mensajes")

    p_ticket = sub.add_parser("ticket", help="Tickets/Soporte")
    p_ticket.add_subparsers(dest="action").add_parser("create", help="Crear ticket, evento y alerta (y cerrar ticket)")

    args = parser.parse_args()

    if args.cmd == "demo":
        run_demo()
    elif args.cmd == "list":
        if args.what == "clients":
            list_clients(args.limit)
        elif args.what == "products":
            list_products(args.limit)
        elif args.what == "orders":
            list_orders(args.limit)
    elif args.cmd == "order" and args.action == "create":
        create_order_flow(search_product=args.q, qty=args.qty)
    elif args.cmd == "chat" and args.action == "create":
        chat_flow()
    elif args.cmd == "ticket" and args.action == "create":
        support_flow()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
