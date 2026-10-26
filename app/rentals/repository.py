import sqlite3


def find_item(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()


def list_items(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM items ORDER BY id").fetchall()


def insert_item(conn: sqlite3.Connection, name: str, category: str) -> int:
    cur = conn.execute("INSERT INTO items (name, category) VALUES (?, ?)", (name, category))
    return int(cur.lastrowid)


def find_rental(conn: sqlite3.Connection, rental_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM rentals WHERE id = ?", (rental_id,)).fetchone()


def list_rentals(conn: sqlite3.Connection, item_id: int | None) -> list[sqlite3.Row]:
    if item_id is None:
        return conn.execute("SELECT * FROM rentals ORDER BY start_date, id").fetchall()
    return conn.execute(
        "SELECT * FROM rentals WHERE item_id = ? ORDER BY start_date, id", (item_id,)
    ).fetchall()


def insert_rental_if_available(
    conn: sqlite3.Connection, item_id: int, borrower: str, start_date: str, end_date: str
) -> int | None:
    """같은 비품의 진행 중인 대여와 기간이 겹치지 않을 때만 저장한다.

    겹침 검사와 저장을 한 문장으로 처리해 동시 요청에서도 겹치는 대여가 둘 생기지 않게 한다.
    """
    cur = conn.execute(
        """
        INSERT INTO rentals (item_id, borrower, start_date, end_date)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM rentals
            WHERE item_id = ? AND status = 'active' AND start_date <= ? AND end_date >= ?
        )
        """,
        (item_id, borrower, start_date, end_date, item_id, end_date, start_date),
    )
    return int(cur.lastrowid) if cur.rowcount == 1 else None


def mark_returned(conn: sqlite3.Connection, rental_id: int, returned_at: str) -> None:
    conn.execute(
        "UPDATE rentals SET status = 'returned', returned_at = ? WHERE id = ?",
        (returned_at, rental_id),
    )
