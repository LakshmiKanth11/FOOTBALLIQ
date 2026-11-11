import json
from app.retrieve import retrieve

# (question, expected page, keyword, type)
NEW = [
    ("Where was Lionel Messi born?", "Lionel Messi", "Rosario", "direct"),
    ("Which club did Messi join in 2021 after leaving Barcelona?", "Lionel Messi", "Paris Saint-Germain", "direct"),
    ("Where was Cristiano Ronaldo born?", "Cristiano Ronaldo", "Funchal", "direct"),
    ("Which club did Pelé play for in Brazil?", "Pelé", "Santos", "direct"),
    ("Which Italian club did Maradona play for in Naples?", "Diego Maradona", "Napoli", "direct"),
    ("In which Paris suburb was Mbappé born?", "Kylian Mbappé", "Bondy", "direct"),
    ("Which region of Spain is FC Barcelona based in?", "FC Barcelona", "Catalonia", "direct"),
    ("Where does Liverpool play its home games?", "Liverpool F.C.", "Anfield", "direct"),
    ("Who won the first Ballon d'Or?", "Ballon d'Or", "Stanley Matthews", "direct"),
    ("Which organisation runs the Champions League?", "UEFA Champions League", "UEFA", "direct"),
    ("Which Argentine forward joined a Spanish academy as a teenager?", "Lionel Messi", "La Masia", "paraphrase"),
    ("Which Portuguese star began his senior career at Sporting?", "Cristiano Ronaldo", "Sporting", "paraphrase"),
    ("Which Brazilian won the World Cup at a very young age in 1958?", "Pelé", "1958", "paraphrase"),
    ("Which Argentine captain scored a controversial goal with his hand?", "Diego Maradona", "Hand of God", "paraphrase"),
    ("Which French striker moved to Paris from Monaco?", "Kylian Mbappé", "Monaco", "paraphrase"),
    ("Which Catalan club uses the motto 'more than a club'?", "FC Barcelona", "club", "paraphrase"),
    ("Which Spanish capital club has the most European Cup wins?", "Real Madrid CF", "European Cup", "paraphrase"),
    ("Which Merseyside club won the Champions League in 2019?", "Liverpool F.C.", "2019", "paraphrase"),
    ("Which player won the Ballon d'Or and the 2022 World Cup?", "Lionel Messi", "2022", "multi-fact"),
    ("Which tournament held in Qatar was won by Argentina?", "2022 FIFA World Cup", "Argentina", "multi-fact"),
    ("Which World Cup is hosted by the US, Canada and Mexico?", "2026 FIFA World Cup", "Canada", "multi-fact"),
    ("How many teams take part in the 2026 World Cup?", "2026 FIFA World Cup", "48", "multi-fact"),
    ("Which English club is based at Old Trafford and nicknamed the Red Devils?", "Manchester United F.C.", "Old Trafford", "multi-fact"),
    ("Which award is given to the best player each year by France Football?", "Ballon d'Or", "France Football", "multi-fact"),
]

K = 4

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

# 1. Validate: does the keyword actually exist in the expected page?
valid = []
for q, page, kw, kind in NEW:
    found = any(c["source"] == page and kw.lower() in c["text"].lower() for c in chunks)
    if found:
        valid.append((q, page, kw, kind))
    else:
        print(f"INVALID (keyword not in page, fix or drop): {q}  [{page} / '{kw}']")
print(f"\n{len(valid)}/{len(NEW)} questions valid\n")

# 2. Score
stats = {}
for q, page, kw, kind in valid:
    results = retrieve(q, k=K)
    page_ok = page in [r["source"] for r in results]
    ans_ok = any(kw.lower() in r["text"].lower() for r in results)
    s = stats.setdefault(kind, [0, 0, 0])
    s[0] += 1
    s[1] += page_ok
    s[2] += ans_ok
    if not (page_ok and ans_ok):
        print(f"MISS page={'Y' if page_ok else 'N'} answer={'Y' if ans_ok else 'N'} [{kind}] {q}")

print("\ntype         n   page   answer")
tn = tp = ta = 0
for kind, (n, p, a) in stats.items():
    print(f"{kind:<12} {n:<3} {p}/{n}    {a}/{n}")
    tn, tp, ta = tn + n, tp + p, ta + a
print(f"{'TOTAL':<12} {tn:<3} {tp}/{tn}    {ta}/{tn}")