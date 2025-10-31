from ..Classes.repos.app_user_repo import AppUserRepo
from ..Classes.repos.ticket_repo import TicketRepo
from ..Classes.repos.calendar_repo import CalendarEventRepo
from ..Classes.models.app_user import AppUserModel
from ..Classes.models.ticket import TicketModel
from ..Classes.models.calendar import CalendarEventModel
import calendar
from datetime import date, datetime

"""
print("AppUserRepo.table: ", AppUserRepo.table)
print("TicketRepo.table: ", TicketRepo.table)
print("CalendarEventRepo.table: ", CalendarEventRepo.table) 



print("AppUserModel campos: ", list(AppUserModel.__fields__.keys()))
print("TicketModel campos: ", list(TicketModel.__fields__.keys()))
print("CalendarEventModel campos: ", list(CalendarEventModel.__fields__.keys()))

print("Metodos publicos de TickerRepo (sin instanciar)",
      [m for m in dir(TicketRepo) if not m.startswith('_')])


try:
    u = AppUserModel(full_name="Pancho Pistola", username="Papi", email="pp.123a@il.com", password_hash="x", role= "empleado")
    print("Instancia valida: ", u.dict())


    u.email = "hola@gmail.com"

    print("corregido: ", u.dict())

except Exception as e:
    print("Error de validacion: ", e)


u = AppUserModel(full_name="Ana Perez", username="ana", email="ana@example.com", password_hash="x", role="empleado")
print("tipo:", type(u))

print("Username: (acceso):", u.username)
print("as dict:", u.dict())

#ver campos y tipos

print("campos: ", list(AppUserModel.__fields__.keys()))

"""



print("--- Listado de tickets abiertos o en progreso ---")
trepo = TicketRepo()
listTickets = []
try:
    tickets = trepo.open_or_wip(limit=20)
    for t in tickets:
        listTickets.append(t)
        print(t.ticket_id, t.subject, t.status, getattr(t, 'created_at', None))
finally:
    trepo.close()

repo = CalendarEventRepo()
listEvents = []
try:
    # Prefer fetching events for the current month (includes past events in the month)
    today = date.today()
    year = today.year
    month = today.month
    first_day = datetime(year, month, 1, 0, 0, 0)
    import calendar as _cal
    last_day = _cal.monthrange(year, month)[1]
    last_dt = datetime(year, month, last_day, 23, 59, 59)
    where = "start_time BETWEEN %s AND %s"
    events = repo.filter(where, (first_day, last_dt), order_by="start_time", limit=200)
    # Debug: report what the repo returned
    try:
        cnt = len(events)
    except Exception:
        cnt = '(no len)'
    print("events returned type:", type(events), "count:", cnt)
    for i, e in enumerate(events):
        print(f"--- event #{i} type={type(e)} ---")
        # If it's a Pydantic model, .dict() is informative
        if hasattr(e, 'dict'):
            try:
                print(" as dict:", e.dict())
            except Exception as ex:
                print(" .dict() failed:", ex)
        else:
            # fallback: try vars() or repr()
            try:
                print(" vars:", vars(e))
            except Exception:
                print(" repr:", repr(e))
        # short attribute list
        print(" attrs:", [a for a in dir(e) if not a.startswith('_')][:30])
    for e in events:
        listEvents.append(e)
        start = getattr(e, 'start_time', getattr(e, 'start_at', None))
        end = getattr(e, 'end_time', getattr(e, 'end_at', None))
        print(getattr(e, 'event_id', '(?)'), getattr(e, 'title', '(no title)'), start, end)
    # If repo returned nothing, fall back to a raw SELECT so we can inspect DB rows
    if (isinstance(cnt, int) and cnt == 0) or cnt == 0:
        print('\n-- Fallback: no events from repo.upcoming(); running raw SELECT to inspect table --')
        try:
            cur = repo.db.cursor()
            cur.execute(f"SELECT * FROM {repo.table} LIMIT 5")
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            print(' columns:', cols)
            for r in rows:
                print(' row:', r)
        except Exception as ex:
            print(' raw SELECT failed:', ex)
