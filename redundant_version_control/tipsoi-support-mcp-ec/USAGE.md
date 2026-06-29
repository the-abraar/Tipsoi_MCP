# Tipsoi-flavored Gemini — usage

A Tipsoi-aware Gemini your users call with the **standard google-genai SDK**.
You host the proxy (it holds your Gemini key + the Tipsoi knowledge base); you
hand someone a link (the base URL) and an access key. Their code is normal
Gemini code with one extra line.

## What you give someone
1. **Base URL** — your deployed proxy, e.g. `https://tipsoi-gemini.onrender.com`
2. **Access key** — e.g. `tsg_…` (you generate these; see "Issue keys")

## Their code

```python
import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key="tsg_THEIR_ACCESS_KEY",                      # the key you gave them
    http_options=types.HttpOptions(base_url="https://tipsoi-gemini.onrender.com"),
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How do I apply for leave in Tipsoi?",
)
print(response.text)
```

That's it — same SDK, same `response.text`. The proxy quietly injects the Tipsoi
support persona and the most relevant knowledge-base articles, then calls real
Gemini with YOUR key. Streaming (`generate_content_stream`), `count_tokens`, and
`models.list` all work too (only generateContent gets the Tipsoi grounding;
everything else passes through).

> Why the extra `http_options` line? The google-genai SDK has no base-URL
> environment variable, so the endpoint must be set on the client. It's the only
> change from vanilla Gemini code.

## Issue keys

Any random string works. Generate one:
```bash
python -c "import secrets;print('tsg_'+secrets.token_urlsafe(32))"
```
Put one or more (comma-separated) in the proxy's `QNA_API_KEYS` env var. To
revoke, remove it and redeploy. For revocable per-user keys without redeploying,
use the KeyStore instead: set `GATEWAY_KEYS_FILE` and run
`python -m gateway.manage_keys create --label "Pilot HR"`.

## Deploy

See `DEPLOY.md`. Quickest options:
- **Render** (persistent URL): push to GitHub → Blueprint deploy → set
  `GEMINI_API_KEY` and `QNA_API_KEYS`. Your base URL is the service URL.
- **Local + tunnel** (instant, no account):
  ```bash
  pip install -r gateway/requirements-proxy.txt
  export GEMINI_API_KEY=...  QNA_API_KEYS=tsg_xxx
  uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port 8000 &
  npx cloudflared tunnel --url http://localhost:8000   # prints your base URL
  ```

## Notes
- Your Gemini key never leaves the server; users only hold `tsg_` keys.
- `QNA_RPM` caps requests/min per key (default 30). A caller can still ask
  off-topic things and spend tokens, so keep a limit and watch usage.
- The model name the caller passes (e.g. `gemini-2.5-flash`) is forwarded as-is,
  so they choose the underlying Gemini model; you choose the Tipsoi flavor.
