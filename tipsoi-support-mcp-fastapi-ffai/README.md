# Tipsoi Support Assistant — MCP v2

A **support-only** MCP server for Tipsoi. It does one job, well: help users with
Tipsoi the way the support team would — answer how-to and troubleshooting
questions from the knowledge base, and escalate to a human when needed.

**Version:** 1.0.0

---

## How this differs from the v1 MCP

The original `tipsoi-mcp` (v0.3.0) is a **data + action** assistant: 15 read
tools over HRM reports (attendance, leave, overtime, employees) plus 4 leave
**write** tools, with per-user OAuth into the Tipsoi API.

This server is the deliberate opposite — the **Support Assistant** persona from
the earlier Botpress 3-node design, rebuilt as an MCP:

| | v1 `tipsoi-mcp` | **v2 `tipsoi-support-mcp`** |
|---|---|---|
| Purpose | Query HRM data, take leave actions | Help & guidance only |
| Tipsoi API access | Yes (per-user OAuth) | **None** |
| Reads org data | Yes | **No** |
| Writes data | Yes (leave) | **No** |
| Knowledge base | — | 28 bundled help articles (EN/BN) |
| Outward action | Tipsoi API calls | One: file a support ticket |
| Auth/secrets needed | Tipsoi OAuth | None (optional ClickUp token for tickets) |

Because it holds no Tipsoi credentials and calls no data APIs, it **cannot** read
or change any organization's HRM data. That containment *is* the safety story —
same principle as v1's read-only Phase 1, taken further.

---

## Tools

| Tool | Type | What it does |
|---|---|---|
| `search_knowledge_base` | read | BM25 search over the help KB. Bilingual (English + বাংলা). |
| `get_article` | read | Fetch a full help article by `doc_id`. |
| `list_help_topics` | read | Browse all articles grouped by category. |
| `escalate_to_support` | action | File a support ticket + return support contacts. |
| `get_support_contacts` | read | Return the support phone/email. |

Plus an MCP **prompt**, `support_assistant_persona`, containing the system
guidelines that turn the host model into the Tipsoi Support Assistant (answer
from the KB, never invent steps, reply in the user's language, escalate when
stuck). Load it as the system/developer prompt.

---

## Knowledge base

28 markdown articles bundled under `tipsoi_support_mcp/kb_docs/`, covering
getting started, attendance, leave, payroll, employee management, shifts,
reports, troubleshooting, and an API reference — including a bilingual official
support FAQ and quick guide.

Search is a small in-process **BM25** index (pure standard library — no vector
DB, no embedding model, no network). Title and tags are boosted over body text.
The tokenizer keeps both ASCII and the Bengali Unicode block, so Bangla queries
work directly.

To update the KB, edit/add `.md` files under `kb_docs/` (YAML front-matter with
`title`, `description`, `category`, `tags` is parsed automatically) and restart
the server. The index rebuilds on first use.

---

## Escalation → ClickUp ticket

The support team tracks tickets in a ClickUp form/list. The form expects:
*Task Name, Client Name, Client Reported Date, Reported By, Task Description,
Steps to reproduce, The Ask, Your Email Address, Attachments, Task Type.*
`escalate_to_support` collects these and files the ticket.

**Why not POST the public form URL directly?** ClickUp does not expose a
documented public-form submission API, and a public form's per-field IDs are
workspace-specific UUIDs that can't be reliably discovered without inspecting a
live browser session. So escalation uses ClickUp's **documented REST API** to
create a task in the same List the form feeds — stable and supported.

Pick a backend with `SUPPORT_TICKET_MODE`:

