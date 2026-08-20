import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.scraper.scrapers import scrape_all_sources
from src.scraper.chunker import chunk_scraped_page
from src.scraper.load_corpus import load_chunks_to_db, DB_PATH

def refresh_corpus():
    print("==========================================================")
    print("🚀 WBLEPA CORPUS REFRESH & INGESTION")
    print("==========================================================")

    print("📡 Step 1: Scraping 7 locked sources (or loading snapshots)...")
    scraped_pages = scrape_all_sources()
    print(f"✅ Successfully fetched/loaded {len(scraped_pages)} pages.")

    print("\n🧩 Step 2: Processing document-structure chunking...")
    all_chunks = []
    for page in scraped_pages:
        chunks = chunk_scraped_page(page)
        all_chunks.extend(chunks)
        print(f"  • [{page['slug']}] -> {len(chunks)} chunks generated.")

    print(f"\n💾 Step 3: Loading {len(all_chunks)} total chunks into SQLite database ({DB_PATH})...")
    total_loaded = load_chunks_to_db(all_chunks)
    print(f"🎉 SUCCESS: {total_loaded} chunks successfully upserted into corpus.db!")
    print("==========================================================")

if __name__ == "__main__":
    refresh_corpus()
