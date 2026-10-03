"""Risk engine tests: determinism, weighting, bands."""
import pytest

from app.ai.risk import compute_risk, risk_band, severity_from_confidence


def test_demo_values_give_high_risk():
    # Max inputs: 100*0.3 + 95*0.2 + 100*0.2 + 100*0.15 + 100*0.15 = 99.
    # (Critical severity maps to 95, not 100.)
    b = compute_risk(100, "Critical", 100, 100, 100)
    assert b.total == pytest.approx(99.0)


def test_zero_inputs_give_low_risk():
    b = compute_risk(0, "Low", 0, 0, 0)
    # severity Low contributes 15 * 0.2 = 3.0
    assert b.total == pytest.approx(3.0)


def test_breakdown_sums_to_total():
    b = compute_risk(91, "High", 85, 70, 80)
    parts = (b.ai_contribution + b.severity_contribution + b.sensor_contribution
             + b.environment_contribution + b.history_contribution)
    assert parts == pytest.approx(b.total)
    assert 0 <= b.total <= 100


def test_deterministic():
    a = compute_risk(91, "High", 85, 70, 80)
    c = compute_risk(91, "High", 85, 70, 80)
    assert a.as_dict() == c.as_dict()


def test_bands():
    assert risk_band(0) == "Healthy"
    assert risk_band(30) == "Healthy"
    assert risk_band(31) == "Watch"
    assert risk_band(50) == "Watch"
    assert risk_band(51) == "At Risk"
    assert risk_band(75) == "At Risk"
    assert risk_band(76) == "Critical"
    assert risk_band(82) == "Critical"
    assert risk_band(100) == "Critical"


def test_severity_mapping():
    assert severity_from_confidence(95) == "High"
    assert severity_from_confidence(80) == "Medium"
    assert severity_from_confidence(50) == "Low"
