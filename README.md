# FootballIQ
A RAG (retrieval-augmented generation) assistant that answers football questions with cited sources, built from Wikipedia pages. The focus of the project is **measuring and improving retrieval quality** with a hand-written eval set.

## How it works

```
Wikipedia pages → chunking → embeddings → ChromaDB ─┐
                                                    ├→ hybrid search → Gemini → answer + sources
                                   BM25 keyword index ┘
```

1. **Ingest:** download 16 Wikipedia pages (players, clubs, tournaments, rules) and split them into 200-word chunks with 40-word overlap (854 chunks).
2. **Embed:** embed each chunk with `all-mpnet-base-v2`, with the page title prepended for context, and store the vectors in ChromaDB.
3. **Retrieve:** hybrid search. Embedding search (meaning) and BM25 (exact words) are merged with reciprocal rank fusion.
4. **Generate:** the top chunks go to Gemini with a prompt that says to answer *only* from the context, cite `[Source N]`, and admit when the answer is missing.
5. **Resilience:** the LLM call retries on server errors and falls back across a list of models.

## Tech stack

Python · sentence-transformers · ChromaDB · rank-bm25 · Google Gemini API (`google-genai`) · python-dotenv

## Project structure

```
footballiq/
├── app/
│   ├── ingest.py       # download + chunk Wikipedia pages -> data/chunks.json
│   ├── embed.py        # embed chunks -> ChromaDB (data/chroma)
│   ├── retrieve.py     # hybrid search (embeddings + BM25)
│   ├── generate.py     # prompt + Gemini call with retry/fallback
│   └── main.py         # placeholder for the FastAPI app (not built yet)
├── evals/
│   ├── eval_retrieval.py   # 22 easy questions (hit rate, MRR)
│   ├── eval_hard.py        # 20 harder questions (page hit, answer hit)
│   └── debug_miss.py       # inspect why a question failed
├── list_models.py      # list Gemini models available to your key
├── test_llm.py         # quick check that the LLM responds
├── requirements.txt
└── README.md
```

## Setup (Windows)

```bash
git clone https://github.com/LakshmiKanth11/FOOTBALLIQ.git
cd FOOTBALLIQ
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On Mac/Linux, activate with `source .venv/bin/activate`.

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_key_here
```

Get a key at [aistudio.google.com](https://aistudio.google.com). Never commit `.env`.

In `app/ingest.py`, replace `your_email@example.com` in `user_agent` with your own email (Wikipedia asks for this).

## Run

Build the data once:

```bash
python app/ingest.py
python app/embed.py
```

Ask questions in the terminal:

```bash
python -m app.generate
```

Run the evals:

```bash
python -m evals.eval_retrieval
python -m evals.eval_hard
```

Run files with `python -m ...` from the project root (not a play button), so that `from app...` imports work.

## Retrieval experiments

Two hand-written test sets: 22 easy questions and 20 harder ones, including vague wording and multi-idea questions. **Page hit** = the right Wikipedia page appears in the top 4. **Answer hit** = a keyword from the answer appears in the top 4 chunks. **MRR** = how high the right page ranks (1.00 means always first).

| Experiment | Page hit | Answer hit | Easy eval (hit / MRR) |
|---|---|---|---|
| Baseline: MiniLM, k=4 | 95% | 95% | 100% / 0.98 |
| A: k=8 | 95% | 95% | not run |
| B: page title added to each chunk | 100% | 90% | 100% / 0.98 |
| C: B + `all-mpnet-base-v2` | 100% | 95% | 100% / 0.94 |
| D: C + hybrid search (BM25) | 95% | 100% | 100% / 0.98 |

## What I learned

- **More results didn't help (A).** Doubling k left the same two misses, so the problem was ranking, not the cutoff.
- **Context in the chunk helps page matching (B).** Chunks like "group stage, followed by..." don't say which page they came from. Prepending the title fixed one page miss.
- **A bigger embedding model handled a two-idea question (C)** ("which country hosted the tournament Argentina won in 2022") but lowered ranking on a few easy ones.
- **Embeddings miss exact phrases (D).** A question about a tournament "held every four years" failed with both models. Adding BM25 keyword search fixed it.
- **Index and query must use the same embedding model.** Changing one without the other raised a dimension-mismatch error (768 vs 384).
- **Retries and fallbacks matter.** The LLM API returned 503 "high demand" errors during development, so the generation step retries with backoff and falls back to a second model.

## Limitations

- **Small eval sets.** With 20-22 questions, one question moves a score by about 5 points, so differences between experiments are suggestive, not conclusive. The answer-hit metric is a keyword check and can pass by accident.
- **Hybrid search regressed one question.** The "hosted by / Argentina / 2022" question found the right page under C but not under D.
- **Generation not yet verified end to end.** LLM availability. Gemini returned intermittent 503 “high demand” errors during development, so generation retries, falls back to a second model, and finally to a local Ollama model.
- **Narrow data.** 16 Wikipedia pages only.

## Roadmap

- [ ] Verify end-to-end answers and add answer-quality evals (faithfulness, citations)
- [ ] Expand the eval set to 50+ questions
- [ ] Query rewriting for multi-idea questions
- [ ] FastAPI endpoint (`app/main.py`) and a simple chat UI
- [ ] Docker and deployment to a live URL
