"""
Use the Tipsoi Support MCP with the Gemini API.

Gemini does not connect to an MCP server on its own. This bridge does the glue:

  1. Launches/connects to the MCP server and lists its tools.
  2. Converts each MCP tool into a Gemini function declaration.
  3. Runs the Gemini Interactions API function-calling loop. When Gemini emits
     a function_call, the bridge executes it via the MCP session and returns the
     result as a function_result, looping until Gemini produces a final answer.
  4. Loads the server's `support_assistant_persona` prompt as the system
     instruction so Gemini behaves like the Tipsoi Support Assistant.

Run:
    export GEMINI_API_KEY="..."
    pip install google-genai mcp
    python examples/gemini_bridge.py

By default it talks to the local stdio server. Set TIPSOI_TRANSPORT/CLICKUP_*
env vars the same way you would for Claude Desktop (see .env.example).
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from google import genai  # pip install google-genai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

# How to start the MCP server (local stdio). Point cwd at the project root.
SERVER = StdioServerParameters(
    command="python",
    args=["-m", "tipsoi_support_mcp.server"],
    # Inherit the current environment so SUPPORT_TICKET_MODE / CLICKUP_* flow through.
    env=os.environ.copy(),
)


# ---------------------------------------------------------------------------
# Schema conversion: MCP inputSchema (JSON Schema) -> Gemini-friendly schema
# ---------------------------------------------------------------------------

_DROP_KEYS = {"$schema", "additionalProperties", "title", "$defs", "definitions"}


def _clean_schema(node: Any) -> Any:
    """Strip JSON-Schema keys Gemini's function parameters don't accept."""
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in _DROP_KEYS:
                continue
            out[k] = _clean_schema(v)
        return out
    if isinstance(node, list):
        return [_clean_schema(v) for v in node]
    return node


def mcp_tools_to_gemini(tools) -> list[dict[str, Any]]:
    gemini_tools = []
    for t in tools:
        params = _clean_schema(t.inputSchema or {"type": "object", "properties": {}})
        gemini_tools.append({
            "type": "function",
            "name": t.name,
            "description": (t.description or "").strip(),
            "parameters": params,
        })
    return gemini_tools


def _mcp_result_text(result) -> str:
    """Flatten an MCP call_tool result into a single text string."""
    parts: list[str] = []
    for block in result.content:
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
        else:
            parts.append(json.dumps(getattr(block, "model_dump", lambda: str(block))()))
    return "\n".join(parts) if parts else "(no content)"


# ---------------------------------------------------------------------------
# Chat loop
# ---------------------------------------------------------------------------

async def run() -> None:
    gclient = genai.Client()  # reads GEMINI_API_KEY

    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tool_list = (await session.list_tools()).tools
            gemini_tools = mcp_tools_to_gemini(tool_list)
            print(f"Bridged {len(gemini_tools)} MCP tools: "
                  f"{', '.join(t['name'] for t in gemini_tools)}")

            # Load the Support Assistant persona from the MCP prompt.
            persona = ""
            try:
                p = await session.get_prompt("support_assistant_persona")
                persona = "\n".join(
                    getattr(m.content, "text", "") for m in p.messages
                ).strip()
            except Exception:
                pass

            previous_id: str | None = None
            print("\nTipsoi Support Assistant (Gemini). Type 'quit' to exit.\n")

            while True:
                user = input("You: ").strip()
                if user.lower() in {"quit", "exit"}:
                    break

                # On the first turn, prime Gemini with the persona. Subsequent
                # turns chain via previous_interaction_id (server keeps history).
                if previous_id is None and persona:
                    pending: Any = [{"type": "text",
                                     "text": f"{persona}\n\n---\nUser: {user}"}]
                else:
                    pending = user

                # Inner loop: keep going while Gemini wants tool calls.
                while True:
                    interaction = gclient.interactions.create(
                        model=MODEL,
                        input=pending,
                        tools=gemini_tools,
                        previous_interaction_id=previous_id,
                    )
                    previous_id = interaction.id

                    results = []
                    for step in interaction.steps:
                        if getattr(step, "type", None) == "function_call":
                            args = step.arguments or {}
                            print(f"  ↳ calling {step.name}({args})")
                            mcp_res = await session.call_tool(step.name, args)
                            results.append({
                                "type": "function_result",
                                "name": step.name,
                                "call_id": step.id,
                                "result": [{"type": "text",
                                            "text": _mcp_result_text(mcp_res)}],
                            })

                    if not results:
                        print(f"\nAssistant: {interaction.output_text}\n")
                        break
                    pending = results  # send tool outputs back, loop again


if __name__ == "__main__":
    asyncio.run(run())
