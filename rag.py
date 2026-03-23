"""
rag.py — Lightweight in-memory RAG for DataReady
- No vector DB needed (works on Render free tier / 512MB RAM)
- Uses Groq's free embedding endpoint (same API key you already have)
- Docs live in ./docs/{domain}/*.md — committed to git, survive redeploys
- Domain filtering: always searches general/ + the selected domain folder
"""

import os
import numpy as np
import httpx
from pathlib import Path
from typing import List

# ── Config ────────────────────────────────────────────────────────────────────
DOCS_DIR    = Path("./docs")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
EMBED_URL   = "https://api.groq.com/openai/v1/embeddings"
EMBED_MODEL = "nomic-embed-text-v1_5"

# ── In-memory store ───────────────────────────────────────────────────────────
_chunks:     List[str]          = []
_embeddings: np.ndarray | None  = None
_sources:    List[str]          = []
_domains:    List[str]          = []


# ── Text chunking ─────────────────────────────────────────────────────────────
def _chunk_text(
    text: str,
    source: str,
    domain: str = "general",
    size: int = 400,
    overlap: int = 80,
) -> List[dict]:
    """Split text into overlapping word-count chunks."""
    words  = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + size])
        chunks.append({"text": chunk, "source": source, "domain": domain})
        i += size - overlap
    return chunks


# ── Doc loader ────────────────────────────────────────────────────────────────
def _load_docs() -> List[dict]:
    """
    Walk ./docs recursively.
    Subfolder name becomes the domain label:
      docs/general/methodology.md          → domain = "general"
      docs/biopharma/biopharma-guide.md    → domain = "biopharma"
      docs/healthcare/healthcare-guide.md  → domain = "healthcare"
      docs/finance/finance-guide.md        → domain = "finance"
       docs/esg/emission-guide.md          → domain = "esg"
    Files directly in ./docs/ are treated as "general".
    """
    DOCS_DIR.mkdir(exist_ok=True)
    all_chunks = []

    for f in DOCS_DIR.glob("**/*"):
        if f.suffix not in {".txt", ".md"} or not f.is_file():
            continue
        try:
            domain = f.parent.name if f.parent != DOCS_DIR else "general"
            text   = f.read_text(encoding="utf-8")
            all_chunks.extend(_chunk_text(text, f.name, domain))
        except Exception as e:
            print(f"RAG: skipping {f.name} — {e}")

    return all_chunks


# ── Groq embedding call ───────────────────────────────────────────────────────
async def _embed(texts: List[str]) -> np.ndarray:
    """Embed a list of texts using Groq's free embedding endpoint."""
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            EMBED_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={"model": EMBED_MODEL, "input": texts},
        )
    if r.status_code != 200:
        raise RuntimeError(f"Groq embedding error {r.status_code}: {r.text}")
    data = r.json()["data"]
    return np.array([d["embedding"] for d in data], dtype=np.float32)


# ── Public: build index ───────────────────────────────────────────────────────
async def build_index():
    """
    Load all docs from ./docs and embed them into memory.
    Called once at app startup via FastAPI lifespan.
    Safe to call again after uploading new docs.
    """
    global _chunks, _embeddings, _sources, _domains

    raw = _load_docs()
    if not raw:
        print("RAG: no docs found in ./docs — RAG disabled until docs are added")
        return

    _chunks  = [c["text"]   for c in raw]
    _sources = [c["source"] for c in raw]
    _domains = [c["domain"] for c in raw]

    print(f"RAG: embedding {len(_chunks)} chunks from {len(set(_sources))} files...")
    _embeddings = await _embed(_chunks)
    print(f"RAG: index ready — {len(_chunks)} chunks across domains: {set(_domains)}")


# ── Public: retrieve ──────────────────────────────────────────────────────────
async def retrieve(query: str, domain: str = "general", top_k: int = 4) -> str:
    """
    Semantic search over the in-memory index.
    Always includes 'general' domain chunks plus the selected domain.
    Returns a formatted context string ready to inject into the LLM prompt.
    Returns empty string if index is empty or no relevant chunks found.
    """
    if _embeddings is None or len(_chunks) == 0:
        return ""

    try:
        # Domain mask: allow general + selected domain
        allowed = {"general", domain}
        mask    = np.array([d in allowed for d in _domains])

        if not mask.any():
            return ""

        # Embed the query
        q_vec  = await _embed([query])

        # Cosine similarity
        norm_q = q_vec       / (np.linalg.norm(q_vec,       axis=1, keepdims=True) + 1e-9)
        norm_d = _embeddings / (np.linalg.norm(_embeddings, axis=1, keepdims=True) + 1e-9)
        scores = (norm_d @ norm_q.T).squeeze()

        # Zero out out-of-domain chunks before ranking
        scores = np.where(mask, scores, -1.0)

        top_idx = np.argsort(scores)[::-1][:top_k]

        parts = []
        for i in top_idx:
            if scores[i] > 0.3:   # relevance threshold — ignore weak matches
                parts.append(f"[{_sources[i]}]\n{_chunks[i]}")

        return "\n\n---\n\n".join(parts)

    except Exception as e:
        print(f"RAG retrieve error: {e}")
        return ""   # graceful fallback — chat still works without RAG context
