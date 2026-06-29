"""
Tipsoi-flavored Gemini — a drop-in, Gemini-compatible proxy.

Consumers use the STANDARD google-genai SDK; the only change is pointing it at
this service. The proxy injects the Tipsoi Support persona + knowledge-base
retrieval into each generateContent call, forwards to the real Gemini API with
YOUR key, and returns Gemini's native response — so `response.text` just works.

    from google import genai
    from google.genai import types
    client = genai.Client(
        api_key="tsg_ACCESS_KEY",                       # the key YOU issued
        http_options=types.HttpOptions(base_url="https://your-proxy"),
    )
    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="How do I apply for leave in Tipsoi?",
    )
    print(r.text)

How it works
  - Consumer's api_key is an access key you hand out (validated here).
  - The proxy calls real Gemini with GEMINI_API_KEY (server-side only).
  - generateContent / streamGenerateContent get Tipsoi persona + KB context
    injected as a systemInstruction; every other endpoint is passed through
    unchanged (so countTokens, models.list, embeddings, etc. still work).

Env:
  GEMINI_API_KEY    your real Gemini key (server-side only)   [required]
  QNA_API_KEYS      comma-separated access keys you hand out
  GATEWAY_KEYS_FILE optional revocable KeyStore file (manage_keys.py)
  QNA_RPM           per-key requests/min for env keys (default 30)
  QNA_TOP_K         KB articles retrieved per question (default 4)
  UPSTREAM_BASE     default https://generativelanguage.googleapis.com
  SUPPORT_PHONE / SUPPORT_EMAIL

Run:
  pip install fastapi "uvicorn[standard]" httpx
  export GEMINI_API_KEY=...  QNA_API_KEYS=tsg_xxx
  uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from tipsoi_support_mcp import kb
from tipsoi_support_mcp.persona import support_persona

from .ratelimit import RateLimiter

UPSTREAM = os.environ.get("UPSTREAM_BASE", "https://generativelanguage.googleapis.com").rstrip("/")
TOP_K = int(os.environ.get("QNA_TOP_K", "4"))
ENV_RPM = int(os.environ.get("QNA_RPM", "30"))
KEYS_FILE = os.environ.get("GATEWAY_KEYS_FILE", "")

try:
    from .auth import KeyStore
except Exception:  # pragma: no cover
    KeyStore = None  # type: ignore

_limiter = RateLimiter()
_store = KeyStore(KEYS_FILE) if (KEYS_FILE and KeyStore) else None

app = FastAPI(title="Tipsoi-flavored Gemini proxy", version="1.0.0")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def _env_keys() -> list[str]:
    return [k.strip() for k in os.environ.get("QNA_API_KEYS", "").split(",") if k.strip()]


def _contacts() -> dict[str, str]:
    return {
        "phone": os.environ.get("SUPPORT_PHONE", "+8809638017170"),
        "email": os.environ.get("SUPPORT_EMAIL", "support@inovacetech.com"),
    }


def verify_key(presented: str) -> tuple[str, int] | None:
    """Return (rate_key_id, rpm) for a valid access key, else None."""
    if not presented:
        return None
    for k in _env_keys():
        if hmac.compare_digest(k, presented):
            return "env:" + hashlib.sha256(k.encode()).hexdigest()[:12], ENV_RPM
    if _store is not None:
        rec = _store.verify(presented)
        if rec:
            _store.mark_used(rec.key_id)
            return rec.key_id, rec.rpm
    return None


def _presented_key(request: Request) -> str:
    # google-genai sends the key in the x-goog-api-key header; also accept
    # Authorization: Bearer and ?key= for flexibility.
    k = request.headers.get("x-goog-api-key")
    if k:
        return k.strip()
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return request.query_params.get("key", "").strip()


# ---------------------------------------------------------------------------
# Request transforms (pure, unit-tested)
# ---------------------------------------------------------------------------

def extract_query(body: dict[str, Any]) -> str:
    """Pull the latest user message text from a generateContent body."""
    contents = body.get("contents")
    if isinstance(contents, str):
        return contents
    if not isinstance(contents, list):
        return ""
    # last item with role user (or the last item) — concatenate its text parts
    for item in reversed(contents):
        if not isinstance(item, dict):
            continue
        if item.get("role") in (None, "user"):
            parts = item.get("parts") or []
            texts = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("text")]
            if texts:
                return "\n".join(texts)
    return ""


def build_injection(query: str) -> tuple[str, list[dict[str, str]]]:
    c = _contacts()
    persona = support_persona(c["phone"], c["email"])
    hits = kb.search(query, limit=TOP_K) if query else []
    blocks = []
    for h in hits:
        art = kb.get_article(h["doc_id"])
        if art:
            blocks.append(f"## {art['title']}  (id: {h['doc_id']})\n{art['content'][:2200]}")
    context = "\n\n".join(blocks) or "(no relevant articles found)"
    text = (
        f"{persona}\n\n"
        "# Knowledge base\n"
        "Answer Tipsoi questions using ONLY the excerpts below. If the answer is "
        f"not in them, say you don't have that information and give the support "
        f"contacts (Phone: {c['phone']}, Email: {c['email']}).\n\n"
        f"{context}"
    )
    return text, [{"doc_id": h["doc_id"], "title": h["title"]} for h in hits]


def inject_system_instruction(body: dict[str, Any], injected: str) -> dict[str, Any]:
    """Prepend our persona+KB to any existing systemInstruction (handles both
    camelCase and snake_case keys the SDK/REST may use)."""
    key = "systemInstruction" if "systemInstruction" in body else (
        "system_instruction" if "system_instruction" in body else "systemInstruction")
    existing = body.get(key)
    existing_parts = []
    if isinstance(existing, dict):
        existing_parts = existing.get("parts") or []
    elif isinstance(existing, str):
        existing_parts = [{"text": existing}]
    body[key] = {"parts": [{"text": injected}] + list(existing_parts)}
    return body


def split_model_method(tail: str) -> tuple[str, str]:
    """'models/gemini-2.5-flash:generateContent' -> ('gemini-2.5-flash','generateContent')."""
    name = tail.split("/", 1)[-1] if tail.startswith("models/") else tail
    if ":" in name:
        model, method = name.rsplit(":", 1)
        return model, method
    return name, ""


# ---------------------------------------------------------------------------
# Proxy
# ---------------------------------------------------------------------------

def _gemini_error(status: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status,
                        content={"error": {"code": status, "message": message, "status": "UNAUTHENTICATED" if status == 401 else "RESOURCE_EXHAUSTED" if status == 429 else "INVALID_ARGUMENT"}})


@app.get("/health")
async def health():
    return {"status": "ok", "upstream": UPSTREAM, "kb_articles": kb.doc_count(),
            "auth": {"env_keys": len(_env_keys()), "key_store": _store is not None}}


@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def proxy(full_path: str, request: Request):
    if not os.environ.get("GEMINI_API_KEY"):
        return _gemini_error(500, "Server missing GEMINI_API_KEY")

    presented = _presented_key(request)
    res = verify_key(presented)
    if not res:
        return _gemini_error(401, "Invalid or missing API key")
    key_id, rpm = res
    allowed, _rem, reset_in = _limiter.check(key_id, rpm)
    if not allowed:
        return _gemini_error(429, f"Rate limit exceeded ({rpm}/min). Retry in {reset_in:.0f}s.")

    # Build upstream URL: same path + version, our real key, preserve query
    # params except the caller's key.
    q = {k: v for k, v in request.query_params.items() if k != "key"}
    url = f"{UPSTREAM}/{full_path}"
    headers = {"Content-Type": "application/json",
               "x-goog-api-key": os.environ["GEMINI_API_KEY"]}

    is_post = request.method == "POST"
    _, method = split_model_method(full_path)
    is_generate = method in ("generateContent", "streamGenerateContent")
    is_stream = method == "streamGenerateContent" or q.get("alt") == "sse"

    body_bytes = await request.body()
    if is_post and is_generate and body_bytes:
        import json as _json
        try:
            body = _json.loads(body_bytes)
            query = extract_query(body)
            injected, _sources = build_injection(query)
            body = inject_system_instruction(body, injected)
            body_bytes = _json.dumps(body).encode("utf-8")
        except Exception:
            pass  # if anything goes wrong, forward the original body unchanged

    timeout = httpx.Timeout(120.0)
    if is_stream:
        async def gen():
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream(request.method, url, params=q, headers=headers,
                                         content=body_bytes if is_post else None) as r:
                    async for chunk in r.aiter_raw():
                        yield chunk
        return StreamingResponse(gen(), media_type="text/event-stream")

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.request(request.method, url, params=q, headers=headers,
                                 content=body_bytes if is_post else None)
    media = r.headers.get("content-type", "application/json")
    return StreamingResponse(iter([r.content]), status_code=r.status_code, media_type=media)
