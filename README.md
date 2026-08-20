# Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

An AI-powered, RAG-driven assistant designed to guide Westminster, CA business owners, landlords, and contractors through business licensing, permit applicability, and application pathways using public city and state data.

---

## 🌐 Public Live Links & Work Sample Demo

- **Web UI Demo (Vercel)**: `https://westminster-license-assistant.vercel.app`
- **Backend API (Render)**: `https://wblepa-backend.onrender.com`
- **OpenAPI Interactive Documentation**: `https://wblepa-backend.onrender.com/docs`
- **GitHub Repository**: `https://github.com/MARIO0O0O0O/westminster-license-assistant`

---

## 🏛️ System Architecture

```
[ Web UI (Vercel) / Termux CLI ]
               │
               ▼  (HTTP JSON API)
   [ FastAPI Backend (Render) ]
        │               │
        ▼               ▼
 [ FTS5 Search ]    [ LLM Synthesis ]
        │               │
        └───────┬───────┘
                ▼
      [ SQLite corpus.db ]
```

- **Data Layer**: 7 locked public source snapshots stored in SQLite `data/corpus.db` with FTS5 indexing.
- **Retrieval Layer**: Keyword + tag-boosted search engine (`src/retrieval/search.py`, 100% top-5 hit rate).
- **Generation Layer**: Faithfulness-constrained LLM prompt synthesis with inline `[chk_id]` citations and non-binding legal disclaimers.
- **API Layer**: FastAPI ASGI service with `slowapi` rate limiting (15 req/min) and CORS authorization.
- **Frontend Layer**: Mobile-first glassmorphism Web UI and interactive Termux CLI.

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.10+
- `git`

### 2. Installation & Setup
```bash
git clone https://github.com/MARIO0O0O0O/westminster-license-assistant.git
cd westminster-license-assistant

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Backend API Server
```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```
View API docs at `http://127.0.0.1:8000/docs`.

### 4. Run CLI Interface
In a separate terminal window:
```bash
python3 src.ui.cli.wblepa_cli.py
```

### 5. Run Web UI
In a separate terminal window:
```bash
npx serve -l 3000 src/ui/web
```
Open `http://localhost:3000` in your web browser.

---

## 📋 Project Phases & Status

- [x] **Phase 0**: Discovery & Environment Setup
- [x] **Phase 1**: Knowledge Layer (Scraper + Corpus)
- [x] **Phase 2**: RAG Retrieval & Prompt Design
- [x] **Phase 3**: Core Logic & Questionnaire Engine
- [x] **Phase 4**: Backend API
- [x] **Phase 5**: Web & CLI Interfaces
- [x] **Phase 6**: Scenario Validation & Testing
- [x] **Phase 7**: Deployment & Monitoring
- [ ] **Phase 8**: Final Handoff & Maintenance (Optional / Post-Launch)
