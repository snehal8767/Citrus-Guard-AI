"""Image preprocessing: decode, resize, normalise, colour-space conversion.

All functions are deterministic and side-effect free so the pipeline is
explainable and testable.
"""
from __future__ import annotations

import cv2
import numpy as np

# Canonical input size for the feature extractor.
TARGET_SIZE = (128, 128)


def decode_image(data: bytes) -> np.ndarray:
    """Decode raw image bytes into a BGR OpenCV array.

    Raises ValueError if the bytes are not a valid image.
    """
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Uploaded file is not a valid image")
    return img


def resize_image(img: np.ndarray, size: tuple[int, int] = TARGET_SIZE) -> np.ndarray:
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def to_hsv(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)


def to_lab(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)


def to_gray(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)


def normalise(img: np.ndarray) -> np.ndarray:
    """Scale pixel values to [0, 1]."""
    return img.astype(np.float32) / 255.0


def preprocess(data: bytes) -> dict[str, np.ndarray]:
    """Full preprocessing pipeline. Returns a dict of derived images."""
    img = decode_image(data)
    img = resize_image(img)
    return {
        "bgr": img,
        "hsv": to_hsv(img),
        "lab": to_lab(img),
        "gray": to_gray(img),
        "bgr_norm": normalise(img),
    }
