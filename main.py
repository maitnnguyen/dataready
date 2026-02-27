import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class AnalysisRequest(BaseModel):
    problem: str
    focus: List[str]
    depth: str  # "quick" or "full"

def build_prompt(problem: str, focus: List[str], depth: str) -> str:
    is_quick = depth == "quick"
    return f"""You are a senior data & AI consultant running a {"quick" if is_quick else "full"} discovery assessment. A client has described the following challenge:

"{problem}"

Focus areas requested: {", ".join(focus)}.

Respond ONLY with a JSON object (no markdown, no preamble, no code fences) in this exact structure:
{{
  "summary": "2-sentence executive summary of the core challenge",
  "readiness_score": <integer 1-10>,
  "readiness_label": "<one of: Critical, Low, Developing, Moderate, Strong>",
  "readiness_rationale": "1-2 sentences explaining the score",
  "capability_gaps": [
    {{ "area": "short area name", "severity": "<high|medium>", "description": "one sentence" }}
  ],
  "governance_flags": ["flag 1", "flag 2"],
  "next_steps": [
    {{ "priority": 1, "action": "concrete action", "owner": "who should own this", "timeframe": "e.g. Week 1-2" }}
  ],
  "key_questions": ["question for client 1", "question 2", "question 3"]
}}

{"Provide 3 gaps, 3 next steps, 2 governance flags, 3 key questions." if is_quick else "Provide 5 gaps, 5 next steps, 3 governance flags, 4 key questions. Be detailed."}"""


@app.post("/api/analyse")
async def analyse(req: AnalysisRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    if not req.problem.strip():
        raise HTTPException(status_code=400, detail="Problem description is required")

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "content-type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": build_prompt(req.problem, req.focus, req.depth)}],
                "max_tokens": 1500,
                "temperature": 0.3,
            },
        )

    if response.status_code != 200:
        print(f"Groq error {response.status_code}: {response.text}")
        raise HTTPException(status_code=502, detail=f"Upstream API error: {response.text}")

    data = response.json()

    try:
        raw = data["choices"][0]["message"]["content"]
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
    except Exception as e:
        print(f"Parse error: {e} | raw: {data}")
        raise HTTPException(status_code=502, detail="Failed to parse model response")

    return result


# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
