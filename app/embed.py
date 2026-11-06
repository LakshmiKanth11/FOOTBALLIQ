import json
import chromadb
from sentence_transformers import SentenceTransformer

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
print(f"Loaded {len(chunks)} chunks")

model = SentenceTransformer("all-mpnet-base-v2")

client = chromadb.PersistentClient(path="data/chroma")

# Start fresh so old embeddings don't mix with new ones
try:
    client.delete_collection("football")
except Exception:
    pass
collection = client.get_or_create_collection("football")

BATCH = 100
for start in range(0, len(chunks), BATCH):
    batch = chunks[start:start + BATCH]
    texts = [c["text"] for c in batch]
    # Embed the title + text, but store only the original text
    to_embed = [f"{c['source']}: {c['text']}" for c in batch]
    embeddings = model.encode(to_embed).tolist()
    collection.upsert(
        ids=[c["id"] for c in batch],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"]} for c in batch],
    )
    print(f"Stored {min(start + BATCH, len(chunks))}/{len(chunks)}")

print(f"\nDone! Database now holds {collection.count()} chunks")