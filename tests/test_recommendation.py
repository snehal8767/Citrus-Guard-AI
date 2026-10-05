"""Recommendation endpoint tests: structured dosage-free action plan."""


def test_recommendation_after_scan(client, auth_headers):
    client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    r = client.get("/zones/2/recommendation", headers=auth_headers)
    assert r.status_code == 200
    rec = r.json()
    assert rec["zone_name"] == "B"
    assert rec["health_status"] == "Critical"
    assert rec["condition"] == "Possible Citrus Disease Stress"
    assert rec["risk"] == 82.0
    assert rec["affected_area"] > 0
    assert len(rec["steps"]) == 5
    assert rec["steps"][0].startswith("Step 1:")
    assert "pesticide" in rec["safety_note"].lower()
    assert "dose" not in " ".join(rec["steps"]).lower()


def test_recommendation_fallback_without_scan(client, auth_headers):
    r = client.get("/zones/3/recommendation", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["condition"] == "Suspected disease/stress"
    assert len(r.json()["steps"]) == 5


def test_recommendation_unknown_zone_404(client, auth_headers):
    assert client.get("/zones/999/recommendation", headers=auth_headers).status_code == 404


def test_recommendation_requires_auth(client):
    assert client.get("/zones/2/recommendation").status_code == 401
