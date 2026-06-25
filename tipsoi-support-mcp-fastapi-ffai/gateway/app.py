"""
Tipsoi Support gateway.

A small multi-user front door for the Tipsoi Support MCP. You host this; it
holds your Gemini API key and runs the MCP server-side. You hand out per-user
gateway keys (revocable, rate-limited). When a user POSTs a message with their
key, the gateway answers them using YOUR Gemini token and the MCP — the user
never sees either secret.

    User ──(gateway key)──► /chat ──► Gemini (your key) ⇄ MCP tools ──► reply

Run:
    export GEMINI_API_KEY=...           # your Gemini key (server-side only)
    export GATEWAY_KEYS_FILE=./keys.json
    pip install -e .. fastapi "uvicorn[standard]" google-genai
    python -m gateway.manage_keys create --label "Pilot HR" --rpm 20   # issue a key
    uvicorn gateway.app:app --host 0.0.0.0 --port 8080

Then a user calls:
    curl -s localhost:8080/chat \
      -H "Authorization: Bearer tsg_xxx" \
      -H "Content-Type: application/json" \
      -d '{"message":"how do I apply for leave?","session_id":"u123"}'
"""

from __future__ import annotations

import asyncio
import os
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tipsoi_support_mcp.gemini_interop import mcp_tools_to_gemini, mcp_result_text

from .auth import KeyStore
from .ratelimit import RateLimiter

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
KEYS_FILE = os.environ.get("GATEWAY_KEYS_FILE", "./keys.json")
MAX_TOOL_ITERS = int(os.environ.get("GATEWAY_MAX_TOOL_ITERS", "6"))

# How to launch the MCP server (stdio). Inherits env so SUPPORT_TICKET_MODE /
# CLICKUP_* configured for the gateway flow through to the server.
MCP_SERVER = StdioServerParameters(
    command=os.environ.get("MCP_PYTHON", "python"),
    args=["-m", "tipsoi_support_mcp.server"],
    env=os.environ.copy(),
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None  # opaque client-chosen id to keep a thread


class AppState:
    gemini: genai.Client
    session: ClientSession
    tools: list[dict[str, Any]]
    persona: str
    keys: KeyStore
    limiter: RateLimiter
    conversations: dict[str, str]      # session_id -> previous_interaction_id
    mcp_lock: asyncio.Lock


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.keys = KeyStore(KEYS_FILE)
    state.limiter = RateLimiter()
    state.conversations = {}
    state.mcp_lock = asyncio.Lock()
    state.gemini = genai.Client()  # reads GEMINI_API_KEY

    async with AsyncExitStack() as stack:
        read, write = await stack.enter_async_context(stdio_client(MCP_SERVER))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        state.session = session
        state.tools = mcp_tools_to_gemini((await session.list_tools()).tools)
        try:
            p = await session.get_prompt("support_assistant_persona")
            state.persona = "\n".join(
                getattr(m.content, "text", "") for m in p.messages
            ).strip()
        except Exception:
            state.persona = ""
        yield  # server runs while the MCP session stays open


app = FastAPI(title="Tipsoi Support Gateway", version="1.0.0", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Auth + rate-limit dependency
# ---------------------------------------------------------------------------

async def require_key(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
):
    presented = ""
    if authorization and authorization.lower().startswith("bearer "):
        presented = authorization[7:].strip()
    elif x_api_key:
        presented = x_api_key.strip()

    rec = state.keys.verify(presented)
    if not rec:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")

    allowed, remaining, reset_in = state.limiter.check(rec.key_id, rec.rpm)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded ({rec.rpm}/min). Retry in {reset_in:.0f}s.",
            headers={"Retry-After": str(int(reset_in) + 1)},
        )
    state.keys.mark_used(rec.key_id)
    return rec


# ---------------------------------------------------------------------------
# Core: run one user message through Gemini + MCP
# ---------------------------------------------------------------------------

async def answer(message: str, prev_id: str | None) -> tuple[str, str]:
    # On the first turn of a conversation, prime with the persona.
    if prev_id is None and state.persona:
        pending: Any = [{"type": "text", "text": f"{state.persona}\n\n---\nUser: {message}"}]
    else:
        pending = message

    for _ in range(MAX_TOOL_ITERS):
        interaction = await asyncio.to_thread(
            state.gemini.interactions.create,
            model=MODEL,
            input=pending,
            tools=state.tools,
            previous_interaction_id=prev_id,
        )
        prev_id = interaction.id

        results = []
        for step in interaction.steps:
            if getattr(step, "type", None) == "function_call":
                args = step.arguments or {}
                async with state.mcp_lock:
                    res = await state.session.call_tool(step.name, args)
                results.append({
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": mcp_result_text(res)}],
                })

        if not results:
            return interaction.output_text, prev_id
        pending = results

    return (
        "Sorry — I couldn't complete that within the allowed number of steps. "
        "Please rephrase, or contact support directly.",
        prev_id or "",
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL, "tools": [t["name"] for t in state.tools]}


@app.post("/chat")
async def chat(req: ChatRequest, request: Request, key=Depends(require_key)):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    sid = req.session_id or ""
    prev_id = state.conversations.get(sid) if sid else None
    reply, new_id = await answer(req.message, prev_id)
    if sid:
        state.conversations[sid] = new_id

    return JSONResponse({
        "reply": reply,
        "conversation_id": new_id,
        "key_id": key.key_id,
    })
