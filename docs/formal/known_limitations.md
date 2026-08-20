# Westminster Business License Assistant (WBLEPA) — Known System Limitations

This document explicitly details technical scope boundaries, architectural constraints, and operational limitations of the WBLEPA system.

---

## 1. Scope & Knowledge Base Constraints

1. **22-Chunk Corpus Boundary**:
   - The knowledge base is limited to 22 structured text chunks derived from 7 public web sources (Westminster City FAQ, Service Directory, Application Instructions, Code Enforcement Rules, HdL Portal Home, HdL Renewal, and CalGold main page).
   - Non-public city rules, internal department guidelines, or unindexed city pages are outside the corpus.

2. **Informational Non-Binding Status**:
   - All AI outputs and checklist items are strictly informational.
   - Outputs do not constitute binding legal determinations or official city approvals. Users are instructed to verify specific applications with the Westminster Business License Division.

---

## 2. Language & Localization

1. **English-Only Primary Processing**:
   - The RAG retrieval engine and prompt synthesis pipeline are optimized for English queries.
   - Non-English queries (e.g. Spanish or Vietnamese) trigger an explicit Language Notice advising users to submit queries in English.

---

## 3. Rate Limiting & Resource Quotas

1. **15 Requests / Minute Rate Limit**:
   - To protect the free-tier Google Gemini API daily quota (1,500 requests/day), the HTTP API enforces a client rate limit of 15 requests per minute per IP via `slowapi`.
   - Exceeding this limit returns a structured HTTP 429 status code.

2. **Stateless Work Sample Architecture**:
   - The application does not maintain user accounts, persistent user history, or application draft state. All interactions are stateless.

---

## 4. Adversarial & Safety Handling

1. **Prompt Injection Defense**:
   - Requests attempting to override system prompts, bypass rules, or request unrelated generation (e.g. jokes, poems, code generation) are intercepted and safely declined.

2. **Strict Citation Mandate**:
   - The LLM generation layer is prohibited from fabricating claims or citing unretrieved chunk IDs. Every statement requires grounding in retrieved context.
