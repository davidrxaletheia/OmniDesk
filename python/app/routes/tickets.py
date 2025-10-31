from fastapi import APIRouter, Query, Depends
from typing import Optional, Literal
from pydantic import BaseModel
from ..repos.ticket_repo import TicketRepo
from ..utils.serializers import to_jsonable
from ..core.deps import get_current_user, require_employee_or_admin

router = APIRouter()


class TicketCreate(BaseModel):
    client_id: int
    subject: str
    description: Optional[str] = None
    priority: Optional[Literal['alta', 'media', 'baja']] = 'media'
    due_at: Optional[str] = None
    assigned_to: Optional[int] = None


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
    ticket = TicketRepo().create(data)
    # legacy create() returns the new row id (int). If so, fetch the created
    # record back via repo.get(). Otherwise assume it's already a model.
    if isinstance(ticket, int):
        created = TicketRepo().get(ticket)
    else:
        created = ticket
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
