"""
Tipsoi Support Assistant — MCP v2 (support-only).

Holds NO Tipsoi credentials and calls NO Tipsoi data APIs. Answers from a
bundled knowledge base and escalates to human support. The only outward call is
filing a support ticket.

Run:
  python -m tipsoi_support_mcp.server                       # stdio
  TIPSOI_TRANSPORT=http python -m tipsoi_support_mcp.server # HTTP connector
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from . import kb
from .escalation import Ticket, submit, support_contacts
from .persona import support_persona

_port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("tipsoi-support", host="0.0.0.0", port=_port)
_ro = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


@mcp.tool(annotations=_ro)
async def search_knowledge_base(query: str, limit: int = 5) -> Any:
    """Search the Tipsoi help KB (bilingual EN/বাংলা). Use this FIRST for any
    how-to / why-is / setup / troubleshooting question. Returns ranked
    {doc_id, title, category, tags, score, snippet}."""
    results = kb.search(query, limit=max(1, min(limit, 15)))
    if not results:
        return {"results": [], "note": "No matches. Try list_help_topics or escalate_to_support."}
    return {"results": results}


@mcp.tool(annotations=_ro)
async def get_article(doc_id: str) -> Any:
    """Fetch the full text of a help article by doc_id. Base answers on this."""
    art = kb.get_article(doc_id)
    if art is None:
        return {"error": "not_found", "detail": f"No article '{doc_id}'."}
    return art


@mcp.tool(annotations=_ro)
async def list_help_topics() -> Any:
    """List every help article grouped by category."""
    grouped: dict[str, list[dict[str, str]]] = {}
    for doc_id in kb.list_doc_ids():
        art = kb.get_article(doc_id)
        if not art:
            continue
        grouped.setdefault(art["category"], []).append({"doc_id": doc_id, "title": art["title"]})
    return {"article_count": kb.doc_count(), "categories": grouped}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True))
async def escalate_to_support(
    task_name: str,
    client_name: str,
    reported_by: str,
    task_description: str,
    task_type: str = "Support",
    steps_to_reproduce: str = "",
    the_ask: str = "",
    email: str = "",
    reported_date: str = "",
) -> Any:
    """File a support ticket and return support contacts. Call only AFTER the KB
    can't resolve the issue and after confirming details with the user."""
    ticket = Ticket(
        task_name=task_name, client_name=client_name, reported_by=reported_by,
        task_description=task_description, task_type=task_type,
        steps_to_reproduce=steps_to_reproduce, the_ask=the_ask, email=email,
        reported_date=reported_date,
    )
    return await submit(ticket)


@mcp.tool(annotations=_ro)
async def get_support_contacts() -> Any:
    """Return the Tipsoi human-support phone and email."""
    return support_contacts()


@mcp.prompt(title="Tipsoi Support Assistant persona")
def support_assistant_persona() -> str:
    """System guidelines that turn the host model into the Tipsoi Support Assistant."""
    c = support_contacts()
    return support_persona(c["phone"], c["email"])


def main() -> None:
    transport = os.environ.get("TIPSOI_TRANSPORT", "stdio").lower()
    if transport in ("http", "streamable-http", "streamable_http"):
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
