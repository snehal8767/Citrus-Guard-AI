"""Health endpoint tests."""


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["version"] == "1.0.0"
    assert body["demo_mode"] is True


def test_root_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["name"] == "CitrusGuardAI"
