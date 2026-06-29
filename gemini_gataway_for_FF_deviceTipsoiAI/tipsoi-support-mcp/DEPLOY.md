# Deploy — get a base URL + access key to share

Deploys the **Tipsoi-flavored Gemini proxy** (`gateway.gemini_proxy`). Consumers
then use the standard google-genai SDK pointed at your base URL (see `USAGE.md`).

```
Consumer (google-genai SDK, access key) ──► your proxy ──► Gemini (your key) + Tipsoi KB ──► answer
```

## 1. Generate access key(s)
```bash
python -c "import secrets;print('tsg_'+secrets.token_urlsafe(32))"
```
These go in `QNA_API_KEYS` (comma-separated). Revoke by removing + redeploying,
or use `gateway/manage_keys.py` + `GATEWAY_KEYS_FILE` for revocable keys.

## 2a. Render (persistent URL)
1. Push this folder to a GitHub repo.
2. Render → New → Blueprint → select the repo (uses `render.yaml`).
3. Set env vars: `GEMINI_API_KEY` (your real key), `QNA_API_KEYS` (your keys).
4. Deploy. Base URL = `https://<service>.onrender.com`.
   (Free tier sleeps when idle; first call after a nap is slow.)

## 2b. Docker anywhere
```bash
docker build -t tipsoi-gemini .
docker run -p 8000:8000 -e GEMINI_API_KEY=... -e QNA_API_KEYS=tsg_xxx tipsoi-gemini
# base URL: http://your-server:8000
```

## 2c. Instant link, no account (local + tunnel)
```bash
pip install -r gateway/requirements-proxy.txt
export GEMINI_API_KEY=...  QNA_API_KEYS=tsg_xxx
uvicorn gateway.gemini_proxy:app --host 0.0.0.0 --port 8000 &
npx cloudflared tunnel --url http://localhost:8000   # prints your https base URL
```

## 3. Verify
```bash
curl -s https://YOUR_BASE/health
# then from Python, run examples/client_example.py with TIPSOI_BASE_URL + TIPSOI_KEY
```

## Notes
- Your Gemini key stays server-side; users only hold `tsg_` access keys.
- `QNA_RPM` caps requests/min per key (default 30).
- Always HTTPS in production (Render/Cloudflare handle TLS).
