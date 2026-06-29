# Tipsoi gateway — three ways to serve the assistant

All three hold your secrets server-side and authenticate callers with access
keys (env `QNA_API_KEYS`, or the revocable `KeyStore` via `GATEWAY_KEYS_FILE`).

| Module | What it is | Consumer |
|---|---|---|
| `gemini_proxy.py` ★ | Gemini-compatible proxy — Tipsoi-flavored Gemini | standard `google-genai` SDK with `base_url` |
| `qna.py` | KB-grounded Q&A: `/ask` JSON + a chat web page | HTTP / browser |
| `app.py` | MCP-backed loop (can also file tickets) | HTTP `/chat` |

## Auth & limits
- `QNA_API_KEYS` — comma-separated keys you hand out (simplest; deploy-friendly).
- `GATEWAY_KEYS_FILE` + `manage_keys.py` — revocable per-user keys:
  ```bash
  python -m gateway.manage_keys create --label "Pilot HR" --rpm 20
  python -m gateway.manage_keys list
  python -m gateway.manage_keys revoke k_ab12cd34
  ```
- `QNA_RPM` (proxy/qna) and per-key `rpm` (store) cap requests/min.

## Run
```bash
# Proxy (recommended) — deps: requirements-proxy.txt
export GEMINI_API_KEY=...  QNA_API_KEYS=tsg_xxx
uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port 8000

# Simple Q&A app — deps: requirements-qna.txt
uvicorn gateway.qna:app --port 8000

# MCP-backed gateway — deps: requirements.txt + pip install -e ..
uvicorn gateway.app:app --port 8080
```

## Scaling
Rate limiter + conversation map are in-memory per-process; move to Redis for
multiple workers. The JSON key store → a DB for many keys. See repo README.
