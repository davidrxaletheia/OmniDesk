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


class ClientIdentify(BaseModel):
    telegram_username: Optional[str] = None
    telegram_user_id: Optional[int] = None
    # If true and full_name provided, create the client when not found
    create_if_missing: Optional[bool] = False
    full_name: Optional[str] = None


class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    telegram_username: Optional[str] = None
    telegram_user_id: Optional[int] = None
    client_type: Optional[str] = None
    status: Optional[str] = None


@router.post("/clients/identify")
def identify_client(body: ClientIdentify):
    repo = ClientRepo()
    client = None
    if body.telegram_user_id:
        client = repo.get_by_telegram_id(body.telegram_user_id)
    if not client and body.telegram_username:
        client = repo.get_by_telegram_username(body.telegram_username)

    if client:
        # return client data and a client token for convenience
        token = create_access_token({"client_id": client.client_id, "type": "client"})
        return to_jsonable({"client": client, "client_token": token})

    # not found
    if body.create_if_missing:
        if not body.full_name:
            raise HTTPException(400, "full_name required when create_if_missing is true")
        data = {"full_name": body.full_name}
        if body.telegram_username:
            data["telegram_username"] = body.telegram_username
        if body.telegram_user_id:
            data["telegram_user_id"] = body.telegram_user_id
        try:
            cid = repo.create(data)
        except Exception as exc:
            raise HTTPException(400, str(exc))
        token = create_access_token({"client_id": cid, "type": "client"})
        client_obj = repo.get(cid)
        return to_jsonable({"client": client_obj, "client_token": token})

    raise HTTPException(404, "Client not found")


@router.patch("/clients/{client_id}")
def update_client(client_id: int, body: ClientUpdate):
    repo = ClientRepo()
    # Build update dict from provided fields
    data = {k: v for k, v in body.dict().items() if v is not None}
    if not data:
        raise HTTPException(400, "No fields to update")
    try:
        rows = repo.update(client_id, data)
    except Exception as exc:
        raise HTTPException(400, str(exc))

    client_obj = repo.get(client_id)
    return to_jsonable({"updated": rows, "client": client_obj})
