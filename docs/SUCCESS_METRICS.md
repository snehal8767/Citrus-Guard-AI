# Success Metrics

How to tell the demo (and later a pilot) is working. All demo targets below were met and are covered by tests.

## Demo success (this build)

- [x] Login → scan → Zone B flagged → alert → verify → intervention → report, repeatable after reset
- [x] Zone B values exact: "Possible Citrus Disease Stress", 91%, High, 82/100
- [x] Every dashboard number from the database (no hardcoded KPIs — grep-verified)
- [x] Invalid upload, invalid transition, and unverified intervention all rejected with clear errors
- [x] 57 backend + 20 frontend tests green; `npm run build` clean

## Pilot success (future field deployment — illustrative)

- Detection lead time: flag stress ≥3 days before visual scouting would
- Spray-area reduction: % of orchard treated vs blanket baseline
- Verification latency: median minutes from alert to farmer decision
- False-alert rate: rejected alerts / total alerts per month
- Data completeness: scans with full sensor + imagery coverage

## Anti-metrics (we do NOT claim)

Yield uplift %, guaranteed pesticide reduction, diagnostic accuracy % — none of these are measured or claimed. The model is synthetic and the risk formula is a prototype.
