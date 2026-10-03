"""Scan flow tests: POST /scans deterministically flags Zone B."""


def test_scan_creates_zone_b_detection(client, auth_headers):
    r = client.post("/scans", json={"orchard_id": 1, "scan_type": "drone_simulation"},
                    headers=auth_headers)
    assert r.status_code == 201
    scan = r.json()
    assert scan["coverage"] > 0
    assert len(scan["detections"]) == 8

    zone_b = [d for d in scan["detections"] if d["zone_id"] == 2]
    assert len(zone_b) == 1
    d = zone_b[0]
    assert d["condition"] == "Possible Citrus Disease Stress"
    assert d["confidence"] == 91.0
    assert d["severity"] == "High"


def test_scan_creates_alert_with_risk_82(client, auth_headers):
    client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    r = client.get("/alerts", headers=auth_headers)
    assert r.status_code == 200
    zone_b_alerts = [a for a in r.json() if a["zone_id"] == 2]
    assert zone_b_alerts
    assert zone_b_alerts[-1]["risk_score"] == 82.0
    assert zone_b_alerts[-1]["status"] == "New"


def test_scan_updates_zone_health(client, auth_headers):
    client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    r = client.get("/zones?orchard_id=1", headers=auth_headers)
    zone_b = [z for z in r.json() if z["zone_name"] == "B"][0]
    assert zone_b["risk_score"] == 82.0
    assert zone_b["health_status"] == "Critical"


def test_scan_appends_history(client, auth_headers):
    client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    r = client.get("/history?orchard_id=1", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 8  # one record per zone


def test_scan_unknown_orchard_404(client, auth_headers):
    r = client.post("/scans", json={"orchard_id": 999}, headers=auth_headers)
    assert r.status_code == 404


def test_list_scans(client, auth_headers):
    client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    r = client.get("/scans?orchard_id=1", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
