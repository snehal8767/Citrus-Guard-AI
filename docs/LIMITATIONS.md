# Limitations

1. **Synthetic AI.** The classifier trains on generated features; real leaves will look different. Treat every condition label as "demo output".
2. **Prototype risk formula.** Weights are reasonable guesses, not agronomy. Recalibration needed before any real decision.
3. **Simulated drone + sensors.** Telemetry and readings are generated; no hardware integration exists yet.
4. **Single-node SQLite.** Fine for demo; concurrent multi-user farm use wants Postgres.
5. **Upload analyses ARE recorded.** Every `POST /ai/analyze` saves an `image_analyses` row and `GET /ai/analyses` lists them (added Oct 2026). Uploaded files on disk are runtime data and gitignored.
6. **English-only UI.** Marathi localization (the language of Vidarbha farmers) is the highest-value UX gap.
7. **No offline mode.** Field connectivity is patchy; a real deployment needs on-device capture + sync.
8. **Coarse auth.** Two roles, no per-orchard permissions, no password reset.
9. **Report is HTML only.** PDF export (print stylesheet or weasyprint) is easy follow-up.
