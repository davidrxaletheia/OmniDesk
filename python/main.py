#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniDesk Admin/Empleado Interactive CLI
---------------------------------------
Prueba integral de la BD OmniDesk desde la perspectiva del admin/empleado.
No cubre autenticación de usuarios finales (lo programarás después).

Requisitos:
  - Python 3.9+
  - mysql-connector-python (o PyMySQL como fallback)

Instalación rápida:
  pip install mysql-connector-python
  # (opcional) pip install PyMySQL

Variables de entorno (o usa argumentos):
  DB_HOST=localhost
  DB_PORT=3306
  DB_USER=root
  DB_PASS=tu_password
  DB_NAME=omnidesk

Ejemplos:
  python omnidesk_admin_cli.py --host localhost --user root --password 123 --db omnidesk
  python omnidesk_admin_cli.py --demo   # ejecuta un flujo de prueba automático

Autor: ChatGPT (OmniDesk helper)
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from typing import Optional, Any, List, Tuple

##############################
# Database configuration (ENV)
##############################
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "omnidesk_dashboard")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

##############################
# Conexión directa (sin pool)
##############################
def get_connection():
    import mysql.connector  # aseguramos que esté instalado si se usa --direct
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        autocommit=False,   # pon True si quieres commits automáticos
    )


# -------------------------
# Conexión a MySQL (connector o PyMySQL)
# -------------------------
class DB:
    def __init__(self, host, port, user, password, db, use_direct: bool=False):
        self.use_direct = use_direct
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.driver = None
        self.conn = None
        self._connect()

    def _connect(self):
        if self.use_direct:
            try:
                self.conn = get_connection()
                self.driver = 'mysql-connector-python'
                return
            except Exception as e:
                print('ERROR usando conexión directa get_connection():', e)
                print('Cayendo a método automático...')
        try:
            import mysql.connector as _driver
            self.driver = 'mysql-connector-python'
            self.conn = _driver.connect(
                host=self.host, port=self.port, user=self.user,
                password=self.password, database=self.db, autocommit=False
            )
        except Exception as e1:
            try:
                import pymysql as _driver
                self.driver = 'PyMySQL'
                self.conn = _driver.connect(
                    host=self.host, port=int(self.port), user=self.user,
                    password=self.password, database=self.db, autocommit=False,
                    cursorclass=_driver.cursors.Cursor
                )
            except Exception as e2:
                print("ERROR: no se pudo conectar con mysql-connector-python ni PyMySQL.")
                print("Instala uno: pip install mysql-connector-python  (o)  pip install PyMySQL")
                print("Detalle:", e1, "|", e2)
                sys.exit(1)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        try:
            self.conn.close()
        except:
            pass


# -------------------------
# Utilidades CLI
# -------------------------
def hr(title: str = "", char: str = "─", width: int = 70):
    bar = char * width
    return f"\n{bar}\n{title}\n{bar}" if title else f"\n{bar}"

def ask(prompt: str) -> str:
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nCancelado.")
        return ""

def pause():
    input("\nPresiona Enter para continuar...")

def print_rows(rows: List[Tuple], headers: Optional[List[str]] = None, limit: int = 20):
    if headers:
        print(" | ".join(headers))
        print("-" * 80)
    shown = 0
    for r in rows:
        print(" | ".join([str(x) if x is not None else "" for x in r]))
        shown += 1
        if shown >= limit:
            if len(rows) > limit:
                print(f"... ({len(rows)-limit} más)")
            break

def choose_from_query(db: DB, sql: str, params: Optional[tuple]=None, show_cols: int=2, label: str="Seleccione ID"):
    cur = db.cursor()
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    if not rows:
        print("No hay resultados.")
        return None
    for r in rows:
        shown = " | ".join([str(x) for x in r[:show_cols]])
        print(f"  {r[0]:>4} -> {shown}")
    while True:
        s = ask(f"{label}: ")
        if not s:
            return None
        try:
            sid = int(s)
            return sid
        except:
            print("Ingrese un número válido.")

