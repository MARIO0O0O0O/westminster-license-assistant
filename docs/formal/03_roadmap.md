# Phased Development Roadmap
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

Roles: Chief Engineer/Architect (planning + artifacts), Antigravity (execution), Visionary/M.E. (direction + approval).
At the start of each phase, detailed sprint planning occurs; this roadmap defines phase goals, key activities, and exit criteria only.

## Phase 0: Discovery and Environment Setup
Validate dev environment, finalize source corpus scope, set up repo/folder structure.
Exit criteria: Antigravity/Termux toolchain confirmed stable; repo initialized; source list locked.

## Phase 1: Knowledge Layer (Offline Indexing)
Build scraper/parser scripts, chunk content, store in SQLite/JSON with metadata.
Exit criteria: Corpus populated, chunked, and spot-checked for accuracy against live source pages.

## Phase 2: Retrieval Engine
Implement keyword or embedding-based search; build test question set; measure retrieval accuracy.
Exit criteria: Retrieval returns correct source chunks for the test question set at an acceptable hit rate.

## Phase 3: AI Generation Layer
Design prompt template enforcing cited, plain-language answers; wire retrieval into LLM calls; evaluate faithfulness and completeness.
Exit criteria: Generated answers are accurate, cited, and consistent across repeated runs of the test set.

## Phase 4: Backend API
Build FastAPI/Express endpoints around the RAG pipeline; add validation, error handling, logging.
Exit criteria: API reliably returns structured, cited JSON responses for all test scenarios.

## Phase 5: Frontend Interfaces
Build questionnaire-driven web UI and Termux CLI client; walk through user journeys for each persona.
Exit criteria: Both interfaces functionally complete and produce correct, cited results for all test personas.

## Phase 6: Integration Testing and Hardening
End-to-end tests across UI, API, retrieval, generation; add disclaimers, edge-case handling, rate limiting.
Exit criteria: No critical bugs; all disclaimers and edge cases verified.

## Phase 7: Deployment and Launch
Deploy to free-tier hosting; confirm scraper refresh job runs on schedule; smoke-test live deployment.
Exit criteria: Publicly accessible, functioning tool with documentation ready to present as a work sample.

## Phase 8 (Optional): Feedback and Iteration
Share tool informally, track anonymized usage, decide on further investment.
Exit criteria: Documented feedback and a clear go/no-go decision on further investment.
