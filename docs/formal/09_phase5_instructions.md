# Phase 5 - Frontend Interfaces
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Build the two user-facing interfaces - a web UI and a Termux CLI client - that call the Phase 4 backend API. Both interfaces share the same underlying API and must produce consistent, correct results for the same input.

## 2. Technical Approach (locked decisions)

### 2.1 Web UI stack
- **Framework:** Next.js (React) with plain CSS/Tailwind - consistent with your existing stack (React/Next.js + Supabase experience), minimizing new tooling to learn.
- **Hosting target:** Vercel free tier (confirmed in Phase 7 deployment, not built here).
- **No Supabase needed for this MVP** - the app is stateless (no user accounts, no persisted user data), so a database-backed auth/storage layer would be unnecessary scope creep for a work sample.

### 2.2 CLI stack
- **Language:** Python (already used throughout the backend), run directly in Termux.
- Use the `requests` library to call the same FastAPI endpoints from Phase 4 - CLI and web UI must never diverge in logic, both are thin clients over the same API.

### 2.3 UX flow (both interfaces)
1. Landing/welcome screen explaining the tool's purpose and the "unofficial, informational only" disclaimer up front.
2. Persona selector: Business Owner / Landlord / Contractor (optional, for framing - not required to submit a query).
3. Free-text question input (calls `/eligibility`) OR topic browse mode (calls `/checklist` with topic dropdown: home-business, landlord, contractor, renewal, CUP, police-permit).
4. Results display: eligibility answer, checklist items, inline citations as clickable links to source URLs, and the disclaimer footer.

## 3. Tasks for Antigravity

### 3.1 Web UI (`src/ui/web/`)
- Scaffold a Next.js app (`npx create-next-app`) inside `src/ui/web/`.
- Build the landing page with disclaimer and persona selector.
- Build the question form (calls `POST /eligibility`) and topic browse dropdown (calls `GET /checklist`).
- Build the results component: renders answer_text, cited sources as a list of links (source_url + section_heading), and disclaimer.
- Point API calls at `http://127.0.0.1:8000` for local dev (make this an environment variable, not hardcoded, so it's easy to swap for the deployed URL in Phase 7).

### 3.2 CLI client (`src/ui/cli/wblepa_cli.py`)
- Build an interactive terminal menu: "1) Ask a question  2) Browse by topic  3) View sources  4) Exit".
- Option 1 posts to `/eligibility` and prints the answer, citations, and disclaimer in readable terminal formatting.
- Option 2 lists available topics, prompts for selection, calls `/checklist`, prints results.
- Option 3 calls `/sources` and lists all 7 source URLs.

### 3.3 Consistency test
- Run the same 3 sample questions through both the web UI and the CLI, confirm both return identical answer_text and cited_chunk_ids (since both hit the same backend, this should be guaranteed - but verify explicitly as a sanity check).

### 3.4 Basic styling and usability pass
- Ensure the web UI is legible on mobile (test in the S24 Ultra's browser via localhost or a tunneled URL).
- Ensure CLI output uses clear formatting (headers, bullet points, line spacing) rather than a dense text wall.

## 4. Deliverables (Definition of Done)
- [ ] Next.js web UI scaffolded and running locally
- [ ] Landing page, persona selector, question form, and topic browse implemented
- [ ] Results component rendering answer, citations (as links), and disclaimer
- [ ] CLI client built with all 4 menu options functional
- [ ] Consistency test passed (web UI and CLI produce identical results for same query)
- [ ] Web UI verified legible/usable on mobile browser
- [ ] All new files committed and pushed with message: "Phase 5: build web UI and CLI frontend"
- [ ] Mirror directory updated to match

## 5. Explicitly Out of Scope for This Phase
- No production deployment (Phase 7)
- No rate limiting, analytics, or hardening (Phase 6)
- No user accounts or persistence layer (out of scope for entire project per charter)

## 6. Next Step
Once both interfaces are functional and consistency-tested, report back to the Chief Engineer/Architect for Phase 6 planning (Integration Testing and Hardening).
