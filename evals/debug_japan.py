from app.retrieve import retrieve

for i, r in enumerate(retrieve("What is the capital of Japan?", k=4), 1):
    print(f"\n[Source {i}] {r['source']}")
    print(r["text"])