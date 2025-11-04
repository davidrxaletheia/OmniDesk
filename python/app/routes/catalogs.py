from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from ..repos.catalog_repo import CatalogRepo
from ..utils.serializers import to_jsonable
from ..core.deps import require_admin

router = APIRouter()


class CatalogCreate(BaseModel):
    name: str
    description: Optional[str] = None
    discount_percentage: Optional[float] = 0.0
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    visible_to: Optional[str] = 'todos'
    active: Optional[bool] = True


class CatalogUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    visible_to: Optional[str] = None
    active: Optional[bool] = None


@router.get("/catalogs")
def list_catalogs(limit: int = Query(50, ge=1, le=1000), offset: int = 0):
    repo = CatalogRepo()
    rows = repo.list(limit=limit, offset=offset)
    return to_jsonable(rows)


@router.get("/catalogs/actives")
def list_active_catalogs():
    repo = CatalogRepo()
    rows = repo.actives()
    return to_jsonable(rows)


@router.get("/catalogs/{catalog_id}")
def get_catalog(catalog_id: int):
    repo = CatalogRepo()
    obj = repo.get(catalog_id)
    if not obj:
        raise HTTPException(404, "Catalog not found")
    return to_jsonable(obj)


@router.post("/catalogs")
def create_catalog(body: CatalogCreate, current_user=Depends(require_admin)):
    repo = CatalogRepo()
    data = body.dict()
    try:
        cid = repo.create(data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    obj = repo.get(cid)
    return to_jsonable(obj)


@router.put("/catalogs/{catalog_id}")
def update_catalog(catalog_id: int, body: CatalogUpdate, current_user=Depends(require_admin)):
    repo = CatalogRepo()
    data = {k: v for k, v in body.dict().items() if v is not None}
    if not data:
        raise HTTPException(400, "No fields to update")
    try:
        repo.update(catalog_id, data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    obj = repo.get(catalog_id)
    return to_jsonable({"updated": catalog_id, "catalog": obj})


@router.delete("/catalogs/{catalog_id}")
def delete_catalog(catalog_id: int, current_user=Depends(require_admin)):
    repo = CatalogRepo()
    try:
        repo.delete(catalog_id)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    return to_jsonable({"deleted": catalog_id})
