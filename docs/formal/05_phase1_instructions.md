# Phase 1 - Knowledge Layer (Scraper & Corpus)
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions.

---

## 1. Objective of This Phase
Build the offline data pipeline that scrapes the 7 locked public sources (docs/sources.md), converts them into clean, structured, well-chunked text, and stores them in a local corpus that later phases (retrieval, generation) will query. No LLM or API code is written in this phase - this is a pure data-engineering phase.

## 2. Technical Approach (locked decisions)
- **Scraping stack:** Python with `requests` for HTTP fetching and `BeautifulSoup4` for HTML parsing - the standard, lightweight combination for static government pages, well-supported in Termux [web:87][web:94].
- **Storage format:** SQLite (`corpus.db`), not flat JSON. SQLite gives indexed querying, avoids loading the entire corpus into memory during retrieval, and scales better than JSON once we add embeddings or metadata filters in Phase 2 [web:86][web:90].
- **Chunking strategy:** Document structure-based chunking as the primary method - split each page along its own headings/FAQ items/sections, since these sources (FAQ lists, HdL help pages) already have natural logical boundaries [web:89][web:95]. Fall back to recursive character-based splitting (target ~300-500 tokens per chunk, ~50 token overlap) only for any long unstructured paragraphs that don't have clear internal headers [web:85][web:92].

## 3. Tasks for Antigravity

### 3.1 Scraper module (`src/scraper/`)
- Create one scraper function per source category (city pages, HdL pages, CalGold page), since each site has different HTML structure.
- Each scraper should extract: page title, section heading (if present), clean body text (strip nav/footer/ads), and source URL.
- Store raw HTML snapshots in `data/raw/` (one file per source, named by date + slug) for auditability and re-processing without re-fetching.
- Add basic error handling: timeout, retry once, log failures to `data/raw/scrape_errors.log` rather than crashing.

### 3.2 Chunking module (`src/scraper/chunker.py`)
- Implement document-structure-based chunking: split on headings/FAQ question blocks first.
- For any chunk exceeding ~500 tokens with no internal structure, apply recursive character splitting with ~50 token overlap.
- Each chunk record must include: chunk_id, source_url, section_heading, chunk_text, topic_tags (manually mapped keywords like "home-business", "landlord", "contractor", "renewal", "CUP", "police-permit"), and scrape_date.

### 3.3 Corpus database (`data/corpus.db`)
- Create a SQLite table `chunks` with columns: `id`, `source_url`, `section_heading`, `chunk_text`, `topic_tags`, `scrape_date`.
- Write an idempotent loader script (`src/scraper/load_corpus.py`) that can be re-run safely - re-scraping should update existing rows for a source rather than duplicating them.

### 3.4 Refresh scheduling (lightweight, manual-trigger for now)
- Add a single script `src/scraper/refresh_all.py` that re-runs all scrapers and reloads the corpus. Full cron/scheduled automation is deferred to a later phase - for now, this should be manually runnable on demand.

### 3.5 Spot-check validation
- After loading, write a small script (`tests/test_corpus_spotcheck.py`) that prints chunk counts per source and prints 3 random chunks per source for manual review against the live pages.

## 4. Deliverables (Definition of Done)
- [ ] Scraper modules built for all 7 sources in `docs/sources.md`
- [ ] Raw HTML snapshots saved in `data/raw/`
- [ ] Chunking module implemented with structure-based + recursive fallback logic
- [ ] `data/corpus.db` populated with chunked, tagged records
- [ ] `refresh_all.py` runs end-to-end without errors
- [ ] Spot-check script output manually reviewed and confirmed accurate against live source pages
- [ ] All new files committed and pushed with message: `Phase 1: build scraper and knowledge corpus`
- [ ] Mirror directory at `/storage/emulated/0/Documents/Westminster/` updated to match

## 5. Explicitly Out of Scope for This Phase
- No retrieval/search logic (Phase 2)
- No LLM prompt or generation logic (Phase 3)
- No API or UI code
- No automated/scheduled cron job (manual refresh only for now)

## 6. Next Step
Once all Deliverables are checked and the spot-check confirms corpus accuracy, report back to the Chief Engineer/Architect for Phase 2 planning (Retrieval Engine).