- **`clickup_api`** *(recommended)* — set `CLICKUP_API_TOKEN` (a personal token,
  `pk_…`) and `CLICKUP_LIST_ID` (the form's destination List). All fields go
  into the task name + a formatted description. Optionally set
  `CLICKUP_CUSTOM_FIELDS` (a JSON map of ticket field → custom-field UUID) to
  populate native ClickUp fields too.
- **`webhook`** — set `SUPPORT_TICKET_WEBHOOK` to your own endpoint
  (Zapier/Make/n8n) and map it to the ClickUp form there. No ClickUp token in
  the server.
- **`off`** *(default when nothing is configured)* — don't submit; return the
  fully formatted ticket so it can be filed by hand.
- **`auto`** *(default)* — `clickup_api` if a token+list are set, else `webhook`
  if a URL is set, else `off`.

**In every mode**, the response includes `support_contacts`, the structured
`ticket`, and a ready-to-paste `ticket_markdown` — so an escalation is never
silently lost, even if automatic filing isn't configured or fails.

Finding the List ID: open the form's destination List in ClickUp — the URL ends
in `/li/<LIST_ID>`. Discover custom-field UUIDs with
`GET https://api.clickup.com/api/v2/list/<LIST_ID>/field`.

---

## Setup

```bash
cd tipsoi-support-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # fill in ticket backend if you want auto-filing
```

### Run locally (Claude Desktop, stdio)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tipsoi-support": {
      "command": "python",
      "args": ["-m", "tipsoi_support_mcp.server"],
      "cwd": "/absolute/path/to/tipsoi-support-mcp",
      "env": {
        "SUPPORT_TICKET_MODE": "clickup_api",
        "CLICKUP_API_TOKEN": "pk_...",
        "CLICKUP_LIST_ID": "901800000000"
      }
    }
  }
}
```

Restart Claude Desktop. (Omit the ClickUp env vars to run in `off` mode — KB Q&A
works fully; escalations return a ready-to-file ticket.)

### Run remotely (HTTP connector)

```bash
TIPSOI_TRANSPORT=http PORT=8000 python -m tipsoi_support_mcp.server
```

Put it behind HTTPS, then add it in Claude → **Settings → Connectors → Add
custom connector** with your `https://…/mcp` URL. No OAuth is required because
the server reads no per-user data.

### Use it with Gemini, or share it with others

- **`examples/`** — `gemini_bridge.py` + `GEMINI_SETUP.md`: use the MCP from the
  Gemini API (Gemini has no built-in MCP client, so a small bridge maps MCP
  tools → Gemini function calls).
- **`gateway/`** — a FastAPI service that lets you give *other people* access
  without sharing your Gemini key: it holds your key + the MCP server-side and
  issues revocable, rate-limited per-user keys. See `gateway/README.md`.

---

## Project layout

```
tipsoi-support-mcp/
├── tipsoi_support_mcp/
│   ├── server.py          # FastMCP app — 5 tools + persona prompt
│   ├── kb.py              # KB loader + in-process BM25 search (stdlib only)
│   ├── escalation.py      # ticket model + ClickUp/webhook submission
│   ├── gemini_interop.py  # shared MCP→Gemini conversion helpers
│   └── kb_docs/           # 28 bundled help articles (EN/BN markdown)
├── examples/              # use the MCP from the Gemini API
│   ├── gemini_bridge.py
│   └── GEMINI_SETUP.md
├── gateway/               # multi-user FastAPI front door (issued keys)
│   ├── app.py · auth.py · ratelimit.py · manage_keys.py
│   ├── README.md · requirements.txt · .env.example
├── GUIDE.md               # setup + demo flows + can/can't
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Notes & next steps

- **No Tipsoi auth by design.** If a user asks this assistant to *do* something
  data-related (check a balance, approve leave), the persona tells them to use
  the Tipsoi app or the v1 data/action assistant. The two MCPs can run side by
  side — the host model routes by intent.
- **First live escalation to verify:** file one test ticket via `clickup_api`
  and confirm it lands in the support List with the right fields.
- **KB freshness:** the bundled articles are a snapshot. Wire a periodic sync
  from the source KB if it changes often.

*Inovace Technologies · Tipsoi Support Assistant (MCP v2) · June 2026*
