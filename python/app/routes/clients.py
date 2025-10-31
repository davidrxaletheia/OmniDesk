from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..repos.client_repo import ClientRepo
from ..core.security import create_access_token
from ..utils.serializers import to_jsonable

router = APIRouter()


class ClientCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


@router.post("/clients")
def create_client(body: ClientCreate):
    data = body.dict()
    try:
        cid = ClientRepo().create(data)
    except Exception as exc:
        raise HTTPException(400, str(exc))

    token = create_access_token({"client_id": cid, "type": "client"})
    return to_jsonable({"client_id": cid, "client_token": token})
