"""Transparent risk engine.

Combines AI confidence, severity, sensor anomaly, environmental conditions and
historical occurrence into a 0-100 risk score with a per-factor breakdown so the
UI can explain the score. This is a prototype formula, NOT a validated
agricultural model.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskBreakdown:
    ai_contribution: float
    severity_contribution: float
    sensor_contribution: float
    environment_contribution: float
    history_contribution: float
    total: float

    def as_dict(self) -> dict:
        return {
            "ai_contribution": round(self.ai_contribution, 1),
            "severity_contribution": round(self.severity_contribution, 1),
            "sensor_contribution": round(self.sensor_contribution, 1),
            "environment_contribution": round(self.environment_contribution, 1),
            "history_contribution": round(self.history_contribution, 1),
            "total": round(self.total, 1),
        }


# Weights sum to 1.0.
WEIGHTS = {
    "ai": 0.30,
    "severity": 0.20,
    "sensor": 0.20,
    "environment": 0.15,
    "history": 0.15,
}

SEVERITY_SCORE = {"Low": 15.0, "Medium": 40.0, "High": 70.0, "Critical": 95.0}


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def compute_risk(
    ai_confidence: float,
    severity: str,
    sensor_anomaly: float,
    environment_stress: float,
    history_frequency: float,
) -> RiskBreakdown:
    """Compute a 0-100 risk score with a transparent per-factor breakdown.

    All inputs are 0-100. The output is a weighted sum, clamped to 0-100.
    """
    sev = SEVERITY_SCORE.get(severity, 40.0)

    ai_c = _clamp(ai_confidence) * WEIGHTS["ai"]
    sev_c = _clamp(sev) * WEIGHTS["severity"]
    sen_c = _clamp(sensor_anomaly) * WEIGHTS["sensor"]
    env_c = _clamp(environment_stress) * WEIGHTS["environment"]
    his_c = _clamp(history_frequency) * WEIGHTS["history"]

    total = _clamp(ai_c + sev_c + sen_c + env_c + his_c)
    return RiskBreakdown(
        ai_contribution=ai_c,
        severity_contribution=sev_c,
        sensor_contribution=sen_c,
        environment_contribution=env_c,
        history_contribution=his_c,
        total=total,
    )


def risk_band(score: float) -> str:
    """Map a 0-100 score to a health band."""
    if score <= 30:
        return "Healthy"
    if score <= 50:
        return "Watch"
    if score <= 75:
        return "At Risk"
    return "Critical"


def severity_from_confidence(confidence: float) -> str:
    """Map AI confidence to a severity label."""
    if confidence >= 90:
        return "High"
    if confidence >= 75:
        return "Medium"
    return "Low"
