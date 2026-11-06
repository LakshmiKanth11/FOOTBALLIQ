import json
from app.retrieve import retrieve

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

CASES = [
    ("Which tournament is held every four years for national teams?", "FIFA World Cup", "four years"),
    ("Which country hosted the tournament won by Argentina in 2022?", "2022 FIFA World Cup", "Qatar"),
]

for question, page, keyword in CASES:
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    in_data = [
        c["id"] for c in chunks
        if c["source"] == page and keyword.lower() in c["text"].lower()
    ]
    print(f"Chunks on '{page}' containing '{keyword}': {len(in_data)} -> {in_data[:5]}")
    for r in retrieve(question, k=4):
        print(f"\n  [{r['source']}] distance {r['distance']:.3f}")
        print("  ", r["text"][:200], "...")