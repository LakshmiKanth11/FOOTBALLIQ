from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.generate import answer
from fastapi.responses import RedirectResponse

app = FastAPI(title="FootballIQ")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


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
