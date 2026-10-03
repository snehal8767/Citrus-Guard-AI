# Cost Analysis (estimates, not quotes)

Bill of materials for a 50-acre pilot, rough INR estimates:

| Item | Estimate | Notes |
|---|---|---|
| Software (this stack) | ₹0 | Open-source; SQLite + OSM free |
| Laptop / local server | ₹40,000–60,000 | Already owned on most farms |
| Soil + microclimate nodes (8–16) | ₹3,000–6,000 each | ESP32 + capacitive moisture + DHT22 class |
| Gateway (phone hotspot / 4G dongle) | ₹2,000–4,000 | Plus data plan |
| Consumer drone + extra batteries | ₹80,000–1,50,000 | Entry mapping drone; optional at start (phone photos work) |
| Labour for scouting app use | existing staff | Farmer/operator time |

The expensive parts are hardware, not software — the whole point of this stack. Phone-photo uploads (`POST /ai/analyze`) give value before any drone or sensor is bought. These are back-of-envelope figures for discussion, not procurement quotes.
