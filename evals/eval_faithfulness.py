import time
from app.generate import answer

# Questions the data should NOT answer -> the system should refuse
OUT_OF_SCOPE = [
    "Who is the president of India?",
    "What is the capital of Japan?",
    "Who wrote the play Hamlet?",
    "How do I bake sourdough bread?",
    "What is the boiling point of water?",
    "What is the ticket price for a Real Madrid match tomorrow?",
    "Who is the head coach of the Russia national team?",
    "Who painted the Mona Lisa?",
    "What is the chemical symbol for gold?",
]

# Questions the data CAN answer -> should answer, with this keyword inside
IN_SCOPE = [
    ("In what year was Messi born?", "1987"),
    ("Which club did Ronaldo join in Saudi Arabia?", "Al-Nassr"),
    ("Which stadium hosts Barcelona home games?", "Camp Nou"),
    ("Which English club plays at Anfield?", "Liverpool"),
    ("Which player is nicknamed CR7?", "Ronaldo"),
]


def refused(text):
    t = text.lower().replace("\u2019", "'")
    return "enough information" in t


print("=== OUT OF SCOPE (should refuse) ===")
correct_refusals = 0
for q in OUT_OF_SCOPE:
    r = answer(q)
    ok = refused(r["answer"])
    correct_refusals += ok
    print(f"{'REFUSED ' if ok else 'ANSWERED'} [{r['model']}] {q}")
    if not ok:
        print("    ->", r["answer"][:150].replace("\n", " "))
    time.sleep(1)

print("\n=== IN SCOPE (should answer) ===")
correct_answers = 0
for q, keyword in IN_SCOPE:
    r = answer(q)
    ok = (not refused(r["answer"])) and keyword.lower() in r["answer"].lower()
    correct_answers += ok
    print(f"{'OK  ' if ok else 'MISS'} [{r['model']}] {q}")
    if not ok:
        print("    ->", r["answer"][:150].replace("\n", " "))
    time.sleep(1)

print(f"\nCorrect refusals: {correct_refusals}/{len(OUT_OF_SCOPE)}")
print(f"Correct answers:  {correct_answers}/{len(IN_SCOPE)}")