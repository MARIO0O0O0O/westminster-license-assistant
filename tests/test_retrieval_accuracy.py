import os
import sys
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.retrieval.search import search

TEST_SET_PATH = os.path.join(PROJECT_ROOT, "tests", "retrieval_test_set.json")

def run_retrieval_evaluation():
    print("==========================================================")
    print("🎯 WBLEPA RETRIEVAL ENGINE ACCURACY EVALUATION")
    print("==========================================================")

    if not os.path.exists(TEST_SET_PATH):
        print(f"❌ Error: Test set file not found at {TEST_SET_PATH}")
        sys.exit(1)

    with open(TEST_SET_PATH, "r", encoding="utf-8") as f:
        test_questions = json.load(f)

    total_questions = len(test_questions)
    hits = 0

    print(f"Loaded {total_questions} test questions.\n")

    for q_data in test_questions:
        q_id = q_data["id"]
        question = q_data["question"]
        persona = q_data["persona"]
        expected_ids = set(q_data["expected_chunk_ids"])

        results = search(question, top_k=5)
        returned_ids = [r["id"] for r in results]

        matched = expected_ids.intersection(set(returned_ids))
        is_hit = len(matched) > 0

        if is_hit:
            hits += 1
            status_str = f"✅ HIT  (Matched: {', '.join(matched)})"
        else:
            status_str = f"❌ MISS (Expected: {', '.join(expected_ids)})"

        print(f"[{q_id}/{total_questions}] Question: \"{question}\"")
        print(f"      Persona : {persona}")
        print(f"      Status  : {status_str}")
        print(f"      Top-3 Results: {returned_ids[:3]}\n")

    hit_rate = (hits / total_questions) * 100
    print("----------------------------------------------------------")
    print(f"📊 SUMMARY: {hits}/{total_questions} Questions Passed Top-5 Retrieval")
    print(f"🎯 ACCURACY HIT-RATE: {hit_rate:.1f}%")
    print("==========================================================")

    if hit_rate < 80.0:
        print("❌ EVALUATION FAILED: Hit rate below 80% threshold.")
        sys.exit(1)
    else:
        print("🎉 EVALUATION PASSED: Hit rate exceeds 80% threshold!")

if __name__ == "__main__":
    run_retrieval_evaluation()