def exec_dml(db: DB, sql: str, params: tuple):
    cur = db.cursor()
    try:
        cur.execute(sql, params)
        db.commit()
        return cur.lastrowid if hasattr(cur, "lastrowid") else None
    except Exception as e:
        db.rollback()
        print("ERROR en DML:", e)
        return None

def query_all(db: DB, sql: str, params: Optional[tuple] = None) -> List[Tuple]:
    cur = db.cursor()
    cur.execute(sql, params or ())
    return cur.fetchall()

# -------------------------
# Módulos funcionales
# -------------------------
# CLIENTES
def clientes_listar(db: DB):
    print(hr("CLIENTES - Listado"))
    rows = query_all(db, "SELECT client_id, full_name, email, phone, client_type, status, registered_at FROM client ORDER BY client_id DESC LIMIT 30")
    print_rows(rows, headers=["ID","Nombre","Email","Tel","Tipo","Status","Registrado"])

def clientes_buscar(db: DB):
    print(hr("CLIENTES - Buscar"))
    q = ask("Texto a buscar (en nombre/email): ")
    rows = query_all(db, "SELECT client_id, full_name, email, phone FROM client WHERE full_name LIKE %s OR email LIKE %s ORDER BY full_name LIMIT 30", (f"%{q}%", f"%{q}%"))
    print_rows(rows, headers=["ID","Nombre","Email","Tel"])

def clientes_crear(db: DB):
    print(hr("CLIENTES - Crear"))
    name = ask("Nombre/Razón social: ")
    phone = ask("Teléfono: ")
    email = ask("Email: ")
    client_type = ask("Tipo (normal/premium) [normal]: ") or "normal"
    sql = """INSERT INTO client (full_name, phone, email, client_type, status, registered_at)
             VALUES (%s,%s,%s,%s,'active',NOW())"""
    rid = exec_dml(db, sql, (name, phone, email, client_type))
    if rid:
        print(f"Cliente creado con ID {rid}")

# PRODUCTOS
def productos_listar(db: DB):
    print(hr("PRODUCTOS - Listado"))
    rows = query_all(db, "SELECT product_id, sku, name, price, stock, status FROM product ORDER BY product_id DESC LIMIT 50")
    print_rows(rows, headers=["ID","SKU","Nombre","Precio","Stock","Status"])

def productos_buscar(db: DB):
    print(hr("PRODUCTOS - Buscar"))
    q = ask("Texto a buscar (en nombre/sku): ")
    rows = query_all(db, "SELECT product_id, sku, name, price, stock FROM product WHERE name LIKE %s OR sku LIKE %s ORDER BY name LIMIT 50", (f"%{q}%", f"%{q}%"))
    print_rows(rows, headers=["ID","SKU","Nombre","Precio","Stock"])

# CATÁLOGOS
def catalogos_listar(db: DB):
    print(hr("CATÁLOGOS - Activos"))
    rows = query_all(db, "SELECT catalog_id, name, discount_percentage, start_date, end_date, visible_to, active FROM catalog ORDER BY catalog_id DESC")
    print_rows(rows, headers=["ID","Nombre","%Desc","Inicio","Fin","Visible","Activo"], limit=100)

def catalogo_productos(db: DB):
    print(hr("CATÁLOGOS - Productos y precio efectivo"))
    cid = choose_from_query(db, "SELECT catalog_id, name, discount_percentage FROM catalog ORDER BY catalog_id", show_cols=3, label="ID de catálogo")
    if not cid:
        return
    rows = query_all(db, """
        SELECT v.product_id, v.product_name, v.base_price, v.discount_percentage, v.special_price, v.effective_price
        FROM v_catalog_effective_price v
        WHERE v.catalog_id = %s
        ORDER BY v.product_name
    """, (cid,))
    print_rows(rows, headers=["ProdID","Producto","Precio Base","%Desc","Especial","Efectivo"], limit=200)

