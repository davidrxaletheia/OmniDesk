from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from ..repos.category_repo import CategoryRepo
from ..utils.serializers import to_jsonable

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


@router.get("/categories")
def list_categories(limit: int = Query(50, ge=1, le=1000), offset: int = 0):
    repo = CategoryRepo()
    rows = repo.list(limit=limit, offset=offset)
    return to_jsonable(rows)


@router.post("/categories")
def create_category(body: CategoryCreate):
    repo = CategoryRepo()
    data = body.dict()
    try:
        cid = repo.create(data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    obj = repo.get(cid)
    return to_jsonable(obj)


@router.get("/categories/roots")
def get_roots():
    repo = CategoryRepo()
    rows = repo.roots()
    return to_jsonable(rows)


@router.get("/categories/{category_id}/children")
def get_children(category_id: int):
    repo = CategoryRepo()
    rows = repo.children(category_id)
    return to_jsonable(rows)


@router.get("/categories/{category_id}")
def get_category(category_id: int):
    repo = CategoryRepo()
    obj = repo.get(category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    return to_jsonable(obj)


@router.patch("/categories/{category_id}")
def update_category(category_id: int, body: CategoryUpdate):
    repo = CategoryRepo()
    data = {k: v for k, v in body.dict().items() if v is not None}
    if not data:
        raise HTTPException(400, "No fields to update")
    try:
        rows = repo.update(category_id, data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    obj = repo.get(category_id)
    return to_jsonable({"updated": rows, "category": obj})