def rent(client, item_id, start, end, borrower="kim@example.com"):
    return client.post(
        "/rentals",
        json={"item_id": item_id, "borrower": borrower, "start_date": start, "end_date": end},
    )


def test_rent_available_item(client, laptop):
    res = rent(client, laptop["id"], "2026-11-02", "2026-11-06")
    assert res.status_code == 201
    assert res.json()["status"] == "active"


def test_overlapping_rental_is_rejected(client, laptop):
    assert rent(client, laptop["id"], "2026-11-02", "2026-11-06").status_code == 201
    res = rent(client, laptop["id"], "2026-11-05", "2026-11-09", borrower="lee@example.com")
    assert res.status_code == 409


def test_adjacent_rental_is_allowed(client, laptop):
    assert rent(client, laptop["id"], "2026-11-02", "2026-11-06").status_code == 201
    assert rent(client, laptop["id"], "2026-11-07", "2026-11-09").status_code == 201


def test_rental_period_is_limited(client, laptop):
    res = rent(client, laptop["id"], "2026-11-02", "2026-11-16")
    assert res.status_code == 400


def test_end_date_before_start_date_is_rejected(client, laptop):
    res = rent(client, laptop["id"], "2026-11-06", "2026-11-02")
    assert res.status_code == 400


def test_return_by_borrower(client, laptop):
    rental = rent(client, laptop["id"], "2026-11-02", "2026-11-06").json()
    res = client.post(f"/rentals/{rental['id']}/return", headers={"X-User-Email": "kim@example.com"})
    assert res.status_code == 200
    assert res.json()["status"] == "returned"


def test_returned_item_can_be_rented_again(client, laptop):
    rental = rent(client, laptop["id"], "2026-11-02", "2026-11-06").json()
    client.post(f"/rentals/{rental['id']}/return", headers={"X-User-Email": "kim@example.com"})
    assert rent(client, laptop["id"], "2026-11-03", "2026-11-05", borrower="lee@example.com").status_code == 201


def test_only_borrower_can_return(client, laptop):
    rental = rent(client, laptop["id"], "2026-11-02", "2026-11-06").json()
    res = client.post(f"/rentals/{rental['id']}/return", headers={"X-User-Email": "lee@example.com"})
    assert res.status_code == 400
