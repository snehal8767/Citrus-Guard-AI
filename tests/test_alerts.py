"""Alert tests: state transitions, verification, intervention guard."""


def _scan(client, auth_headers):
    r = client.post("/scans", json={"orchard_id": 1}, headers=auth_headers)
    assert r.status_code == 201


def _zone_b_alert_id(client, auth_headers) -> int:
    r = client.get("/alerts", headers=auth_headers)
    alerts = [a for a in r.json() if a["zone_id"] == 2 and a["status"] == "New"]
    assert alerts
    return alerts[-1]["id"]


def test_verify_transitions_to_verified(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    r = client.post(f"/alerts/{alert_id}/verify",
                    json={"decision": "verify", "comment": "confirmed"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "Verified"


def test_reject_transitions_to_rejected(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    r = client.post(f"/alerts/{alert_id}/reject",
                    json={"decision": "reject"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "Rejected"


def test_rescan_transitions_to_rescan_requested(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    r = client.post(f"/alerts/{alert_id}/rescan",
                    json={"decision": "rescan"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "Rescan Requested"


def test_invalid_transition_rejected(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    # Verify first (New -> Verified), then verify again (Verified -> Verified is invalid).
    client.post(f"/alerts/{alert_id}/verify", json={"decision": "verify"}, headers=auth_headers)
    r = client.post(f"/alerts/{alert_id}/verify", json={"decision": "verify"}, headers=auth_headers)
    assert r.status_code == 400
    assert "Invalid transition" in r.json()["detail"]


def test_unknown_decision_rejected(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    r = client.post(f"/alerts/{alert_id}/verify",
                    json={"decision": "maybe"}, headers=auth_headers)
    assert r.status_code == 400


def test_intervention_requires_verified_alert(client, auth_headers):
    _scan(client, auth_headers)
    # Zone 3 has no alert at all -> must be rejected.
    r = client.post("/interventions", json={
        "zone_id": 3, "intervention_type": "X", "target_area": 1.0}, headers=auth_headers)
    assert r.status_code == 400
    assert "Verified" in r.json()["detail"]


def test_intervention_after_verify(client, auth_headers):
    _scan(client, auth_headers)
    alert_id = _zone_b_alert_id(client, auth_headers)
    client.post(f"/alerts/{alert_id}/verify", json={"decision": "verify"}, headers=auth_headers)
    r = client.post("/interventions", json={
        "zone_id": 2,
        "intervention_type": "Targeted canopy inspection and treatment",
        "target_area": 6.25,
    }, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["target_area"] == 6.25
    # Alert advanced to Action Planned.
    r = client.get(f"/alerts/{alert_id}", headers=auth_headers)
    assert r.json()["status"] == "Action Planned"


def test_intervention_unverified_new_alert_rejected(client, auth_headers):
    _scan(client, auth_headers)
    # Zone B alert is still New (not verified) -> rejected.
    r = client.post("/interventions", json={
        "zone_id": 2, "intervention_type": "X", "target_area": 1.0}, headers=auth_headers)
    assert r.status_code == 400
