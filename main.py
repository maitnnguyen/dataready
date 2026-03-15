import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="DataReady — AI Data Consulting", version="2.0.0")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"

# ── Models ────────────────────────────────────────────────────────────────────
ANALYSIS_MODEL = "llama-3.3-70b-versatile"   # upgraded from 8b
CHAT_MODEL     = "llama-3.3-70b-versatile"

# ── Domain personas ───────────────────────────────────────────────────────────
DOMAIN_PERSONAS = {
    "biopharma": """Finished PhD in bioinformatics and precision medicine (oncology), 
bioinformatics pipelilnes, clinical trials, and real-world evidence. 
Deep expertise in OMOP CDM, CDISC (SDTM/ADaM), FHIR R4, HL7, ICH E6/E8 guidelines. 
Understand GxP data governance, 21 CFR Part 11, pharmacovigilance, and biomarker analysis 
pipelines. You speak the language of CDOs, heads of data science, and clinical operations 
leaders in life sciences.""",

    "healthcare": """Senior data & AI consultant specialising in healthcare 
IT, hospital systems, and clinical data governance. Deep expertise in 
EHR/EMR systems, FHIR R4, HL7 v2/v3, ICD-10/SNOMED coding, NHS/HIPAA/GDPR 
compliance, and clinical decision support systems. Understand the operational 
realities of hospital data teams, interoperability challenges, and patient safety 
data requirements.""",

    "finance": """Data & AI consultant specialising in financial 
services data strategy. Deep expertise in data governance frameworks 
(BCBS 239, DAMA-DMBOK), regulatory reporting (MiFID II, Basel III), risk data 
aggregation, and ML model risk management. You understand the challenges of 
legacy core banking systems, data lineage, and model validation requirements.""",

    "general": """Senior data & AI consultant with 15+ years of experience 
across multiple industries. You apply DAMA-DMBOK governance frameworks, have deep 
knowledge of modern data stack architecture, MLOps, and organisational change 
management. You are pragmatic, direct, and focused on actionable outcomes.""",
}

# ── Schemas ───────────────────────────────────────────────────────────────────
class AnalysisRequest(BaseModel):
    problem:  str
    focus:    List[str]
    depth:    str                   # "quick" | "full"
    domain:   str = "general"      # "biopharma" | "healthcare" | "finance" | "general"

class ChatRequest(BaseModel):
    message:  str
    context:  dict                  # previous analysis result
    history:  List[dict] = []       # conversation history [{role, content}]
    domain:   str = "general"

class RefinementRequest(BaseModel):
    analysis: dict                  # original analysis
    section:  str                   # which section to refine
    instruction: str                # what to change
    domain:   str = "general"


# ── Prompt builder ────────────────────────────────────────────────────────────
def build_analysis_prompt(problem: str, focus: List[str], depth: str, domain: str) -> str:
    is_quick = depth == "quick"
    gaps      = 3 if is_quick else 6
    steps     = 3 if is_quick else 6
    flags     = 2 if is_quick else 4
    questions = 3 if is_quick else 5

    return f"""You are conducting a {"rapid" if is_quick else "comprehensive"} data readiness assessment.

CLIENT CHALLENGE:
"{problem}"

FOCUS AREAS: {", ".join(focus)}
DOMAIN: {domain}

Respond ONLY with a valid JSON object — no markdown, no preamble, no code fences.

{{
  "summary": "2-sentence executive summary of the core challenge and what is at stake",
  "readiness_score": <integer 1-10>,
  "readiness_label": "<one of: Critical | Low | Developing | Moderate | Strong>",
  "readiness_rationale": "2-3 sentences explaining the score with specific reasoning",
  "maturity_dimensions": {{
    "data_quality":      <integer 1-10>,
    "governance":        <integer 1-10>,
    "infrastructure":    <integer 1-10>,
    "people_process":    <integer 1-10>,
    "analytics_ai":      <integer 1-10>
  }},
  "capability_gaps": [
    {{ "area": "short area name", "severity": "<critical|high|medium>", "description": "one specific, actionable sentence", "impact": "business impact if unaddressed" }}
  ],
  "governance_flags": [
    {{ "flag": "flag description", "risk_level": "<high|medium|low>", "regulation": "relevant regulation if applicable" }}
  ],
  "next_steps": [
    {{ "priority": 1, "action": "concrete specific action", "owner": "role who should own this", "timeframe": "e.g. Week 1-2", "effort": "<low|medium|high>" }}
  ],
  "key_questions": ["specific probing question 1", "question 2"],
  "quick_wins": ["something achievable in <2 weeks", "another quick win"],
  "recommended_tools": ["specific tool or framework relevant to their stack"]
}}

Provide exactly {gaps} capability_gaps, {steps} next_steps, {flags} governance_flags, {questions} key_questions, 3 quick_wins, 3 recommended_tools.
Be specific to their domain and challenge — avoid generic consulting clichés."""


