"""Predictor interface and the scikit-learn demo classifier.

The Predictor protocol is the clean seam where a real field-trained model can
later replace the synthetic demo classifier without touching the rest of the app.
"""
from __future__ import annotations

import os
import pickle
from typing import Protocol

import numpy as np

from app.core.config import get_settings

# Condition classes the demo classifier can predict.
CONDITION_CLASSES = [
    "Healthy",
    "Pest Stress",
    "Disease Stress",
    "Water Stress",
    "Nutrient Stress",
]

MODEL_FILENAME = "demo_model.joblib"


def model_path() -> str:
    settings = get_settings()
    return os.path.join(settings.upload_dir, MODEL_FILENAME)


class Predictor(Protocol):
    """Interface any crop-health predictor must implement."""

    def predict(self, features: np.ndarray) -> dict:
        """Return {'condition': str, 'confidence': float (0-100)}."""
        ...


class SklearnDemoPredictor:
    """Wraps a pickled scikit-learn classifier trained on synthetic features."""

    def __init__(self, path: str | None = None):
        self.path = path or model_path()
        self._model = None
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            raise FileNotFoundError(
                f"Demo model not found at {self.path}. Run: python -m app.ai.train_demo_model"
            )
        with open(self.path, "rb") as f:
            self._model = pickle.load(f)

    def predict(self, features: np.ndarray) -> dict:
        X = features.reshape(1, -1)
        proba = self._model.predict_proba(X)[0]
        idx = int(np.argmax(proba))
        condition = CONDITION_CLASSES[idx] if idx < len(CONDITION_CLASSES) else "Unknown"
        confidence = round(float(proba[idx]) * 100, 1)
        return {"condition": condition, "confidence": confidence}


def get_predictor() -> Predictor:
    return SklearnDemoPredictor()
