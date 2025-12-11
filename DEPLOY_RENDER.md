Render deployment guide for covid-vaccine-tracker

Overview
--------
This repository contains a Streamlit frontend (`app/streamlit_app.py`) and a FastAPI backend (`app/api`). Use Render to host the FastAPI backend and Streamlit Cloud (already hosting) to serve the frontend.

Prepare repo
------------
1. Ensure `requirements.txt` contains `fastapi`, `uvicorn[standard]`, `pydantic`, etc. (already included).
2. Add `render.yaml` (optional) or create the service via Render web UI.
3. Add a `.env` on Render with required values (do NOT commit secrets).

Quick Render UI steps
---------------------
1. Sign in at https://dashboard.render.com and click "New" → "Web Service".
2. Connect your GitHub and select the `Mmaneesh007/covid-vaccine-tracker` repo and branch `main`.
3. For the root, choose the repository root (the FastAPI app is at `app/api` but the Python package root is `app`).
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.api.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables (in Render dashboard → Environment):
   - `API_KEY` (generate a strong key, same value can be set in Streamlit if required for tests)
   - `DATABASE_URL` (if using Postgres on Render set the connection URL here)
   - `ALLOWED_ORIGINS` (comma-separated list of allowed frontends)
7. Create the service and wait for build + deploy to finish. Note the service URL (e.g., `https://covid-vaccine-tracker-api.onrender.com`).

Using `render.yaml` (optional)
-----------------------------
You can include a `render.yaml` in the repo. Render will pick it up when creating a service via the web UI. Example snippet (already added to repo):

```
services:
  - type: web_service
    name: covid-vaccine-tracker-api
    env: python
    plan: free
    region: oregon
    branch: main
    rootDir: .
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.api.main:app --host 0.0.0.0 --port $PORT"
    autoDeploy: true
```

Notes about persistence
----------------------
- SQLite is file-based. Render's filesystem is ephemeral across deploys. For production use, provision a managed PostgreSQL database and set `DATABASE_URL` accordingly. If you keep SQLite, ensure you have a persistent disk service (Render offers persistent disks on some plans).

Update Streamlit Cloud
----------------------
1. In the Streamlit Cloud dashboard, open your app settings.
2. Add an env var `API_BASE_URL` with value: `https://<your-render-service>.onrender.com/api/v1`
3. Save and trigger a redeploy (Streamlit Cloud will redeploy automatically when it detects a change or when you re-run the app).

Verify
------
- Visit the Render service URL: `https://<your-render-service>.onrender.com/health` (or `/api/v1/health`) to confirm backend up.
- Visit your Streamlit public URL and check new features.
- If you see CORS errors, add the streamlit origin to `ALLOWED_ORIGINS` and redeploy.

Troubleshooting
---------------
- Build failures: check the build logs in Render to see pip install errors.
- Runtime errors: check the service logs on Render for stack traces.
- DB issues: switch to managed Postgres for reliability.

If you want, I can also:
- Create a `render.yaml` tuned to Render's schema and add deployment steps,
- Or attempt to create the Render service via the Render CLI (you must provide API key), or
- Walk you through the Render UI and set env vars manually.
