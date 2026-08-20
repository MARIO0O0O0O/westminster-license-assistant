# Westminster Business License Assistant (WBLEPA) — Deployment Architecture Notes

This document captures the deployment choices, environment variables, hosting configurations, and automated maintenance workflows for public release.

---

## 1. Hosting Architecture & Service Split

1. **Backend Service (FastAPI)**:
   - **Host**: **Render** (Free Tier Web Service)
   - **Repository Branch**: `main`
   - **Configuration File**: [`render.yaml`](../../render.yaml)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Storage**: Persistent disk enabled for SQLite `data/corpus.db` state.

2. **Frontend Interface (Web UI)**:
   - **Host**: **Vercel** (Free Tier)
   - **Root Directory**: `src/ui/web`
   - **Environment Variable**: `NEXT_PUBLIC_API_URL` (points to Render production URL)

---

## 2. Environment Variables & Secrets

| Location | Variable Name | Purpose | Value Example |
| :---: | :--- | :--- | :--- |
| **Render Dashboard** | `GEMINI_API_KEY` | Google Gemini API Authentication Key | `AIzaSy...` (Kept secret, out of git) |
| **Render Dashboard** | `PYTHON_VERSION` | Runtime Python Environment | `3.11.0` |
| **Vercel Dashboard** | `NEXT_PUBLIC_API_URL` | Live Backend Endpoint for Web UI | `https://wblepa-backend.onrender.com` |
| **Local Termux CLI** | `WBLEPA_API_URL` | CLI Target Endpoint Toggle | `http://127.0.0.1:8000` or Render URL |

---

## 3. Scraper Refresh Automation

- **Workflow File**: [`.github/workflows/refresh_corpus.yml`](../../.github/workflows/refresh_corpus.yml)
- **Schedule**: Every Sunday at midnight UTC (`cron: '0 0 * * 0'`) + manual trigger (`workflow_dispatch`).
- **Function**: Executes `python src/scraper/refresh_all.py`, validates chunk counts with `test_corpus_spotcheck.py`, and commits updated snapshots to GitHub if changes are detected.

---

## 4. CORS & Security Setup

- Backend CORS is restricted in [`src/api/main.py`](../../src/api/main.py) to:
  - `http://localhost:3000` / `http://127.0.0.1:3000` (Local dev)
  - `http://localhost:8000` / `http://127.0.0.1:8000` (Local API & Swagger docs)
  - `https://westminster-license-assistant.vercel.app` (Vercel production UI)
