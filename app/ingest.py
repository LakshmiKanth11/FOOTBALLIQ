import json
import os
import wikipediaapi

# 1. Connect to Wikipedia
wiki = wikipediaapi.Wikipedia(
    user_agent="FootballIQ/1.0 (ss903646@gmail.com)",
    language="en",
)

# 2. Which pages to download
PAGES = [
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Pelé",
    "Diego Maradona",
    "Kylian Mbappé",
    "FC Barcelona",
    "Real Madrid CF",
    "Manchester United F.C.",
    "Liverpool F.C.",
    "FIFA World Cup",
    "UEFA Champions League",
    "Premier League",
    "2022 FIFA World Cup",
    "2026 FIFA World Cup",
    "Offside (association football)",
    "Ballon d'Or",
]


# 3. Cut text into overlapping chunks of words
def chunk_text(text, size=200, overlap=40):
    words = text.split()
    chunks = []
    step = size - overlap
    for start in range(0, len(words), step):
        piece = " ".join(words[start:start + size])
        if piece:
            chunks.append(piece)
    return chunks


# 4. Download each page and chunk it
all_chunks = []
for title in PAGES:
    page = wiki.page(title)
    if not page.exists():
        print(f"SKIPPED (not found): {title}")
        continue
    pieces = chunk_text(page.text)
    for i, piece in enumerate(pieces):
        all_chunks.append({
            "id": f"{title}-{i}",
            "source": title,
            "text": piece,
        })
    print(f"{title}: {len(pieces)} chunks")

# 5. Save everything to a file
os.makedirs("data", exist_ok=True)
with open("data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(all_chunks)} chunks to data/chunks.json")
