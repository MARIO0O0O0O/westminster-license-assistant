# Bug Fix & Direct Deployment Correction
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 0. FIRST STEP — Confirm Platform Access (Do Not Skip)

Before making any changes, Antigravity must confirm whether it currently has authenticated CLI access to Vercel and Render. Run the following checks:

```bash
# Check Vercel CLI auth status
npx vercel whoami

# Check Render CLI auth status (if Render CLI is installed)
render whoami
```

### If Vercel is NOT authenticated:
Run:
```bash
npx vercel login
```
This will output either a login link or a "check your email" confirmation flow. **Antigravity must stop and display the exact login link or instructions to M.E.** so he can complete authentication manually in a browser (this cannot be completed by the agent alone, since it requires clicking a link tied to his personal account).

### If Render CLI is NOT installed or NOT authenticated:
Render's CLI login also requires interactive browser-based authentication. Run:
```bash
render login
```
If this fails or the Render CLI is not installed, **do not attempt to install or force it**. Instead, report back to M.E. with a clear statement: "Render does not support unattended CLI login in this environment. The following actions must be done manually in the Render dashboard: [list the specific settings to change]."

### Reporting requirement
Regardless of outcome, Antigravity must explicitly report back one of the following before proceeding to Section 1:
- "✅ Vercel CLI authenticated as [account]. Proceeding with direct fixes."
- "⚠️ Vercel CLI requires login. Login link: [link]. Waiting for M.E. to authenticate before proceeding."
- "✅ Render CLI authenticated as [account]. Proceeding with direct fixes."
- "⚠️ Render does not support automated login here. Manual dashboard steps required: [steps]."

Do not fabricate a success message. If access is not confirmed with real command output, treat it as not authenticated.

---

## 1. Confirmed Bugs From Codebase Audit (August 20, 2026)

1. **CLI hardcoded wrong production URL** — `src/ui/cli/wblepa_cli.py` has `PROD_API_URL = "https://wblepa-backend.onrender.com"`, but the actual live Render service is `https://westminster-license-assistant.onrender.com`.
2. **render.yaml service name mismatch** — declares `name: wblepa-backend`, but the real deployed service is named/routed as `westminster-license-assistant`.
3. **Vercel misconfigured as Next.js/FastAPI** — the actual frontend in `src/ui/web/` is a static HTML5/CSS3/JS site (no Next.js, no React, no build step), but Vercel's project settings were previously set to auto-detected frameworks (FastAPI, then attempted Next.js), causing repeated deployment failures.

## 2. Tasks for Antigravity (only after Section 0 is resolved)

### 2.1 Fix CLI hardcoded URL
- Open `src/ui/cli/wblepa_cli.py`.
- Change `PROD_API_URL` from `"https://wblepa-backend.onrender.com"` to `"https://westminster-license-assistant.onrender.com"`.
- Save.

### 2.2 Fix render.yaml service name
- Open `render.yaml`.
- Update the `name:` field under the `web` service to `westminster-license-assistant` so it matches the real deployed service name in the Render dashboard.
- If Render CLI access is confirmed (Section 0), also verify this change is reflected live by running the equivalent Render CLI command to inspect the live service config (e.g., `render services list` or `render service <id>`), and reconcile manually if the dashboard name cannot be changed via config alone.

### 2.3 Fix Vercel project configuration
If Vercel CLI access is confirmed in Section 0, run the following directly from the project root to reconfigure and redeploy without needing the dashboard:

```bash
cd ~/projects/westminster-license-assistant
npx vercel link   # link to the existing westminster-license-assistant project if not already linked
npx vercel project ls   # confirm project name/id
```

Then set the correct root directory and framework via a `vercel.json` file placed at the repository root (this is the CLI-native way to force these settings without needing dashboard clicks):

```json
{
  "buildCommand": "",
  "outputDirectory": "src/ui/web",
  "framework": null
}
```

- Commit this `vercel.json` to the repo.
- Run `npx vercel --prod` to trigger a new production deployment using this corrected configuration.
- Capture and report the real deployment URL and status from the CLI output (not a summary — the actual terminal output).

If Vercel CLI access is NOT available, instead produce a clear, numbered manual instruction list for M.E. to perform in the Vercel dashboard:
1. Go to Project Settings → General
2. Set Framework Preset to "Other"
3. Set Root Directory to `src/ui/web`
4. Clear the Build Command field
5. Set Output Directory to `.`
6. Save and trigger a redeploy

### 2.4 Update documentation to reflect reality
- In `docs/formal/02_architecture.md` and `README.md`, replace any reference to "Next.js" frontend with "Static HTML5/CSS3/JavaScript frontend, served via Vercel static hosting."

### 2.5 Verify the fix end-to-end
Once redeployed (via CLI or after M.E. confirms manual dashboard steps are done), run:
```bash
curl -I https://westminster-license-assistant.onrender.com/health
curl -I https://<the-real-vercel-url>
```
Report the actual raw output of both commands. A `200 OK` on both is the only acceptable definition of "fixed" — do not report success without this raw confirmation.

## 3. Deliverables (Definition of Done)
- [ ] Section 0 access check completed and honestly reported (not fabricated)
- [ ] CLI production URL corrected
- [ ] render.yaml service name corrected
- [ ] Vercel reconfigured (via CLI if possible, or clear manual steps delivered to M.E.)
- [ ] Documentation updated to reflect static frontend, not Next.js
- [ ] Real curl verification of both live endpoints, raw output included in report
- [ ] All changes committed and pushed with message: "Fix: correct CLI prod URL, render.yaml service name, and Vercel static config"
- [ ] Mirror directory updated to match

## 4. Explicitly Out of Scope
- No new features
- No changes to backend logic, retrieval, generation, or corpus
- Do not fabricate or assume deployment success without raw command output as evidence

## 5. Next Step
Report back to the Chief Engineer/Architect with the Section 0 access status and the final raw curl results. If manual dashboard steps were required, clearly list exactly what M.E. still needs to click through himself.
