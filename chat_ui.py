import os
import subprocess
import sys

import gradio as gr

# First start (e.g. on a fresh server): build the knowledge base
if not os.path.exists("data/chroma"):
    subprocess.run([sys.executable, "app/ingest.py"], check=True)
    subprocess.run([sys.executable, "app/embed.py"], check=True)

from app.generate import answer


def chat(message, history):
    result = answer(message)
    text = result["answer"]
    if result["sources"]:
        text += "\n\n*Sources: " + ", ".join(result["sources"]) + "*"
    return text


demo = gr.ChatInterface(
    fn=chat,
    title="FootballIQ",
    description="Ask football questions. Answers come only from Wikipedia pages, with sources.",
    examples=[
        "Who is Cristiano Ronaldo?",
        "What is the offside rule?",
        "Who won the 2022 World Cup?",
    ],
)

if __name__ == "__main__":
    demo.launch()