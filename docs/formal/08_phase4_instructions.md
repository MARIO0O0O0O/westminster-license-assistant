# Phase 4 - Backend API
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Wrap the validated retrieval (Phase 2) and generation (Phase 3) pipeline in a stable, well-structured HTTP API that the frontend (Phase 5) will call. No UI code is written in this phase - this is purely the service layer that exposes `answer_question()` and related functions over HTTP.

## 2. Technical Approach (locked decisions)
- **Framework:** FastAPI (Python) - chosen over Express/Node since the entire pipeline (scraper, retrieval, generation) is already Python, avoiding a cross-language handoff. FastAPI also gives free automatic OpenAPI docs, which doubles as living API documentation for this work sample.
- **Server:** Uvicorn as the ASGI server, run locally during development via Termux; deployment target (Render/Railway free tier) confirmed in Phase 7, not this phase.
- **Response format:** All endpoints return structured JSON with a consistent envelope: `{success, data, error}`.

## 3. Tasks for Antigravity

### 3.1 API scaffolding (`src/api/main.py`)
- Set up FastAPI app instance with CORS enabled (permissive for now, to be tightened in Phase 6 hardening).
- Add a root health-check endpoint `GET /health` returning `{status: "ok"}`.

### 3.2 Core endpoints
- `POST /eligibility` - accepts `{question: str}`, calls `answer_question()` from Phase 3, returns `{answer_text, cited_chunk_ids, disclaimer, sources}` where `sources` resolves chunk_ids to their source_url + section_heading for display.
- `GET /checklist` - accepts a `topic` query param (e.g., "home-business", "landlord"), retrieves all chunks tagged with that topic via a direct DB query (not LLM), and returns a structured plain checklist of relevant chunk headings/snippets. This gives users a non-AI fallback browsing option.
- `GET /sources` - returns the full list of the 7 locked source URLs from docs/sources.md, for transparency/attribution display in the UI.

### 3.3 Input validation and error handling
- Use Pydantic models for all request/response bodies.
- Validate `question` is non-empty and under a reasonable length cap (e.g., 500 chars) to avoid abuse.
- Wrap LLM and DB calls in try/except; return structured error responses (e.g., `{success: false, error: "LLM quota exceeded, try again later"}`) rather than raw stack traces.

### 3.4 Logging
- Log every request to `/eligibility` (timestamp, question text, cited chunk_ids, success/failure) to a local file `logs/api_requests.log` for later analysis - no personal data is collected since this is anonymous public tool usage.

### 3.5 Local testing
- Test all three endpoints locally via curl from Termux (document exact curl commands used in `docs/formal/api_test_commands.md`).
- Confirm FastAPI's auto-generated docs are viewable at `/docs` when running locally.

## 4. Deliverables (Definition of Done)
- [ ] FastAPI app scaffolded with health-check endpoint
- [ ] `/eligibility`, `/checklist`, `/sources` endpoints implemented and functional
- [ ] Pydantic validation in place for all request bodies
- [ ] Error handling returns structured JSON, never raw stack traces
- [ ] Request logging implemented to `logs/api_requests.log`
- [ ] All 3 endpoints tested locally via curl with results documented
- [ ] `/docs` auto-generated API documentation confirmed working
- [ ] All new files committed and pushed with message: "Phase 4: build backend API"
- [ ] Mirror directory updated to match

## 5. Explicitly Out of Scope for This Phase
- No frontend/UI code (Phase 5)
- No production deployment (Phase 7)
- No rate limiting, auth, or CORS hardening (Phase 6)

## 6. Next Step
Once all endpoints are tested and confirmed functional, report back to the Chief Engineer/Architect for Phase 5 planning (Frontend Interfaces).
