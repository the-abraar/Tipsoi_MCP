# Tipsoi Support Gateway

A multi-user front door for the Tipsoi Support MCP. **You** host it; it holds
your Gemini API key and runs the MCP server-side. You issue per-user gateway
keys that are revocable and rate-limited. When a user sends a message with their
key, the gateway answers them using **your** Gemini token and the MCP — the user
never sees either secret.

```
User ──(gateway key)──► POST /chat ──► Gemini (your key) ⇄ MCP tools ──► reply
```

This is the safe alternative to sharing your raw Gemini key: a Gemini key is one
unscoped bearer secret tied to your billing with no per-user revocation. The
gateway gives you exactly that — per-user identity, limits, and an off switch.

## What's here

| File | Purpose |
|---|---|
| `app.py` | FastAPI app: opens one MCP session for its lifetime, exposes `/chat` and `/health`. |
| `auth.py` | API-key store — salted-SHA-256 hashes on disk, individual revocation. |
| `ratelimit.py` | Per-key fixed-window rate limiter (requests/min). |
| `manage_keys.py` | CLI to create / list / revoke keys. |
| `requirements.txt` · `.env.example` | Deps and config template. |

## Setup

```bash
cd tipsoi-support-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .                       # the MCP server
pip install -r gateway/requirements.txt

cp gateway/.env.example gateway/.env   # set GEMINI_API_KEY (+ CLICKUP_* if filing tickets)
set -a; source gateway/.env; set +a
```

### Issue a key for a user

```bash
python -m gateway.manage_keys create --label "Pilot HR — Dhaka" --rpm 20
```

This prints the secret **once** (e.g. `tsg_…`). Give that to the user. Manage:

```bash
python -m gateway.manage_keys list
python -m gateway.manage_keys revoke k_ab12cd34
```

### Run the gateway

```bash
uvicorn gateway.app:app --host 0.0.0.0 --port 8080
```

### A user calls it

```bash
curl -s localhost:8080/chat \
  -H "Authorization: Bearer tsg_THEIR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"device punches but no attendance today","session_id":"user-123"}'
```

```json
{ "reply": "Here's what to check…", "conversation_id": "v1_…", "key_id": "k_ab12cd34" }
```

Pass the same `session_id` on follow-up messages to keep conversation context
(the gateway maps it to Gemini's `previous_interaction_id`). Auth also accepts
`X-API-Key: tsg_…` instead of the bearer header.

## How requests are handled

1. **Auth** — the key is hash-verified against the store; revoked/unknown → 401.
2. **Rate limit** — per-key requests/min; over limit → 429 with `Retry-After`.
3. **Answer** — the message runs through Gemini with the MCP tools attached. On a
   `function_call`, the gateway executes the tool via the shared MCP session and
   feeds the result back, looping up to `GATEWAY_MAX_TOOL_ITERS` times (a
   runaway-cost guard) until Gemini produces a final reply.
4. **State** — usage counters persist to the keys file; conversation threads are
   kept in memory keyed by `session_id`.

## Security & cost notes

- **Your secrets stay server-side.** Users only ever hold a `tsg_` gateway key.
- **Revocation is immediate** — the store reloads when the keys file changes; no
  restart needed.
- **Abuse/cost ceiling.** Even with the support persona as system prompt, a user
  could prompt Gemini off-topic and spend your tokens. The per-key `rpm` and
  `GATEWAY_MAX_TOOL_ITERS` cap blast radius; add a monthly per-key budget if you
  expose this widely.
- **This MCP is low-risk to share** — it's support-only, reads no HRM data, and
  serves the same KB to everyone, so a single shared backend is appropriate.
  (The v1 data MCP is different: it needs per-user OAuth because it reads each
  user's own org data — don't multi-tenant that one behind a single token.)
- **Run it over HTTPS** in production (terminate TLS at a reverse proxy / load
  balancer). Keys travel in the Authorization header.

## Scaling beyond a pilot

- The rate limiter and conversation map are **in-memory, per-process**. For
  multiple workers/instances, move both to Redis (key → window counter, and
  `session_id` → `previous_interaction_id`).
- The keys store is a JSON file. For many keys or concurrent admins, back
  `KeyStore` with a database (same interface: `verify`, `create`, `revoke`).
- One MCP session is shared across requests under an async lock. If tool latency
  becomes a bottleneck, run a small pool of MCP sessions.
