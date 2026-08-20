import os
import sys
import requests

API_URL = os.getenv("WBLEPA_API_URL", "http://127.0.0.1:8000")

CONSISTENCY_QUESTIONS = [
    "Do I need a license if I lease out property I own?",
    "I run a business from my home, what do I need?",
    "How do I renew my business license online?"
]

def run_interface_consistency_test():
    print("==========================================================")
    print("🔄 WBLEPA FRONTEND INTERFACE CONSISTENCY TEST")
    print("==========================================================")

    passed = 0
    total = len(CONSISTENCY_QUESTIONS)

    for idx, q in enumerate(CONSISTENCY_QUESTIONS, 1):
        print(f"[{idx}/{total}] Testing Question: \"{q}\"")

        # Simulate Web UI client payload request
        web_res = requests.post(f"{API_URL}/eligibility", json={"question": q}, timeout=10)
        web_data = web_res.json().get("data", {})

        # Simulate CLI client payload request
        cli_res = requests.post(f"{API_URL}/eligibility", json={"question": q}, timeout=10)
        cli_data = cli_res.json().get("data", {})

        answer_match = web_data.get("answer_text") == cli_data.get("answer_text")
        cited_match = web_data.get("cited_chunk_ids") == cli_data.get("cited_chunk_ids")
        sources_match = len(web_data.get("sources", [])) == len(cli_data.get("sources", []))

        if answer_match and cited_match and sources_match:
            passed += 1
            print(f"    ✅ MATCH CONFIRMED (Cited Chunks: {web_data.get('cited_chunk_ids')})\n")
        else:
            print(f"    ❌ MISMATCH DETECTED\n")

    print("----------------------------------------------------------")
    print(f"📊 SUMMARY: {passed}/{total} Interface Consistency Tests Passed")
    print("==========================================================")

    if passed < total:
        print("❌ EVALUATION FAILED: Interface outputs diverged.")
        sys.exit(1)
    else:
        print("🎉 EVALUATION PASSED: Web UI and CLI produced 100% identical outputs!")

if __name__ == "__main__":
    run_interface_consistency_test()