# PEDIDOS
def pedidos_crear(db: DB):
    print(hr("PEDIDOS - Crear"))
    cid = choose_from_query(db, "SELECT client_id, full_name, email FROM client ORDER BY full_name LIMIT 50", show_cols=3, label="ID de cliente")
    if not cid:
        return
    created_by = choose_from_query(db, "SELECT user_id, full_name, username FROM app_user ORDER BY user_id LIMIT 50", show_cols=3, label="Creado por (user_id)")
    notes = ask("Notas: ") or "Pedido generado desde CLI"
    rid = exec_dml(db, "INSERT INTO customer_order (client_id, created_at, created_by, notes) VALUES (%s,NOW(),%s,%s)", (cid, created_by, notes))
    if not rid:
        return
    order_id = rid
    print(f"Pedido creado con ID {order_id}")
    while True:
        add = (ask("¿Agregar ítem? (s/n): ") or "n").lower()
        if add != "s":
            break
        pid = choose_from_query(db, "SELECT product_id, sku, name, price FROM product ORDER BY name LIMIT 50", show_cols=4, label="ID de producto")
        if not pid:
            break
        qty = int(ask("Cantidad: ") or "1")
        # obtener snapshot
        row = query_all(db, "SELECT sku, name, price FROM product WHERE product_id = %s", (pid,))
        if not row:
            print("Producto no encontrado.")
            continue
        sku, name, price = row[0]
        tax_rate = 16.00
        exec_dml(db, """INSERT INTO order_item
                        (order_id, product_id, quantity, product_name, sku, unit_price, discount_pct, discount_amount, tax_rate)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                 (order_id, pid, qty, name, sku, price, 0, None, tax_rate))
        print("Ítem agregado.")
    # ver totales
    rows = query_all(db, "SELECT v_subtotal, v_discount_total, v_tax_total, v_items_total FROM v_order_totals WHERE order_id = %s", (order_id,))
    if rows:
        v_sub, v_dis, v_tax, v_tot = rows[0]
        print(f"Totales (desde vista): Subtotal={v_sub} Desc={v_dis} IVA={v_tax} Total={v_tot}")
    else:
        print("No hay ítems aún.")
    pause()

def pedidos_facturar_y_avanzar(db: DB):
    print(hr("PEDIDOS - Facturar y cambiar estado"))
    oid = choose_from_query(db, "SELECT order_id, client_id, status, payment_status FROM customer_order ORDER BY order_id DESC LIMIT 50", show_cols=4, label="ID de pedido")
    if not oid:
        return
    # crear al menos una factura
    inv_no = ask("Número de factura (e.g., INV-TEST-0001): ") or f"INV-CLI-{oid:04d}"
    series = ask("Serie [A/B/C] (default A): ") or "A"
    exec_dml(db, "INSERT INTO invoice (order_id, invoice_number, series, issued_at, currency_code, status, notes) VALUES (%s,%s,%s,NOW(),'MXN','emitida','Factura creada desde CLI')", (oid, inv_no, series))
    print("Factura creada.")
    # intentar avanzar estado (requiere ≥ 1 factura)
    new_status = ask("Nuevo estado (confirmado/preparando/enviado/entregado) [confirmado]: ") or "confirmado"
    pay_status = ask("Estado de pago (pendiente/pagado) [pendiente]: ") or "pendiente"
    cur = db.cursor()
    try:
        cur.execute("UPDATE customer_order SET status=%s, payment_status=%s WHERE order_id=%s", (new_status, pay_status, oid))
        db.commit()
        print("Pedido actualizado.")
    except Exception as e:
        db.rollback()
        print("ERROR al actualizar estado (¿falta factura?):", e)
    pause()

def pedidos_ver(db: DB):
    print(hr("PEDIDOS - Ver"))
    oid = choose_from_query(db, "SELECT order_id, client_id, status, payment_status, created_at FROM customer_order ORDER BY order_id DESC LIMIT 50", show_cols=5, label="ID de pedido")
    if not oid:
        return
    head = query_all(db, """SELECT c.order_id, cl.full_name, c.status, c.payment_status, c.subtotal, c.discount_total, c.tax_total, c.shipping_total, c.grand_total, c.created_at
                             FROM customer_order c
                             JOIN client cl ON cl.client_id = c.client_id
                             WHERE c.order_id=%s""", (oid,))
    items = query_all(db, "SELECT product_name, sku, quantity, unit_price, line_total FROM order_item WHERE order_id=%s", (oid,))
    invs = query_all(db, "SELECT invoice_number, status, issued_at FROM invoice WHERE order_id=%s", (oid,))
    print_rows(head, headers=["ID","Cliente","Estatus","Pago","Subt","Desc","IVA","Envio","Total","Creado"], limit=5)
    print_rows(items, headers=["Producto","SKU","Cant","Precio","Total"], limit=100)
    print_rows(invs, headers=["Factura","Estatus","Fecha"], limit=20)
    pause()

# TICKETS
def tickets_crear(db: DB):
    print(hr("TICKETS - Crear"))
    cid = choose_from_query(db, "SELECT client_id, full_name FROM client ORDER BY full_name LIMIT 50", show_cols=2, label="ID de cliente")
    if not cid:
        return
    subject = ask("Asunto: ")
    description = ask("Descripción: ")
    priority = ask("Prioridad (alta/media/baja) [media]: ") or "media"
    assigned_to = choose_from_query(db, "SELECT user_id, full_name FROM app_user ORDER BY user_id LIMIT 50", show_cols=2, label="Asignar a (user_id)")
    rid = exec_dml(db, """INSERT INTO ticket (client_id, subject, description, priority, status, created_at, due_at, assigned_to)
                          VALUES (%s,%s,%s,%s,'abierto',NOW(), DATE_ADD(NOW(), INTERVAL 3 DAY), %s)""",
                   (cid, subject, description, priority, assigned_to))
    if rid:
        print(f"Ticket creado con ID {rid}")
    pause()

def tickets_cambiar_estado(db: DB):
    print(hr("TICKETS - Cambiar estado"))
    tid = choose_from_query(db, "SELECT ticket_id, subject, status FROM ticket ORDER BY ticket_id DESC LIMIT 50", show_cols=3, label="ID de ticket")
    if not tid:
        return
    new_status = ask("Nuevo estado (abierto/en_progreso/cerrado) [en_progreso]: ") or "en_progreso"
    try:
        exec_dml(db, "UPDATE ticket SET status=%s WHERE ticket_id=%s", (new_status, tid))
        print("Ticket actualizado (si fue cerrado, resolved_at se estableció por trigger).")
    except Exception as e:
        print("ERROR:", e)
    pause()

def tickets_listar(db: DB):
    print(hr("TICKETS - Listar"))
    rows = query_all(db, "SELECT ticket_id, subject, priority, status, created_at, due_at, resolved_at FROM ticket ORDER BY ticket_id DESC LIMIT 50")
    print_rows(rows, headers=["ID","Asunto","Prio","Status","Creado","Due","Resuelto"])

# CALENDARIO
def calendario_crear_evento(db: DB):
    print(hr("CALENDARIO - Crear evento"))
    title = ask("Título: ")
    description = ask("Descripción: ")
    start = ask("Inicio (YYYY-MM-DD HH:MM) [ahora]: ") or datetime.now().strftime("%Y-%m-%d %H:%M")
    end = ask("Fin (YYYY-MM-DD HH:MM) [+1h]: ") or (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    created_by = choose_from_query(db, "SELECT user_id, full_name FROM app_user ORDER BY user_id LIMIT 50", show_cols=2, label="Creado por (user_id)")
    tid = ask("Ticket ID (opcional): ")
    ticket_id = int(tid) if tid.strip().isdigit() else None
    rid = exec_dml(db, "INSERT INTO calendar_event (title, description, start_time, end_time, created_by, ticket_id) VALUES (%s,%s,%s,%s,%s,%s)",
                   (title, description, start, end, created_by, ticket_id))
    if rid:
        print(f"Evento creado con ID {rid}")
    pause()

def calendario_listar(db: DB):
    print(hr("CALENDARIO - Próximos 10"))
    rows = query_all(db, "SELECT event_id, title, start_time, end_time, created_by, ticket_id FROM calendar_event ORDER BY start_time DESC LIMIT 10")
    print_rows(rows, headers=["ID","Título","Inicio","Fin","Creador","Ticket"], limit=10)

# ALERTAS
def alertas_crear(db: DB):
    print(hr("ALERTAS - Crear"))
    when = ask("Fecha/hora (YYYY-MM-DD HH:MM) [+2h]: ") or (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    msg = ask("Mensaje (<=255): ")
    kind = ask("Tipo (ticket/event/incident) [incident]: ") or "incident"
    ttxt = ask("Ticket ID (opcional): ")
    etxt = ask("Event ID (opcional): ")
    ticket_id = int(ttxt) if ttxt.strip().isdigit() else None
    event_id  = int(etxt) if etxt.strip().isdigit() else None
    created_by = choose_from_query(db, "SELECT user_id, full_name FROM app_user ORDER BY user_id LIMIT 50", show_cols=2, label="Creado por (user_id)")
    rid = exec_dml(db, "INSERT INTO alert (alert_time, message, kind, ticket_id, event_id, sent, created_by, created_at) VALUES (%s,%s,%s,%s,%s,0,%s,NOW())",
                   (when, msg, kind, ticket_id, event_id, created_by))
    if rid:
        print(f"Alerta creada con ID {rid}")
    pause()

def alertas_pendientes(db: DB):
    print(hr("ALERTAS - Pendientes"))
    rows = query_all(db, "SELECT alert_id, alert_time, kind, message, ticket_id, event_id FROM alert WHERE sent=0 ORDER BY alert_time ASC LIMIT 20")
    print_rows(rows, headers=["ID","Cuando","Tipo","Mensaje","Ticket","Evento"], limit=20)
    mark = (ask("¿Marcar alguna como enviada? (id o Enter): ") or "").strip()
    if mark.isdigit():
        exec_dml(db, "UPDATE alert SET sent=1 WHERE alert_id=%s", (int(mark),))
        print("Marcada como enviada.")

# CONVERSACIONES Y MENSAJES (simple)
def conversaciones_nueva(db: DB):
    print(hr("CONVERSACIONES - Nueva"))
    cid = choose_from_query(db, "SELECT client_id, full_name FROM client ORDER BY full_name LIMIT 50", show_cols=2, label="ID de cliente")
    if not cid:
        return
    channel = ask("Canal (web/telegram/whatsapp/email/other) [web]: ") or "web"
    external_id = ask("external_chat_id (opcional): ")
    rid = exec_dml(db, "INSERT INTO conversation (client_id, channel, external_chat_id, active, handled_by_bot, created_at) VALUES (%s,%s,%s,1,1,NOW())",
                   (cid, channel, external_id if external_id else None))
    if rid:
        print(f"Conversación creada con ID {rid}")
    pause()

def mensajes_enviar(db: DB):
    print(hr("MENSAJES - Enviar"))
    conv = choose_from_query(db, "SELECT conversation_id, client_id, channel, last_message_at FROM conversation ORDER BY conversation_id DESC LIMIT 50", show_cols=4, label="ID de conversación")
    if not conv:
        return
    sender = ask("Remitente (client/user/bot) [user]: ") or "user"
    content = ask("Mensaje: ")
    ext_id = ask("external_message_id (opcional): ")
    exec_dml(db, "INSERT INTO message (conversation_id, sender, content, external_message_id, created_at) VALUES (%s,%s,%s,%s,NOW())",
             (conv, sender, content, ext_id if ext_id else None))
    print("Mensaje enviado.")
    pause()

def mensajes_listar(db: DB):
    print(hr("MENSAJES - Últimos"))
    conv = choose_from_query(db, "SELECT conversation_id, client_id, channel, last_message_at FROM conversation ORDER BY conversation_id DESC LIMIT 50", show_cols=4, label="ID de conversación")
    if not conv:
        return
    rows = query_all(db, "SELECT message_id, sender, content, created_at FROM message WHERE conversation_id=%s ORDER BY created_at DESC LIMIT 20", (conv,))
    print_rows(rows, headers=["ID","Sender","Contenido","Fecha"], limit=20)
    pause()

# -------------------------
# DEMO AUTOMÁTICO (end-to-end)
# -------------------------
def run_demo(db: DB):
    print(hr("DEMO AUTOMÁTICO - Inicio"))
    # 1) Crear un pedido con 2 ítems, facturar y avanzar
    print("1) Crear pedido rápido")
    client_id = query_all(db, "SELECT client_id FROM client ORDER BY RAND() LIMIT 1")[0][0]
    user_id = query_all(db, "SELECT user_id FROM app_user ORDER BY RAND() LIMIT 1")[0][0]
    rid = exec_dml(db, "INSERT INTO customer_order (client_id, created_at, created_by, notes) VALUES (%s,NOW(),%s,'Pedido DEMO')",
                   (client_id, user_id))
    if not rid:
        return
    oid = rid
    # 2 productos al azar
    pids = [r[0] for r in query_all(db, "SELECT product_id FROM product ORDER BY RAND() LIMIT 2")]
    for pid in pids:
        sku, name, price = query_all(db, "SELECT sku, name, price FROM product WHERE product_id=%s", (pid,))[0]
        exec_dml(db, """INSERT INTO order_item (order_id, product_id, quantity, product_name, sku, unit_price, discount_pct, discount_amount, tax_rate)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                 (oid, pid, 1, name, sku, price, 0, None, 16.00))
    # totales desde vista
    v = query_all(db, "SELECT v_subtotal, v_discount_total, v_tax_total, v_items_total FROM v_order_totals WHERE order_id=%s", (oid,))
    if v:
        print(f"   Totales DEMO: {v[0]}")
    # factura
    exec_dml(db, "INSERT INTO invoice (order_id, invoice_number, series, issued_at, currency_code, status, notes) VALUES (%s,%s,%s,NOW(),'MXN','emitida','Factura DEMO')",
             (oid, f"INV-DEMO-{oid:04d}", "A"))
    # avanzar estado
    exec_dml(db, "UPDATE customer_order SET status='confirmado', payment_status='pendiente' WHERE order_id=%s", (oid,))
    print(f"   Pedido DEMO {oid} creado y confirmado.")

    # 2) Crear ticket y evento asociado
    print("2) Crear ticket + evento")
    tid = exec_dml(db, """INSERT INTO ticket (client_id, subject, description, priority, status, created_at, due_at, assigned_to)
                          VALUES (%s,'Ticket DEMO','Prueba de flujo CLI','media','abierto',NOW(), DATE_ADD(NOW(), INTERVAL 2 DAY), %s)""",
                   (client_id, user_id))
    if tid:
        exec_dml(db, "INSERT INTO calendar_event (title, description, start_time, end_time, created_by, ticket_id) VALUES ('Evento DEMO','Seguimiento DEMO', NOW(), DATE_ADD(NOW(), INTERVAL 1 HOUR), %s, %s)",
                 (user_id, tid))
        print(f"   Ticket DEMO {tid} y evento asociado creados.")

    # 3) Conversación + mensaje
    print("3) Conversación y mensaje DEMO")
    conv = exec_dml(db, "INSERT INTO conversation (client_id, channel, external_chat_id, active, handled_by_bot, created_at) VALUES (%s,'web',NULL,1,1,NOW())",
                    (client_id,))
    if conv:
        exec_dml(db, "INSERT INTO message (conversation_id, sender, content, external_message_id, created_at) VALUES (%s,'user','Hola desde DEMO',NULL,NOW())",
                 (conv,))
        print(f"   Conversación {conv} con mensaje enviado.")

    # 4) Alerta rápida
    print("4) Alerta programada DEMO")
    exec_dml(db, "INSERT INTO alert (alert_time, message, kind, ticket_id, event_id, sent, created_by, created_at) VALUES (DATE_ADD(NOW(), INTERVAL 1 HOUR),'Recordatorio DEMO','ticket',%s,NULL,0,%s,NOW())",
             (tid, user_id))
    print("DEMO finalizada.")
    pause()

