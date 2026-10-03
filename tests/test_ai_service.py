"""AI service tests: preprocessing, features, classifier, image analysis."""
import cv2
import numpy as np

from app.ai import features as feat
from app.ai import preprocessing as pre
from app.ai.service import AIService


def _green_image_bytes() -> bytes:
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = (40, 180, 60)  # green BGR
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return buf.tobytes()


def _brown_image_bytes() -> bytes:
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = (40, 100, 150)  # brownish BGR
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return buf.tobytes()


def test_preprocess_returns_all_views():
    out = pre.preprocess(_green_image_bytes())
    assert set(out) == {"bgr", "hsv", "lab", "gray", "bgr_norm"}
    assert out["bgr"].shape == (128, 128, 3)


def test_preprocess_rejects_garbage():
    try:
        pre.preprocess(b"this is not an image")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_extract_features_shape_and_names():
    vec = feat.extract_features(pre.preprocess(_green_image_bytes()))
    assert vec.shape == (len(feat.FEATURE_NAMES),)
    assert len(feat.FEATURE_NAMES) == 10


def test_analyze_image_returns_all_fields():
    svc = AIService()
    res = svc.analyze_image(_green_image_bytes())
    for field in ("condition", "confidence", "severity", "explanation", "next_step", "model_type"):
        assert field in res, f"missing {field}"
    assert 0 <= res["confidence"] <= 100
    assert res["severity"] in ("Low", "Medium", "High")


def test_analyze_different_images_valid():
    svc = AIService()
    for blob in (_green_image_bytes(), _brown_image_bytes()):
        res = svc.analyze_image(blob)
        assert res["condition"] in (
            "Healthy", "Pest Stress", "Disease Stress", "Water Stress", "Nutrient Stress"
        )


def test_analyze_zone_risk():
    svc = AIService()
    out = svc.analyze_zone(
        ai_confidence=91.0,
        severity="High",
        sensor_anomaly=85.0,
        environment_stress=70.0,
        history_frequency=80.0,
    )
    assert 0 <= out["risk_score"] <= 100
    assert out["risk_band"] in ("Healthy", "Watch", "At Risk", "Critical")
    assert "breakdown" in out
