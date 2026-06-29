"""
Tipsoi Support — standalone Q&A service (no MCP server required).

This is the simplest way to let someone use your model: you host this, hand out
an auth key + the link, and the recipient asks questions and gets answers.

It grounds every answer in the bundled Tipsoi knowledge base IN-PROCESS (BM25
retrieval from tipsoi_support_mcp.kb — pure stdlib, no MCP subprocess), then
asks Gemini to answer using only those excerpts.

  GET  /          → minimal chat web page (open the link, paste key, ask)
  GET  /health    → status
  POST /ask       → {"question": "...", "session_id": "..."} → {"answer": "..."}

Auth: send the key as `Authorization: Bearer <key>`, `X-API-Key: <key>`, or
(for the web page convenience) `?key=<key>`. Keys come from either:
  - QNA_API_KEYS  : comma-separated plaintext keys (simplest; great for deploy)
  - GATEWAY_KEYS_FILE : the revocable KeyStore file (manage_keys.py)

Env:
  GEMINI_API_KEY   your Gemini key (server-side only)
  GEMINI_MODEL     default gemini-3.5-flash
  QNA_API_KEYS     comma-separated allowed keys
  GATEWAY_KEYS_FILE optional path to a revocable key store
  QNA_RPM          per-key requests/min for env keys (default 30)
  QNA_TOP_K        KB articles to retrieve per question (default 4)
  SUPPORT_PHONE / SUPPORT_EMAIL  shown when the KB can't help

Run:
  pip install fastapi "uvicorn[standard]" google-genai
  export GEMINI_API_KEY=... QNA_API_KEYS=tsg_xxx
  uvicorn gateway.qna:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import hashlib
import hmac
import os
from contextlib import asynccontextmanager
import asyncio
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from google import genai

from tipsoi_support_mcp import kb
from tipsoi_support_mcp.persona import support_persona

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TOP_K = int(os.environ.get("QNA_TOP_K", "4"))
ENV_RPM = int(os.environ.get("QNA_RPM", "30"))
KEYS_FILE = os.environ.get("GATEWAY_KEYS_FILE", "")

from .ratelimit import RateLimiter

try:
    from .auth import KeyStore
except Exception:  # pragma: no cover
    KeyStore = None  # type: ignore


def _env_keys() -> list[str]:
    return [k.strip() for k in os.environ.get("QNA_API_KEYS", "").split(",") if k.strip()]


def _contacts() -> dict[str, str]:
    return {
        "phone": os.environ.get("SUPPORT_PHONE", "+8809638017170"),
        "email": os.environ.get("SUPPORT_EMAIL", "support@inovacetech.com"),
    }


class State:
    gemini: genai.Client
    limiter: RateLimiter
    store: Any
    persona: str


state = State()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.gemini = genai.Client()  # reads GEMINI_API_KEY
    state.limiter = RateLimiter()
    state.store = KeyStore(KEYS_FILE) if (KEYS_FILE and KeyStore) else None
    c = _contacts()
    state.persona = support_persona(c["phone"], c["email"])
    # warm the KB index
    kb.doc_count()
    yield


app = FastAPI(title="Tipsoi Support Q&A", version="1.0.0", lifespan=lifespan)


# ---- auth -----------------------------------------------------------------

def _verify(presented: str) -> tuple[str, int] | None:
    """Return (rate_key_id, rpm) for a valid key, else None."""
    if not presented:
        return None
    for k in _env_keys():
        if hmac.compare_digest(k, presented):
            kid = "env:" + hashlib.sha256(k.encode()).hexdigest()[:12]
            return kid, ENV_RPM
    if state.store is not None:
        rec = state.store.verify(presented)
        if rec:
            state.store.mark_used(rec.key_id)
            return rec.key_id, rec.rpm
    return None


async def require_key(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
    key: str | None = Query(default=None),
):
    presented = ""
    if authorization and authorization.lower().startswith("bearer "):
        presented = authorization[7:].strip()
    elif x_api_key:
        presented = x_api_key.strip()
    elif key:
        presented = key.strip()

    res = _verify(presented)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    key_id, rpm = res
    allowed, _remaining, reset_in = state.limiter.check(key_id, rpm)
    if not allowed:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded ({rpm}/min). Retry in {reset_in:.0f}s.",
                            headers={"Retry-After": str(int(reset_in) + 1)})
    return key_id


# ---- RAG answering --------------------------------------------------------

def _build_context(question: str) -> tuple[str, list[dict[str, Any]]]:
    hits = kb.search(question, limit=TOP_K)
    blocks = []
    for h in hits:
        art = kb.get_article(h["doc_id"])
        if art:
            blocks.append(f"## {art['title']}  (id: {h['doc_id']})\n{art['content'][:2200]}")
    return "\n\n".join(blocks), hits


def _gemini_answer(question: str, context: str) -> str:
    contacts = _contacts()
    prompt = (
        f"{state.persona}\n\n"
        "Answer the user's question using ONLY the knowledge base excerpts below. "
        "If the answer is not in them, say you don't have that information and give the "
        f"support contacts (Phone: {contacts['phone']}, Email: {contacts['email']}).\n\n"
        f"<knowledge_base>\n{context or '(no relevant articles found)'}\n</knowledge_base>\n\n"
        f"User question: {question}"
    )
    interaction = state.gemini.interactions.create(model=MODEL, input=prompt)
    return interaction.output_text


class AskRequest(BaseModel):
    question: str
    session_id: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL, "kb_articles": kb.doc_count(),
            "auth": {"env_keys": len(_env_keys()), "key_store": state.store is not None}}


@app.post("/ask")
async def ask(req: AskRequest, key_id: str = Depends(require_key)):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="question is required")
    context, hits = _build_context(q)
    answer = await asyncio.to_thread(_gemini_answer, q, context)
    return JSONResponse({
        "answer": answer,
        "sources": [{"doc_id": h["doc_id"], "title": h["title"]} for h in hits],
    })


# ---- minimal chat web page ------------------------------------------------

_PAGE = """<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Tipsoi Support Assistant</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,Segoe UI,Roboto,sans-serif;max-width:760px;margin:0 auto;padding:16px;background:#0b1020;color:#e7ecf5}
h1{font-size:1.15rem;margin:.2rem 0 1rem}
#log{display:flex;flex-direction:column;gap:10px;margin-bottom:90px}
.msg{padding:10px 14px;border-radius:14px;max-width:85%;white-space:pre-wrap;line-height:1.45}
.me{align-self:flex-end;background:#2563eb;color:#fff;border-bottom-right-radius:4px}
.bot{align-self:flex-start;background:#1a2238;border:1px solid #2a3556;border-bottom-left-radius:4px}
.src{font-size:.72rem;opacity:.7;margin-top:6px}
#bar{position:fixed;left:0;right:0;bottom:0;background:#0b1020;border-top:1px solid #2a3556;padding:10px;display:flex;gap:8px;max-width:760px;margin:0 auto}
#q{flex:1;padding:11px;border-radius:10px;border:1px solid #2a3556;background:#0f1730;color:#e7ecf5;font-size:1rem}
button{padding:11px 16px;border:0;border-radius:10px;background:#2563eb;color:#fff;font-weight:600;cursor:pointer}
button:disabled{opacity:.5}
.hint{font-size:.8rem;opacity:.7}
</style></head><body>
<h1>Tipsoi Support Assistant</h1>
<div id=log><div class="msg bot">Hi! Ask me anything about using Tipsoi — attendance, leave, payroll, shifts, devices, the mobile app. (English or বাংলা)</div></div>
<div id=bar><input id=q placeholder="Type your question…" autocomplete=off><button id=send>Send</button></div>
<script>
const log=document.getElementById('log'),q=document.getElementById('q'),send=document.getElementById('send');
const params=new URLSearchParams(location.search);
let key=params.get('key')||localStorage.getItem('tipsoi_key')||'';
if(params.get('key'))localStorage.setItem('tipsoi_key',key);
if(!key){key=prompt('Enter your access key (starts with tsg_):')||'';if(key)localStorage.setItem('tipsoi_key',key);}
function add(text,cls,sources){const d=document.createElement('div');d.className='msg '+cls;d.textContent=text;
 if(sources&&sources.length){const s=document.createElement('div');s.className='src';s.textContent='Sources: '+sources.map(x=>x.title).join(' · ');d.appendChild(s);}
 log.appendChild(d);window.scrollTo(0,document.body.scrollHeight);}
async function ask(){const text=q.value.trim();if(!text)return;add(text,'me');q.value='';send.disabled=true;
 try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},body:JSON.stringify({question:text})});
 if(r.status===401){add('Access key invalid. Reload and enter a valid key.','bot');localStorage.removeItem('tipsoi_key');}
 else if(r.status===429){add('Rate limit reached — please wait a moment and try again.','bot');}
 else{const j=await r.json();add(j.answer||('Error: '+(j.detail||'unknown')),'bot',j.sources);}}
 catch(e){add('Network error: '+e,'bot');}finally{send.disabled=false;q.focus();}}
send.onclick=ask;q.addEventListener('keydown',e=>{if(e.key==='Enter')ask();});
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return _PAGE
