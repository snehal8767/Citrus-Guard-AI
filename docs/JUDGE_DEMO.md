# Judge Demo Checklist

Run through once, in order, before presenting:

- [ ] Backend up: `/health` returns `{"status":"ok","demo_mode":true}`
- [ ] Frontend up at :5173, login as farmer works
- [ ] `seed --reset` run → Dashboard shows 14-day history charts
- [ ] RUN ORCHARD SCAN → Zone B Critical 82/100, alert appears
- [ ] Map: Zone B red, detail panel complete
- [ ] Alert Center: VERIFY flips status to Verified
- [ ] Intervention: plan created for Zone B only; confirm unverified zone gives a clear error
- [ ] Command Console: `run scan`, `show zone B risk`, `list alerts` all answer
- [ ] Reports: HTML downloads and opens
- [ ] `/docs` loads; `/health`, login, scan callable from Swagger
- [ ] Tests: `pytest tests -q` and `npm test` green (run morning-of)
- [ ] Backup: screenshots in `docs/screenshots/` if the network dies (map tiles need internet)
- [ ] Say the honesty lines: synthetic model, simulated drone, prototype risk, no dosage
