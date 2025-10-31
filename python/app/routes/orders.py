from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..core.deps import get_bearer_token
from ..core.security import decode_token
from ..repos.order_repo import OrderRepo
from ..repos.client_repo import ClientRepo
from ..utils.serializers import to_jsonable

router = APIRouter()


class OrderItem(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    client_id: Optional[int] = None
    items: list[OrderItem]
    notes: Optional[str] = None


@router.post("/orders")
def create_order(body: OrderCreate, token: str = Depends(get_bearer_token)):
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(401, "Invalid token")
    sub = payload.get("sub", {})
    # determine client_id: if token is client token, use that; if user token, require body.client_id
    client_id = sub.get("client_id")
    if not client_id:
        # user token
        if not body.client_id:
            raise HTTPException(400, "client_id required when using user token")
        client_id = body.client_id

    # verify client exists
    client = ClientRepo().get(client_id)
    if not client:
        raise HTTPException(404, "Client not found")

    payload_dict = {"client_id": client_id, "notes": body.notes, "items": [i.dict() for i in body.items], "client_type": getattr(client, 'client_type', None)}
    try:
        created = OrderRepo().create(payload_dict)
    except ValueError as ve:
        raise HTTPException(400, str(ve))
    except Exception as exc:
        raise HTTPException(500, str(exc))

    return to_jsonable(created.dict())


@router.get("/orders")
def list_orders(token: str = Depends(get_bearer_token), limit: int = 50, offset: int = 0):
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(401, "Invalid token")
    sub = payload.get("sub", {})
    client_id = sub.get("client_id")
    if client_id:
        orders = OrderRepo().list_by_client(client_id, limit=limit, offset=offset)
        return to_jsonable([o.dict() for o in orders])
    # no client claim -> assume user token (admin/employee)
    # TODO: restrict by role in future
    repo = OrderRepo()
    # fallback to listing recent orders
    orders = repo._order.list(limit=limit, offset=offset)
    return to_jsonable([o.dict() for o in orders])
