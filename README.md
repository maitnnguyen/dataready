# DataReady — AI Consulting Discovery Tool

> Turn a business problem into a structured consulting brief in seconds.

**[🚀 Live Demo →](https://dataready.onrender.com)** *(replace with your URL after deploying)*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## What it does

DataReady takes a plain-language description of a data or AI challenge and generates a structured consulting artifact — the kind a senior consultant would produce at the start of a discovery engagement:

| Output | Description |
|---|---|
| **Executive Summary** | 2-sentence framing of the core challenge |
| **Data Readiness Score** | 1–10 score with rationale |
| **Capability Gaps** | Identified gaps, colour-coded by severity |
| **Next Steps** | Prioritised actions with owner and timeframe |
| **Governance Flags** | Risks and compliance considerations |
| **Key Client Questions** | Questions to ask in the first workshop |

---

## Why I built this

I work at the intersection of data, AI, and business — and a recurring bottleneck in early-stage engagements is translating a messy problem statement into a structured starting point. This tool automates that first analytical step, freeing consultants to focus on the nuances that actually require human judgment.

It's built on the same frameworks I apply in my work: DAMA-aligned governance thinking, data readiness assessment, and structured discovery methodology.

---

## Tech stack

- **Backend**: FastAPI (Python) — lightweight, async, easy to deploy
- **Frontend**: Vanilla HTML/CSS/JS — no build step, loads fast
- **AI**: Groq API with Llama 3.1 (free tier, fast inference)
- **Deploy**: Render (free tier)

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/maitnnguyen/dataready.git
cd dataready
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set your API key**
```bash
export GROQ_API_KEY=gsk_your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com) — no credit card needed.

**5. Start the server**
```bash
uvicorn main:app --reload
```

**6. Open in browser**
```
http://localhost:8000
```

---

## Deploy to Render (free, 5 minutes)

1. Fork this repo to your GitHub account
2. Go to [render.com](https://render.com) and sign up (free)
3. Click **New → Web Service** → connect your GitHub repo
4. Render auto-detects `render.yaml` — just click **Deploy**
5. Go to **Environment** tab → add variable:
   - Key: `GROQ_API_KEY`
   - Value: your Groq API key
6. Your live URL will be `https://dataready-xxxx.onrender.com`

---

## About

Built by **Mai Nguyen** — data & AI consultant with a background in clinical data platforms, regulated domains, and business transformation.

- [LinkedIn](https://www.linkedin.com/in/mai-n-347a1331/)
- [GitHub](https://github.com/maitnnguyen)
