from typing import Optional
from fastapi import APIRouter, Query, Depends, Header
from ..repos.product_repo import ProductRepo
from ..repos.client_repo import ClientRepo
from ..utils.serializers import to_jsonable
from ..core.deps import require_admin
from ..core.security import decode_token
from ..core.config import settings

router = APIRouter()


@router.get("/products")
def list_products(q: Optional[str] = Query(None), limit: int = 50, offset: int = 0):
    repo = ProductRepo()
    if q:
        prods = repo.search(q, limit=limit)
    else:
        prods = repo.list(limit=limit, offset=offset)
    return to_jsonable([p.dict() for p in prods])

@router.get("/products/for-client")
def list_products_for_client(authorization: Optional[str] = Header(None), q: Optional[str] = Query(None), limit: int = 50, offset: int = 0):
    """List products and compute a `price_for_client` depending on client_type.

    If no valid client token is provided, returns standard product price.
    Premium clients receive a discount configured by `PREMIUM_DISCOUNT_PCT`.
    """
    repo = ProductRepo()
    if q:
        prods = repo.search(q, limit=limit)
    else:
        prods = repo.list(limit=limit, offset=offset)

    client_type = None
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token = parts[1]
            try:
                payload = decode_token(token)
                sub = payload.get('sub', {})
                cid = sub.get('client_id')
                if cid:
                    c = ClientRepo().get(cid)
                    client_type = getattr(c, 'client_type', None)
            except Exception:
                client_type = None

    out = []
    discount_pct = float(getattr(settings, 'PREMIUM_DISCOUNT_PCT', 0.0))
    for p in prods:
        data = p.dict()
        price = data.get('price')
        try:
            base = float(price)
        except Exception:
            base = price
        if client_type == 'premium' and isinstance(base, (int, float)) and discount_pct > 0:
            pf = round(base * (1.0 - discount_pct), 2)
        else:
            pf = base
        data['price_for_client'] = pf
        out.append(data)
    return to_jsonable(out)


@router.get("/products/{product_id}")
def get_product(product_id: int):
    p = ProductRepo().get(product_id)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, "Product not found")
    return to_jsonable(p.dict())


@router.post("/products")
def create_product(body: dict, current_user=Depends(require_admin)):
    try:
        pid = ProductRepo().create(body)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"product_id": pid})


@router.put("/products/{product_id}")
def update_product(product_id: int, body: dict, current_user=Depends(require_admin)):
    try:
        ProductRepo().update(product_id, body)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"updated": product_id})


@router.delete("/products/{product_id}")
def delete_product(product_id: int, current_user=Depends(require_admin)):
    try:
        ProductRepo().delete(product_id)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(400, str(exc))
    return to_jsonable({"deleted": product_id})
