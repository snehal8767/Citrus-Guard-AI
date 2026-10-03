"""Feature extraction from preprocessed images.

Produces a fixed-length numeric feature vector that the classifier consumes.
Features are deliberately simple and explainable: colour histograms, greenness
ratio, texture (local std-dev) and a lesion proxy (dark/brown pixel fraction).
"""
from __future__ import annotations

import cv2
import numpy as np

from app.ai.preprocessing import TARGET_SIZE

# Feature names in canonical order — the classifier is trained on this order.
FEATURE_NAMES = [
    "hue_mean",
    "hue_std",
    "sat_mean",
    "val_mean",
    "green_ratio",
    "brown_ratio",
    "dark_ratio",
    "texture_contrast",
    "lab_a_mean",
    "lab_b_mean",
]


def _hist_stats(channel: np.ndarray) -> tuple[float, float]:
    hist = cv2.calcHist([channel], [0], None, [16], [0, 180]).flatten()
    hist = hist / (hist.sum() + 1e-9)
    centers = np.arange(16) * (180 / 16) + (180 / 32)
    mean = float(np.sum(hist * centers))
    std = float(np.sqrt(np.sum(hist * (centers - mean) ** 2)))
    return mean, std


def extract_features(preprocessed: dict[str, np.ndarray]) -> np.ndarray:
    """Return a (10,) float32 feature vector."""
    hsv = preprocessed["hsv"]
    lab = preprocessed["lab"]
    gray = preprocessed["gray"]

    h, s, v = cv2.split(hsv)
    hue_mean, hue_std = _hist_stats(h)
    sat_mean = float(s.mean())
    val_mean = float(v.mean())

    # Greenness: fraction of pixels whose hue is in the green band (35-85 OpenCV hue).
    green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    green_ratio = float(np.count_nonzero(green_mask) / green_mask.size)

    # Brown/dark lesion proxy: low value + moderate saturation.
    brown_mask = cv2.inRange(hsv, (5, 60, 30), (25, 255, 180))
    brown_ratio = float(np.count_nonzero(brown_mask) / brown_mask.size)

    dark_mask = v < 60
    dark_ratio = float(np.count_nonzero(dark_mask) / dark_mask.size)

    # Texture: local standard deviation of the grayscale image.
    mean, std = cv2.meanStdDev(gray)
    texture_contrast = float(std[0][0])

    l, a, b = cv2.split(lab)
    lab_a_mean = float(a.mean())
    lab_b_mean = float(b.mean())

    vec = np.array(
        [
            hue_mean,
            hue_std,
            sat_mean,
            val_mean,
            green_ratio,
            brown_ratio,
            dark_ratio,
            texture_contrast,
            lab_a_mean,
            lab_b_mean,
        ],
        dtype=np.float32,
    )
    return vec
