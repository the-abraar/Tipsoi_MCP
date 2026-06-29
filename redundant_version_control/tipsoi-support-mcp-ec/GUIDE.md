# Tipsoi Support Assistant — guide

## In one line
A support-only Tipsoi assistant: answers "how do I…/why is…" from a built-in
knowledge base and escalates to humans. No access to your HRM data.

## Pick your path
- **Tipsoi-flavored Gemini (most common):** your users call the standard
  google-genai SDK pointed at your proxy. Setup + deploy → `USAGE.md`, `DEPLOY.md`.
- **MCP connector (Claude Desktop / custom host):** add `tipsoi_support_mcp.server`.
- **Hosted chat / API:** run `gateway/qna.py` (web page + `/ask`).

## Demo questions (any path)
1. "How do I apply for leave in Tipsoi?"
2. "How do I set up overtime rules for payroll?"
3. "Attendance punched on the device but nothing shows on the dashboard today."
4. "An employee can't log in to the mobile app — what should I check?"
5. "ডিভাইস ডাটা আসছে না, কী করব?"  (answers in Bangla)

## What it CAN do
Answer how-to/troubleshooting from 28 bundled articles (EN/বাংলা); cite sources;
file a support ticket; run offline for Q&A (only escalation/Gemini reach out).

## What it CANNOT do
Read HRM data (balances, attendance, employee records); take Tipsoi actions
(apply/approve leave, edit anything); access anything per-organization. It
explains *how*; the v1 data/action MCP is for doing.

## Support contacts
Phone +8809638017170 · Email support@inovacetech.com
