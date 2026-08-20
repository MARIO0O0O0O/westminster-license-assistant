# Phase 0 — Discovery & Environment Setup
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Role reminder:** Chief Engineer/Architect (this document's author) defines scope and acceptance criteria. Antigravity executes. Visionary (M.E.) approves direction and unblocks decisions. No manual work should be needed beyond review/approval.

---

## 1. Objective of This Phase
Validate the development environment, establish the project's folder/repo structure, lock the source list, and set up the mirrored documentation directory — with zero application code written yet.

## 2. Tasks for Antigravity

### 2.1 Environment validation
- Confirm Antigravity CLI (`agy`) runs correctly inside Termux on the S24 Ultra.
- Verify the following are installed and working: `git`, `python3`, `node`, `curl`. Install any that are missing via `pkg install`.
- Confirm internet access from Termux (test with a `curl` to a public URL).

### 2.2 Project folder structure (Termux — working directory)
Create the following structure under `~/projects/westminster-license-assistant/`:
```
westminster-license-assistant/
├── docs/
├── data/
│   └── raw/
├── src/
│   ├── scraper/
│   ├── retrieval/
│   ├── generation/
│   ├── api/
│   └── ui/
├── tests/
├── .gitignore
└── README.md
```
- `.gitignore` should exclude: `node_modules/`, `__pycache__/`, `.env`, `*.pyc`, `venv/`.
- `README.md` should contain: project name, one-paragraph description, and a placeholder "Phases Completed" checklist (Phase 0 through Phase 8, all unchecked).

### 2.3 Mirror directory (visionary's read/reference copy)
Create a mirrored folder at `/storage/emulated/0/Documents/Westminster/` with the **same subfolder structure** as above.
- This mirror is for M.E.'s personal reference only — it should not be the active git working directory.
- After every phase's commit, copy (not symlink) all changed/new files from the Termux project directory into this mirror, preserving the same relative paths.

### 2.4 GitHub repository setup
- Initialize a git repo inside `~/projects/westminster-license-assistant/`.
- Create a new **private** GitHub repository named `westminster-license-assistant` (use `gh repo create` if GitHub CLI is authenticated, otherwise prompt M.E. for a personal access token).
- Set the remote origin and push the initial commit (folder structure + README + .gitignore).
- Commit message format for all phases going forward: `Phase N: <short description>`.

### 2.5 Source corpus lock-list
Create `docs/sources.md` listing each public source URL to be scraped in Phase 1, with a one-line note on content type:
- Westminster Business License FAQ page
- Westminster Business License service directory entry
- Westminster Business/Apply-For page
- Westminster Commercial Violations / Code Enforcement page
- HdL Business License portal home + "Getting Started"/requirements page
- HdL Renewal page
- CalGold permit assistance tool main page

## 3. Deliverables (Definition of Done)
- [ ] `agy` confirmed working in Termux with all dependencies installed
- [ ] Full folder structure created in Termux project directory
- [ ] Identical folder structure mirrored in `/storage/emulated/0/Documents/Westminster/`
- [ ] `README.md` and `.gitignore` committed
- [ ] Private GitHub repo created, remote linked, initial commit pushed
- [ ] `docs/sources.md` populated with the 7 locked source URLs
- [ ] Mirror directory synced to match the Termux repo exactly

## 4. Explicitly Out of Scope for This Phase
- No scraping code
- No API or UI code
- No LLM/prompt work

## 5. Next Step
Once all Deliverables are checked, report back to the Chief Engineer/Architect for Phase 1 planning (Knowledge Layer — scraper + corpus).
