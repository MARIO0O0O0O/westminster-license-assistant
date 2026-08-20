import os
import glob
import time
import requests
from datetime import datetime

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

SOURCES_CONFIG = [
    {
        "slug": "westminster_faq",
        "url": "https://www.westminster-ca.gov/departments/community-development/planning-building/business-license-faq",
        "title": "Westminster Business License FAQ",
        "default_tags": "faq,eligibility,home-business,landlord,contractor,police-permit,CUP"
    },
    {
        "slug": "westminster_service_directory",
        "url": "https://www.westminster-ca.gov/services/business-licenses",
        "title": "Westminster Business Licenses Service Directory",
        "default_tags": "contact,hours,location,phone,hdl-support"
    },
    {
        "slug": "westminster_apply",
        "url": "https://www.westminster-ca.gov/business/apply-for/business-license",
        "title": "Apply for a Westminster Business License",
        "default_tags": "application,zoning,fees,sb1186,display-requirement"
    },
    {
        "slug": "westminster_code_enforcement",
        "url": "https://www.westminster-ca.gov/departments/police/code-enforcement",
        "title": "Westminster Code Enforcement & Commercial Violations",
        "default_tags": "violations,penalties,misdemeanor,unlicensed-business,fines"
    },
    {
        "slug": "hdl_portal_home",
        "url": "https://westminster.hdlgov.com/",
        "title": "HdL Business License Portal Home & Requirements",
        "default_tags": "hdl,online-portal,fein,cslb,sellers-permit,requirements"
    },
    {
        "slug": "hdl_renewal",
        "url": "https://westminster.hdlgov.com/Renew",
        "title": "HdL Business License Renewal & Payment",
        "default_tags": "renewal,due-date,december-31,penalties,online-payment"
    },
    {
        "slug": "calgold_main",
        "url": "https://www.calgold.ca.gov/",
        "title": "CalGold Permit Assistance Tool Main Page",
        "default_tags": "calgold,state-permits,sellers-permit,oc-health,scaqmd,cslb"
    }
]

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
ERROR_LOG_PATH = os.path.join(RAW_DATA_DIR, "scrape_errors.log")

def log_scrape_error(msg: str):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def fetch_or_load_snapshot(source_info: dict) -> dict:
    url = source_info["url"]
    slug = source_info["slug"]
    today_str = datetime.now().strftime("%Y%m%d")
    snapshot_filename = f"{today_str}_{slug}.html"
    snapshot_path = os.path.join(RAW_DATA_DIR, snapshot_filename)

    html_content = None
    fetched_live = False

    # Prefer reading snapshot if available for static consistency across all 7 sources
    pattern = os.path.join(RAW_DATA_DIR, f"*_{slug}.html")
    matching_files = sorted(glob.glob(pattern), reverse=True)
    if matching_files:
        snapshot_path = matching_files[0]
        with open(snapshot_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        # Live fetch attempt
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
            if response.status_code == 200 and len(response.text) > 200:
                html_content = response.text
                fetched_live = True
            else:
                log_scrape_error(f"Attempt 1 failed for {url} with status {response.status_code}")
        except Exception as e:
            log_scrape_error(f"Attempt 1 exception for {url}: {e}")

        if fetched_live and html_content:
            os.makedirs(RAW_DATA_DIR, exist_ok=True)
            with open(snapshot_path, "w", encoding="utf-8") as f:
                f.write(html_content)

    if not html_content:
        raise FileNotFoundError(f"Could not retrieve live or snapshot content for {slug}")

    return {
        "slug": slug,
        "url": url,
        "title": source_info["title"],
        "raw_html": html_content,
        "default_tags": source_info["default_tags"],
        "scrape_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def scrape_all_sources() -> list:
    results = []
    for source in SOURCES_CONFIG:
        try:
            res = fetch_or_load_snapshot(source)
            results.append(res)
        except Exception as e:
            log_scrape_error(f"Fatal error processing source {source['slug']}: {e}")
    return results