finally:
    try: repo.close()
    except: pass


def tickets_by_day(tickets):
    """Return dict day -> list of tickets for that day.
    We use ticket.due_at if present, otherwise ticket.created_at."""
    by_day = {}
    for t in tickets:
        dt = getattr(t, 'due_at', None) or getattr(t, 'created_at', None)
        if not dt:
            continue
        # dt may be a datetime or a string; try to normalize
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt)
            except Exception:
                continue
        day = dt.date().day
        by_day.setdefault(day, []).append((dt, t))
    # sort tickets for each day by datetime
    for day in by_day:
        by_day[day].sort(key=lambda x: x[0])
    return by_day

def normalize_dt(v):
    """Normalize various datetime representations into a datetime or None."""
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, date) and not isinstance(v, datetime):
        return datetime(v.year, v.month, v.day)
    if isinstance(v, str):
        # try ISO first, then common SQL formats
        try:
            return datetime.fromisoformat(v)
        except Exception:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(v, fmt)
                except Exception:
                    pass
    return None


def items_by_day(items, date_fields):
    """Generic mapper: returns dict day -> list of (datetime, item).
    Accepts model instances, dicts, or simple objects.
    """
    by_day = {}
    for it in items:
        dt = None
        for f in date_fields:
            dt = getattr(it, f, None)
            if dt:
                break
        if not dt and isinstance(it, dict):
            for f in date_fields:
                dt = it.get(f)
                if dt:
                    break
        if not dt:
            continue
        dt = normalize_dt(dt)
        if not dt:
            continue
        day = dt.day
        by_day.setdefault(day, []).append((dt, it))
    for day in by_day:
        by_day[day].sort(key=lambda x: x[0])
    return by_day


def print_month_calendar_with_tickets_and_events(tickets, events, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    tickets_map = items_by_day(tickets, ['due_at', 'created_at', 'created_at_time'])
    events_map = items_by_day(events, ['start_time', 'start_at', 'start'])

    cal = calendar.monthcalendar(year, month)

    # Header
    print()
    print(f"     {calendar.month_name[month]} {year}")
    print(" Mo  Tu  We  Th  Fr  Sa  Su")

    # For visual alignment we will use width=4 per cell
    for week in cal:
        row = []
        for d in week:
            if d == 0:
                row.append("    ")
            else:
                has_t = d in tickets_map
                has_e = d in events_map
                if has_t and has_e:
                    s = "TE"
                elif has_t:
                    s = "T "
                elif has_e:
                    s = "E "
                else:
                    s = f"{d:2d}  "
                row.append(f"{s:4}")
        print("".join(row))

    # Print details below calendar
    if not tickets_map and not events_map:
        print("\nNo hay tickets ni eventos en este mes.\n")
        return

    print("\nDetalles por día:\n")
    days = sorted(set(list(tickets_map.keys()) + list(events_map.keys())))
    for day in days:
        print(f"{year}-{month:02d}-{day:02d}:")
        if day in events_map:
            for dt, ev in events_map[day]:
                time_str = dt.strftime("%H:%M") if isinstance(dt, datetime) else str(dt)
                title = getattr(ev, 'title', getattr(ev, 'description', '(evento)'))
                eid = getattr(ev, 'event_id', '(?)')
                print(f"  E {time_str}  #{eid}  {title}")
        if day in tickets_map:
            for dt, t in tickets_map[day]:
                time_str = dt.strftime("%H:%M") if isinstance(dt, datetime) else str(dt)
                subject = getattr(t, 'subject', '(sin asunto)')
                tid = getattr(t, 'ticket_id', '(?)')
                status = getattr(t, 'status', '(?)')
                print(f"  T {time_str}  #{tid}  [{status}] {subject}")
        print()

# --- fin del bloque ---

print("\n--- Calendario del mes actual con tickets y eventos marcados ---")
print_month_calendar_with_tickets_and_events(listTickets, listEvents)
# --- fin del bloque ---
