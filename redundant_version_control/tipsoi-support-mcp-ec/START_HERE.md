# START HERE — Tipsoi Support Assistant

This is the master guide: what's in the box, how to ship it, and what to do
next. For deeper detail, follow the links to the other docs.

---

## What this is

A **support-only** Tipsoi assistant. It answers "how do I… / why is…" questions
about Tipsoi from a built-in, bilingual (English + বাংলা) knowledge base, and
escalates to human support when it can't help. It holds **no Tipsoi credentials**
and reads **no HRM data** — it explains how to use Tipsoi; it never touches an
organization's records.

It ships in three forms. Pick the one you need (you can run more than one):

| You want… | Run this | Consumers use |
|---|---|---|
| ⭐ **Tipsoi-flavored Gemini** (drop-in SDK) | `gateway/gemini_proxy.py` | standard `google-genai`, one extra `base_url` line |
| An **MCP connector** (Claude Desktop / custom host) | `tipsoi_support_mcp/server.py` | add as an MCP server |
| A **hosted chat page / `/ask` API** | `gateway/qna.py` | a browser, or HTTP POST |

The path you asked for is the first one (the Gemini proxy).

---

## Your access key

I generated one ready-to-use access key:

```
tsg_Z9m1LlodRgZmKhbRnZ_SMcxLssRMbeQSqC3igTTEVVk
```

This is what you hand to other people. Put it in the server's `QNA_API_KEYS`
env var. Generate more anytime:

```bash
python -c "import secrets;print('tsg_'+secrets.token_urlsafe(32))"
```

`QNA_API_KEYS` takes a comma-separated list. To revoke, remove a key and
redeploy — or use revocable per-user keys (`gateway/manage_keys.py` +
`GATEWAY_KEYS_FILE`).

---

## Quick start (Tipsoi-flavored Gemini)

**1. Run the proxy** (it holds YOUR Gemini key; users never see it):

```bash
pip install -r gateway/requirements-proxy.txt
export GEMINI_API_KEY="your-real-gemini-key"
export QNA_API_KEYS="tsg_Z9m1LlodRgZmKhbRnZ_SMcxLssRMbeQSqC3igTTEVVk"
uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port 8000
```

**2. Get a public link.** Either deploy (see `DEPLOY.md`) or tunnel instantly:

```bash
npx cloudflared tunnel --url http://localhost:8000   # prints an https base URL
```

**3. Give someone the base URL + the access key.** Their code:

```python
from google import genai
from google.genai import types

client = genai.Client(
    api_key="tsg_Z9m1LlodRgZmKhbRnZ_SMcxLssRMbeQSqC3igTTEVVk",
    http_options=types.HttpOptions(base_url="https://YOUR-BASE-URL"),
)
print(client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How do I apply for leave in Tipsoi?").text)
```

Same SDK, same `response.text`. The proxy injects the Tipsoi persona + the most
relevant KB articles, then calls real Gemini with your key. (The one change from
vanilla Gemini code is the `base_url` line — the SDK has no base-URL env var.)

Full usage: `USAGE.md` · Deploy options (Render / Docker / tunnel): `DEPLOY.md`

---

## What's in the box

```
tipsoi-support-mcp/
├── START_HERE.md            ← you are here
├── README.md                project overview
├── USAGE.md                 ⭐ how consumers use the Tipsoi-flavored Gemini
├── DEPLOY.md                deploy to get a public base URL + key
├── GUIDE.md                 setup + demo questions + can/can't
├── Dockerfile  render.yaml  container + one-click Render deploy
├── pyproject.toml  .env.example  .gitignore
│
├── tipsoi_support_mcp/      the assistant's brain
│   ├── server.py            MCP server (5 tools + persona prompt)
│   ├── kb.py                in-process BM25 search (pure stdlib)
│   ├── persona.py           the support persona (shared everywhere)
│   ├── escalation.py        file a ClickUp ticket / webhook / fallback
│   ├── gemini_interop.py    MCP→Gemini schema helpers
│   └── kb_docs/             28 bundled help articles (EN/বাংলা)
│
├── gateway/
│   ├── gemini_proxy.py      ⭐ Tipsoi-flavored Gemini (drop-in SDK proxy)
│   ├── qna.py               hosted chat page + /ask JSON API
│   ├── app.py               MCP-backed multi-user gateway (also files tickets)
│   ├── auth.py              revocable, hashed API-key store
│   ├── ratelimit.py         per-key rate limiting
│   ├── manage_keys.py       CLI: create / list / revoke keys
│   ├── requirements-proxy.txt   (proxy: fastapi, uvicorn, httpx)
│   ├── requirements-qna.txt     (qna: fastapi, uvicorn, google-genai)
│   ├── requirements.txt         (MCP gateway: + mcp)
│   ├── README.md  .env.example
│
└── examples/
    ├── client_example.py    the consumer snippet (copy/paste)
    ├── gemini_bridge.py     optional: Gemini calling the MCP tools
    └── GEMINI_SETUP.md      both Gemini paths explained
```

---

## How escalation works (optional)

When the assistant can't resolve something, `escalate_to_support` files a ticket
into your ClickUp via its REST API and returns the support contacts. Configure
with `SUPPORT_TICKET_MODE` (`clickup_api` / `webhook` / `off`); details in
`tipsoi_support_mcp/escalation.py` and `.env.example`. Left `off`, it returns a
ready-to-file ticket so nothing is lost. (Escalation is wired into the MCP
server and the MCP-backed gateway; the plain Gemini proxy focuses on Q&A.)

Support contacts: Phone +8809638017170 · Email support@inovacetech.com

---

## What to do next

1. **Try it locally** — run the proxy (above) and `examples/client_example.py`
   with `TIPSOI_BASE_URL=http://localhost:8000` and `TIPSOI_KEY=<your key>`.
2. **Smoke-test** — `curl http://localhost:8000/health` should report the KB
   article count and that your key is loaded.
3. **Deploy for a real link** — `DEPLOY.md` (Render is the same host your v1 MCP
   used). Set `GEMINI_API_KEY` and `QNA_API_KEYS` in the dashboard.
4. **Hand it out** — give a teammate the base URL + an access key. Watch usage;
   keep `QNA_RPM` sane (default 30/min per key) since callers can ask off-topic
   things and spend your Gemini tokens.
5. **Refresh the KB when it changes** — edit/add `.md` files in
   `tipsoi_support_mcp/kb_docs/` and restart.
6. **Protect the work** — this folder is not a git repo. Run `git init` and
   commit so nothing is lost. (Happy to do this for you.)

### Known limitations / honest notes
- The live HTTP path (proxy → real Gemini) was **not run end-to-end here** — the
  build sandbox has no network and no Gemini key. All offline logic is unit-
  tested (KB search, key auth, request transforms). First thing to confirm on
  your machine: one real `generate_content` call returns a sensible answer.
- The proxy grounds answers in the KB but doesn't expose the MCP *tools* to the
  caller; if you want Gemini to also file tickets via function-calling, use
  `examples/gemini_bridge.py` or the MCP-backed `gateway/app.py`.

*Inovace Technologies · Tipsoi Support Assistant · 2026*
