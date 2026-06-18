# Tipsoi MCP — Phase 1 (Read-Only)

An MCP server that lets Claude read from the Tipsoi HRM API: employees,
attendance, leave, overtime, notifications, and org setup. **Phase 1 is
strictly read-only** — the server registers only GET endpoints, so the
assistant physically cannot create, edit, approve, or delete anything.

---

## What's exposed (15 tools)

| Tool | Reads |
|---|---|
| `list_employees` | Employee directory |
| `get_employee` | One employee's profile |
| `monthly_attendance` | Monthly attendance report |
| `daily_attendance_summary` | One day's attendance |
| `daily_absent_report` | Absentees for a date |
| `late_report` | Late / leave / absent over a range |
| `mobile_punch_report` | App/selfie punches over a range |
| `leave_balance_report` | Leave balances |
| `applied_leave_list` | Leave applications (view only) |
| `monthly_overtime_report` | Overtime report |
| `list_workplaces` | Offices/locations |
| `list_departments` | Departments |
| `list_designations` | Job titles |
| `list_holidays` | Holidays |
| `list_notifications` | Recent notifications |

Write endpoints from the API collection (create/update/delete employee, apply/
approve leave, change OT status, etc.) are **deliberately not registered**.
They belong to Phase 2+, behind per-user auth, confirmation, and audit logging.

---

## 1. Install

Requires Python 3.10+.

```bash
cd tipsoi-mcp
python -m venv .venv && source .venv/bin/activate    # optional but recommended
pip install -e .
```

## 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env`:

```
TIPSOI_EMAIL=service-account@yourcompany.com
TIPSOI_PASSWORD=...
TIPSOI_OFFICE_ID=4397        # optional default; discover via list_workplaces
TIPSOI_COMPANY_ID=4146       # optional default
```

> **Use a dedicated read-scoped service account.** Whatever this account can
> see in Tipsoi is the ceiling of what the assistant can read. Even though the
> server exposes no write tools, scope the account to read-only roles as a
> second line of defense.

The server reads env vars directly. To load `.env`, either export the vars in
your shell or use a tool like `direnv` / `dotenv`.

## 3. Test locally (stdio)

```bash
set -a; source .env; set +a
python -m tipsoi_mcp.server
```

It will start on stdio and wait for an MCP client. Use the MCP Inspector for a
quick manual check:

```bash
npx @modelcontextprotocol/inspector python -m tipsoi_mcp.server
```

Call `list_workplaces` first — it confirms auth works and shows valid
`office_id` values.

---

## 4. Use it as a Claude connector

You have two paths. **Local (stdio)** is the fastest for one machine; **remote
(HTTP)** is what you want for a shared team connector.

### Option A — Local, via Claude Desktop (stdio)

Claude Desktop launches the server as a subprocess.

1. Open Claude Desktop → **Settings → Developer → Edit Config**
   (this opens `claude_desktop_config.json`).
2. Add the server:

```json
{
  "mcpServers": {
    "tipsoi": {
      "command": "python",
      "args": ["-m", "tipsoi_mcp.server"],
      "cwd": "/absolute/path/to/tipsoi-mcp",
      "env": {
        "TIPSOI_EMAIL": "service-account@yourcompany.com",
        "TIPSOI_PASSWORD": "...",
        "TIPSOI_OFFICE_ID": "4397",
        "TIPSOI_COMPANY_ID": "4146"
      }
    }
  }
}
```

   Use the **full path** to your `python` (the venv one) if `python` isn't on
   Claude Desktop's PATH — e.g. `/path/to/tipsoi-mcp/.venv/bin/python`.

3. Restart Claude Desktop. You'll see a tools/connector icon; "tipsoi" and its
   15 tools should appear. Ask: *"List our Tipsoi workplaces"* or *"Show the
   daily attendance summary for 2026-02-18."*

### Option B — Remote, via Claude.ai / Claude Desktop Custom Connector (HTTP)

For a connector your team adds by URL, run the server in streamable-HTTP mode
behind HTTPS.

1. Run it in HTTP mode:

```bash
set -a; source .env; set +a
TIPSOI_TRANSPORT=http python -m tipsoi_mcp.server
```

   FastMCP serves the streamable-HTTP endpoint at `/mcp` (default host/port
   `127.0.0.1:8000`). Put it behind a reverse proxy (nginx/Caddy) or a tunnel
   so it's reachable over **HTTPS** — remote MCP connectors require TLS.

2. In Claude: **Settings → Connectors → Add custom connector**, then paste the
   public URL, e.g. `https://tipsoi-mcp.yourcompany.com/mcp`.

3. Claude lists the tools; enable them and start asking questions.

> **Phase 1 caveat on remote mode:** this build authenticates with a single
> service account and does **not** implement OAuth, so every user of the remote
> connector reads through that one account's permissions. That's acceptable for
> a read-only internal pilot but **must not** be how you ship write actions.
> Per-user OAuth is the first thing Phase 2 adds. Until then, if you deploy
> remotely, restrict network access (VPN/allowlist) so only your team can reach
> the endpoint.

---

## Example prompts once connected

- "Which employees were absent on 2026-02-18?"
- "Give me February 2026 attendance for the Dhaka office."
- "Show the overtime report for February 2026."
- "What's the leave balance for everyone this quarter?"
- "Pull the mobile/selfie punch report for last week."

## Design notes

- **Dates:** tools take `YYYY-MM-DD` (or `year`/`month`); the server converts to
  Tipsoi's epoch-millisecond format using `Asia/Dhaka` (UTC+6). Override with
  `TIPSOI_TZ_OFFSET_HOURS`.
- **Auth refresh:** on a 401 the client refreshes the token, then re-signs in if
  needed — transparent to the caller.
- **Errors:** API/auth failures return a structured `{"error": ...}` object
  instead of throwing, so Claude can explain the problem instead of failing
  opaquely.

## What Phase 2 will add (not in this build)

Per-user OAuth, role-gated write tools (apply/approve leave, OT status, roster
edits) behind a preview→confirm step, idempotency keys, and full audit logging
of every AI-initiated action.
