"""Command parser + misc endpoint tests."""


def test_help_lists_commands(client, auth_headers):
    r = client.post("/commands?orchard_id=1", json={"command": "help"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["intent"] == "help"
    assert "run scan" in r.json()["data"]["supported_commands"]


def test_unknown_command_returns_help(client, auth_headers):
    r = client.post("/commands?orchard_id=1", json={"command": "fly to the moon"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["intent"] == "help"


def test_command_zone_risk(client, auth_headers):
    r = client.post("/commands?orchard_id=1", json={"command": "show zone C risk"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["intent"] == "zone_risk"
    assert r.json()["data"]["zone_name"] == "C"


def test_command_list_zones(client, auth_headers):
    r = client.post("/commands?orchard_id=1", json={"command": "list zones"}, headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()["data"]) == 8


def test_command_run_scan(client, auth_headers):
    r = client.post("/commands?orchard_id=1", json={"command": "run scan"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["intent"] == "run_scan"


def test_metrics_endpoint(client, auth_headers):
    r = client.get("/metrics?orchard_id=1", headers=auth_headers)
    assert r.status_code == 200
    m = r.json()
    assert m["total_orchard_area"] == 50.0
    assert m["monitored_area"] == 50.0


def test_report_endpoint(client, auth_headers):
    r = client.get("/reports?orchard_id=1", headers=auth_headers)
    assert r.status_code == 200
    assert "Orchard Health Report" in r.text


def test_invalid_upload_rejected(client, auth_headers):
    r = client.post("/ai/analyze", files={"file": ("x.txt", b"nope", "text/plain")},
                    headers=auth_headers)
    assert r.status_code == 400


def test_orchard_crud(client, auth_headers):
    r = client.post("/orchards", json={"name": "Second", "area": 10.0}, headers=auth_headers)
    assert r.status_code == 201
    oid = r.json()["id"]
    assert client.get(f"/orchards/{oid}", headers=auth_headers).status_code == 200
    r = client.put(f"/orchards/{oid}", json={"area": 12.0}, headers=auth_headers)
    assert r.json()["area"] == 12.0
    assert client.delete(f"/orchards/{oid}", headers=auth_headers).status_code == 204
