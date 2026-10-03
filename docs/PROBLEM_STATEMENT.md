# Problem Statement

## Context: Vidarbha's orange economy

Vidarbha (Nagpur, Amravati, Wardha belt) produces India's best-known mandarins (Nagpur Santra). Orchards of 20–100+ acres are common. Profitability swings on early pest/disease control, water management, and input costs.

## The problems

1. **Late detection.** A farmer walking 50 acres spots disease days after it spreads. Citrus psylla, canker, gummosis, and phytophthora move fast in Vidarbha's hot-humid monsoon window.
2. **Blanket spraying.** Without zone-level diagnosis, the whole orchard gets sprayed — wasting chemicals, money, and harming beneficial insects.
3. **No records.** Spray dates, affected patches, and recovery are kept in memory or paper notebooks. There is no trend to learn from.
4. **Sensor blindness.** Soil-moisture probes and weather data (where they exist) are never fused with visual observations.
5. **Cost barrier.** Commercial precision-ag platforms are priced for large agribusiness, not Indian family orchards.

## What a good solution needs

- Zone-level monitoring (not whole-farm averages)
- Early, explainable stress detection with a confidence score
- Alerts a farmer can confirm or reject (no autonomous spraying, ever)
- Precision action limited to the affected area
- Full history + reports for learning and (later) agronomist review
- Low cost: open-source stack, no paid APIs, runs on a basic laptop

CitrusGuardAI is a **working prototype** of exactly that loop: scan → detect → alert → verify → act precisely → record.
