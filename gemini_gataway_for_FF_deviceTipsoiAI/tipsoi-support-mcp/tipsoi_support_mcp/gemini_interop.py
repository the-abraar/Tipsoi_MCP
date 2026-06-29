"""
Shared helpers for bridging this MCP server to the Gemini Interactions API.
Pure data transforms — no Gemini or MCP imports here, so it's trivially testable.
"""

from __future__ import annotations

import json
from typing import Any

_DROP_KEYS = {"$schema", "additionalProperties", "title", "$defs", "definitions"}


def clean_schema(node: Any) -> Any:
    if isinstance(node, dict):
        return {k: clean_schema(v) for k, v in node.items() if k not in _DROP_KEYS}
    if isinstance(node, list):
        return [clean_schema(v) for v in node]
    return node


def mcp_tools_to_gemini(tools: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for t in tools:
        schema = getattr(t, "inputSchema", None) or {"type": "object", "properties": {}}
        out.append({
            "type": "function",
            "name": t.name,
            "description": (getattr(t, "description", "") or "").strip(),
            "parameters": clean_schema(schema),
        })
    return out


def mcp_result_text(result: Any) -> str:
    parts: list[str] = []
    for block in getattr(result, "content", []) or []:
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
        else:
            dump = getattr(block, "model_dump", None)
            parts.append(json.dumps(dump()) if dump else str(block))
    return "\n".join(parts) if parts else "(no content)"
