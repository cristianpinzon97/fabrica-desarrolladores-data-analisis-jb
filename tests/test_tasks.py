import json


def get_token(client, username="carol", password="secret"):
    client.post(
        "/v1/auth/register",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )
    resp = client.post(
        "/v1/auth/login",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )
    data = resp.get_json()
    return data["data"]["access_token"]


def test_create_and_list_tasks(client):
    token = get_token(client)
    # create task
    resp = client.post(
        "/v1/tareas",
        data=json.dumps({"title": "Task 1", "description": "Desc"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["code"] == 0
    assert data["data"]["title"] == "Task 1"

    # list tasks
    resp = client.get("/v1/tareas", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1


def test_task_not_found_returns_404(client):
    token = get_token(client, username="dave")
    resp = client.get("/v1/tareas/9999", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404


def test_update_and_delete_task(client):
    token = get_token(client, username="eve")
    # create
    resp = client.post(
        "/v1/tareas",
        data=json.dumps({"title": "To update"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    task_id = resp.get_json()["data"]["id"]

    # update
    resp = client.put(
        f"/v1/tareas/{task_id}",
        data=json.dumps({"title": "Updated"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["data"]["title"] == "Updated"

    # delete
    resp = client.delete(f"/v1/tareas/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["data"]["id"] == task_id

