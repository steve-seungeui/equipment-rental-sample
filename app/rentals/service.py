import sqlite3
from datetime import date

from app.errors import ConflictError, NotFoundError, ValidationError
from app.rentals import repository

MAX_RENTAL_DAYS = 14


def _parse_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{field}는 YYYY-MM-DD 형식이어야 합니다.") from exc


def _validate_period(start: date, end: date) -> None:
    if end < start:
        raise ValidationError("반납 예정일은 대여 시작일보다 빠를 수 없습니다.")
    if (end - start).days + 1 > MAX_RENTAL_DAYS:
        raise ValidationError(f"대여 기간은 최대 {MAX_RENTAL_DAYS}일입니다.")


def create_rental(
    conn: sqlite3.Connection, item_id: int, borrower: str, start_date: str, end_date: str
) -> dict:
    start = _parse_date(start_date, "start_date")
    end = _parse_date(end_date, "end_date")
    _validate_period(start, end)
    if not borrower.strip():
        raise ValidationError("borrower는 비어 있을 수 없습니다.")

    item = repository.find_item(conn, item_id)
    if item is None:
        raise NotFoundError("비품을 찾을 수 없습니다.")
    if item["status"] != "available":
        raise ConflictError("대여할 수 없는 상태의 비품입니다.")

    rental_id = repository.insert_rental_if_available(
        conn, item_id, borrower, start.isoformat(), end.isoformat()
    )
    if rental_id is None:
        raise ConflictError("같은 기간에 이미 대여된 비품입니다.")
    return dict(repository.find_rental(conn, rental_id))


def return_rental(conn: sqlite3.Connection, rental_id: int, requested_by: str, today: date) -> dict:
    rental = repository.find_rental(conn, rental_id)
    if rental is None:
        raise NotFoundError("대여 기록을 찾을 수 없습니다.")
    if rental["borrower"] != requested_by:
        raise ValidationError("대여한 사람만 반납할 수 있습니다.")
    if rental["status"] != "active":
        raise ConflictError("이미 반납되었거나 취소된 대여입니다.")
    repository.mark_returned(conn, rental_id, today.isoformat())
    return dict(repository.find_rental(conn, rental_id))
