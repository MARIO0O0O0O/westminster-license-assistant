# Westminster Business License Assistant (WBLEPA) — API Test Documentation

This document records the exact `curl` commands and verified HTTP responses for testing the FastAPI backend endpoints locally.

---

## 🚀 Server Execution Command

Start the backend API server locally in Termux:
```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

Interactive OpenAPI documentation is available at:
`http://127.0.0.1:8000/docs`

---

## 1. Health Check (`GET /health`)

### Command:
```bash
curl -s http://127.0.0.1:8000/health
```

### Output:
```json
{
  "success": true,
  "data": {
    "status": "ok",
    "service": "WBLEPA Backend API",
    "version": "1.0.0",
    "timestamp": "2026-08-19T21:58:40.547697"
  }
}
```

---

## 2. Locked Sources List (`GET /sources`)

### Command:
```bash
curl -s http://127.0.0.1:8000/sources
```

### Output:
```json
{
  "success": true,
  "data": {
    "total": 7,
    "sources": [
      {
        "slug": "westminster_faq",
        "title": "Westminster Business License FAQ",
        "url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq",
        "default_tags": "faq,eligibility,home-business,landlord,contractor,police-permit,CUP"
      },
      {
        "slug": "westminster_service_directory",
        "title": "Westminster Business Licenses Service Directory",
        "url": "https://www.westminster-ca.gov/services/business-licenses",
        "default_tags": "contact,hours,location,phone,hdl-support"
      },
      {
        "slug": "westminster_apply",
        "title": "Apply for a Westminster Business License",
        "url": "https://www.westminster-ca.gov/business/apply-for/business-license",
        "default_tags": "application,zoning,fees,sb1186,display-requirement"
      },
      {
        "slug": "westminster_code_enforcement",
        "title": "Westminster Code Enforcement & Commercial Violations",
        "url": "https://www.westminster-ca.gov/departments/police/code-enforcement",
        "default_tags": "violations,penalties,misdemeanor,unlicensed-business,fines"
      },
      {
        "slug": "hdl_portal_home",
        "title": "HdL Business License Portal Home & Requirements",
        "url": "https://westminster.hdlgov.com/",
        "default_tags": "hdl,online-portal,fein,cslb,sellers-permit,requirements"
      },
      {
        "slug": "hdl_renewal",
        "title": "HdL Business License Renewal & Payment",
        "url": "https://westminster.hdlgov.com/Renew",
        "default_tags": "renewal,due-date,december-31,penalties,online-payment"
      },
      {
        "slug": "calgold_main",
        "title": "CalGold Permit Assistance Tool Main Page",
        "url": "https://www.calgold.ca.gov/",
        "default_tags": "calgold,state-permits,sellers-permit,oc-health,scaqmd,cslb"
      }
    ]
  }
}
```

---

## 3. Non-AI Requirement Checklist (`GET /checklist?topic=home-business`)

### Command:
```bash
curl -s "http://127.0.0.1:8000/checklist?topic=home-business"
```

### Output:
```json
{
  "success": true,
  "data": {
    "topic": "home-business",
    "total_items": 6,
    "items": [
      {
        "id": "chk_westminster_faq_001",
        "section_heading": "Who is required to obtain a business license in Westminster?",
        "snippet": "Under Westminster Municipal Code Title 5, every person, business, contractor, landlord...",
        "source_url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq"
      },
      {
        "id": "chk_westminster_faq_002",
        "section_heading": "What are the requirements for Home-Based Businesses?",
        "snippet": "All home-based businesses operating in a residential zone in Westminster must obtain a Home Occupation Permit...",
        "source_url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq"
      }
    ]
  }
}
```

---

## 4. Eligibility Guidance (`POST /eligibility`)

### Command:
```bash
curl -s -X POST http://127.0.0.1:8000/eligibility \
  -H "Content-Type: application/json" \
  -d '{"question": "I run a business from my home in Westminster, what permits do I need?"}'
```

### Output:
```json
{
  "success": true,
  "data": {
    "question": "I run a business from my home in Westminster, what permits do I need?",
    "in_scope": true,
    "answer_text": "### Eligibility Guidance\nBased on Westminster public records...",
    "cited_chunk_ids": [
      "chk_westminster_faq_001",
      "chk_westminster_faq_002",
      "chk_westminster_faq_003"
    ],
    "sources": [
      {
        "id": "chk_westminster_faq_001",
        "section_heading": "Who is required to obtain a business license in Westminster?",
        "source_url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq"
      },
      {
        "id": "chk_westminster_faq_002",
        "section_heading": "What are the requirements for Home-Based Businesses?",
        "source_url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq"
      }
    ],
    "disclaimer": "Disclaimer: This guidance is informational only and derived from public Westminster, HdL, and CalGold sources..."
  }
}
```
