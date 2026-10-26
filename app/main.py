import os

from fastapi import FastAPI

from app.api import items, rentals
from app.db import connect
from app.errors import register_error_handlers


def create_app(db_path: str | None = None) -> FastAPI:
    app = FastAPI(title="비품 대여 API")
    app.state.db = connect(db_path or os.environ.get("RENTAL_DB_PATH", "data/rental.db"))
    register_error_handlers(app)
    app.include_router(items.router)
    app.include_router(rentals.router)
    return app


app = create_app()
