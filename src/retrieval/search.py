import os
import re
import sqlite3

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "corpus.db")

STOP_WORDS = {
    "a", "an", "the", "do", "i", "you", "he", "she", "it", "we", "they", "is", "am",
    "are", "was", "were", "be", "been", "being", "have", "has", "had", "does", "did",
    "what", "how", "where", "when", "why", "who", "which", "my", "your", "if", "or",
    "and", "to", "in", "on", "at", "for", "with", "from", "by", "of", "about"
}

QUERY_TAG_MAP = [
    ("landlord", ["lease", "landlord", "rent", "renting", "tenant", "property", "units"]),
    ("home-business", ["home", "home-based", "residential", "occupation"]),
    ("contractor", ["contractor", "out-of-city", "construction", "plumbing", "cslb", "electrical", "hvac"]),
    ("code-enforcement", ["operate without", "unlicensed", "penalty", "penalties", "violation", "fine", "misdemeanor"]),
    ("renewal", ["renew", "renewal", "annual", "december 31", "due date", "late"]),
    ("requirements", ["apply", "application", "information", "fein", "ssn", "documents", "getting started"]),
    ("police-permit", ["special permit", "police permit", "massage", "firearms", "pawnshop", "secondhand", "alcohol", "cannabis"]),
    ("CUP", ["cup", "conditional use permit", "zoning clearance"]),
    ("state-permits", ["state", "state-level", "calgold", "health", "air quality", "oc health", "scaqmd", "cdtfa", "seller's permit"]),
    ("eligibility", ["need a license", "required", "eligibility", "who", "must get"])
]

def infer_query_tags(query: str) -> set:
    q_lower = query.lower()
    inferred = set()
    for tag, keywords in QUERY_TAG_MAP:
        if any(kw in q_lower for kw in keywords):
            inferred.add(tag)
    return inferred

def extract_keywords(query: str) -> list:
    words = re.findall(r'\b[a-zA-Z0-9_-]+\b', query.lower())
    return [w for w in words if w not in STOP_WORDS and len(w) > 1]

def search(query: str, top_k: int = 5, db_path: str = DB_PATH) -> list:
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    inferred_tags = infer_query_tags(query)
    keywords = extract_keywords(query)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all chunks from database
    cursor.execute("SELECT id, source_url, section_heading, chunk_text, topic_tags FROM chunks")
    all_rows = cursor.fetchall()
    conn.close()

    scored_results = []

    for cid, source_url, heading, text, tags in all_rows:
        chunk_tags_set = set([t.strip() for t in tags.split(",") if t.strip()])
        combined_text = f"{heading} {text}".lower()

        # FTS / Keyword match score
        kw_matches = sum(1 for kw in keywords if kw in combined_text)
        fts_score = kw_matches * 1.5

        # Tag boost score
        tag_overlap = len(inferred_tags.intersection(chunk_tags_set))
        tag_boost = tag_overlap * 2.5

        # Heading exact keyword boost
        heading_boost = sum(1.0 for kw in keywords if kw in heading.lower())

        total_score = fts_score + tag_boost + heading_boost

        scored_results.append({
            "id": cid,
            "source_url": source_url,
            "section_heading": heading,
            "chunk_text": text,
            "topic_tags": tags,
            "score": round(total_score, 2)
        })

    # Sort descending by score
    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results[:top_k]

if __name__ == "__main__":
    import sys
    test_q = sys.argv[1] if len(sys.argv) > 1 else "Do I need a license if I lease out property I own?"
    print(f"Query: {test_q}\n")
    results = search(test_q, top_k=3)
    for r in results:
        print(f"[{r['score']}] {r['id']} | {r['section_heading']}")
        print(f"      Tags: {r['topic_tags']}")
        print(f"      Text: {r['chunk_text'][:120]}...\n")
