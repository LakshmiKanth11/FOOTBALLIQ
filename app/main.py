from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.generate import answer

app = FastAPI(title="FootballIQ")


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(body: Question):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return answer(body.question)
