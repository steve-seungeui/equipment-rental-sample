from datetime import date

from fastapi import APIRouter, Header, Request
from pydantic import BaseModel

from app.rentals import repository, service

router = APIRouter(prefix="/rentals", tags=["rentals"])


class RentalCreate(BaseModel):
    item_id: int
    borrower: str
    start_date: str
    end_date: str


@router.get("")
def list_rentals(request: Request, item_id: int | None = None) -> list[dict]:
    return [dict(row) for row in repository.list_rentals(request.app.state.db, item_id)]


@router.post("", status_code=201)
def create_rental(body: RentalCreate, request: Request) -> dict:
    return service.create_rental(
        request.app.state.db, body.item_id, body.borrower, body.start_date, body.end_date
    )


@router.post("/{rental_id}/return")
def return_rental(rental_id: int, request: Request, x_user_email: str = Header()) -> dict:
    return service.return_rental(request.app.state.db, rental_id, x_user_email, date.today())
