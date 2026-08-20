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

PROMPT_INJECTION_KEYWORDS = [
    "ignore prior", "ignore previous", "forget rules", "tell me a joke", "write a poem",
    "system prompt", "jailbreak", "override instructions", "dan mode"
]

FOREIGN_LANGUAGE_KEYWORDS = [
    "tôi cần", "xin giấy phép", "giấy phép kinh doanh", "tiếng việt", "hola", "xin chào", "español"
]

def check_out_of_scope(question: str) -> tuple:
    """
    Returns (is_out_of_scope, reason_type)
    reason_type can be: "out_of_scope", "prompt_injection", "foreign_language", or None
    """
    q_lower = question.lower()
    
    for kw in PROMPT_INJECTION_KEYWORDS:
        if kw in q_lower:
            return True, "prompt_injection"

    for kw in FOREIGN_LANGUAGE_KEYWORDS:
        if kw in q_lower:
            return True, "foreign_language"

    for kw in OUT_OF_SCOPE_KEYWORDS:
        if kw in q_lower:
            return True, "out_of_scope"

    return False, None

def answer_question(question: str) -> dict:
    is_out, reason = check_out_of_scope(question)

    if is_out:
        if reason == "prompt_injection":
            out_msg = (
                "Safety Notice: I am the Westminster Business License Assistant. I cannot comply with requests "
                "to override system rules, ignore instructions, or generate unrelated content. I can only assist "
                "with Westminster business licensing, permits, and municipal regulations.\n\n" + DISCLAIMER_TEXT
            )
        elif reason == "foreign_language":
            out_msg = (
                "Language Notice: The Westminster Business License Assistant currently operates in English. "
                "Please submit your licensing query in English for accurate guidance.\n\n" + DISCLAIMER_TEXT
            )
        else:
            out_msg = (
                f"I am the Westminster Business License Assistant. Your question (\"{question[:100]}\") "
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
    
    if not chunks or chunks[0]["score"] == 0.0:
        ungrounded_msg = (
            f"I could not find specific public records in the Westminster knowledge base to answer: \"{question[:100]}\". "
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

    cited_ids = sorted(list(set(re.findall(r'\[(chk_[a-zA-Z0-9_]+)\]', answer_text))))

    return {
        "question": question,
        "in_scope": True,
        "answer_text": answer_text,
        "cited_chunk_ids": cited_ids,
        "retrieved_chunk_ids": [c["id"] for c in chunks],
        "disclaimer": DISCLAIMER_TEXT
    }
