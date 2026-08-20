# Phase 7 - Deployment and Launch
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Ship the hardened MVP (Phase 6 passed 13/13) to free-tier public hosting, confirm the scraper refresh job runs on a schedule, and validate the live deployment end-to-end from both a browser and the Termux CLI. This is the phase where WBLEPA becomes a real, shareable, publicly accessible work sample.

## 2. Technical Approach (locked decisions)

### 2.1 Hosting split
- **Backend (FastAPI):** Deploy to **Render** free tier - supports long-running Python web services (unlike Vercel, which is optimized for serverless/edge functions and less suited to a persistent FastAPI + SQLite process). Render's free tier includes a persistent disk option needed to keep corpus.db intact between deploys.
- **Frontend (Next.js):** Deploy to **Vercel** free tier - the standard, zero-config choice for Next.js apps, consistent with your existing Vercel experience.
- **CORS update:** Update the Phase 6 CORS allow-list to include the final Vercel production URL once assigned.

### 2.2 Environment and secrets
- Move the Gemini API key from local `.env` into Render's environment variable dashboard (never committed to git).
- Set the frontend's API base URL environment variable to the deployed Render backend URL.

### 2.3 Scraper refresh scheduling
- Since Render free tier does not include native cron jobs on all plans, use a simple external trigger: either Render's built-in Cron Job feature (if available on free tier) or a GitHub Actions scheduled workflow (`.github/workflows/refresh_corpus.yml`) that runs `refresh_all.py` weekly and commits any corpus updates back to the repo.

## 3. Tasks for Antigravity

### 3.1 Backend deployment (Render)
- Create a `render.yaml` or use Render's dashboard to deploy the FastAPI app from the GitHub repo.
- Configure the Gemini API key and any other secrets as Render environment variables.
- Confirm persistent disk (or equivalent) is configured so corpus.db survives redeploys.
- Verify `/health`, `/eligibility`, `/checklist`, `/sources` all respond correctly on the live Render URL.

### 3.2 Frontend deployment (Vercel)
- Connect the GitHub repo to Vercel, deploy `src/ui/web/`.
- Set the API base URL environment variable to the live Render backend URL.
- Verify the deployed web UI loads and successfully calls the live backend (test all 3 sample questions from Phase 5).

### 3.3 CORS and cross-origin validation
- Update backend CORS allow-list to include the final `*.vercel.app` (or custom domain) URL.
- Re-test from the live frontend to confirm no CORS errors in browser console.

### 3.4 Scraper refresh automation
- Implement the chosen scheduling mechanism (Render Cron Job or GitHub Actions) to run `refresh_all.py` weekly.
- Manually trigger one test run of the scheduled job to confirm it executes successfully and commits any corpus changes.

### 3.5 CLI production mode
- Update `wblepa_cli.py` to allow pointing at the production Render URL via an environment variable or config flag, defaulting to production once deployed.
- Run all 4 CLI menu options against the live backend to confirm functionality.

### 3.6 Final smoke test (full live stack)
- From the S24 Ultra: open the live Vercel URL in the mobile browser, run through the full user journey (landing -> question -> results with citations).
- From Termux: run the CLI in production mode, run through all 4 menu options.
- Confirm both surfaces produce correct, cited, disclaimer-inclusive results identical to local testing.

### 3.7 Work-sample documentation
- Update the main `README.md` with: live demo URL (Vercel), architecture diagram, link to GitHub repo, and a short "How to run locally" section for anyone reviewing the code.
- Write a `docs/formal/deployment_notes.md` capturing hosting choices, environment variable setup, and the refresh automation mechanism, so this deployment is fully reproducible.

## 4. Deliverables (Definition of Done)
- [ ] Backend deployed and live on Render, all 4 endpoints verified
- [ ] Frontend deployed and live on Vercel, verified against live backend
- [ ] CORS updated and cross-origin calls confirmed working
- [ ] Scraper refresh automation configured and one successful run confirmed
- [ ] CLI updated to support production mode, tested against live backend
- [ ] Full live-stack smoke test passed on both mobile browser and Termux CLI
- [ ] README.md updated with live demo link and run instructions
- [ ] `deployment_notes.md` written documenting the full deployment setup
- [ ] All changes committed and pushed with message: "Phase 7: deploy to production (Render + Vercel)"
- [ ] Mirror directory updated to match

## 5. Explicitly Out of Scope for This Phase
- No new features - deployment only
- No custom domain purchase (optional future enhancement, not required for work sample)
- No paid hosting tier upgrades

## 6. Next Step
Once the live deployment is confirmed working end-to-end and documented, report back to the Chief Engineer/Architect. At that point WBLEPA is a complete, shareable work sample - Phase 8 (Feedback and Iteration) becomes optional and can be scheduled at your discretion.
