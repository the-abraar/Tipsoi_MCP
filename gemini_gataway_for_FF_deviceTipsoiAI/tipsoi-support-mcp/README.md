# Tipsoi Support Assistant

A support-only Tipsoi assistant that answers from a bundled, bilingual (EN/বাংলা)
knowledge base and escalates to human support. It holds **no Tipsoi
credentials** and reads **no HRM data** — it explains how to use Tipsoi and files
support tickets. Ships in three ways so you can use it however you like:

| Want… | Use | Consumer code |
|---|---|---|
| **Tipsoi-flavored Gemini** (drop-in SDK) | `gateway/gemini_proxy.py` | standard `google-genai`, just set `base_url` |
| An MCP connector (Claude Desktop / custom) | `tipsoi_support_mcp/server.py` | add as MCP server / connector |
| A simple hosted chat / `/ask` API | `gateway/qna.py` | HTTP POST or the built-in web page |

The **primary** path most people want is the Gemini proxy — see `USAGE.md`.

## Tipsoi-flavored Gemini (quick look)

```python
from google import genai
from google.genai import types
client = genai.Client(
    api_key="tsg_ACCESS_KEY",
    http_options=types.HttpOptions(base_url="https://your-proxy"),
)
print(client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How do I apply for leave in Tipsoi?").text)
```

The proxy injects the Tipsoi persona + the most relevant KB articles, then calls
real Gemini with **your** key. Your key stays server-side; users hold only a
`tsg_` access key. Details + deploy: `USAGE.md`, `DEPLOY.md`.

## Knowledge base
28 markdown articles under `tipsoi_support_mcp/kb_docs/` (getting started,
attendance, leave, payroll, employees, shifts, reports, troubleshooting, API).
Search is an in-process **BM25** index — pure stdlib, offline, bilingual.
Update by editing/adding `.md` files and restarting.

## MCP server
`python -m tipsoi_support_mcp.server` (stdio) or `TIPSOI_TRANSPORT=http …`.
Tools: `search_knowledge_base`, `get_article`, `list_help_topics`,
`escalate_to_support`, `get_support_contacts`, plus a `support_assistant_persona`
prompt. Escalation files a ClickUp ticket via the documented REST API
(`SUPPORT_TICKET_MODE`); see `tipsoi_support_mcp/escalation.py`.

## Project layout
```
tipsoi-support-mcp/
├── tipsoi_support_mcp/      # MCP server + KB + persona + escalation
│   ├── server.py  kb.py  persona.py  escalation.py  gemini_interop.py
│   └── kb_docs/             # 28 bundled help articles
├── gateway/
│   ├── gemini_proxy.py      # ★ Tipsoi-flavored Gemini (drop-in SDK proxy)
│   ├── qna.py               # simple hosted chat + /ask API
│   ├── app.py               # MCP-backed multi-user gateway (/chat, files tickets)
│   ├── auth.py  ratelimit.py  manage_keys.py
│   └── requirements*.txt  README.md  .env.example
├── examples/                # client_example.py, gemini_bridge.py, *.md
├── USAGE.md  DEPLOY.md  GUIDE.md  Dockerfile  render.yaml  pyproject.toml
```

*Inovace Technologies · Tipsoi Support Assistant · 2026*
