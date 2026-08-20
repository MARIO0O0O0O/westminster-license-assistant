import os
import sys
import random
import sqlite3

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "corpus.db")

def run_spotcheck():
    print("==========================================================")
    print("🔍 WBLEPA CORPUS SPOT-CHECK VALIDATION")
    print("==========================================================")

    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Corpus database not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chunks")
    total_chunks = cursor.fetchone()[0]
    print(f"📊 Total Chunks in Database: {total_chunks}\n")

    cursor.execute("SELECT source_url, COUNT(*) FROM chunks GROUP BY source_url")
    source_counts = cursor.fetchall()

    print("--- Summary by Source URL ---")
    for url, count in source_counts:
        print(f"  • {count} chunks | {url}")
    print("----------------------------------------------------------\n")

    print("--- Random Spot-Check Samples (3 Chunks per Source) ---")

    for url, _ in source_counts:
        cursor.execute(
            "SELECT id, section_heading, topic_tags, chunk_text FROM chunks WHERE source_url = ?",
            (url,)
        )
        rows = cursor.fetchall()
        sample_size = min(3, len(rows))
        random_samples = random.sample(rows, sample_size)

        print(f"\n🌐 Source: {url}")
        for idx, (cid, heading, tags, text) in enumerate(random_samples, 1):
            clean_preview = text.replace("\n", " ")[:150] + ("..." if len(text) > 150 else "")
            print(f"  [{idx}] ID: {cid}")
            print(f"      Heading: {heading}")
            print(f"      Tags   : {tags}")
            print(f"      Preview: \"{clean_preview}\"")

    conn.close()
    print("\n==========================================================")
    print("✅ SPOT-CHECK COMPLETED SUCCESSFULLY")
    print("==========================================================")

if __name__ == "__main__":
    run_spotcheck()
