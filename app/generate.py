import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from app.retrieve import retrieve

# Read the key from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Models to try, in order. If one fails, we move to the next.
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash"]


def ask_llm(prompt):
    """Try each model (2 attempts each). Return (text, model_used)."""
    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text, model
            except (errors.ServerError, errors.ClientError) as e:
                code = getattr(e, "code", "error")
                print(f"{model} failed ({code}), trying again...")
                time.sleep(2)
    return None, None


def answer(question):
    # 1. Find the most relevant chunks
    chunks = retrieve(question, k=4)

    # 2. Put them into a labelled block of context
    context = "\n\n".join(
        f"[Source {i + 1}: {c['source']}]\n{c['text']}"
        for i, c in enumerate(chunks)
    )

    # 3. Tell the AI exactly how to behave
    prompt = f"""You are FootballIQ, a football assistant.
Answer the question using ONLY the context below.
Cite sources like [Source 1]. If the context does not contain the answer,
say "I don't have enough information on that."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # 4. Ask the AI (with fallback)
    text, model_used = ask_llm(prompt)
    if text is None:
        return {"answer": "The AI service is busy. Please try again.",
                "sources": [], "model": None}

    return {
        "answer": text,
        "sources": sorted({c["source"] for c in chunks}),
        "model": model_used,
    }


if __name__ == "__main__":
    while True:
        q = input("\nAsk a football question (or type quit): ")
        if q.lower() == "quit":
            break
        result = answer(q)
        print("\n" + result["answer"])
        print("\nSources:", ", ".join(result["sources"]))
        print("Model used:", result["model"])