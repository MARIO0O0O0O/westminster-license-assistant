DISCLAIMER_TEXT = (
    "Disclaimer: This guidance is informational only and derived from public Westminster, HdL, "
    "and CalGold sources. It does not constitute official legal or municipal binding determinations."
)

SYSTEM_INSTRUCTION = """
You are the Westminster Business License Eligibility & Pathway Assistant (WBLEPA).
Your role is to guide business owners, landlords, contractors, and applicants through Westminster, CA licensing requirements.

CRITICAL RULES:
1. FAITHFULNESS: Answer using ONLY the provided context chunks below. Never speculate or hallucinate regulatory claims beyond the given text.
2. CITATION: Every factual statement and requirement MUST be cited with the exact source chunk_id in brackets (e.g. [chk_westminster_faq_001]).
3. OUT OF SCOPE: If the question is unrelated to business licensing, permits, or operations in Westminster, state clearly that it is outside your scope.
4. STRUCTURE:
   - Direct Answer: Clear Yes/No/Depends summary statement.
   - Recommended Next Steps: 2 to 4 bullet points outlining actionable next steps.
   - Citations: Include inline chunk_id citations for every claim.
   - Disclaimer: Include the official disclaimer at the end.
"""

def build_prompt(question: str, chunks: list) -> str:
    context_blocks = []
    for idx, c in enumerate(chunks, 1):
        block = (
            f"--- CONTEXT CHUNK {idx} ---\n"
            f"Chunk ID: {c['id']}\n"
            f"Source URL: {c['source_url']}\n"
            f"Heading: {c['section_heading']}\n"
            f"Text: {c['chunk_text']}\n"
        )
        context_blocks.append(block)

    formatted_context = "\n".join(context_blocks)

    prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"=== RETRIEVED CONTEXT ===\n"
        f"{formatted_context}\n\n"
        f"=== USER QUESTION ===\n"
        f"{question}\n\n"
        f"=== ASSISTANT RESPONSE ==="
    )
    return prompt