# ── Groq helper ───────────────────────────────────────────────────────────────
async def call_groq(messages: list, model: str, max_tokens: int = 2000, temperature: float = 0.3) -> str:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={
                "model":       model,
                "messages":    messages,
                "max_tokens":  max_tokens,
                "temperature": temperature,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Groq API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/api/analyse")
async def analyse(req: AnalysisRequest):
    """
    Generate a full data readiness consulting brief.
    Upgraded: llama-3.3-70b, domain personas, maturity dimensions, quick wins.
    """
    if not req.problem.strip():
        raise HTTPException(status_code=400, detail="Problem description is required")

    persona = DOMAIN_PERSONAS.get(req.domain, DOMAIN_PERSONAS["general"])
    prompt  = build_analysis_prompt(req.problem, req.focus, req.depth, req.domain)

    messages = [
        {"role": "system", "content": persona},
        {"role": "user",   "content": prompt},
    ]

    raw = await call_groq(messages, ANALYSIS_MODEL, max_tokens=2500, temperature=0.3)

    try:
        clean  = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        result["domain"] = req.domain   # echo back for frontend
        return result
    except Exception as e:
        print(f"Parse error: {e} | raw: {raw[:500]}")
        raise HTTPException(status_code=502, detail="Failed to parse model response")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """
    Multi-turn follow-up conversation about the analysis.
    User can ask follow-up questions, request clarification, or explore specific areas.
    """
    persona = DOMAIN_PERSONAS.get(req.domain, DOMAIN_PERSONAS["general"])

    system = f"""{persona}

The client has received a data readiness assessment with the following results:
- Overall readiness score: {req.context.get('readiness_score', 'N/A')}/10 ({req.context.get('readiness_label', '')})
- Summary: {req.context.get('summary', '')}
- Key gaps: {', '.join([g.get('area','') for g in req.context.get('capability_gaps', [])])}

You are now in a consulting conversation with them. Be specific, direct, and practical.
Reference their actual situation. Give concrete recommendations, not generic advice.
Keep responses concise — 3-5 sentences unless a detailed explanation is clearly needed."""

    messages = [
        {"role": "system",    "content": system},
        {"role": "assistant", "content": f"I've completed your data readiness assessment — score {req.context.get('readiness_score','N/A')}/10. What would you like to explore further?"},
        *req.history,
        {"role": "user",      "content": req.message},
    ]

    reply = await call_groq(messages, CHAT_MODEL, max_tokens=600, temperature=0.5)
    return {"reply": reply}


@app.post("/api/refine")
async def refine(req: RefinementRequest):
    """
    Refine a specific section of the analysis based on user instruction.
    e.g. 'Make the next steps more specific to a team of 3 people'
    """
    persona = DOMAIN_PERSONAS.get(req.domain, DOMAIN_PERSONAS["general"])
    section_data = req.analysis.get(req.section, {})

    prompt = f"""The client wants to refine the '{req.section}' section of their data readiness assessment.

Current content:
{json.dumps(section_data, indent=2)}

Client instruction: "{req.instruction}"

Respond ONLY with the updated JSON for the '{req.section}' field — same structure, refined content.
No preamble, no explanation, just the JSON value."""

    messages = [
        {"role": "system", "content": persona},
        {"role": "user",   "content": prompt},
    ]

    raw = await call_groq(messages, ANALYSIS_MODEL, max_tokens=800, temperature=0.3)

    try:
        clean   = raw.replace("```json", "").replace("```", "").strip()
        refined = json.loads(clean)
        return {"section": req.section, "refined": refined}
    except Exception as e:
        # Return as text if not valid JSON (e.g. for string fields)
        return {"section": req.section, "refined": raw.strip()}


@app.post("/api/action-plan")
async def action_plan(req: AnalysisRequest):
    """
    Generate a detailed 90-day action plan based on the analysis.
    """
    persona = DOMAIN_PERSONAS.get(req.domain, DOMAIN_PERSONAS["general"])

    prompt = f"""Based on this data challenge: "{req.problem}"
Focus areas: {", ".join(req.focus)}

Generate a structured 90-day action plan as JSON:
{{
  "vision": "one sentence: what success looks like at 90 days",
  "phases": [
    {{
      "phase": "Phase 1: Foundation",
      "weeks": "Weeks 1-4",
      "theme": "short theme",
      "objectives": ["objective 1", "objective 2"],
      "actions": [
        {{ "week": "Week 1", "action": "specific action", "owner": "role", "deliverable": "tangible output" }}
      ]
    }},
    {{
      "phase": "Phase 2: Build",
      "weeks": "Weeks 5-8",
      "theme": "short theme",
      "objectives": ["objective 1", "objective 2"],
      "actions": [
        {{ "week": "Week 5-6", "action": "specific action", "owner": "role", "deliverable": "tangible output" }}
      ]
    }},
    {{
      "phase": "Phase 3: Scale",
      "weeks": "Weeks 9-12",
      "theme": "short theme",
      "objectives": ["objective 1", "objective 2"],
      "actions": [
        {{ "week": "Week 9-10", "action": "specific action", "owner": "role", "deliverable": "tangible output" }}
      ]
    }}
  ],
  "success_metrics": ["KPI 1", "KPI 2", "KPI 3"],
  "risks": [
    {{ "risk": "description", "mitigation": "how to address" }}
  ]
}}

Be specific and actionable. No generic advice."""

    messages = [
        {"role": "system", "content": persona},
        {"role": "user",   "content": prompt},
    ]

    raw = await call_groq(messages, ANALYSIS_MODEL, max_tokens=2000, temperature=0.3)

    try:
        clean  = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail="Failed to parse action plan")


@app.get("/api/health")
async def health():
    return {
        "status":  "healthy",
        "version": "2.0.0",
        "model":   ANALYSIS_MODEL,
        "features": ["analysis", "chat", "refine", "action-plan"],
    }


# ── Serve frontend ────────────────────────────────────────────────────────────
app.mount("/", StaticFiles(directory="static", html=True), name="static")
