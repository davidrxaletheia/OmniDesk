from fastapi import APIRouter, Query, Depends
from typing import Optional
from pydantic import BaseModel, EmailStr
from ..repos.app_user_repo import AppUserRepo
from ..utils.serializers import to_jsonable
from ..core.deps import require_admin
from ..core.security import hash_password

router_admin = APIRouter(prefix="/admin")

router = APIRouter()


@router.get("/users")
def list_users(active: Optional[bool] = Query(None), role: Optional[str] = Query(None), limit: int = 50, offset: int = 0, current_user=Depends(require_admin)):
    users = AppUserRepo().list(limit=limit, offset=offset)
    # simple filtering in python for demo purposes
    out = []
    for u in users:
        # legacy repo returns Pydantic models; convert to dict and remove sensitive fields
        data = u.dict()
        data.pop("password_hash", None)
        if active is not None and data.get("active") != active:
            continue
        if role and data.get("role") != role:
            continue
        out.append(data)

    return to_jsonable(out)


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: Optional[EmailStr] = None
    password: str
    role: Optional[str] = 'empleado'


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None


@router_admin.post("/users")
def admin_create_user(body: UserCreate, current_user=Depends(require_admin)):
    data = body.dict()
    try:
        uid = AppUserRepo().create(data)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"user_id": uid})


@router_admin.get("/users/{user_id}")
def admin_get_user(user_id: int, current_user=Depends(require_admin)):
    u = AppUserRepo().get(user_id)
    if not u:
        from fastapi import HTTPException
        raise HTTPException(404, "User not found")
    data = u.dict()
    data.pop('password_hash', None)
    return to_jsonable(data)


@router_admin.put("/users/{user_id}")
def admin_update_user(user_id: int, body: UserUpdate, current_user=Depends(require_admin)):
    try:
        AppUserRepo().update(user_id, {k: v for k, v in body.dict().items() if v is not None})
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"updated": user_id})


@router_admin.delete("/users/{user_id}")
def admin_delete_user(user_id: int, current_user=Depends(require_admin)):
    try:
        AppUserRepo().delete(user_id)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"deleted": user_id})
