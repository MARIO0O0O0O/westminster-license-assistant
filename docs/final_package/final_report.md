# Final Project Report
## Westminster Business License Eligibility & Pathway Assistant (WBLEPA)

**Prepared for:** City of Westminster, Economic Development Division / Community Development Department
**Prepared by:** Mario Espindola, MPA, IPMA-SCP
**Date:** August 19, 2026
**Status:** Complete — Live, Deployed Work Sample

---

## Executive Summary

This report documents the research, design, and delivery of a functioning, no-cost AI application built to address a specific, evidence-based pain point in the City of Westminster's business licensing process. The application — WBLEPA — is fully deployed, publicly accessible, and required zero financial investment or staff involvement from the City. It is offered here as a demonstration of applied AI capability and a starting point for a potential conversation about further collaboration.

## Part 1: Original Research — Identifying the Pain Points

### Research Methodology

This project began with a structured review of the City of Westminster's public-facing Economic Development and business licensing infrastructure, cross-referencing the City's own website, the third-party HdL licensing portal, and the State of California's CalGold permit assistance tool.

### Key Findings

**Fragmented, multi-system licensing process.** Business licensing is administered through a third-party vendor (HdL Companies) separate from the City's own website, while state-level permit requirements are hosted on a third system entirely (CalGold). Business owners are required to navigate three disconnected platforms to determine and complete their obligations.

**Confusing resource landscape.** The Economic Development page lists over a dozen partner organizations (SBDC, SCORE, multiple ethnic chambers of commerce, Employment Training Panel, etc.) without clear guidance on which organization best serves a given business's specific situation — creating decision paralysis, particularly for first-time or immigrant entrepreneurs in this majority-Vietnamese-American community.

**Language and accessibility gaps.** While materials exist in English, Spanish, and Vietnamese, they are static PDF documents rather than interactive guidance tools, and in-person assistance is limited to a single monthly office-hours session and a rotating mobile workforce unit.

**Eligibility ambiguity.** City FAQ content clarifies that leasing commercial property, or three or more residential units, legally constitutes "doing business" and triggers licensing requirements — a nuance easily missed by property owners unfamiliar with Municipal Code Title 5.

**Manual, error-prone permit and application processes.** The City's own instructional materials indicate that inaccurate project descriptions or missing documentation are common causes of processing delays.

### Opportunity Identified

These findings pointed to a specific, well-bounded opportunity: an AI-powered eligibility and navigation assistant that consolidates public information from all three systems (City site, HdL, CalGold) into a single, plain-language, cited guidance tool — reducing user confusion without requiring the City to change vendors, systems, or processes.

## Part 2: How AI Addresses These Pain Points

| Pain Point | AI-Based Solution | Cost Impact to City |
|---|---|---|
| Multi-system navigation | Retrieval-augmented assistant consolidates City, HdL, and CalGold guidance into one interface | $0 — no integration with City systems |
| Eligibility ambiguity | AI eligibility checker answers plain-language questions, cites exact Municipal Code source | $0 — sourced from already-public FAQ content |
| Static, hard-to-search resources | Conversational interface replaces static PDF browsing | $0 — hosted independently on free-tier infrastructure |
| Limited multilingual/after-hours support | 24/7 availability (English at launch; multilingual expansion identified as future opportunity) | $0 — no staffing cost |

By design, this project maintains a strictly cost-neutral posture toward the City: no City budget, staff time, licensing fees, or system integration was required at any stage of research, design, build, or deployment.

## Part 3: Final Deliverables

### System Overview
WBLEPA is a retrieval-augmented generation (RAG) application that ingests public City, HdL, and CalGold content, and answers eligibility and process questions with citations back to the original source material — ensuring every answer is traceable and verifiable.

### Live Deployment
- **Web Application:** https://westminster-license-assistant.vercel.app
- **Backend API:** https://wblepa-backend.onrender.com
- **API Documentation:** https://wblepa-backend.onrender.com/docs
- **Source Code Repository:** https://github.com/MARIO0O0O0O/westminster-license-assistant

### Validated Performance
- 100% retrieval accuracy across an 8-question representative test set spanning all major user personas (home-based business, landlord, contractor, new applicant, renewal, specialized permits, state-level requirements)
- 100% citation faithfulness — zero fabricated or hallucinated regulatory claims across all tested scenarios
- 13/13 end-to-end integration and adversarial security tests passed, including prompt-injection resistance and rate-limiting under load
- Automated weekly corpus refresh via scheduled GitHub Actions workflow, ensuring guidance remains current as City/HdL/CalGold content changes

### Architecture
A four-layer system: public data ingestion, retrieval engine (SQLite full-text search with topic-tag boosting), AI generation layer (Google Gemini, grounded strictly in retrieved source text), and dual user interfaces (responsive web application and command-line client). Full technical architecture documentation, including diagrams, is included in the accompanying documentation package.

## Part 4: Known Limitations

This tool is explicitly scoped as a proof-of-concept work sample, not a production City system. Its known limitations are documented transparently:

- **English-only at launch.** Spanish and Vietnamese language support — reflecting the City's own published materials — was identified during research as a valuable future enhancement but was not built in this phase.
- **Limited corpus scope.** The knowledge base currently covers 7 core public sources (22 content chunks); expansion to cover additional City departments (Planning, Building, Fire) is a natural next phase.
- **Free-tier infrastructure constraints.** The backend is hosted on a free hosting tier, which may introduce brief cold-start delays after periods of inactivity, and is subject to usage rate limits appropriate for a demonstration tool rather than high-volume production traffic.
- **Informational tool only.** WBLEPA does not submit applications, process payments, or replace official City or HdL systems — it is strictly a guidance and navigation layer sitting atop existing public information.
- **Independent, unofficial status.** This tool is not officially affiliated with, endorsed by, or integrated into any City of Westminster system. It was built and is maintained independently by the author.

## Part 5: Recommendations for Potential Next Steps

Should the City wish to explore further collaboration, natural extensions include: multilingual support matching the City's existing Spanish/Vietnamese materials, expansion of the knowledge corpus to cover Planning, Building, and Fire Department permitting, and/or a formal review and potential co-branding of the tool as an official City resource, at the City's discretion and on terms to be separately determined.

## Closing

This project was undertaken independently, at no cost, as a demonstration of how modern AI tooling can meaningfully reduce administrative friction for residents and business owners without requiring significant municipal investment. I welcome the opportunity to discuss this work further.

Respectfully submitted,

**Mario Espindola, MPA, IPMA-SCP**
