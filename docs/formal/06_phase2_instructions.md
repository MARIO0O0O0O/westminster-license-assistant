# Phase 2 - Retrieval Engine
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Build and validate the retrieval mechanism that finds the correct chunks from corpus.db for a given user query - completely independent of any LLM. Retrieval quality is tested and proven here before any generation logic is added in Phase 3. This separation is standard practice: a RAG system's accuracy is bottlenecked by retrieval quality, so it must be validated in isolation first.

## 2. Technical Approach (locked decisions)
- **Retrieval method:** Hybrid approach - keyword/BM25-style search (via SQLite FTS5 full-text search extension) as the primary method, since our corpus is small (22 chunks) and highly structured with clear topic_tags already assigned in Phase 1. Pure keyword/tag-based retrieval is often sufficient and more predictable than embeddings at this corpus size; embeddings can be added later if query variety demands it.
- **Ranking signal:** Combine FTS5 text match score with topic_tags overlap (if user's inferred intent tags match chunk tags, boost ranking).
- **No vector database needed at this scale** - avoids adding an embedding model dependency, API cost, or infra complexity for only 22 records.

## 3. Tasks for Antigravity

### 3.1 Verify source URL mapping (carry-over check from Phase 1)
- Before building retrieval, confirm the two city-page source URLs match the original docs/sources.md list (business-license-faq vs frequently-asked-questions; services/business-licenses vs apply-for/business-license). Update docs/sources.md if the site's actual current URLs differ from what was originally recorded, and note the correction in a short changelog entry in docs/sources.md.

### 3.2 Enable full-text search (`src/retrieval/`)
- Create an SQLite FTS5 virtual table (`chunks_fts`) indexing `chunk_text`, `section_heading`, and `topic_tags` from the `chunks` table.
- Write a sync step in load_corpus.py (or a new script) so chunks_fts stays in sync whenever corpus.db is updated.

### 3.3 Query interface (`src/retrieval/search.py`)
- Build a function `search(query: str, top_k: int = 5)` that:
  - Runs the query against `chunks_fts` for text relevance.
  - Extracts likely topic tags from the query (simple keyword matching against known tags: home-business, landlord, contractor, renewal, CUP, police-permit, eligibility, fees, code-enforcement).
  - Boosts and re-ranks results where topic_tags overlap with inferred query tags.
  - Returns top_k chunk records (id, source_url, section_heading, chunk_text, score).

### 3.4 Test question set (`tests/retrieval_test_set.json`)
- Create a JSON file with at least 8 representative test questions covering all major personas, each with the expected correct chunk_id(s):
  1. "Do I need a license if I lease out property I own?"
  2. "I run a business from my home, what do I need?"
  3. "I'm a contractor working in Westminster but based elsewhere, do I need a license?"
  4. "What happens if I operate without a license?"
  5. "How do I renew my business license online?"
  6. "What information do I need to apply for a license?"
  7. "Do I need a special permit for certain business types?"
  8. "Where do I check state-level permit requirements?"

### 3.5 Retrieval evaluation script (`tests/test_retrieval_accuracy.py`)
- Run all test questions through `search()`, check whether the expected chunk_id appears in the top_k results.
- Report a simple hit-rate metric (e.g., "7/8 = 87.5% top-5 hit rate") and print any misses with the actual top results returned for manual review.

## 4. Deliverables (Definition of Done)
- [ ] Source URL discrepancy from Phase 1 reviewed and docs/sources.md corrected/annotated if needed
- [ ] FTS5 virtual table created and kept in sync with chunks table
- [ ] `search()` function implemented with tag-boosted ranking
- [ ] Test question set with 8+ questions and expected chunk IDs created
- [ ] Retrieval evaluation script run, hit-rate reported and reviewed
- [ ] Any misses investigated and retrieval logic adjusted until hit-rate is acceptable (target: 80%+ top-5 hit rate)
- [ ] All new files committed and pushed with message: "Phase 2: build and validate retrieval engine"
- [ ] Mirror directory updated to match

## 5. Explicitly Out of Scope for This Phase
- No LLM calls or prompt design (Phase 3)
- No API or UI code
- No embeddings/vector database (deferred unless keyword+tag retrieval proves insufficient)

## 6. Next Step
Once hit-rate is validated at an acceptable level, report back to the Chief Engineer/Architect for Phase 3 planning (AI Generation Layer).
