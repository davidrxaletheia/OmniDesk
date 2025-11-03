from fastapi import APIRouter, Query, Depends
from typing import Optional, Literal
from pydantic import BaseModel
from ..repos.ticket_repo import TicketRepo
from ..repos.client_repo import ClientRepo
from ..repos.calendar_repo import CalendarRepo
from ..utils.serializers import to_jsonable, parse_iso_datetime
from ..core.deps import get_current_user, require_employee_or_admin

router = APIRouter()


class TicketCreate(BaseModel):
    client_id: int
    subject: str
    description: Optional[str] = None
    priority: Optional[Literal['alta', 'media', 'baja']] = 'media'
    due_at: Optional[str] = None
    assigned_to: Optional[int] = None
    create_event: Optional[bool] = False


@router.get("/tickets")
def list_tickets(status: Optional[str] = Query(None), priority: Optional[str] = Query(None), client_id: Optional[int] = Query(None), limit: int = 50, offset: int = 0, current_user=Depends(get_current_user)):
    tickets = TicketRepo().list(status=status, priority=priority, client_id=client_id, limit=limit, offset=offset)
    return to_jsonable([t.dict() for t in tickets])


@router.post("/tickets")
def create_ticket(body: TicketCreate, current_user=Depends(get_current_user)):
    data = body.dict()
    # Do not assume the legacy DB/table contains a `created_by` column.
    # Only include fields provided by the client and let the legacy repo
    # decide what columns to persist.
    # Validate client exists before attempting DB insert to provide clearer error
    cid = data.get('client_id')
    if cid is None or ClientRepo().get(cid) is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"client_id {cid} no existe")

    try:
        ticket = TicketRepo().create(data)
    except Exception as exc:
        from fastapi import HTTPException
        # surface DB/constraint errors as 400 with message to help debugging
        raise HTTPException(status_code=400, detail=str(exc))
    # legacy create() returns the new row id (int). If so, fetch the created
    # record back via repo.get(). Otherwise assume it's already a model.
    if isinstance(ticket, int):
        created = TicketRepo().get(ticket)
    else:
        created = ticket

    # If ticket has due_at or client requested an event, create a calendar event
    try:
        created_id = created.event_id if hasattr(created, 'event_id') else (getattr(created, 'ticket_id', None) or (ticket if isinstance(ticket, int) else None))
    except Exception:
        created_id = ticket if isinstance(ticket, int) else None

    # Use provided due_at or create_event flag to add calendar entry
    if data.get('due_at') or data.get('create_event'):
        start = parse_iso_datetime(data.get('due_at')) if data.get('due_at') else None
        end = None
        if start:
            # default duration 1 hour
            from datetime import timedelta
            end = start + timedelta(hours=1)
        event_payload = {
            'title': data.get('subject'),
            'description': data.get('description'),
            'start_time': start,
            'end_time': end,
            'created_by': getattr(current_user, 'user_id', None),
            'ticket_id': created_id or None,
        }
        try:
            CalendarRepo().create(event_payload)
        except Exception:
            # Do not fail ticket creation if calendar insert fails; log could be added.
            pass
    return to_jsonable(created.dict() if hasattr(created, 'dict') else {'id': created})


class TicketStatusUpdate(BaseModel):
    status: str


@router.patch("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: int, body: TicketStatusUpdate, current_user=Depends(require_employee_or_admin)):
    # allow employees or admins to update ticket status
    try:
        updated = TicketRepo().update(ticket_id, {'status': body.status})
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({'ticket_id': ticket_id, 'status': body.status})
