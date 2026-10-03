"""Train the demo classifier on SYNTHETIC feature data and save it to disk.

This is a demo model. It is NOT trained on real field data and must NOT be
presented as scientifically validated. It exists so the full pipeline
(preprocessing -> features -> classifier -> risk) runs end to end.
"""
from __future__ import annotations

import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from app.ai.features import FEATURE_NAMES
from app.ai.predictor import CONDITION_CLASSES, model_path

# Synthetic class centroids in feature space (roughly separated so the
# classifier learns a decision boundary). Order matches CONDITION_CLASSES.
# Features: hue_mean, hue_std, sat_mean, val_mean, green_ratio, brown_ratio,
#           dark_ratio, texture_contrast, lab_a_mean, lab_b_mean
CENTROIDS = {
    "Healthy":        [60, 18, 120, 150, 0.55, 0.05, 0.05, 22, 128, 145],
    "Pest Stress":    [45, 28, 100, 120, 0.35, 0.20, 0.15, 35, 135, 130],
    "Disease Stress": [30, 35, 90, 100, 0.25, 0.35, 0.25, 45, 145, 120],
    "Water Stress":   [70, 15, 80, 110, 0.30, 0.15, 0.30, 28, 125, 150],
    "Nutrient Stress":[80, 20, 110, 140, 0.40, 0.10, 0.10, 25, 130, 155],
}

SAMPLES_PER_CLASS = 200
NOISE = 12.0


def generate_synthetic_data(seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X, y = [], []
    for cls_idx, cls in enumerate(CONDITION_CLASSES):
        centroid = np.array(CENTROIDS[cls], dtype=np.float32)
        samples = centroid + rng.normal(0, NOISE, size=(SAMPLES_PER_CLASS, len(centroid)))
        X.append(samples)
        y.extend([cls_idx] * SAMPLES_PER_CLASS)
    return np.vstack(X).astype(np.float32), np.array(y)


def train() -> None:
    X, y = generate_synthetic_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"[train] Synthetic demo model trained. Hold-out accuracy: {acc:.3f}")
    print(f"[train] Features ({len(FEATURE_NAMES)}): {', '.join(FEATURE_NAMES)}")
    print("[train] NOTE: trained on synthetic data — demo only, not field-validated.")

    path = model_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle_bytes = __import__("pickle").dumps(clf)
        f.write(pickle_bytes)
    print(f"[train] Model saved to {path}")


if __name__ == "__main__":
    train()
