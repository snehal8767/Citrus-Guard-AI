# Field Validation (not done — roadmap)

Be explicit with judges: **nothing here is field-validated.** The classifier never saw a real leaf; the risk weights are guesses; sensor values are simulated.

## What validation would require

1. **Labelled imagery.** ≥1,000 geotagged leaf/canopy photos per class, labelled by a plant pathologist, across seasons (Vidarbha summer vs monsoon look different).
2. **Sensor ground truth.** Calibrated probes vs lab soil tests; leaf-wetness sensors vs observed drying times.
3. **Risk-weight calibration.** Fit weights to historical outbreak records (e.g. past phytophthora events vs sensor logs), then freeze and back-test.
4. **Pilot protocol.** 2–3 orchards, one season: system recommendations vs agronomist recommendations, blinded; measure lead time and false-alert rate.
5. **Safety review.** Any chemical advice needs a licensed agronomist sign-off — the system must stay dosage-free regardless.

## What is already validation-friendly

- `Predictor` protocol: retrain on real data, drop the file in, no code changes.
- Every prediction is stored with confidence + explanation → ready-made audit dataset.
- Verification decisions (`farmer_verifications`) are free labels for retraining.
