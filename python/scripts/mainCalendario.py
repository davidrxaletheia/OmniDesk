#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive helper for tickets, calendar events and alerts.

Usage: run the script and follow the menu prompts.

This file uses the legacy `Classes` DB and repos (TicketRepo, CalendarEventRepo, AlertRepo)
so it works with the project's DB configuration (.env).
"""
import sys
import os
from pprint import pprint
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.Classes.db import DB
from python.Classes.repos.ticket_repo import TicketRepo
from python.Classes.repos.calendar_repo import CalendarEventRepo
from python.Classes.repos.alert_repo import AlertRepo
from python.Classes.repos.client_repo import ClientRepo
from python.Classes.repos.app_user_repo import AppUserRepo
from getpass import getpass
import bcrypt
from types import SimpleNamespace
import calendar


# current authenticated user (dict with user_id, full_name, username, role)
CURRENT_USER = None


def authenticate_user():
    """Interactive login: prompt for username/email and password and validate.

    Sets global CURRENT_USER to the authenticated AppUserModel or returns None
    if the user cancels (empty identifier).
    """
    global CURRENT_USER
    with DB() as db:
        repo = AppUserRepo(db)
        cur = db.cursor()
        # fetch minimal list for display without instantiating AppUserModel
        cur.execute("SELECT user_id, full_name, username, role FROM app_user ORDER BY user_id LIMIT 100")
        rows = cur.fetchall()
        if not rows:
            print('No hay usuarios en la base de datos. Crea uno primero.')
            return None

        print(hr('INICIAR SESIÓN'))
        print('Usa tu nombre de usuario o email. Deja vacío para cancelar.')
        print('\nUsuarios (id -> username | full_name | role):')
        for r in rows:
            print(f"({r[0]}) {r[2]} | {r[1]} | {r[3]}")

        while True:
            identifier = input('Usuario o email: ').strip()
            if not identifier:
                return None
            password = getpass('Contraseña: ')

            # fetch full row by username or email using raw SQL to avoid model validation
            cur = db.cursor()
            cur.execute("SELECT * FROM app_user WHERE username=%s LIMIT 1", (identifier,))
            row = cur.fetchone()
            if not row and '@' in identifier:
                cur.execute("SELECT * FROM app_user WHERE email=%s LIMIT 1", (identifier,))
                row = cur.fetchone()

            if not row:
                print('Usuario no encontrado. Intenta de nuevo.')
                continue

            cols = [d[0] for d in cur.description]
            data = {cols[i]: row[i] for i in range(len(cols))}
            stored_hash = (data.get('password_hash') or '').encode('utf-8')
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    # success: update last_login_at via repo
                    try:
                        repo.update(data.get('user_id'), {'last_login_at': datetime.utcnow()})
                    except Exception:
                        pass
                    # build a lightweight CURRENT_USER object (avoid model validation)
                    CURRENT_USER = SimpleNamespace(user_id=data.get('user_id'), full_name=data.get('full_name'), username=data.get('username'), role=data.get('role'))
                    print(f"Autenticado como {CURRENT_USER.full_name} (id={CURRENT_USER.user_id}, role={CURRENT_USER.role})")
                    return CURRENT_USER
            except Exception:
                # bcrypt errors or bad hash
                pass

            print('Autenticación fallida. Usuario o contraseña incorrectos. Intenta de nuevo o deja vacío para cancelar.')



def hr(title: str = '', width: int = 70):
    line = '─' * width
    return f"\n{line}\n{title}\n{line}" if title else f"\n{line}"


def choose_from_list(rows, show_cols=2, label='Elige ID'):
    if not rows:
        print('No hay resultados')
        return None
    for r in rows:
        # r is a model object; show first columns
        vals = []
        for i in range(min(show_cols, len(r.__dict__))):
            # best-effort inspection
            try:
                vals.append(str(list(r.__dict__.values())[i]))
            except Exception:
                vals.append('')
        print(f"  {getattr(r, list(r.__dict__.keys())[0])} -> {' | '.join(vals)}")
    while True:
        s = input(f"{label}: ").strip()
        if not s:
            return None
        try:
            return int(s)
        except ValueError:
            print('Ingresa un número válido')


def list_tickets(limit: int = 50):
    with DB() as db:
        repo = TicketRepo(db)
        rows = repo.list(limit=limit, order_by='ticket_id', desc=True)
        print(hr('TICKETS'))
        for t in rows:
            print(f"ID={t.ticket_id} | cliente={t.client_id} | asunto={t.subject[:40]} | prio={t.priority} | status={t.status} | creado={t.created_at} | due={t.due_at}")


def create_ticket():
    with DB() as db:
        client_repo = ClientRepo(db)
        user_repo = AppUserRepo(db)
        ticket_repo = TicketRepo(db)
        cur = db.cursor()

        # choose client
        clients = client_repo.list(limit=50, order_by='full_name')
        print(hr('Clientes'))
        for c in clients:
            print(f"({c.client_id}) {c.full_name} | {c.email or ''}")
        s = input('client_id (ENTER para cancelar): ').strip()
        if not s:
            return
        try:
            client_id = int(s)
        except ValueError:
            print('client_id inválido')
            return

        subject = input('Asunto: ').strip() or 'Sin asunto'
        description = input('Descripción (ENTER para vacío): ').strip() or None
        priority = input('Prioridad (alta/media/baja) [media]: ').strip() or 'media'
        due_in_days = input('Due en cuántos días o fecha (ENTER para ninguno): ').strip()
        due_at = None
        if due_in_days:
            # allow either an integer number of days or several date formats
            try:
                days = int(due_in_days)
                due_at = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                # try to parse explicit date formats (common variants)
                parsed = None
                for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%d-%m-%Y %H:%M'):
                    try:
                        parsed = datetime.strptime(due_in_days, fmt)
                        break
                    except Exception:
                        parsed = None
                if parsed:
                    # if time not provided, keep midnight time from parsed
                    due_at = parsed.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    print('Formato de fecha inválido. Use un número de días (ej. 6) o una fecha YYYY-MM-DD o DD-MM-YYYY.')
                    due_at = None

        # list users via raw SQL to avoid pydantic validation errors on bad email values
        cur.execute("SELECT user_id, full_name, username FROM app_user ORDER BY user_id LIMIT 50")
        assigned_rows = cur.fetchall()
        print('\nUsuarios disponibles:')
        for r in assigned_rows:
            print(f"({r[0]}) {r[2]} | {r[1]}")
        if CURRENT_USER:
            a = input(f'Asignar a user_id (ENTER para asignar a tí [{CURRENT_USER.user_id}] / 0 para ninguno): ').strip()
            if not a:
                assigned_to = CURRENT_USER.user_id
            elif a == '0':
                assigned_to = None
            else:
                assigned_to = int(a) if a.isdigit() else None
        else:
            a = input('Asignar a user_id (ENTER para ninguno): ').strip()
            assigned_to = int(a) if a.isdigit() else None

        payload = {
            'client_id': client_id,
            'subject': subject,
            'description': description,
            'priority': priority,
            'status': 'abierto',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'due_at': due_at,
            'assigned_to': assigned_to
        }
        tid = ticket_repo.create(payload)
        print(f'Ticket creado id={tid}')


def change_ticket_status():
    with DB() as db:
        repo = TicketRepo(db)
        rows = repo.list(limit=50, order_by='ticket_id', desc=True)
        print(hr('Selecciona ticket para cambiar estado'))
        for t in rows:
            print(f"({t.ticket_id}) {t.subject[:60]} | status={t.status}")
        s = input('ticket_id (ENTER cancelar): ').strip()
        if not s:
            return
        try:
            tid = int(s)
        except ValueError:
            print('ticket_id inválido')
            return
        new_status = input('Nuevo estado (abierto/en_progreso/cerrado) [en_progreso]: ').strip() or 'en_progreso'
        payload = {'status': new_status}
        # if closing, set resolved_at to now and mark assigned_to as current user if available
        if new_status == 'cerrado':
            payload['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if CURRENT_USER:
                payload['assigned_to'] = CURRENT_USER.user_id
            # interactive: ask for a short resolution note to store (appended to description)
            note = input('Nota de resolución (ENTER para omitir): ').strip()
            if note:
                # fetch current ticket to preserve description
                cur = repo.get(tid)
                existing = cur.description or ''
                stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                appended = existing + ("\n\n[RESOLUCIÓN - " + stamp + "] " + note)
                payload['description'] = appended
        repo.update(tid, payload)
        print('Estado actualizado')


def list_events(limit: int = 50):
    with DB() as db:
        repo = CalendarEventRepo(db)
        rows = repo.list(limit=limit, order_by='start_time', desc=False)
        print(hr('EVENTOS DE CALENDARIO'))
        for e in rows:
            print(f"ID={e.event_id} | {e.title[:40]} | {e.start_time} -> {e.end_time} | ticket={e.ticket_id}")


def create_event():
    with DB() as db:
        event_repo = CalendarEventRepo(db)
        client_repo = ClientRepo(db)
        cur = db.cursor()

        def parse_dt_input(s: str, default_dt: datetime = None) -> datetime:
            s = s.strip()
            if not s:
                return default_dt
            # if contains ':' assume time provided
            has_time = ':' in s
            for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d', '%d-%m-%Y %H:%M', '%d-%m-%Y', '%d/%m/%Y'):
                try:
                    dt = datetime.strptime(s, fmt)
                    if not has_time:
                        # if user didn't provide time, prefer default_dt's time if available
                        if default_dt is not None:
                            dt = datetime.combine(dt.date(), default_dt.time())
                        else:
                            # midnight
                            dt = datetime.combine(dt.date(), datetime.min.time())
                    return dt
                except Exception:
                    continue
            return None

        title = input('Título: ').strip() or 'Sin título'
        description = input('Descripción (ENTER vacío): ').strip() or None

        now = datetime.now()
        start_in = input('Inicio (YYYY-MM-DD HH:MM) [ahora]: ').strip()
        start_dt = parse_dt_input(start_in, default_dt=now) if start_in else now

        end_default = start_dt + timedelta(hours=1)
        end_in = input('Fin (YYYY-MM-DD HH:MM) [+1h]: ').strip()
        end_dt = parse_dt_input(end_in, default_dt=end_default) if end_in else end_default

        # list users via raw SQL to avoid pydantic validation issues
        cur.execute("SELECT user_id, full_name FROM app_user ORDER BY user_id LIMIT 20")
        users = cur.fetchall()
        print('\nUsuarios (creador):')
        for r in users:
            print(f"({r[0]}) {r[1]}")
        created_by = input('created_by user_id (ENTER para ninguno): ').strip()
        if not created_by and CURRENT_USER:
            created_by_id = CURRENT_USER.user_id
        else:
            created_by_id = int(created_by) if created_by.isdigit() else None
        ticket_id = input('Ticket ID asociado (ENTER para ninguno): ').strip()
        ticket_id_val = int(ticket_id) if ticket_id.isdigit() else None

        payload = {
            'title': title,
            'description': description,
            'start_time': start_dt.strftime('%Y-%m-%d %H:%M'),
            'end_time': end_dt.strftime('%Y-%m-%d %H:%M'),
            'created_by': created_by_id,
            'ticket_id': ticket_id_val
        }
        eid = event_repo.create(payload)
        print(f'Evento creado id={eid}')


def list_alerts():
    with DB() as db:
        cur = db.cursor()
        # Use raw SQL to avoid Pydantic validation errors if DB contains bad enum values
        cur.execute("SELECT alert_id, alert_time, message, kind, sent, ticket_id, event_id FROM alert ORDER BY alert_time LIMIT 50")
        rows = cur.fetchall()
        print(hr('ALERTAS'))
        cols = [d[0] for d in cur.description]
        for r in rows:
            data = {cols[i]: r[i] for i in range(len(cols))}
            # normalize kind for display
            kind = data.get('kind') or '<invalid>'
            print(f"ID={data.get('alert_id')} | when={data.get('alert_time')} | msg={str(data.get('message'))[:60]} | kind={kind} | sent={data.get('sent')} | ticket={data.get('ticket_id')} | event={data.get('event_id')}")


def create_alert():
    with DB() as db:
        repo = AlertRepo(db)
        kind = input('Tipo (ticket/event/incident) [incident]: ').strip() or 'incident'
        when = input('Fecha/hora (YYYY-MM-DD HH:MM) [+1h]: ').strip() or (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
        msg = input('Mensaje (<=255): ').strip() or 'Recordatorio'
        ticket_id = input('Ticket ID (opcional): ').strip()
        event_id = input('Event ID (opcional): ').strip()
        ticket_val = int(ticket_id) if ticket_id.isdigit() else None
        event_val = int(event_id) if event_id.isdigit() else None
        created_by = input('Creado por user_id (opcional): ').strip()
        if not created_by and CURRENT_USER:
            created_by_val = CURRENT_USER.user_id
        else:
            created_by_val = int(created_by) if created_by.isdigit() else None
        payload = {
            'alert_time': when,
            'message': msg,
            'kind': kind,
            'ticket_id': ticket_val,
            'event_id': event_val,
            'sent': 0,
            'created_by': created_by_val,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        aid = repo.create(payload)
        print(f'Alerta creada id={aid}')


def mark_alert_sent():
    with DB() as db:
        repo = AlertRepo(db)
        pending = repo.pending(limit=50)
        if not pending:
            print('No hay alertas pendientes')
            return
        for a in pending:
            print(f"({a.alert_id}) when={a.alert_time} | {a.message[:60]}")
        s = input('ID alerta a marcar como enviada (ENTER cancelar): ').strip()
        if not s:
            return
        try:
            aid = int(s)
        except ValueError:
            print('ID inválido')
            return
        repo.update(aid, {'sent': 1})
        print('Alerta marcada como enviada')


def run_demo():
    with DB() as db:
        client_repo = ClientRepo(db)
        ticket_repo = TicketRepo(db)
        event_repo = CalendarEventRepo(db)
        alert_repo = AlertRepo(db)

        # pick a client or create one
        clients = client_repo.list(limit=1)
        if clients:
            client_id = clients[0].client_id
        else:
            client_id = client_repo.create({'full_name': 'Cliente DEMO'})

        tid = ticket_repo.create({'client_id': client_id, 'subject': 'Demo ticket', 'description': 'Flujo demo', 'priority': 'media', 'status': 'abierto', 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'assigned_to': (CURRENT_USER.user_id if CURRENT_USER else None)})
        print(f'Demo ticket id={tid}')
        start = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
        end = (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
        eid = event_repo.create({'title': 'Demo evento', 'description': 'Evento demo', 'start_time': start, 'end_time': end, 'created_by': (CURRENT_USER.user_id if CURRENT_USER else None), 'ticket_id': tid})
        print(f'Demo event id={eid}')
        aid = alert_repo.create({'alert_time': (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), 'message': 'Demo alerta', 'kind': 'ticket', 'ticket_id': tid, 'event_id': None, 'sent': 0, 'created_by': (CURRENT_USER.user_id if CURRENT_USER else None), 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        print(f'Demo alert id={aid}')


def print_month_calendar(year: int = None, month: int = None):
    """Print a month calendar (weeks Sunday->Saturday) marking days with:
    A = Alert, T = Ticket, E = Event. Multiple letters concatenated if more than one.

    If year/month are None the current month is used. Queries DB for events,
    alerts and tickets occurring in that month.
    """
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    # compute month range
    first_day = datetime(year, month, 1)
    # last day: use calendar.monthrange
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num)

    # prepare date strings YYYY-MM-DD
    start_date = first_day.strftime('%Y-%m-%d')
    end_date = last_day.strftime('%Y-%m-%d')

    # gather markers from DB using raw SQL to avoid model validation
    with DB() as db:
        cur = db.cursor()

        # Alerts by date
        cur.execute(
            "SELECT DATE(alert_time) as d, COUNT(*) as cnt FROM alert WHERE DATE(alert_time) BETWEEN %s AND %s GROUP BY DATE(alert_time)",
            (start_date, end_date)
        )
        alerts = {r[0].strftime('%Y-%m-%d'): r[1] for r in cur.fetchall()}

        # Tickets by created_at or due_at
        cur.execute(
            "SELECT DATE(created_at) as d, COUNT(*) FROM ticket WHERE DATE(created_at) BETWEEN %s AND %s GROUP BY DATE(created_at)",
            (start_date, end_date)
        )
        tickets_created = {r[0].strftime('%Y-%m-%d'): r[1] for r in cur.fetchall()}
        cur.execute(
            "SELECT DATE(due_at) as d, COUNT(*) FROM ticket WHERE due_at IS NOT NULL AND DATE(due_at) BETWEEN %s AND %s GROUP BY DATE(due_at)",
            (start_date, end_date)
        )
        tickets_due = {r[0].strftime('%Y-%m-%d'): r[1] for r in cur.fetchall()}

        # Events overlapping the day (use DATE(start_time) <= day <= DATE(end_time))
        cur.execute(
            "SELECT DATE(start_time) as d, COUNT(*) FROM calendar_event WHERE DATE(start_time) BETWEEN %s AND %s GROUP BY DATE(start_time)",
            (start_date, end_date)
        )
        events = {r[0].strftime('%Y-%m-%d'): r[1] for r in cur.fetchall()}

    # build calendar weeks starting on Sunday
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(year, month)

    # Header
    month_name = calendar.month_name[month]
    title = f"{month_name} {year}"
    print('\n' + title.center(20))
    print('Dom Lun Mar Mie Jue Vie Sab')

    for week in weeks:
        line = ''
        for day in week:
            if day == 0:
                line += '    '.ljust(8)
            else:
                day_date = f"{year:04d}-{month:02d}-{day:02d}"
                markers = ''
                if alerts.get(day_date):
                    markers += 'A'
                # ticket: either created or due
                if tickets_created.get(day_date) or tickets_due.get(day_date):
                    if 'T' not in markers:
                        markers += 'T'
                if events.get(day_date):
                    markers += 'E'
                if not markers:
                    cell = f"{day:2d}"
                else:
                    cell = f"{day:2d}{markers}"
                # pad cell to width 6
                line += cell.ljust(8)
        print(line)




def show_menu():
    header = 'OmniDesk - Calendario / Tickets / Alertas'
    if CURRENT_USER:
        header = f"{header}    (usuario: {CURRENT_USER.full_name} id={CURRENT_USER.user_id} role={CURRENT_USER.role})"
    print(hr(header))
    print('1) Tickets: Listar')
    print('2) Tickets: Crear')
    print('3) Tickets: Cambiar estado')
    print('4) Eventos: Listar')
    print('5) Eventos: Crear')
    print('6) Alertas: Listar')
    print('7) Alertas: Crear')
    print('8) Alertas: Marcar enviada')
    print('U) Cambiar usuario (login)')
    print('C) Calendario (mes)')
    print('D) Demo')
    print('Q) Salir')


def main():
    # Authenticate at start
    authenticate_user()

    while True:
        show_menu()
        op = input('\nOpción: ').strip().lower()
        if op == '1':
            list_tickets()
        elif op == '2':
            create_ticket()
        elif op == '3':
            change_ticket_status()
        elif op == '4':
            list_events()
        elif op == '5':
            create_event()
        elif op == '6':
            list_alerts()
        elif op == '7':
            create_alert()
        elif op == '8':
            mark_alert_sent()
        elif op == 'u':
            authenticate_user()
        elif op == 'c':
            print_month_calendar(2025, 11)
        elif op == 'd':
            run_demo()
        elif op == 'q':
            break
        else:
            print('Opción no válida')


if __name__ == '__main__':
    main()
