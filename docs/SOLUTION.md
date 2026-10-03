# Solution

## The loop

```
SCAN → DETECT → RISK-SCORE → ALERT → FARMER VERIFIES → PRECISION PLAN → HISTORY → REPORT
```

## How each problem is addressed

| Problem | CitrusGuardAI answer |
|---|---|
| Late detection | Scheduled drone-simulation scans + on-demand image analysis; Zone B demo shows the full flag-to-alert path |
| Blanket spraying | Intervention plans target one 6.25-acre zone; UI shows precision vs full-orchard area side by side |
| No records | Every scan/detection/verification/intervention is stored; History page + downloadable report |
| Sensor blindness | Sensor readings fused into the risk engine; Sensors page shows status vs normal ranges |
| Cost barrier | 100% open-source stack; SQLite + OpenStreetMap = zero running cost |

## Key design choices

- **Deterministic demo.** The official scan always flags Zone B with the same values, so the story is repeatable for judges. Real uploaded images go through the genuine ML pipeline instead.
- **Human-in-the-loop as a constraint, not a feature.** The server refuses interventions without a Verified alert (`POST /interventions` returns 400). This is tested.
- **Explainability over accuracy claims.** The risk score ships with a per-factor breakdown; the UI shows it. No "100% accurate" claims anywhere.
- **Replaceable AI.** The `Predictor` protocol means a field-trained model drops in without touching routes or services.

## What it is not (yet)

Not a validated disease diagnostic, not drone control software, not a pesticide advisor. See LIMITATIONS.md and FIELD_VALIDATION.md.
