from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.errors import ValidationError
from app.rentals import repository

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    category: str


@router.get("")
def list_items(request: Request) -> list[dict]:
    return [dict(row) for row in repository.list_items(request.app.state.db)]


@router.post("", status_code=201)
def create_item(body: ItemCreate, request: Request) -> dict:
    if not body.name.strip() or not body.category.strip():
        raise ValidationError("name과 category는 비어 있을 수 없습니다.")
    conn = request.app.state.db
    item_id = repository.insert_item(conn, body.name.strip(), body.category.strip())
    return dict(repository.find_item(conn, item_id))
