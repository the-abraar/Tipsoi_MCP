"""
Tipsoi Support Assistant — MCP v2

A support-only MCP server. Unlike the v1 data/action MCP (which reads HRM
reports and performs leave writes), this server does exactly one job: help
users with Tipsoi the way the support team would — answer how-to questions
from the knowledge base, and escalate to human support when needed.

It holds NO Tipsoi credentials and calls NO Tipsoi data APIs. It cannot read
or change any organization's HRM data. Its only outward call is filing a
support ticket on escalation.

Tools:
  - search_knowledge_base   find relevant help articles (BM25, EN/BN)
  - get_article             fetch the full text of a help article
  - list_help_topics        browse available articles by category
  - escalate_to_support     file a support ticket + return support contacts

Run modes:
  python -m tipsoi_support_mcp.server                     # stdio (Claude Desktop)
  TIPSOI_TRANSPORT=http python -m tipsoi_support_mcp.server   # HTTP (remote connector)
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from . import kb
from .escalation import Ticket, submit, support_contacts

_port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("tipsoi-support", host="0.0.0.0", port=_port)

_ro = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


# ---------------------------------------------------------------------------
# Knowledge base tools (read-only)
# ---------------------------------------------------------------------------

@mcp.tool(annotations=_ro)
async def search_knowledge_base(query: str, limit: int = 5) -> Any:
    """Search the Tipsoi help knowledge base for articles relevant to a
    user's question. Use this FIRST for any "how do I…", "why is…",
    setup, troubleshooting, or feature question about Tipsoi.

    The KB is bilingual (English + বাংলা), so queries in either language work.

    Args:
        query: The user's question or keywords (e.g. "device not syncing",
               "how to apply for leave", "ডিভাইস ডাটা আসছে না").
        limit: Max number of articles to return (default 5).

    Returns a ranked list of {doc_id, title, category, tags, score, snippet}.
    Pass a doc_id to get_article to read the full article before answering.
    """
    results = kb.search(query, limit=max(1, min(limit, 15)))
    if not results:
        return {
            "results": [],
            "note": (
                "No matching articles. Try different keywords, call "
                "list_help_topics to browse, or escalate_to_support if the "
                "user's issue can't be resolved from the knowledge base."
            ),
        }
    return {"results": results}


@mcp.tool(annotations=_ro)
async def get_article(doc_id: str) -> Any:
    """Fetch the full text of a single help article by its doc_id
    (as returned by search_knowledge_base or list_help_topics).

    Args:
        doc_id: e.g. "03-leave-management/leave-management-overview".

    Returns {doc_id, title, category, tags, description, content}.
    Base every answer on this content — never invent steps the article
    does not contain.
    """
    art = kb.get_article(doc_id)
    if art is None:
        return {
            "error": "not_found",
            "detail": f"No article '{doc_id}'. Use list_help_topics for valid ids.",
        }
    return art


@mcp.tool(annotations=_ro)
async def list_help_topics() -> Any:
    """List every available help article, grouped by category. Use this to
    discover what the knowledge base covers when a search comes up empty or
    when the user asks "what can you help with?"."""
    grouped: dict[str, list[dict[str, str]]] = {}
    for doc_id in kb.list_doc_ids():
        art = kb.get_article(doc_id)
        if not art:
            continue
        grouped.setdefault(art["category"], []).append(
            {"doc_id": doc_id, "title": art["title"]}
        )
    return {"article_count": kb.doc_count(), "categories": grouped}


# ---------------------------------------------------------------------------
# Escalation tool (the only outward action)
# ---------------------------------------------------------------------------

@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True)
)
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
    """Escalate an unresolved issue to the human support team by filing a
    support ticket, and return the support contacts.

    Only call this AFTER searching the knowledge base and confirming the
    issue can't be resolved from it. Before calling, make sure you have
    gathered, in the user's own words: who they are, their company, what's
    wrong, and what they want. Confirm with the user before filing.

    Args:
        task_name: Short ticket title summarizing the issue.
        client_name: The client's / company's name (for support tracking).
        reported_by: Name of the person reporting the issue.
        task_description: Full description of the problem.
        task_type: Ticket category (e.g. "Bug", "Support", "Feature"). Default "Support".
        steps_to_reproduce: Steps that trigger the issue, if applicable.
        the_ask: What the user actually wants to happen.
        email: Reporter's email address for follow-up.
        reported_date: YYYY-MM-DD. Defaults to today (Asia/Dhaka).

    Returns the filing result plus the formatted ticket and support contacts.
    The ticket text is always returned, so it can be filed manually if
    automatic submission is not configured.
    """
    ticket = Ticket(
        task_name=task_name,
        client_name=client_name,
        reported_by=reported_by,
        task_description=task_description,
        task_type=task_type,
        steps_to_reproduce=steps_to_reproduce,
        the_ask=the_ask,
        email=email,
        reported_date=reported_date,
    )
    return await submit(ticket)


@mcp.tool(annotations=_ro)
async def get_support_contacts() -> Any:
    """Return the Tipsoi human-support phone and email. Share these whenever
    a user wants to reach a person directly."""
    return support_contacts()


# ---------------------------------------------------------------------------
# Persona prompt — the Support Assistant guidelines
# ---------------------------------------------------------------------------

@mcp.prompt(title="Tipsoi Support Assistant persona")
def support_assistant_persona() -> str:
    """System guidelines that turn the host model into the Tipsoi Support
    Assistant. Load this as the system/developer prompt when using the
    connector."""
    contacts = support_contacts()
    return f"""You are the Tipsoi Support Assistant — the friendly, knowledgeable \
support agent for Tipsoi, an HRM and attendance platform used across South and \
Southeast Asia. Your job is to make every user feel helped, not transferred.

# What you do
1. Answer how-to and troubleshooting questions about any Tipsoi feature
   (Employees, Attendance, Leave, Payroll, Shifts/Roster, Reports, Settings,
   Biometric Devices, Mobile App).
2. Guide users step by step, grounded in the knowledge base.
3. Escalate to human support when an issue cannot be resolved from the KB.

# How to answer
- ALWAYS call search_knowledge_base first. Read the most relevant article with
  get_article before answering. Base your answer on that content.
- NEVER invent steps or features that aren't in the knowledge base. If you
  don't know, say so honestly.
- Keep how-to answers as short, scannable numbered steps — not walls of text.
- Reply in the user's language. The KB is bilingual (English + বাংলা); answer
  in Bangla if the user writes in Bangla, English otherwise. Never mix.
- Warm, conversational, like a helpful colleague. Use the user's first name
  occasionally.

# This assistant is support-only
You CANNOT read HRM data (attendance, leave balances, employee records) or
perform actions like applying for or approving leave. If a user asks you to DO
one of those, explain that this assistant handles help and guidance, and point
them to where in the Tipsoi app they can do it (or to the data/action assistant
if their deployment has one).

# Escalation
If the knowledge base can't resolve the issue:
1. Confirm the user's name and company.
2. Ask what they've already tried and what they want to happen.
3. Confirm with the user, then call escalate_to_support to file a ticket.
4. Tell them it's been forwarded and share the contacts below.

Support contacts — Phone: {contacts['phone']} · Email: {contacts['email']}

# Hard rules
1. Reply in the user's language only — never mix English and Bangla.
2. Never invent steps or features not found in the knowledge base.
3. Never share data from other users or organizations (you have no data access).
4. Don't loop: if a feature is genuinely unsupported, say so once and offer the
   support contacts.
"""


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    transport = os.environ.get("TIPSOI_TRANSPORT", "stdio").lower()
    if transport in ("http", "streamable-http", "streamable_http"):
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
