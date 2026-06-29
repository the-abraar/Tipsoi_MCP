"""
Tipsoi Support gateway (MCP-backed) — the 'nice to have' upgrade of qna.py.

Same multi-user front door, but answers by running the full MCP tool loop
(search_knowledge_base / get_article / escalate_to_support) through Gemini,
so it can also FILE TICKETS, not just answer. Holds your Gemini key + the MCP
server-side; users authenticate with revocable, rate-limited gateway keys.

For pure Q&A with no MCP subprocess, use gateway.qna instead.
"""

from __future__ import annotations

import asyncio
import os
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException
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

MCP_SERVER = StdioServerParameters(
    command=os.environ.get("MCP_PYTHON", "python"),
    args=["-m", "tipsoi_support_mcp.server"],
    env=os.environ.copy(),
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class AppState:
    gemini: genai.Client
    session: ClientSession
    tools: list[dict[str, Any]]
    persona: str
    keys: KeyStore
    limiter: RateLimiter
    conversations: dict[str, str]
    mcp_lock: asyncio.Lock


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.keys = KeyStore(KEYS_FILE)
    state.limiter = RateLimiter()
    state.conversations = {}
    state.mcp_lock = asyncio.Lock()
    state.gemini = genai.Client()
    async with AsyncExitStack() as stack:
        read, write = await stack.enter_async_context(stdio_client(MCP_SERVER))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        state.session = session
        state.tools = mcp_tools_to_gemini((await session.list_tools()).tools)
        try:
            p = await session.get_prompt("support_assistant_persona")
            state.persona = "\n".join(getattr(m.content, "text", "") for m in p.messages).strip()
        except Exception:
            state.persona = ""
        yield


app = FastAPI(title="Tipsoi Support Gateway", version="1.0.0", lifespan=lifespan)


async def require_key(authorization: str | None = Header(default=None),
                      x_api_key: str | None = Header(default=None)):
    presented = ""
    if authorization and authorization.lower().startswith("bearer "):
        presented = authorization[7:].strip()
    elif x_api_key:
        presented = x_api_key.strip()
    rec = state.keys.verify(presented)
    if not rec:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")
    allowed, _r, reset_in = state.limiter.check(rec.key_id, rec.rpm)
    if not allowed:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded ({rec.rpm}/min). Retry in {reset_in:.0f}s.",
                            headers={"Retry-After": str(int(reset_in) + 1)})
    state.keys.mark_used(rec.key_id)
    return rec


async def answer(message: str, prev_id: str | None) -> tuple[str, str]:
    if prev_id is None and state.persona:
        pending: Any = [{"type": "text", "text": f"{state.persona}\n\n---\nUser: {message}"}]
    else:
        pending = message
    for _ in range(MAX_TOOL_ITERS):
        interaction = await asyncio.to_thread(
            state.gemini.interactions.create,
            model=MODEL, input=pending, tools=state.tools, previous_interaction_id=prev_id,
        )
        prev_id = interaction.id
        results = []
        for step in interaction.steps:
            if getattr(step, "type", None) == "function_call":
                args = step.arguments or {}
                async with state.mcp_lock:
                    res = await state.session.call_tool(step.name, args)
                results.append({"type": "function_result", "name": step.name,
                                "call_id": step.id, "result": [{"type": "text", "text": mcp_result_text(res)}]})
        if not results:
            return interaction.output_text, prev_id
        pending = results
    return ("Sorry — I couldn't complete that within the allowed steps. Please rephrase or contact support.",
            prev_id or "")


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL, "tools": [t["name"] for t in state.tools]}


@app.post("/chat")
async def chat(req: ChatRequest, key=Depends(require_key)):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")
    sid = req.session_id or ""
    prev_id = state.conversations.get(sid) if sid else None
    reply, new_id = await answer(req.message, prev_id)
    if sid:
        state.conversations[sid] = new_id
    return JSONResponse({"reply": reply, "conversation_id": new_id, "key_id": key.key_id})
