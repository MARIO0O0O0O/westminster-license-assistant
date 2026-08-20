import os
import sys
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.retrieval.search import search
from src.generation.prompt_template import build_prompt, DISCLAIMER_TEXT
from src.generation.llm_client import generate_llm_response

OUT_OF_SCOPE_KEYWORDS = [
    "weather", "temperature", "rain", "forecast", "personal income tax", "tax return",
    "sports", "football", "recipe", "movie", "president", "stock market", "crypto"
]

def check_out_of_scope(question: str) -> bool:
    q_lower = question.lower()
    for kw in OUT_OF_SCOPE_KEYWORDS:
        if kw in q_lower:
            return True
    return False

def answer_question(question: str) -> dict:
    if check_out_of_scope(question):
        out_msg = (
            f"I am the Westminster Business License Assistant. Your question (\"{question}\") "
            "is outside the scope of Westminster business licensing, permits, and municipal regulations. "
            "I can only assist with business license eligibility, renewals, landlord permits, contractor rules, "
            "and related city/state permit pathways.\n\n" + DISCLAIMER_TEXT
        )
        return {
            "question": question,
            "in_scope": False,
            "answer_text": out_msg,
            "cited_chunk_ids": [],
            "retrieved_chunk_ids": [],
            "disclaimer": DISCLAIMER_TEXT
        }

    chunks = search(question, top_k=5)
    
    # If top score is 0.0 or no chunks returned, handle as out of scope or ungrounded
    if not chunks or chunks[0]["score"] == 0.0:
        ungrounded_msg = (
            f"I could not find specific public records in the Westminster knowledge base to answer: \"{question}\". "
            "Please consult the Westminster Business License Division directly at (714) 548-3254.\n\n" + DISCLAIMER_TEXT
        )
        return {
            "question": question,
            "in_scope": False,
            "answer_text": ungrounded_msg,
            "cited_chunk_ids": [],
            "retrieved_chunk_ids": [c["id"] for c in chunks],
            "disclaimer": DISCLAIMER_TEXT
        }

    prompt = build_prompt(question, chunks)
    answer_text = generate_llm_response(prompt, chunks, question)

    # Extract cited chunk IDs using regex
    cited_ids = sorted(list(set(re.findall(r'\[(chk_[a-zA-Z0-9_]+)\]', answer_text))))

    return {
        "question": question,
        "in_scope": True,
        "answer_text": answer_text,
        "cited_chunk_ids": cited_ids,
        "retrieved_chunk_ids": [c["id"] for c in chunks],
        "disclaimer": DISCLAIMER_TEXT
    }

if __name__ == "__main__":
    test_q = sys.argv[1] if len(sys.argv) > 1 else "I run a business from my home, what do I need?"
    res = answer_question(test_q)
    print(f"Question: {res['question']}")
    print(f"In Scope: {res['in_scope']}")
    print(f"Cited Chunks: {res['cited_chunk_ids']}")
    print(f"Response:\n{res['answer_text']}")
