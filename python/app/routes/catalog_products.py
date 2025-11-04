from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..repos.catalog_product_repo import CatalogProductRepo
from ..utils.serializers import to_jsonable
from ..core.deps import require_admin

router = APIRouter()
repo = CatalogProductRepo()


class CatalogProductCreate(BaseModel):
    product_id: int
    special_price: Optional[float] = None
    assigned_stock: Optional[int] = None


class CatalogProductUpdate(BaseModel):
    special_price: Optional[float] = None
    assigned_stock: Optional[int] = None


@router.get("/catalogs/{catalog_id}/products")
def list_catalog_products(catalog_id: int):
    rows = repo.list_by_catalog(catalog_id)
    return to_jsonable(rows)


@router.get("/catalogs/{catalog_id}/products/{product_id}")
def get_catalog_product(catalog_id: int, product_id: int):
    obj = repo.get(catalog_id, product_id)
    if not obj:
        raise HTTPException(404, 'Not found')
    return to_jsonable(obj)


@router.post("/catalogs/{catalog_id}/products")
def create_catalog_product(catalog_id: int, body: CatalogProductCreate, current_user=Depends(require_admin)):
    data = body.dict()
    data['catalog_id'] = catalog_id
    try:
        repo.create(data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    return to_jsonable({'created': True, 'catalog_id': catalog_id, 'product_id': data.get('product_id')})


@router.put("/catalogs/{catalog_id}/products/{product_id}")
def update_catalog_product(catalog_id: int, product_id: int, body: CatalogProductUpdate, current_user=Depends(require_admin)):
    data = {k: v for k, v in body.dict().items() if v is not None}
    if not data:
        raise HTTPException(400, 'No fields to update')
    try:
        rows = repo.update(catalog_id, product_id, data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    return to_jsonable({'updated': rows})


@router.delete("/catalogs/{catalog_id}/products/{product_id}")
def delete_catalog_product(catalog_id: int, product_id: int, current_user=Depends(require_admin)):
    try:
        rows = repo.delete(catalog_id, product_id)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    return to_jsonable({'deleted': rows})
