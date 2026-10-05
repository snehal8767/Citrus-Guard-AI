"""Image analysis persistence tests: every upload is recorded."""
import cv2
import numpy as np


def _leaf_jpg() -> bytes:
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = (40, 180, 60)
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return buf.tobytes()


def test_analyze_persists_record(client, auth_headers):
    r = client.post("/ai/analyze",
                    files={"file": ("leaf.jpg", _leaf_jpg(), "image/jpeg")},
                    headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert "id" in body
    for field in ("condition", "confidence", "severity", "explanation", "next_step"):
        assert field in body


def test_analyses_list_shows_uploads(client, auth_headers):
    r = client.post("/ai/analyze",
                    files={"file": ("leaf.jpg", _leaf_jpg(), "image/jpeg")},
                    headers=auth_headers)
    record_id = r.json()["id"]
    r = client.get("/ai/analyses", headers=auth_headers)
    assert r.status_code == 200
    assert any(a["id"] == record_id and a["filename"] == "leaf.jpg" for a in r.json())


def test_analyses_require_auth(client):
    assert client.get("/ai/analyses").status_code == 401
