import os
import sys
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.generation.generate_answer import answer_question, DISCLAIMER_TEXT

TEST_SET_PATH = os.path.join(PROJECT_ROOT, "tests", "retrieval_test_set.json")

OUT_OF_SCOPE_TESTS = [
    "What is the weather in Westminster?",
    "Can you help me file my personal income taxes?"
]

def run_generation_quality_evaluation():
    print("==========================================================")
    print("🧠 WBLEPA AI GENERATION LAYER QUALITY & FAITHFULNESS EVAL")
    print("==========================================================")

    if not os.path.exists(TEST_SET_PATH):
        print(f"❌ Error: Test set file not found at {TEST_SET_PATH}")
        sys.exit(1)

    with open(TEST_SET_PATH, "r", encoding="utf-8") as f:
        in_scope_questions = json.load(f)

    total_tests = len(in_scope_questions) + len(OUT_OF_SCOPE_TESTS)
    passed_tests = 0

    print(f"Evaluating {len(in_scope_questions)} In-Scope + {len(OUT_OF_SCOPE_TESTS)} Out-Of-Scope Questions...\n")

    # Part 1: In-Scope Questions Evaluation
    print("--- Part 1: In-Scope Questions & Citation Traceability ---")
    for q_data in in_scope_questions:
        q_id = q_data["id"]
        question = q_data["question"]
        persona = q_data["persona"]

        res = answer_question(question)
        answer_text = res["answer_text"]
        cited_ids = res["cited_chunk_ids"]
        retrieved_ids = set(res["retrieved_chunk_ids"])

        # Traceability validation: All cited IDs must exist in retrieved IDs
        unretrieved_citations = [cid for cid in cited_ids if cid not in retrieved_ids]

        is_valid_scope = res["in_scope"] is True
        is_valid_citations = len(cited_ids) > 0 and len(unretrieved_citations) == 0
        has_disclaimer = "Disclaimer:" in answer_text

        if is_valid_scope and is_valid_citations and has_disclaimer:
            passed_tests += 1
            status_str = f"✅ PASS (Citations Valid: {cited_ids})"
        else:
            status_str = f"❌ FAIL (Citations: {cited_ids}, Invalid: {unretrieved_citations})"

        print(f"[{q_id}/{total_tests}] Question: \"{question}\"")
        print(f"       Persona : {persona}")
        print(f"       Status  : {status_str}\n")

    # Part 2: Out-Of-Scope Questions Evaluation
    print("--- Part 2: Out-Of-Scope Handling & Safety ---")
    for idx, oos_q in enumerate(OUT_OF_SCOPE_TESTS, len(in_scope_questions) + 1):
        res = answer_question(oos_q)
        answer_text = res["answer_text"]

        is_valid_scope = res["in_scope"] is False
        has_disclaimer = "Disclaimer:" in answer_text

        if is_valid_scope and has_disclaimer:
            passed_tests += 1
            status_str = "✅ PASS (Correctly identified Out-Of-Scope)"
        else:
            status_str = "❌ FAIL (Failed Out-Of-Scope check)"

        print(f"[{idx}/{total_tests}] Question: \"{oos_q}\"")
        print(f"       Status  : {status_str}\n")

    pass_rate = (passed_tests / total_tests) * 100
    print("----------------------------------------------------------")
    print(f"📊 SUMMARY: {passed_tests}/{total_tests} Tests Passed")
    print(f"🎯 GENERATION FAITHFULNESS PASS-RATE: {pass_rate:.1f}%")
    print("==========================================================")

    if pass_rate < 100.0:
        print("❌ EVALUATION FAILED: Generation quality did not reach 100%.")
        sys.exit(1)
    else:
        print("🎉 EVALUATION PASSED: 100% Generation Faithfulness & Traceability Confirmed!")

if __name__ == "__main__":
    run_generation_quality_evaluation()
