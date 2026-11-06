import json
import re
import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# Embedding model: must match app/embed.py
model = SentenceTransformer("all-mpnet-base-v2")

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("football")

# Keyword index built from the same chunks
with open("data/chunks.json", encoding="utf-8") as f:
    CHUNKS = json.load(f)
BY_ID = {c["id"]: c for c in CHUNKS}


def tokenize(text):
    return re.findall(r"\w+", text.lower())


bm25 = BM25Okapi([tokenize(f"{c['source']}: {c['text']}") for c in CHUNKS])


def retrieve(question, k=4, pool=20):
    """Hybrid search: embeddings + keywords, merged by rank."""
    # 1. Embedding search
    q_emb = model.encode([question]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=pool)
    vec_ids = res["ids"][0]

    # 2. Keyword search
    scores = bm25.get_scores(tokenize(question))
    top = sorted(range(len(CHUNKS)), key=lambda i: scores[i], reverse=True)[:pool]
    kw_ids = [CHUNKS[i]["id"] for i in top]

    # 3. Merge: a chunk ranked high in either list gets a high score
    fused = {}
    for ranking in (vec_ids, kw_ids):
        for rank, cid in enumerate(ranking):
            fused[cid] = fused.get(cid, 0) + 1 / (60 + rank)

    best = sorted(fused, key=fused.get, reverse=True)[:k]
    # "distance" is kept so the other files still work; more negative = better
    return [
        {
            "text": BY_ID[cid]["text"],
            "source": BY_ID[cid]["source"],
            "distance": -fused[cid],
        }
        for cid in best
    ]


if __name__ == "__main__":
    while True:
        q = input("\nAsk a football question (or type quit): ")
        if q.lower() == "quit":
            break
        for r in retrieve(q):
            print(f"\n[{r['source']}] (score {r['distance']:.4f})")
            print(r["text"][:300], "...")