from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "NavX backend running"}

@app.post("/analyze")
def analyze(query: Query):
    return {
        "question": query.question,
        "options": [
            {
                "name": "Option A",
                "pros": ["High efficiency"],
                "cons": ["Takes time"],
                "status": "considered"
            },
            {
                "name": "Option B",
                "pros": ["Quick start"],
                "cons": ["Less scalable"],
                "status": "eliminated"
            }
        ],
        "final_decision": "Option A is الأفضل based on long-term benefits"
    }