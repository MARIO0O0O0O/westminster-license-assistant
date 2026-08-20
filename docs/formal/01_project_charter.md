# Project Charter
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

### 1. Project Name and Description
**Project Name:** Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

This project delivers a lightweight, AI-powered web and CLI tool that helps Westminster, CA business owners, landlords, and contractors determine whether they need a city business license and routes them to the correct public application, renewal, and permit resources. The tool is built and hosted independently by the developer at no cost to the City of Westminster, using only publicly available information from the city's website, HdL licensing portal, and the state's CalGold permit assistance tool.

### 2. Business Case and Justification
Westminster's licensing process is fragmented across three separate systems — the city's own FAQ/service directory, the third-party HdL application portal, and the state CalGold permit lookup — with no unified guidance connecting them. This creates confusion for first-time, ESL, and non-expert applicants who must self-interpret dense municipal rules (e.g., what counts as "doing business," home business Planning approval requirements, CUP/police permit triggers).

This project addresses that gap by demonstrating a practical, evidence-based application of AI orchestration and retrieval-augmented generation (RAG) to reduce user confusion and administrative friction, at zero cost and zero integration risk to the city, while serving as a functional work sample of the developer's applied AI and full-stack capabilities.

### 3. Project Purpose and Objectives
**Purpose:** Build and deploy a functional, publicly accessible AI assistant that clarifies Westminster business licensing eligibility and next steps using only public source material.

**Objectives:**
- Reduce time and confusion for users trying to determine license/permit applicability, measured by user completion of the eligibility questionnaire.
- Provide accurate, source-cited guidance derived exclusively from Westminster's FAQ, HdL portal text, and CalGold content, with no fabricated regulatory claims.
- Demonstrate a deployable, no-cost, no-integration AI tool suitable for showcasing to prospective clients or the city itself as a proof of concept.
- Complete development entirely on a mobile-first stack (Samsung S24 Ultra, Termux, Antigravity CLI) to demonstrate mobile AI orchestration capability.

### 4. Success Criteria
- Functional MVP deployed and publicly accessible (web UI + CLI) within the defined timeline.
- Assistant correctly identifies license/permit applicability for at least 5 representative test scenarios (home business, landlord with 3+ units, in-city vs out-of-city contractor, standard retail, food/alcohol use) validated against the source FAQ text.
- Every AI-generated response includes a citation back to the specific public source paragraph used.
- Zero cost incurred by the City of Westminster; zero access to or modification of official city or HdL systems.

### 5. Project Scope
**In scope:**
- Web scraping/indexing of public Westminster FAQ, service directory, HdL portal pages, and CalGold help content into a local knowledge corpus.
- RAG-based reasoning layer that answers eligibility questions and generates a personalized checklist with citations.
- Simple web UI (React/Next.js or plain HTML/JS) and CLI interface (Termux/Python) for user interaction.
- Deployment on free-tier hosting (e.g., Vercel, Railway, Render) under the developer's own accounts.

**Out of scope:**
- Submitting, modifying, or storing actual business license applications or payments.
- Any integration with HdL, CalGold, or official city databases/APIs.
- Legal advice or binding determinations — all outputs are informational and explicitly disclaimed as unofficial guidance.
- Multi-city expansion (future phase, not part of this charter).

### 6. Stakeholders and Roles
| Role | Party | Responsibility |
|---|---|---|
| Project Sponsor / Owner | M.E. (developer) | Funds, builds, and owns the project end-to-end |
| Project Manager / Developer | M.E. (developer) | Designs architecture, builds, tests, deploys the tool |
| Primary Customer (indirect) | Westminster Economic Development Division | Beneficiary if tool is later shared; no obligations or cost |
| End Users | Business owners, landlords, contractors in Westminster | Use the tool to determine licensing/permit needs |
| Secondary Reference Source | HdL Companies (licensing vendor), CalGold (state tool) | Source of public content only; no active involvement |

### 7. High-Level Requirements
- Accurate ingestion and periodic re-scraping of source pages to keep the knowledge corpus current.
- Retrieval mechanism (keyword or embedding-based search) to surface relevant text chunks per user query.
- LLM-based synthesis layer constrained to cite only retrieved source content (no open-ended generation of regulatory claims).
- Lightweight backend (FastAPI/Express) and minimal frontend, deployable on free-tier infrastructure.
- Development and testing conducted via Termux and Antigravity CLI on an Android device (S24 Ultra).

### 8. High-Level Architecture Summary
The system consists of four layers: (1) a data/knowledge layer that scrapes and stores public Westminster, HdL, and CalGold content; (2) an AI reasoning layer using RAG to retrieve relevant fragments and generate cited, plain-language answers; (3) a backend API (Python/FastAPI or Node/Express) handling questionnaire logic and LLM calls; and (4) frontend interfaces (web UI and Termux CLI) for user interaction, all developed and orchestrated via Antigravity CLI running natively in Termux on the S24 Ultra. See `architecture.md` and `architecture_diagram.png` for full detail.

### 9. Milestones and Summary Timeline
| Milestone | Target Timeframe |
|---|---|
| Corpus scraping and knowledge base setup | Week 1 |
| RAG retrieval + LLM prompt design and testing | Week 2 |
| Backend API build and integration | Week 3 |
| Frontend (web + CLI) build | Week 3-4 |
| Internal testing against representative scenarios | Week 4 |
| Deployment to free-tier hosting | Week 5 |
| Final validation and documentation | Week 5 |

### 10. Budget and Resources
**Estimated cost to City of Westminster:** $0 — no license fees, staff time, or infrastructure costs required.

**Developer-side resources:** Free-tier hosting (Vercel/Railway/Render), Antigravity CLI, existing S24 Ultra hardware, and Termux (open-source, free). Any paid LLM API usage (if not covered under free tiers) is the developer's own minor operating cost, not billed to the city.

### 11. Assumptions and Constraints
**Assumptions:**
- Public web pages (Westminster FAQ, HdL, CalGold) remain accessible and stable enough for periodic re-scraping.
- Antigravity CLI continues to function reliably in the Termux/Android arm64 environment per current community documentation.
- The city has no objection to an independently built, unofficial informational tool referencing its public content.

**Constraints:**
- Development is mobile-only (S24 Ultra via Termux), limiting some tooling compared to a desktop environment.
- No access to internal city systems, staff, or non-public data — corpus is limited strictly to what is publicly published.
- Antigravity-on-Termux is a community-maintained, non-official setup and may require ongoing compatibility fixes.

### 12. High-Level Risks
| Risk | Mitigation |
|---|---|
| Source pages change structure, breaking scraper | Schedule periodic re-scrape and add change-detection alerts |
| LLM generates inaccurate or hallucinated regulatory guidance | Constrain prompts to cite only retrieved text; add disclaimers |
| Antigravity/Termux compatibility issues on Android | Use documented community fixes; maintain fallback CLI-only mode |
| Tool mistaken for an official city service | Clear "unofficial, informational only" disclaimers throughout UI |
| Free-tier hosting limits (rate limits, downtime) | Monitor usage; have backup free-tier host ready |

### 13. Project Approval and Governance
Given this is a self-directed work sample rather than a client-commissioned engagement, the developer (M.E.) acts as both sponsor and project manager, with sole authority to approve scope, timeline, and deployment decisions. Success is determined by the developer against the criteria in Section 4, with optional informal feedback sought from the Westminster Economic Development Division post-launch if the tool is shared publicly.

**Prepared by:** M.E., Developer/Project Sponsor
**Date:** August 19, 2026
**Status:** Draft — pending self-approval to proceed to build phase
