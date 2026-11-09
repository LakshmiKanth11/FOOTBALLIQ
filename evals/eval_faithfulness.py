import time
from app.generate import answer

OUT_OF_SCOPE = [
    "Who is the president of India?",
    "Who wrote the play Hamlet?",
    "How do I bake sourdough bread?",
    "What is the boiling point of water?",
    "What is the ticket price for a Real Madrid match tomorrow?",
    "Who is the head coach of the Russia national team?",
    "Who painted the Mona Lisa?",
    "What is the chemical symbol for gold?",
]


# Borderline: the context only implies the answer. Shown, not scored.
BORDERLINE = ["What is the capital of Japan?"]

IN_SCOPE = [
    ("In what year was Messi born?", "1987"),
    ("Which club did Ronaldo join in Saudi Arabia?", "Al-Nassr"),
    ("Which stadium hosts Barcelona home games?", "Camp Nou"),
    ("Which English club plays at Anfield?", "Liverpool"),
    ("Which player is nicknamed CR7?", "Ronaldo"),
]

PAUSE = 10  # seconds between questions, to stay under rate limits


def refused(text):
    return "enough information" in text.lower().replace("\u2019", "'")


ran_out = ok_out = ran_in = ok_in = 0

print("=== OUT OF SCOPE (should refuse) ===")
for q in OUT_OF_SCOPE:
    r = answer(q)
    if r["model"] is None:
        print("SKIPPED:", q)
    else:
        ran_out += 1
        ok = refused(r["answer"])
        ok_out += ok
        print(f"{'REFUSED ' if ok else 'ANSWERED'} [{r['model']}] {q}")
        if not ok:
            print("    ->", r["answer"][:150].replace("\n", " "))
    time.sleep(PAUSE)

print("\n=== IN SCOPE (should answer) ===")
for q, keyword in IN_SCOPE:
    r = answer(q)
    if r["model"] is None:
        print("SKIPPED:", q)
    else:
        ran_in += 1
        ok = (not refused(r["answer"])) and keyword.lower() in r["answer"].lower()
        ok_in += ok
        print(f"{'OK  ' if ok else 'MISS'} [{r['model']}] {q}")
        if not ok:
            print("    ->", r["answer"][:150].replace("\n", " "))
    time.sleep(PAUSE)

print("\n=== BORDERLINE (not scored) ===")
for q in BORDERLINE:
    r = answer(q)
    print(f"[{r['model']}] {q}\n    -> {r['answer'][:150]}".replace("\n    ->", "\n    ->"))

print(f"\nCorrect refusals: {ok_out}/{ran_out} (of {len(OUT_OF_SCOPE)} asked)")
print(f"Correct answers:  {ok_in}/{ran_in} (of {len(IN_SCOPE)} asked)")