# -------------------------
# Menú principal
# -------------------------
def show_menu():
    print(hr("OmniDesk - Admin/Empleado CLI"))
    print("1) Clientes: Listar")
    print("2) Clientes: Buscar")
    print("3) Clientes: Crear")
    print("4) Productos: Listar")
    print("5) Productos: Buscar")
    print("6) Catálogos: Listar")
    print("7) Catálogo: Ver productos y precio efectivo")
    print("8) Pedidos: Crear + ítems")
    print("9) Pedidos: Facturar y cambiar estado")
    print("10) Pedidos: Ver detalle")
    print("11) Tickets: Crear")
    print("12) Tickets: Cambiar estado")
    print("13) Tickets: Listar")
    print("14) Calendario: Crear evento")
    print("15) Calendario: Listar próximos")
    print("16) Alertas: Crear")
    print("17) Alertas: Ver pendientes / Marcar enviada")
    print("18) Conversaciones: Nueva")
    print("19) Mensajes: Enviar a conversación")
    print("20) Mensajes: Listar por conversación")
    print("D) DEMO automático end-to-end")
    print("Q) Salir")

def main():
    parser = argparse.ArgumentParser(description="OmniDesk Admin/Empleado CLI")
    parser.add_argument("--host", default=os.environ.get("DB_HOST","localhost"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("DB_PORT","3306")))
    parser.add_argument("--user", default=os.environ.get("DB_USER","root"))
    parser.add_argument("--password", default=os.environ.get("DB_PASS",""))
    parser.add_argument("--db", default=os.environ.get("DB_NAME","omnidesk"))
    parser.add_argument("--demo", action="store_true", help="Ejecutar demo end-to-end y salir")
    parser.add_argument("--direct", action="store_true", help="Usar get_connection() con variables de entorno (MYSQL_*)")
    args = parser.parse_args()

    db = DB(args.host, args.port, args.user, args.password, args.db, use_direct=args.direct)

    try:
        if args.demo:
            run_demo(db)
            return
        while True:
            show_menu()
            op = (ask("\nOpción: ") or "").strip().lower()
            if op == "1":
                clientes_listar(db)
            elif op == "2":
                clientes_buscar(db)
            elif op == "3":
                clientes_crear(db)
            elif op == "4":
                productos_listar(db)
            elif op == "5":
                productos_buscar(db)
            elif op == "6":
                catalogos_listar(db)
            elif op == "7":
                catalogo_productos(db)
            elif op == "8":
                pedidos_crear(db)
            elif op == "9":
                pedidos_facturar_y_avanzar(db)
            elif op == "10":
                pedidos_ver(db)
            elif op == "11":
                tickets_crear(db)
            elif op == "12":
                tickets_cambiar_estado(db)
            elif op == "13":
                tickets_listar(db)
            elif op == "14":
                calendario_crear_evento(db)
            elif op == "15":
                calendario_listar(db)
            elif op == "16":
                alertas_crear(db)
            elif op == "17":
                alertas_pendientes(db)
            elif op == "18":
                conversaciones_nueva(db)
            elif op == "19":
                mensajes_enviar(db)
            elif op == "20":
                mensajes_listar(db)
            elif op == "d":
                run_demo(db)
            elif op == "q":
                break
            else:
                print("Opción no válida.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
