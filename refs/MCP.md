

I'll start by reading the API collection to understand the available endpoints, then build the Phase 1 (read-only) MCP server.Let me look at each group's endpoints in detail.Now let me examine the authentication flow and a few key read endpoints in detail to get request/response shapes, headers, and auth mechanism.Let me look at the read-only report endpoints in detail (params, headers) and the sign-in response to understand the token shape.Let me check the sign-in response shape and any auth headers to confirm how the token comes back, plus check `Get Single Employee` response.No saved response examples, so I'll design defensively. The key facts I have:

- **Base URL:** `https://hrm.tipsoi.pro/inovace-client/api/v1`
- **Auth:** Bearer token; sign-in returns a token + `userId`; refresh uses `refreshToken` + `userId`
- **Reports** use Unix-millisecond timestamps for `from`/`to`, and require `officeId`
- Several reports reference `companyId=4146` and `officeId=4397`

Let me check the docx skill since I'll produce a setup guide, then build the server. First, building the MCP server.Now I'll build the server. I'm using FastMCP (Python) with the **streamable-HTTP** transport so it can run as a remote connector, plus a local **stdio** mode for testing. Phase 1 is strictly read-only.Now a small date helper (Tipsoi reports use Unix-millisecond timestamps, which an LLM should never have to compute by hand):Now the main MCP server with the Phase 1 read-only tools:Now the project files (pyproject, env example, gitignore), then I'll verify everything imports and the tools register correctly.Now let me install deps and verify the server imports and registers all tools correctly.All 15 read-only tools register cleanly. Let me verify the date helpers produce sane timestamps and the sign-in error handling behaves before packaging.The date math is correct. Two confirmations from the collection's own sample timestamps:

- `1769882400000` = month start (matches the **Leave Balance** report's `from`)
- `1771351200000` = day start for 2026-02-18 (matches the **Daily Summary** sample exactly)

The `late_report` sample used `1771092000000` which is mid-month (Feb 15), not month start — that's just how that particular saved request was set up, not a discrepancy in my logic. Auth failure also returns a clean structured error rather than crashing.

Now let me write the README/setup guide and Claude connector instructions, then package it.Let me do a final structural verification and confirm the multi-value `status` query encoding in `applied_leave_list` works correctly (it passes a pre-built query string through the path).Everything works. The repeated `status` keys survive into the final URL correctly. Let me package it as a zip for download.Done. Phase 1 Tipsoi MCP server is built, verified, and packaged.

## What's in it

A read-only MCP server wrapping your API collection. I parsed all 12 endpoint groups and exposed **15 GET-only tools** — no create/update/delete endpoints are registered, so the assistant physically cannot mutate anything. That registration boundary _is_ the Phase 1 safety story.

```
tipsoi-mcp/
├── tipsoi_mcp/
│   ├── server.py   # 15 read-only tools (FastMCP)
│   ├── client.py   # auth: sign-in, token refresh on 401, bearer GETs
│   └── dates.py    # YYYY-MM-DD → Tipsoi epoch-ms (Asia/Dhaka)
├── README.md       # full setup + connector guide
├── pyproject.toml
└── .env.example
```

Tools cover: employees (list/profile), attendance (monthly, daily summary, absent, late, mobile/selfie punch), leave (balance, applied list — view only), overtime, and org reference data (workplaces, departments, designations, holidays, notifications).

**Verified against your collection:** the date math matches the collection's own sample timestamps exactly (e.g. `1771351200000` = 2026-02-18 start), tools register cleanly, multi-value `status` params encode correctly, and auth failures return structured errors instead of crashing. I couldn't hit the live API (no credentials, and I shouldn't use real ones), so the request shapes are mirrored from your collection but unvalidated against live responses — first real call to make is `list_workplaces`, which confirms auth end to end.

## Using it as a Claude connector — two paths

**Local (fastest), via Claude Desktop:** add the server to `claude_desktop_config.json` under `mcpServers` with `command: python`, `args: ["-m","tipsoi_mcp.server"]`, your `cwd`, and credentials in `env`. Restart Desktop. Full JSON block is in the README.

**Remote (shared team connector):** run with `TIPSOI_TRANSPORT=http`, put it behind HTTPS, then add it in Claude → **Settings → Connectors → Add custom connector** with your `https://.../mcp` URL.

## Two things to flag before you deploy

1. **Single service account.** Phase 1 authenticates with one account (env vars), no OAuth. Every connector user reads through that account's permissions — fine for a read-only internal pilot, but use a **read-scoped** account, and if you go remote, restrict network access (VPN/allowlist) since there's no per-user identity yet.
    
2. **Setup needs a developer.** Installing Python deps, running the server, and editing JSON config isn't an end-user flow — it's a one-time engineering setup, after which your team just chats.
    

Per-user OAuth is the first thing Phase 2 adds, before any write tools. When you're ready for that, I'd want to check the current MCP authorization spec since it changes often — but that's later. For now, Phase 1 is complete.


