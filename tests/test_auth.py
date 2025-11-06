import json


def test_register_and_login(client):
    # Register a new user
    resp = client.post(
        "/v1/auth/register",
        data=json.dumps({"username": "alice", "password": "secret", "email": "alice@example.com"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["code"] == 0
    assert data["data"]["username"] == "alice"

    # Login with the user
    resp = client.post(
        "/v1/auth/login",
        data=json.dumps({"username": "alice", "password": "secret"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["code"] == 0
    assert "access_token" in data["data"]


def test_register_duplicate_username(client):
    # Register first
    client.post(
        "/v1/auth/register",
        data=json.dumps({"username": "bob", "password": "secret"}),
        content_type="application/json",
    )
    # Register duplicate
    resp = client.post(
        "/v1/auth/register",
        data=json.dumps({"username": "bob", "password": "secret2"}),
        content_type="application/json",
    )
    assert resp.status_code == 409 or resp.status_code == 400 or resp.status_code == 422

