from app.retrieve import retrieve

# (question, the page that should come back)
EVAL_SET = [
    ("Who is Lionel Messi?", "Lionel Messi"),
    ("Which Argentine player won the 2022 World Cup?", "Lionel Messi"),
    ("Who is Cristiano Ronaldo?", "Cristiano Ronaldo"),
    ("Which Portuguese forward plays for Al-Nassr?", "Cristiano Ronaldo"),
    ("Who is Pelé?", "Pelé"),
    ("Which Brazilian legend won three World Cups?", "Pelé"),
    ("Who is Diego Maradona?", "Diego Maradona"),
    ("What was the Hand of God goal?", "Diego Maradona"),
    ("Who is Kylian Mbappé?", "Kylian Mbappé"),
    ("Which French forward scored a hat-trick in the 2022 final?", "Kylian Mbappé"),
    ("Tell me about FC Barcelona", "FC Barcelona"),
    ("Which club plays at Camp Nou?", "FC Barcelona"),
    ("Tell me about Real Madrid", "Real Madrid CF"),
    ("Which club plays at the Santiago Bernabéu?", "Real Madrid CF"),
    ("Tell me about Manchester United", "Manchester United F.C."),
    ("Which club plays at Anfield?", "Liverpool F.C."),
    ("How does the FIFA World Cup work?", "FIFA World Cup"),
    ("How does the Champions League format work?", "UEFA Champions League"),
    ("How many teams are in the Premier League?", "Premier League"),
    ("What is the offside rule?", "Offside (association football)"),
    ("Who wins the Ballon d'Or?", "Ballon d'Or"),
    ("Who won the 2022 World Cup in Qatar?", "2022 FIFA World Cup"),
]

K = 4  # how many chunks we retrieve per question

hits = 0
rank_scores = 0.0

for question, expected in EVAL_SET:
    results = retrieve(question, k=K)
    sources = [r["source"] for r in results]

    if expected in sources:
        rank = sources.index(expected) + 1
        hits += 1
        rank_scores += 1 / rank
        print(f"PASS (rank {rank})  {question}")
    else:
        print(f"FAIL (got {sources[0]})  {question}")

total = len(EVAL_SET)
print(f"\nHit rate @{K}: {hits}/{total} = {hits / total:.0%}")
print(f"Average rank score (MRR): {rank_scores / total:.2f}")