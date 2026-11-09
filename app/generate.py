import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from app.retrieve import retrieve

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Cloud models to try first, in order
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash"]
# Local model used if every cloud model fails
LOCAL_MODEL = "llama3.2"


def ask_gemini(prompt):
    """Try each Gemini model twice. Return (text, model) or (None, None)."""
    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text, model
            except (errors.ServerError, errors.ClientError) as e:
                print(f"{model} failed ({getattr(e, 'code', 'error')}), trying again...")
                time.sleep(15 if getattr(e, "code", None) == 429 else 2)
    return None, None


def ask_local(prompt):
    """Ask the local Ollama model. Return (text, model) or (None, None)."""
    try:
        import ollama
        response = ollama.chat(
            model=LOCAL_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"], f"{LOCAL_MODEL} (local)"
    except Exception as e:
        print(f"Local model failed: {str(e)[:120]}")
        return None, None


def ask_llm(prompt):
    mode = os.getenv("LLM_MODE", "auto")  # auto | gemini | local
    if mode == "local":
        return ask_local(prompt)
    text, model = ask_gemini(prompt)
    if text is None and mode == "auto":
        print("Cloud models unavailable, using local model...")
        text, model = ask_local(prompt)
    return text, model


def answer(question):
    chunks = retrieve(question, k=4)

    context = "\n\n".join(
        f"[Source {i + 1}: {c['source']}]\n{c['text']}"
        for i, c in enumerate(chunks)
    )

    prompt = f"""You are FootballIQ, a football assistant.
Answer the question using ONLY the context below. Do not use outside
knowledge, even if you are sure of the answer. Cite sources like [Source 1],
and only cite a source if it explicitly states the fact.
If the context does not explicitly answer the question,
say "I don't have enough information on that."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    text, model_used = ask_llm(prompt)
    if text is None:
        return {"answer": "No AI model is available right now. Please try again.",
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