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
- **AI**: Claude API (Haiku model for speed and cost efficiency)
- **Deploy**: Render (free tier)

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/maitnnguyen/dataready.git
cd dataready
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**
```bash
export ANTHROPIC_API_KEY=your_key_here
```
Get a key at [console.anthropic.com](https://console.anthropic.com)

**4. Start the server**
```bash
uvicorn main:app --reload
```

**5. Open in browser**
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
   - Key: `ANTHROPIC_API_KEY`
   - Value: your Anthropic API key
6. Your live URL will be `https://dataready-xxxx.onrender.com`

---

## About

Built by **Mai Nguyen** — data & AI consultant with a background in clinical data platforms, regulated domains, and business transformation.

- [LinkedIn](https://www.linkedin.com/in/mai-n-347a1331/)
- [GitHub](https://github.com/maitnnguyen)
