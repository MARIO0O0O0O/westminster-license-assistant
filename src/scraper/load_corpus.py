import os
import sqlite3

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "corpus.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chunks (
    id TEXT PRIMARY KEY,
    source_url TEXT NOT NULL,
    section_heading TEXT,
    chunk_text TEXT NOT NULL,
    topic_tags TEXT,
    scrape_date TEXT NOT NULL
);
"""

UPSERT_CHUNK_SQL = """
INSERT OR REPLACE INTO chunks (id, source_url, section_heading, chunk_text, topic_tags, scrape_date)
VALUES (?, ?, ?, ?, ?, ?);
"""

def init_db(db_path: str = DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()

def load_chunks_to_db(chunks: list, db_path: str = DB_PATH) -> int:
    init_db(db_path)
    inserted_count = 0
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for chunk in chunks:
            cursor.execute(
                UPSERT_CHUNK_SQL,
                (
                    chunk["id"],
                    chunk["source_url"],
                    chunk.get("section_heading", ""),
                    chunk["chunk_text"],
                    chunk.get("topic_tags", ""),
                    chunk["scrape_date"]
                )
            )
            inserted_count += 1
        conn.commit()
    return inserted_count
