from fastapi import APIRouter, Query, Depends
from typing import Optional
from pydantic import BaseModel
from ..utils.serializers import parse_iso_datetime, to_jsonable
from ..repos.calendar_repo import CalendarRepo
from ..core.deps import get_current_user

router = APIRouter()


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    ticket_id: Optional[int] = None


@router.get("/events")
def list_events(start: Optional[str] = Query(None), end: Optional[str] = Query(None), limit: int = 50, offset: int = 0, current_user=Depends(get_current_user)):
    start_dt = parse_iso_datetime(start)
    end_dt = parse_iso_datetime(end)
    events = CalendarRepo().list_range(start=start_dt, end=end_dt, limit=limit, offset=offset)
    return to_jsonable([e.dict() for e in events])


@router.post("/events")
def create_event(body: EventCreate, current_user=Depends(get_current_user)):
    data = body.dict()
    # Convert ISO strings to datetimes if needed — legacy repo may accept strings
    data['start_time'] = parse_iso_datetime(data['start_time']) if data.get('start_time') else None
    data['end_time'] = parse_iso_datetime(data['end_time']) if data.get('end_time') else None
    # Do not assume the legacy DB/table contains a `created_by` column.
    # Let the legacy repo decide which fields to persist.
    event = CalendarRepo().create(data)
    if isinstance(event, int):
        created = CalendarRepo().get(event)
    else:
        created = event
    return to_jsonable(created.dict() if hasattr(created, 'dict') else {'id': created})
