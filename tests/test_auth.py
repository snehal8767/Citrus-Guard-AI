"""Auth tests: login success/failure, protected endpoints."""


def test_login_farmer(client):
    r = client.post("/auth/login", json={"username": "farmer", "password": "farmer123"})
    assert r.status_code == 200
    assert r.json()["role"] == "farmer"
    assert r.json()["access_token"]


def test_login_operator(client):
    r = client.post("/auth/login", json={"username": "operator", "password": "operator123"})
    assert r.status_code == 200
    assert r.json()["role"] == "operator"


def test_login_wrong_password(client):
    r = client.post("/auth/login", json={"username": "farmer", "password": "wrong"})
    assert r.status_code == 401


def test_login_unknown_user(client):
    r = client.post("/auth/login", json={"username": "nobody", "password": "x"})
    assert r.status_code == 401


def test_protected_requires_token(client):
    assert client.get("/orchards").status_code == 401
    assert client.get("/alerts").status_code == 401
    assert client.get("/metrics").status_code == 401


def test_protected_with_token(client, auth_headers):
    assert client.get("/orchards", headers=auth_headers).status_code == 200
