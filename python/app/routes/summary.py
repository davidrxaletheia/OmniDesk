from fastapi import APIRouter, Depends
from ..repos.app_user_repo import AppUserRepo
from ..repos.ticket_repo import TicketRepo
from ..repos.calendar_repo import CalendarRepo
from ..core.deps import get_current_user

router = APIRouter()


@router.get("/summary")
def get_summary(current_user=Depends(get_current_user)):
    users = AppUserRepo().list(limit=100000)
    tickets_open = TicketRepo().list(status="abierto", limit=100000)
    tickets_in_progress = TicketRepo().list(status="en_progreso", limit=100000)
    tickets_closed = TicketRepo().list(status="cerrado", limit=100000)
    upcoming_events = CalendarRepo().upcoming(limit=10)
    return {
        "users_count": len(users),
        "tickets": {
            "open": len(tickets_open),
            "in_progress": len(tickets_in_progress),
            "closed": len(tickets_closed),
        },
        "upcoming_events": len(upcoming_events),
        "unread_messages": 0,
    }
