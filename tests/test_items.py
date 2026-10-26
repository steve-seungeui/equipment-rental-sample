def test_create_and_list_items(client):
    res = client.post("/items", json={"name": "프로젝터 1", "category": "프로젝터"})
    assert res.status_code == 201
    assert res.json()["status"] == "available"

    items = client.get("/items").json()
    assert [item["name"] for item in items] == ["프로젝터 1"]


def test_item_name_is_required(client):
    res = client.post("/items", json={"name": " ", "category": "노트북"})
    assert res.status_code == 400
