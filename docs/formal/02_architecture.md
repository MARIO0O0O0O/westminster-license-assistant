# Technical Architecture
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

See `architecture_diagram.png` for the visual diagram.

### Layers

**1. Frontend Layer**
- Web UI (Next.js or plain HTML/JS) — questionnaire-driven interface for end users.
- CLI (Termux/Python) — for local demos, dogfooding, and development testing.
- Both call the same backend API to ensure consistent behavior.

**2. Backend API Layer**
- FastAPI (Python) or Express (Node) service.
- Endpoints: `/eligibility`, `/checklist`, `/sources`.
- Handles questionnaire submissions, orchestrates retrieval + generation, returns structured JSON.

**3. AI Reasoning Layer (RAG)**
- Retrieval Engine: keyword (BM25) or embedding-based semantic search over the local knowledge corpus.
- LLM Synthesis: generates plain-language, cited answers constrained strictly to retrieved source content — no open-ended hallucination of regulatory claims.

**4. Knowledge Layer**
- Local Corpus: SQLite or JSON store of scraped content, chunked and tagged with metadata (source URL, section heading, topic tags).
- Scraper/Indexer: scheduled job that periodically re-scrapes public sources to keep the corpus current.

**5. Public Sources (read-only, never written to)**
- Westminster City FAQ & Service Directory
- HdL Business License Portal
- CalGold State Permit Assistance Tool

### Development & Deployment Environment
All development is performed on a Samsung S24 Ultra using Termux and the Antigravity CLI (`agy`), which builds and deploys the frontend, backend, and knowledge pipeline layers. Hosting is on free-tier platforms (Vercel, Railway, or Render) so there is zero cost to the City of Westminster and zero integration with official city systems.

### Design Principles
- **One-way data flow from public sources** — scraper only reads; nothing is written back to official systems.
- **Grounded AI responses** — LLM only operates on retrieved chunks, keeping every answer traceable to a citation.
- **Decoupled frontend/backend** — web UI and CLI share the same API and logic.
- **Zero-cost, zero-integration footprint** — no city infrastructure is touched at any point.
