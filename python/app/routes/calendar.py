from fastapi import APIRouter, Query, Depends
from typing import Optional
from ..repos.calendar_repo import CalendarRepo
from ..repos.ticket_repo import TicketRepo
from ..repos.alert_repo import AlertRepo
from ..core.deps import get_current_user, require_employee_or_admin
from ..utils.serializers import parse_iso_datetime, to_jsonable

router = APIRouter()


@router.get('/calendar/view')
def calendar_view(start: Optional[str] = Query(None), end: Optional[str] = Query(None), limit: int = 200, current_user=Depends(get_current_user)):
    """Devuelve un arreglo unificado de eventos, tickets (con due_at) y alertas dentro del rango dado."""
    start_dt = parse_iso_datetime(start)
    end_dt = parse_iso_datetime(end)

    # Events
    events = CalendarRepo().list_range(start=start_dt, end=end_dt, limit=limit)
    ev_entries = []
    for e in events:
        d = e.dict()
        ev_entries.append({
            'id': f"event-{d.get('event_id')}",
            'kind': 'event',
            'title': d.get('title'),
            'description': d.get('description'),
            'start': d.get('start_time').isoformat() if d.get('start_time') else None,
            'end': d.get('end_time').isoformat() if d.get('end_time') else None,
            'meta': {'event_id': d.get('event_id'), 'ticket_id': d.get('ticket_id'), 'created_by': d.get('created_by')}
        })

    # Tickets with due_at in range
    ticket_params = []
    where_clauses = []
    if start_dt:
        where_clauses.append('due_at >= %s')
        ticket_params.append(start_dt)
    if end_dt:
        where_clauses.append('due_at <= %s')
        ticket_params.append(end_dt)
    tickets = []
    if where_clauses:
        where = ' AND '.join(where_clauses)
        tickets = TicketRepo()._legacy.filter(where, tuple(ticket_params), limit=limit)
    else:
        # fallback: recent open tickets
        tickets = TicketRepo().list(limit=limit)

    tk_entries = []
    for t in tickets:
        d = t.dict()
        if not d.get('due_at'):
            continue
        tk_entries.append({
            'id': f"ticket-{d.get('ticket_id')}",
            'kind': 'ticket',
            'title': f"Ticket: {d.get('subject')}",
            'description': d.get('description'),
            'start': d.get('due_at').isoformat() if d.get('due_at') else None,
            'end': None,
            'meta': {'ticket_id': d.get('ticket_id'), 'status': d.get('status'), 'priority': d.get('priority'), 'client_id': d.get('client_id')}
        })

    # Alerts in range (or pending if no range)
    alerts = []
    if start_dt or end_dt:
        where_clauses = []
        params = []
        if start_dt:
            where_clauses.append('alert_time >= %s')
            params.append(start_dt)
        if end_dt:
            where_clauses.append('alert_time <= %s')
            params.append(end_dt)
        where = ' AND '.join(where_clauses) if where_clauses else None
        alerts = AlertRepo().list(where=where, params=tuple(params), limit=limit)
    else:
        alerts = AlertRepo().pending(limit=limit)

    al_entries = []
    for a in alerts:
        d = a.dict()
        al_entries.append({
            'id': f"alert-{d.get('alert_id')}",
            'kind': 'alert',
            'title': d.get('message'),
            'description': None,
            'start': d.get('alert_time').isoformat() if d.get('alert_time') else None,
            'end': None,
            'meta': {'alert_id': d.get('alert_id'), 'ticket_id': d.get('ticket_id'), 'sent': d.get('sent')}
        })

    merged = ev_entries + tk_entries + al_entries
    # Simple sort by start (None goes last)
    merged.sort(key=lambda x: (x['start'] is None, x['start'] or ''))
    return to_jsonable(merged)
