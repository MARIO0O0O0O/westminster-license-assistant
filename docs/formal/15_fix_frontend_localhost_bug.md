# Antigravity Prompt — Fix Frontend Localhost Bug & Confirm Render Backend Live

Context: The Vercel static frontend deployment succeeded — the UI is live and 
rendering correctly at the production URL. However, submitting a question 
returns: "Connection Error: Could not connect to API server at 
http://127.0.0.1:8000. Ensure backend API server is running." This confirms 
the frontend JavaScript is still hardcoded to call the local Termux backend 
instead of the live Render production URL.

Execute the following steps in order. Do not report success on any step 
without pasting the real, raw terminal output as proof.

## Step 1: Locate the hardcoded localhost reference
Run:
```
cd ~/projects/westminster-license-assistant
grep -rn "127.0.0.1:8000" src/ui/web/
```
Paste the raw output showing the exact file and line number(s).

## Step 2: Fix the API URL
Open the file identified in Step 1 (likely src/ui/web/app.js). Replace the 
hardcoded local API URL:
```
http://127.0.0.1:8000
```
with the live Render production URL:
```
https://westminster-license-assistant.onrender.com
```
Confirm there are no other remaining references to 127.0.0.1 or localhost 
anywhere in src/ui/web/ by re-running the grep command from Step 1 after the 
edit — it should return no results.

## Step 3: Verify the Render backend is actually live
Run:
```
curl -I https://westminster-license-assistant.onrender.com/health
```
Paste the raw output. If it returns anything other than HTTP 200, the Render 
service has not redeployed with the corrected render.yaml and CLI URL fixes 
from earlier. In that case:
- Report this clearly as a blocker
- State explicitly that a manual "Manual Deploy → Deploy latest commit" click 
  is required in the Render dashboard at https://dashboard.render.com since 
  Render CLI is not available in this environment
- Do not proceed to claim end-to-end success until this returns HTTP 200

## Step 4: Commit and push the frontend fix
```
git add src/ui/web/app.js
git commit -m "Fix: point frontend to live Render backend instead of localhost"
git push
```
Paste the raw git output confirming the push succeeded and which commit hash 
was created.

## Step 5: Sync mirror directory
Copy the updated project state to the mirror directory at 
/storage/emulated/0/Documents/Westminster/ as done in previous phases.

## Step 6: Final end-to-end verification
Once Vercel's auto-deploy picks up the new commit (wait ~30-60 seconds), run:
```
curl -I https://westminster-license-assistant.vercel.app
```
Paste the raw output confirming HTTP 200.

Then report back to the Chief Engineer/Architect with:
- The exact line(s) that were hardcoded to localhost (Step 1 output)
- Confirmation of the fix (Step 2)
- The real curl result for the Render backend health check (Step 3)
- The commit hash from the push (Step 4)
- The real curl result for the Vercel frontend (Step 6)
- If Render is not live, a clear explicit statement of what manual action is 
  required in the Render dashboard before this can be considered fully working

Do not fabricate or assume success at any step. If a step fails, stop and 
report the failure with raw output rather than proceeding to the next step.
