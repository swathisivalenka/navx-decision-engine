from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "NavX backend running"}

@app.post("/analyze")
def analyze(query: Query):
    question = query.question

    url = "https://api.featherless.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = prompt = f"""
You are a smart decision-making assistant.

User question: {question}

Generate:
- 3 possible options
- For each option: pros and cons
- Mark one option as selected and others as eliminated
- Provide a final decision and reasoning

Return ONLY valid JSON like this:

{{
  "options": [
    {{
      "name": "Option A",
      "pros": ["..."],
      "cons": ["..."],
      "status": "selected"
    }},
    {{
      "name": "Option B",
      "pros": ["..."],
      "cons": ["..."],
      "status": "eliminated"
    }}
  ],
  "final_decision": "Option A",
  "reasoning": "Why it is best"
}}
"""

    data = {
    "model": "Sao10K/Fimbulvetr-11B-v2",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 500
}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(result)
    import re

    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            raise Exception("No JSON found")
    except:
        parsed = {
            "options": [],
            "final_decision": "Error parsing AI response",
            "reasoning": content
        }

    return parsed