# AI / ML

## Pipeline

```
image bytes → decode → resize 128×128 → HSV/LAB/gray
  → 10 features (hue stats, saturation, value, green ratio,
     brown-lesion ratio, dark ratio, texture, Lab a/b means)
  → RandomForest (synthetic-trained) → condition + confidence
  → severity → risk engine → recommendation
```

## Classes

Healthy, Pest Stress, Disease Stress, Water Stress, Nutrient Stress.

## Training

`python -m app.ai.train_demo_model` generates 200 synthetic samples per class around hand-set centroids, trains a 120-tree RandomForest, prints hold-out accuracy (~0.85), and saves `data/uploads/demo_model.joblib`. **Synthetic = demo only.**

## Predictor protocol

```python
class Predictor(Protocol):
    def predict(self, features: np.ndarray) -> dict: ...
```

`SklearnDemoPredictor` implements it; `AIService` depends on the protocol, so a real field-trained model (e.g. a CNN exported to ONNX) replaces it without touching routes or services.

## Risk engine (prototype, not agronomy)

Weighted sum, clamped 0–100:

| Factor | Weight |
|---|---|
| AI confidence | 0.30 |
| Severity (Low 15 / Med 40 / High 70 / Crit 95) | 0.20 |
| Sensor anomaly | 0.20 |
| Environmental stress | 0.15 |
| Historical occurrence | 0.15 |

Bands: 0–30 Healthy · 31–50 Watch · 51–75 At Risk · 76–100 Critical. The API returns the per-factor breakdown; the UI can explain every point.

## Demo mode

`DEMO_MODE=true` (in `.env`): the official orchard scan bypasses the classifier for Zone B and returns the fixed story (condition "Possible Citrus Disease Stress", 91%, High, 82/100). Uploaded images always use the real pipeline. This split is deliberate: repeatable judging + honest ML path.
