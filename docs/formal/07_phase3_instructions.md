# Phase 3 - AI Generation Layer
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Add the LLM synthesis layer on top of the validated retrieval engine (Phase 2, 100% hit-rate). The generation layer must produce plain-language, cited answers that are strictly grounded in retrieved chunks - it must never speculate beyond the retrieved context. This phase is evaluated on faithfulness (answer only uses retrieved content) and traceability (every claim is tied to a specific chunk), not just fluency.

## 2. Technical Approach (locked decisions)

### 2.1 LLM Provider (cost-conscious, no-cost-to-city constraint)
Use **Google Gemini API (Flash tier)** as the primary model: free tier offers 1,500 requests/day and 1M tokens/day at zero cost, which comfortably covers a small demo/work-sample app, no credit card required. Groq (Llama 3.3 70B, 1,000 req/day, no card) is the fallback provider if Gemini's key setup is blocked from Termux, since it offers very low latency and a generous free daily quota.

### 2.2 Prompting Strategy (grounded generation)
The prompt must enforce, in this order of priority:
1. **Faithfulness mandate**: "Answer using ONLY the provided context chunks. Never speculate beyond the given context. If the context does not contain enough information, say so explicitly rather than guessing."
2. **Citation mandate**: Every factual claim must be tagged with the source chunk_id it came from, e.g., "You likely need a license [chk_westminster_faq_001]."
3. **Output structure**: (a) a direct yes/no/depends eligibility answer, (b) a 2-4 item plain-language checklist of next steps, (c) inline citations throughout, (d) a disclaimer that this is unofficial guidance derived from public city/state sources.
4. **Tone**: Plain language, no legal jargon, written for a first-time or non-expert business owner.

### 2.3 Context Assembly
- Pass the top_k chunks returned by search() from Phase 2 directly into the prompt as labeled context blocks (chunk_id, source_url, section_heading, chunk_text).
- Order context by relevance score (highest first) - place most relevant chunk closest to the question in the prompt, per RAG prompt engineering best practice on context hierarchy.

## 3. Tasks for Antigravity

### 3.1 LLM client wrapper (`src/generation/llm_client.py`)
- Implement a thin wrapper around the Gemini API (google-generativeai Python SDK or direct REST call) that accepts a prompt string and returns the model's text response.
- Store the API key in a `.env` file (already gitignored) - never hardcode the key in source.
- Add basic retry-once-on-failure logic and a clear error message if the daily quota is hit.

### 3.2 Prompt template (`src/generation/prompt_template.py`)
- Implement the prompt structure defined in Section 2.2 as a reusable function `build_prompt(question: str, chunks: list) -> str`.
- Include a hard-coded system instruction block enforcing faithfulness, citation, and disclaimer rules exactly as specified above.

### 3.3 Generation pipeline (`src/generation/generate_answer.py`)
- Implement `answer_question(question: str) -> dict` that:
  1. Calls `search()` from Phase 2 to retrieve top_k chunks.
  2. Builds the prompt via `build_prompt()`.
  3. Calls the LLM client and returns a structured dict: `{answer_text, cited_chunk_ids, disclaimer}`.

### 3.4 Faithfulness/citation evaluation (`tests/test_generation_quality.py`)
- Reuse the 8 test questions from `tests/retrieval_test_set.json`.
- For each question, run `answer_question()` and manually/programmatically check:
  - Every cited chunk_id actually appears in the retrieved context for that question (no fabricated citations).
  - No factual claim contradicts the source chunk text (spot-check by human review, logged in a simple pass/fail table).
- Report a faithfulness pass-rate (target: 8/8 or explicitly flag and fix any failures).

### 3.5 Edge case handling
- Test at least 2 out-of-scope questions (e.g., "What's the weather in Westminster?" or "Can you help me file my taxes?") and confirm the model correctly responds that this is outside its scope rather than hallucinating an answer.

## 4. Deliverables (Definition of Done)
- [ ] Gemini (or Groq fallback) API key obtained and stored in `.env`
- [ ] `llm_client.py` implemented with retry and error handling
- [ ] `build_prompt()` implemented enforcing faithfulness, citation, and disclaimer rules
- [ ] `answer_question()` pipeline implemented end-to-end
- [ ] All 8 test questions produce cited, faithful answers (pass-rate reported)
- [ ] 2+ out-of-scope questions correctly handled without hallucination
- [ ] All new files committed and pushed with message: "Phase 3: build and validate AI generation layer"
- [ ] Mirror directory updated to match
- [ ] `.env` confirmed NOT committed to git (verify against .gitignore)

## 5. Explicitly Out of Scope for This Phase
- No backend API endpoints (Phase 4)
- No frontend/UI code (Phase 5)
- No production rate-limiting or caching (deferred to hardening phase)

## 6. Next Step
Once faithfulness pass-rate is validated and edge cases are handled correctly, report back to the Chief Engineer/Architect for Phase 4 planning (Backend API).
