import os
import sys
import requests

PROD_API_URL = "https://westminster-license-assistant.onrender.com"
LOCAL_API_URL = "http://127.0.0.1:8000"

API_URL = os.getenv("WBLEPA_API_URL", LOCAL_API_URL)

def print_banner():
    mode_label = "PRODUCTION (Render)" if "onrender.com" in API_URL else "LOCAL (Termux)"
    print("\n" + "="*65)
    print("🏛️  WESTMINSTER BUSINESS LICENSE ELIGIBILITY ASSISTANT (WBLEPA)")
    print(f"   Mode: [{mode_label}] | API Endpoint: {API_URL}")
    print("   Unofficial Informational Guide for City & State Permits")
    print("="*65 + "\n")

def ask_question_cli():
    print("\n--- ❓ ASK A QUESTION ---")
    question = input("Enter your business licensing question: ").strip()
    if not question:
        print("⚠️ Question cannot be empty.")
        return

    print("\n⏳ Querying backend assistant...")
    try:
        res = requests.post(
            f"{API_URL}/eligibility",
            json={"question": question},
            timeout=15
        )
        if res.status_code == 200:
            data = res.json().get("data", {})
            print("\n" + "="*60)
            print(f"Question: {data.get('question')}")
            print(f"In Scope: {'Yes' if data.get('in_scope') else 'No'}")
            print("="*60)
            print(f"\n{data.get('answer_text')}\n")
            
            sources = data.get("sources", [])
            if sources:
                print("🔗 CITED SOURCES & REFERENCES:")
                for idx, src in enumerate(sources, 1):
                    print(f"   [{idx}] {src['section_heading']}")
                    print(f"       URL: {src['source_url']}")
            print("="*60 + "\n")
        else:
            print(f"❌ Error from server: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def browse_topic_cli():
    print("\n--- 📂 BROWSE REQUIREMENT CHECKLIST BY TOPIC ---")
    topics = [
        ("1", "home-business", "Home Occupation Permits & Rules"),
        ("2", "landlord", "Residential & Commercial Landlord Licensing"),
        ("3", "contractor", "In-City & Out-of-City Contractor Registration"),
        ("4", "renewal", "Annual Renewals & Delinquent Penalty Dates"),
        ("5", "police-permit", "Special Permits (Massage/Auto/Alcohol/CUP)"),
        ("6", "state-permits", "State & County Permits (CalGold/OC Health/CDTFA)")
    ]

    for num, tag, label in topics:
        print(f"  {num}) {label} ({tag})")

    choice = input("\nSelect topic (1-6): ").strip()
    selected_topic = None
    for num, tag, label in topics:
        if choice == num or choice == tag:
            selected_topic = tag
            break

    if not selected_topic:
        selected_topic = "home-business"

    print(f"\n⏳ Fetching checklist for topic: {selected_topic}...")
    try:
        res = requests.get(f"{API_URL}/checklist?topic={selected_topic}", timeout=15)
        if res.status_code == 200:
            items = res.json().get("data", {}).get("items", [])
            print(f"\n📋 CHECKLIST ({len(items)} Items Found):\n")
            for idx, item in enumerate(items, 1):
                print(f"  [{idx}] {item['section_heading']}")
                print(f"      Tags: {item['topic_tags']}")
                print(f"      Snippet: {item['snippet']}")
                print(f"      URL: {item['source_url']}\n")
        else:
            print(f"❌ Error from server: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def view_sources_cli():
    print("\n--- 🌐 LOCKED PUBLIC SOURCE URLS ---")
    try:
        res = requests.get(f"{API_URL}/sources", timeout=15)
        if res.status_code == 200:
            sources = res.json().get("data", {}).get("sources", [])
            print(f"Found {len(sources)} verified public sources:\n")
            for idx, s in enumerate(sources, 1):
                print(f"  [{idx}] {s['title']}")
                print(f"      URL: {s['url']}")
                print(f"      Tags: {s['default_tags']}\n")
        else:
            print(f"❌ Error from server: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def toggle_endpoint_cli():
    global API_URL
    if API_URL == LOCAL_API_URL:
        API_URL = PROD_API_URL
        print(f"\n🔄 Switched API endpoint to PRODUCTION: {PROD_API_URL}\n")
    else:
        API_URL = LOCAL_API_URL
        print(f"\n🔄 Switched API endpoint to LOCAL: {LOCAL_API_URL}\n")

def main():
    print_banner()
    while True:
        print("MAIN MENU:")
        print("  1) ❓ Ask an Eligibility Question")
        print("  2) 📂 Browse Checklist by Topic")
        print("  3) 🌐 View Locked Source URLs")
        print("  4) ⚙️ Toggle API Endpoint (Local vs Prod)")
        print("  5) 🚪 Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        if choice == "1":
            ask_question_cli()
        elif choice == "2":
            browse_topic_cli()
        elif choice == "3":
            view_sources_cli()
        elif choice == "4":
            toggle_endpoint_cli()
        elif choice in ["5", "exit", "q", "quit"]:
            print("\nThank you for using the Westminster Business License Assistant. Goodbye! 👋\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, 3, 4, or 5.\n")

if __name__ == "__main__":
    main()
