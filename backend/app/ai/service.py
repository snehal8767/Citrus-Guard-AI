"""High-level AI service: image analysis and zone risk analysis.

This is the single entry point the API layer calls. It orchestrates
preprocessing -> feature extraction -> classification -> risk scoring.
"""
from __future__ import annotations

import numpy as np

from app.ai import features as feat
from app.ai import preprocessing as pre
from app.ai.predictor import Predictor, get_predictor
from app.ai.risk import RiskBreakdown, compute_risk, risk_band, severity_from_confidence


class AIService:
    def __init__(self, predictor: Predictor | None = None):
        self.predictor = predictor or get_predictor()

    def analyze_image(self, image_bytes: bytes) -> dict:
        """Run the full pipeline on an uploaded image.

        Returns condition, confidence, severity, explanation and next step.
        """
        preprocessed = pre.preprocess(image_bytes)
        vector = feat.extract_features(preprocessed)
        result = self.predictor.predict(vector)
        condition = result["condition"]
        confidence = result["confidence"]
        severity = severity_from_confidence(confidence)
        explanation = self._explain(condition, vector)
        next_step = self._next_step(condition, severity)
        return {
            "condition": condition,
            "confidence": confidence,
            "severity": severity,
            "explanation": explanation,
            "next_step": next_step,
            "model_type": "synthetic_demo_rf",
        }

    def analyze_zone(
        self,
        ai_confidence: float,
        severity: str,
        sensor_anomaly: float,
        environment_stress: float,
        history_frequency: float,
    ) -> dict:
        """Compute a transparent risk score for a zone."""
        breakdown = compute_risk(
            ai_confidence, severity, sensor_anomaly, environment_stress, history_frequency
        )
        return {
            "risk_score": round(breakdown.total, 1),
            "risk_band": risk_band(breakdown.total),
            "breakdown": breakdown.as_dict(),
        }

    @staticmethod
    def _explain(condition: str, vector: np.ndarray) -> str:
        names = feat.FEATURE_NAMES
        d = dict(zip(names, vector))
        if condition == "Healthy":
            return (
                f"Canopy appears healthy (green ratio {d['green_ratio']:.2f}, "
                f"low lesion proxy {d['brown_ratio']:.2f})."
            )
        if condition == "Disease Stress":
            return (
                f"Elevated lesion/brown pixel ratio ({d['brown_ratio']:.2f}) and "
                f"reduced greenness ({d['green_ratio']:.2f}) suggest possible disease stress."
            )
        if condition == "Water Stress":
            return (
                f"Low value/brightness ({d['val_mean']:.0f}) and high dark ratio "
                f"({d['dark_ratio']:.2f}) are consistent with water stress."
            )
        if condition == "Pest Stress":
            return (
                f"Texture contrast ({d['texture_contrast']:.1f}) and colour distribution "
                f"suggest possible pest damage."
            )
        return (
            f"Colour profile (hue mean {d['hue_mean']:.0f}) suggests possible nutrient deficiency."
        )

    @staticmethod
    def _next_step(condition: str, severity: str) -> str:
        if condition == "Healthy":
            return "Continue routine monitoring."
        if severity == "High":
            return "Verify affected trees before intervention."
        if severity == "Medium":
            return "Monitor closely and schedule a follow-up scan."
        return "Observe and recheck at next scheduled scan."


def get_ai_service() -> AIService:
    return AIService()
