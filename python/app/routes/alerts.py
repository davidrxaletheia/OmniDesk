from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from ..repos.alert_repo import AlertRepo
from ..utils.serializers import to_jsonable, parse_iso_datetime
from ..core.deps import require_employee_or_admin, get_current_user

router = APIRouter()


class AlertCreate(BaseModel):
    alert_time: str
    message: str
    kind: Optional[str] = 'incident'
    ticket_id: Optional[int] = None
    event_id: Optional[int] = None


@router.post('/alerts')
def create_alert(body: AlertCreate, current_user=Depends(get_current_user)):
    data = body.dict()
    data['alert_time'] = parse_iso_datetime(data['alert_time']) if data.get('alert_time') else None
    data['created_by'] = getattr(current_user, 'user_id', None)
    rid = AlertRepo().create(data)
    if isinstance(rid, int):
        created = AlertRepo().get(rid)
    else:
        created = rid
    return to_jsonable(created.dict() if hasattr(created, 'dict') else {'id': created})


@router.get('/alerts')
def list_alerts(limit: int = 50, offset: int = 0, current_user=Depends(require_employee_or_admin)):
    alerts = AlertRepo().list(limit=limit, offset=offset)
    return to_jsonable([a.dict() for a in alerts])


@router.get('/alerts/pending')
def list_pending_alerts(limit: int = 50, current_user=Depends(require_employee_or_admin)):
    alerts = AlertRepo().pending(limit=limit)
    return to_jsonable([a.dict() for a in alerts])
