# Tipsoi Support Assistant — Quick Start & Usage Guide

A plain-language guide to setting up the support MCP, trying it out, and knowing
exactly what it can and can't do. For the deeper technical reference, see
`README.md`.

---

## 1. What this is, in one line

A help desk in a box: it answers "how do I…" and "why is…" questions about
Tipsoi from a built-in knowledge base, and files a support ticket when it can't
help. It has **no access to your HRM data**.

---

## 2. Setup (about 5 minutes)

### Step 1 — Install

```bash
cd tipsoi-support-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### Step 2 — Decide how escalations get filed

Copy the example env file and pick one option:

```bash
cp .env.example .env
```

- **Just trying it out?** Do nothing. Escalations come back as a ready-to-paste
  ticket you can drop into the ClickUp form by hand. (`SUPPORT_TICKET_MODE=off`)
- **Want tickets filed automatically?** In `.env` set:
  ```
  SUPPORT_TICKET_MODE=clickup_api
  CLICKUP_API_TOKEN=pk_your_token_here
  CLICKUP_LIST_ID=901800000000
  ```
  Get the token from ClickUp → *Settings → Apps → API Token*. Get the List ID
  by opening the support form's destination List — its URL ends in
  `/li/<LIST_ID>`.
- **Prefer no ClickUp token in the server?** Use a webhook instead:
  ```
  SUPPORT_TICKET_MODE=webhook
  SUPPORT_TICKET_WEBHOOK=https://hooks.zapier.com/...
  ```
  and map that automation to the ClickUp form.

### Step 3 — Connect it to Claude

**Claude Desktop (local):** add to `claude_desktop_config.json`:

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

Restart Claude Desktop.

**Remote connector (HTTP):**

```bash
TIPSOI_TRANSPORT=http PORT=8000 python -m tipsoi_support_mcp.server
```

Put it behind HTTPS and add it in Claude → *Settings → Connectors → Add custom
connector* with your `https://…/mcp` URL.

### Step 4 — Load the persona (recommended)

The server ships a prompt called **`support_assistant_persona`**. Load it as the
system/developer prompt so the assistant answers from the KB, replies in the
user's language, and escalates properly. Without it the tools still work, but
the assistant won't follow the support playbook as tightly.

---

## 3. Demo questions to try

Ask these in plain language — the assistant searches the KB, reads the best
article, and answers. (Behind the scenes: `search_knowledge_base` →
`get_article` → reply.)

### How-to flows
1. **"How do I apply for leave in Tipsoi?"**
   → finds the leave-management overview, returns the steps.
2. **"How do I set up overtime rules for payroll?"**
   → finds overtime/custom-payroll-rules articles.
3. **"How do I create a shift and assign a roster?"**
   → finds the shift-management articles.

### Troubleshooting flows
4. **"Attendance punched on the device but nothing shows on the dashboard today."**
   → biometric device troubleshooting (network / SIM / WiFi checks).
5. **"An employee can't log in to the mobile app — what should I check?"**
   → mobile-app troubleshooting.

### Bilingual (বাংলা) flow
6. **"ডিভাইস ডাটা আসছে না, কী করব?"** *(Device data isn't coming, what do I do?)*
   → matches the bilingual official FAQ and answers in Bangla.

### "What can you help with?" flow
7. **"What topics can you help me with?"**
   → `list_help_topics` shows every article grouped by category.

### Escalation flow
8. **"Attendance still isn't showing after I checked the network — I need a person to fix this."**
   → the assistant confirms your name + company + what you've tried, then asks
   to file a ticket. On confirmation it calls `escalate_to_support` and shares
   the support phone and email.

   Try it end to end: *"My company is ACME Garments, I'm Mahir, device is online
   but today's attendance is missing, I've already restarted the device. Please
   escalate this."*

---

## 4. What it CAN do

- Answer how-to, setup, and troubleshooting questions about Tipsoi features:
  Employees, Attendance, Leave, Payroll, Shifts/Roster, Reports, Settings,
  Biometric Devices, Mobile App.
- Search a bundled knowledge base of 28 help articles, in **English and বাংলা**.
- Show you the full text of any help article.
- List everything it knows about ("what can you help with?").
- File a support ticket to the human team and give you the support contacts.
- Run fully offline for Q&A — no internet needed to answer (only escalation
  reaches out).

## 5. What it CANNOT do

- ❌ **Read your HRM data.** It cannot tell you a leave balance, who was absent,
  attendance numbers, overtime totals, or look up an employee record. It holds
  no Tipsoi login and calls no Tipsoi data APIs.
- ❌ **Take actions in Tipsoi.** It cannot apply for, approve, or reject leave;
  it cannot edit employees, shifts, or payroll. It can only *explain how* you do
  those things yourself.
- ❌ **Access anything live or per-organization.** Answers come from the bundled
  knowledge base, not from your account — so it never sees or mixes data between
  organizations.
- ❌ **Invent steps.** If the knowledge base doesn't cover something, it says so
  and offers to escalate rather than guessing.

> Need to actually *query data or take an action* (e.g. "who was absent today?",
> "approve Rahim's leave")? That's the job of the separate **v1 data/action MCP
> (`tipsoi-mcp`)**, not this one. The two can run side by side, and Claude will
> route to whichever fits the request.

---

## 6. Quick troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Assistant gives generic answers, ignores the KB | Load the `support_assistant_persona` prompt as the system prompt. |
| Escalation says `filed: false`, `channel: none` | No ticket backend configured — that's `off` mode. Set `clickup_api` or `webhook` in `.env`, or file the returned ticket text manually. |
| Escalation error from ClickUp | Check `CLICKUP_API_TOKEN` is valid and `CLICKUP_LIST_ID` is correct. |
| KB answer is out of date | Edit the markdown under `tipsoi_support_mcp/kb_docs/` and restart the server. |
| Bangla question gets an English-looking match | Still works — the FAQ/quick-guide articles are bilingual; the answer should be given in Bangla if the persona prompt is loaded. |

---

*Inovace Technologies · Tipsoi Support Assistant (MCP v2) · June 2026*
