import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for model in ["gemini-3.8-flash", "gemini-3.7-flash"]:
    try:
        r = client.models.generate_content(model=model, contents="Say hello in 5 words.")
        print(model, "->", r.text)
    except Exception as e:
        print(model, "-> FAILED:", str(e)[:150])