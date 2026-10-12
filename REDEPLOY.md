# Redeploying CitrusGuardAI

Plain-language guide for updating the live app after a code change.

## Live URLs

| What | URL |
|---|---|
| Frontend (Vercel) | https://citrus-guard-ai.vercel.app |
| Backend (Render) | https://citrus-guard-ai.onrender.com |
| API docs | https://citrus-guard-ai.onrender.com/docs |

Demo logins: `farmer` / `farmer123` (farmer) · `operator` / `operator123` (operator)

## The 3-minute flow

1. Edit your code in VS Code.
2. Run the tests first (must stay green):
   - Backend (from repo root): `backend\.venv\Scripts\python.exe -m pytest tests -q`
   - Frontend (from `frontend\`): `npm test`
3. In the VS Code terminal, one line at a time:
   ```powershell
   git add -A
   git commit -m "short description of the change"
   git push
   ```
4. **Backend (Render):** render.com → Citrus-Guard-AI service → **Manual Deploy → Deploy latest commit**.
   (Auto-deploy is OFF for this service — you must click this every time.)
5. **Frontend (Vercel):** only if you changed files in `frontend/` → vercel.com →
   project → **Deployments** → latest → **⋯ → Redeploy** (uncheck "Use existing Build Cache"
   if you changed environment variables).
6. Check it works: open https://citrus-guard-ai.onrender.com/health —
   you should see `{"status":"ok","demo_mode":true}`.

## First boot after a fresh deploy

The backend migrates the database, seeds the demo orchard, and trains the demo
model **automatically at startup** (look for `[startup] ...` lines in the Render
Logs tab). On the free tier the first request after a deploy can take up to
~60 seconds — that is normal, just wait.

## Environment variables (already set — don't change)

**Render (backend):** `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`,
`DEMO_MODE`, `UPLOAD_DIR`

**Vercel (frontend):** `VITE_API_URL` = `https://citrus-guard-ai.onrender.com`

⚠️ `VITE_API_URL` is baked in at **build time** — after changing it you must
redeploy **without** the build cache.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "Failed to fetch" on the login page | `VITE_API_URL` missing/wrong on Vercel, or backend asleep | Check the Vercel env var. Free backend sleeps after 15 min — wait ~60 s and retry. |
| 404 `DEPLOYMENT_NOT_FOUND` | Old/dead Vercel deployment | Use the URL from Vercel dashboard → project → latest deployment. |
| CORS error in the browser console | Backend `CORS_ORIGINS` doesn't include your frontend URL | Render → Environment → set `CORS_ORIGINS=https://citrus-guard-ai.vercel.app,http://localhost:5173` → Save (auto-redeploys). |
| Login returns 500 | Fresh instance still bootstrapping | Wait ~60 s; check Render Logs for `[startup] Bootstrap complete.` |
| "Invalid transition: Verified -> Verified" | The alert was already verified (normal) | The UI hides the buttons for settled alerts — use the Intervention page instead. |
| Empty dashboard | Database empty (should not happen — startup seeds it) | Render Logs → look for `[seed] Done.` |

## Local run

```powershell
# Backend (from backend\)
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000

# Frontend (from frontend\)
npm run dev
```

App: http://localhost:5173 · API docs: http://localhost:8000/docs
