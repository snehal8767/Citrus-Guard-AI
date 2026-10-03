# Precision Agriculture

## Principle: treat the zone, not the farm

When Zone B (6.25 ac) is flagged, the intervention plan covers 6.25 acres — 12.5% of the 50-acre estate. The Intervention page shows this comparison explicitly so the farmer sees input savings versus blanket treatment.

## Guardrails

1. **Verified-alert gate.** `POST /interventions` rejects (400) unless a Verified alert exists for the zone. The AI proposes; the human disposes.
2. **No dosage.** The system never states pesticide names, quantities, or spray schedules. Intervention types are actions ("targeted canopy inspection", "localized irrigation adjustment", "pruning and sanitation", "follow-up monitoring").
3. **State-tracked.** A verified alert moves to Action Planned when a plan is created, then Resolved — full audit trail in `farmer_verifications`.

## Why this matters for Vidarbha

Citrus input costs (sprays, labour, water) dominate margins. Zone-level action cuts treated area by up to ~87% in the demo scenario, and the history table lets the farmer compare recovery across zones over seasons. These are demo illustrations, not yield guarantees.
