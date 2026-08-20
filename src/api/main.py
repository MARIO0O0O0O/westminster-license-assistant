import os
import sys
import sqlite3
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.generation.generate_answer import answer_question
from src.scraper.scrapers import SOURCES_CONFIG

DB_PATH = os.path.join(PROJECT_ROOT, "data", "corpus.db")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
REQUEST_LOG_PATH = os.path.join(LOG_DIR, "api_requests.log")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://westminster-license-assistant.vercel.app"
]

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="Westminster Business License Assistant (WBLEPA) API",
    description="Backend HTTP API providing RAG-powered guidance and official source checklists for Westminster business licensing.",
    version="1.0.0"
)

app.state.limiter = limiter

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    log_api_request(request.url.path, "RATE_LIMITED", [], False, "429 Rate Limit Exceeded")
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Rate limit exceeded (15 requests/minute). Please wait before making additional requests."
        }
    )

app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def log_api_request(endpoint: str, question: str, cited_ids: list, success: bool, error_msg: str = ""):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().isoformat()
    status_str = "SUCCESS" if success else f"ERROR: {error_msg}"
    log_line = f"[{timestamp}] {endpoint} | question: \"{question[:100]}\" | cited: {cited_ids} | status: {status_str}\n"
    with open(REQUEST_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)

def resolve_sources_metadata(cited_chunk_ids: list) -> list:
    if not cited_chunk_ids or not os.path.exists(DB_PATH):
        return []

    sources_map = {}
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(cited_chunk_ids))
        query = f"SELECT id, source_url, section_heading FROM chunks WHERE id IN ({placeholders})"
        cursor.execute(query, cited_chunk_ids)
        rows = cursor.fetchall()
        for cid, url, heading in rows:
            sources_map[cid] = {"id": cid, "source_url": url, "section_heading": heading}

    return [sources_map[cid] for cid in cited_chunk_ids if cid in sources_map]

class EligibilityRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="User question regarding Westminster business licensing or permits."
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_api_request(request.url.path, "", [], False, str(exc))
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": f"Internal Server Error: {str(exc)}"}
    )

@app.get("/health", summary="Health Check Endpoint")
async def health_check():
    return {
        "success": True,
        "data": {
            "status": "ok",
            "service": "WBLEPA Backend API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    }

@app.post("/eligibility", summary="Determine Business License Eligibility & Pathways")
@limiter.limit("15/minute")
async def post_eligibility(request: Request, req: EligibilityRequest):
    try:
        result = answer_question(req.question)
        cited_ids = result.get("cited_chunk_ids", [])
        sources = resolve_sources_metadata(cited_ids)

        log_api_request("/eligibility", req.question, cited_ids, True)

        return {
            "success": True,
            "data": {
                "question": result["question"],
                "in_scope": result["in_scope"],
                "answer_text": result["answer_text"],
                "cited_chunk_ids": cited_ids,
                "sources": sources,
                "disclaimer": result["disclaimer"]
            }
        }
    except Exception as e:
        log_api_request("/eligibility", req.question, [], False, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/checklist", summary="Get Requirement Checklist by Topic Tag")
async def get_checklist(topic: str = Query("home-business", description="Topic keyword filter")):
    try:
        if not os.path.exists(DB_PATH):
            return {"success": False, "error": "Corpus database not found"}

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            pattern = f"%{topic.strip().lower()}%"
            query = """
            SELECT id, source_url, section_heading, chunk_text, topic_tags
            FROM chunks
            WHERE LOWER(topic_tags) LIKE ? OR LOWER(section_heading) LIKE ?
            """
            cursor.execute(query, (pattern, pattern))
            rows = cursor.fetchall()

        checklist_items = []
        for cid, url, heading, text, tags in rows:
            snippet = text.split("\n")[0][:180] + ("..." if len(text) > 180 else "")
            checklist_items.append({
                "id": cid,
                "source_url": url,
                "section_heading": heading,
                "snippet": snippet,
                "topic_tags": tags
            })

        return {
            "success": True,
            "data": {
                "topic": topic,
                "total_items": len(checklist_items),
                "items": checklist_items
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sources", summary="Get List of Locked Source URLs")
async def get_sources():
    sources_list = []
    for cfg in SOURCES_CONFIG:
        sources_list.append({
            "slug": cfg["slug"],
            "title": cfg["title"],
            "url": cfg["url"],
            "default_tags": cfg["default_tags"]
        })
    return {
        "success": True,
        "data": {
            "total": len(sources_list),
            "sources": sources_list
        }
    }
