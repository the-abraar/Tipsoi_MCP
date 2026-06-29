"""
MCP + Gemini bridge (optional path).

Gemini has no built-in MCP client, so this bridges them: it lists the Tipsoi
MCP tools, exposes them to Gemini as function declarations, and on each
function_call executes the tool via the MCP session and feeds the result back —
looping until Gemini produces a final answer. Loads the server's persona prompt
as the system instruction.

For plain Q&A without running the MCP server, prefer the proxy (../USAGE.md).

    pip install -e .. google-genai
    export GEMINI_API_KEY=...
    python examples/gemini_bridge.py
"""

from __future__ import annotations

import asyncio
import os

from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tipsoi_support_mcp.gemini_interop import mcp_tools_to_gemini, mcp_result_text

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
SERVER = StdioServerParameters(command="python", args=["-m", "tipsoi_support_mcp.server"],
                               env=os.environ.copy())


async def run() -> None:
    gclient = genai.Client()
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = mcp_tools_to_gemini((await session.list_tools()).tools)
            persona = ""
            try:
                p = await session.get_prompt("support_assistant_persona")
                persona = "\n".join(getattr(m.content, "text", "") for m in p.messages).strip()
            except Exception:
                pass
            print("Tipsoi Support (Gemini + MCP). Type 'quit' to exit.\n")
            prev = None
            while True:
                user = input("You: ").strip()
                if user.lower() in {"quit", "exit"}:
                    break
                pending = [{"type": "text", "text": f"{persona}\n\n---\nUser: {user}"}] if (prev is None and persona) else user
                while True:
                    it = gclient.interactions.create(model=MODEL, input=pending, tools=tools,
                                                     previous_interaction_id=prev)
                    prev = it.id
                    results = []
                    for step in it.steps:
                        if getattr(step, "type", None) == "function_call":
                            res = await session.call_tool(step.name, step.arguments or {})
                            results.append({"type": "function_result", "name": step.name,
                                            "call_id": step.id,
                                            "result": [{"type": "text", "text": mcp_result_text(res)}]})
                    if not results:
                        print(f"\nAssistant: {it.output_text}\n")
                        break
                    pending = results


if __name__ == "__main__":
    asyncio.run(run())
