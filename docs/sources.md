# WBLEPA Source Corpus Lock-List

This document lists the locked public source URLs to be scraped and indexed for the Westminster Business License Assistant knowledge base.

1. **Westminster Business License FAQ**
   - URL: `https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq`
   - Content: Frequently asked questions, license requirement triggers, home occupation rules.

2. **Westminster Business License Service Directory Entry**
   - URL: `https://www.westminster-ca.gov/services/business-licenses`
   - Content: General overview of licensing requirements, contact details, office hours.

3. **Westminster Apply for a Business License Page**
   - URL: `https://www.westminster-ca.gov/business/apply-for/business-license`
   - Content: Step-by-step application instructions and fee schedule overviews.

4. **Westminster Code Enforcement / Commercial Violations Page**
   - URL: `https://www.westminster-ca.gov/departments/police/code-enforcement`
   - Content: Commercial licensing violations, zoning enforcement rules, police permit requirements.

5. **HdL Business License Portal Home & Requirements**
   - URL: `https://westminster.hdlgov.com/`
   - Content: HdL online portal instructions, filing requirements, online application workflow.

6. **HdL Renewal & Payment Page**
   - URL: `https://westminster.hdlgov.com/Renew`
   - Content: Annual license renewal procedure, deadline rules, payment methods.

7. **CalGold Permit Assistance Tool Main Page**
   - URL: `https://www.calgold.ca.gov/`
   - Content: California state permit lookup tool for Westminster-specific business types.

---

## 📝 Changelog & URL Verification Log

- **2026-08-20 (Phase 2 Verification)**: Verified all 7 source URLs. Confirmed city pages (`/services/business-licenses`, `/business/apply-for/business-license`, `/departments/community-development/planning-building/business-license-faq`) and HdL portal endpoints (`westminster.hdlgov.com`, `westminster.hdlgov.com/Renew`) match expected site endpoints. Local HTML snapshots (`data/raw/`) mapped and indexed into SQLite database with FTS5 search table.
