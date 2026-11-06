from app.retrieve import retrieve

# (question, expected page, keyword that must appear in a retrieved chunk)
HARD_SET = [
    ("In what year was Messi born?", "Lionel Messi", "1987"),
    ("Which club did Ronaldo join in Saudi Arabia?", "Cristiano Ronaldo", "Al-Nassr"),
    ("How many Ballon d'Or awards has Messi won?", "Lionel Messi", "Ballon d'Or"),
    ("Which country did Maradona captain to the 1986 title?", "Diego Maradona", "Argentina"),
    ("Who scored the Hand of God goal against England?", "Diego Maradona", "England"),
    ("Which player is nicknamed CR7?", "Cristiano Ronaldo", "CR7"),
    ("What is the footballer known as the Brazilian king of football?", "Pelé", "Brazil"),
    ("Which French team does Mbappé play for in his youth?", "Kylian Mbappé", "Monaco"),
    ("Which stadium hosts Barcelona home games?", "FC Barcelona", "Camp Nou"),
    ("Which club is known as Los Blancos?", "Real Madrid CF", "Real Madrid"),
    ("Which English club is known as the Red Devils?", "Manchester United F.C.", "Old Trafford"),
    ("Which English club plays at Anfield?", "Liverpool F.C.", "Anfield"),
    ("Which tournament is held every four years for national teams?", "FIFA World Cup", "four years"),
    ("What is the top European club competition?", "UEFA Champions League", "Champions League"),
    ("What is the top division of English football?", "Premier League", "Premier League"),
    ("When is a player in an offside position?", "Offside (association football)", "offside"),
    ("Which award honours the best player of the year?", "Ballon d'Or", "Ballon d'Or"),
    ("Which country hosted the tournament won by Argentina in 2022?", "2022 FIFA World Cup", "Qatar"),
    ("Who won the penalty shootout in the 2022 final?", "2022 FIFA World Cup", "penalt"),
    ("Which player moved to Real Madrid from Manchester United in 2009?", "Cristiano Ronaldo", "Real Madrid"),
]

K = 4

page_hits = 0
answer_hits = 0

for question, page, keyword in HARD_SET:
    results = retrieve(question, k=K)
    page_ok = page in [r["source"] for r in results]
    answer_ok = any(keyword.lower() in r["text"].lower() for r in results)
    page_hits += page_ok
    answer_hits += answer_ok
    status = "OK  " if (page_ok and answer_ok) else "MISS"
    print(f"{status} page={'Y' if page_ok else 'N'} answer={'Y' if answer_ok else 'N'}  {question}")

n = len(HARD_SET)
print(f"\nPage hit rate @{K}:   {page_hits}/{n} = {page_hits / n:.0%}")
print(f"Answer hit rate @{K}: {answer_hits}/{n} = {answer_hits / n:.0%}")