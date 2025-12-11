from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
from typing import List, Literal

app = FastAPI(title="NoSQLNoEscape API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizQuestion(BaseModel):
    id: str
    level: Literal["basic", "standard", "hard"]
    question: str
    options: List[str]
    answerIndex: int
    explanation: str

class QuizResponse(BaseModel):
    total: int
    count: int
    level: str
    items: List[QuizQuestion]

with open("quiz_data.json", "r", encoding="utf-8") as f:
    _DATA: List[QuizQuestion] = [QuizQuestion(**q) for q in json.load(f)]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/quizzes", response_model=QuizResponse)
def get_quizzes(level: Literal["basic", "standard", "hard"] = "basic", count: int = 10, shuffle: bool = True):
    if count <= 0:
        raise HTTPException(status_code=400, detail="count must be positive")

    filtered = [q for q in _DATA if q.level == level]
    if not filtered:
        raise HTTPException(status_code=404, detail="level not found")

    items = filtered.copy()
    if shuffle:
        random.shuffle(items)
    items = items[:count]

    return QuizResponse(total=len(filtered), count=len(items), level=level, items=items)

@app.get("/quiz/{question_id}", response_model=QuizQuestion)
def get_quiz(question_id: str):
    for q in _DATA:
        if q.id == question_id:
            return q
    raise HTTPException(status_code=404, detail="question not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
