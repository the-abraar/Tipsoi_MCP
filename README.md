# Tipsoi MCP Server

An MCP server that gives Claude access to the Tipsoi HRM API — employees,
attendance, leave, overtime, and org setup. Employees and managers can ask
Claude natural-language questions about HRM data and take common actions
without opening the Tipsoi dashboard.

**Current version:** 0.3.0  
**Deployed at:** `https://tipsoi-mcp.onrender.com/mcp`

---

## What's been built

### Phase 1 — 15 read-only tools ✅

Every tool carries `readOnlyHint: true` (required for Connectors Directory
submission). The server is physically incapable of mutating data.

| Tool | What it reads |
|---|---|
| `list_employees` | Employee directory |
| `get_employee` | Single employee profile |
| `monthly_attendance` | Monthly attendance report |
| `daily_attendance_summary` | One day's attendance |
| `daily_absent_report` | Absentees for a date |
| `late_report` | Late / leave / absent over a range |
| `mobile_punch_report` | App / selfie punches over a range |
| `leave_balance_report` | Leave balances |
| `applied_leave_list` | Leave applications (view only) |
| `monthly_overtime_report` | Overtime report |
| `list_workplaces` | Offices / locations |
| `list_departments` | Departments |
| `list_designations` | Job titles |
| `list_holidays` | Holidays |
| `list_notifications` | Recent notifications |

### Phase 2 — Per-user OAuth 2.1 ✅

Clients no longer share a service account. When a user adds the connector in
Claude, they are redirected to a hosted login page and sign in with their own
Tipsoi credentials. Their session is stored server-side and all tool calls are
made with their personal token — so each user only sees data their Tipsoi
account is permitted to access.

**What was built:**
- `token_store.py` — in-memory store for auth codes and access tokens (with PKCE support)
- `oauth_routes.py` — full OAuth 2.1 Authorization Code + PKCE endpoints:
  - `GET /.well-known/oauth-authorization-server` — server metadata (RFC 8414)
  - `GET /.well-known/oauth-protected-resource` — resource metadata (RFC 9728)
  - `POST /register` — dynamic client registration (RFC 7591)
  - `GET /authorize` — login page
  - `POST /authorize` — form submit: authenticates against Tipsoi, issues code, redirects
  - `POST /token` — code → access token exchange
- `_SessionMiddleware` — pure ASGI middleware that reads the Bearer token from
  each MCP request, looks up the user's Tipsoi session, and injects it via a
  `ContextVar`. Tools call `_client()` which returns the per-user
  `TipsoiClient` automatically.
- After OAuth sign-in, the server fetches the employee's profile to discover
  their `officeId` automatically — users don't need to configure anything.

### Phase 3 — Write tools ✅

Four write tools added. These use the per-user session from Phase 2 so actions
are attributed to the correct employee, not a service account.

| Tool | What it does | Annotation |
|---|---|---|
| `apply_leave` | Submit a leave application for an employee | `readOnlyHint: false` |
| `approve_leave` | Approve a pending leave application | `readOnlyHint: false` |
| `reject_leave` | Reject or cancel a leave application | `destructiveHint: true` |
| `adjust_leave` | Change the dates on an existing leave application | `readOnlyHint: false` |

### Deployment ✅

- **Dockerfile** — Python 3.12, installs the package and its dependencies
- **render.yaml** — free-tier Render web service, Docker runtime
- Hosted at `https://tipsoi-mcp.onrender.com`

---

## Quick start

### Local (Claude Desktop — single account)

```bash
cd tipsoi-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # fill in credentials
```

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tipsoi": {
      "command": "/absolute/path/to/.venv/bin/python3",
      "args": ["-m", "tipsoi_mcp.server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/tipsoi-mcp",
        "TIPSOI_EMAIL": "you@company.com",
        "TIPSOI_PASSWORD": "...",
        "TIPSOI_OFFICE_ID": "279",
        "TIPSOI_COMPANY_ID": "4146"
      }
    }
  }
}
```

Restart Claude Desktop. Ask: *"Who was absent today?"*

### Remote connector (per-user OAuth)

Clients add the connector URL in Claude → **Settings → Connectors → Add
custom connector**:

```
https://tipsoi-mcp.onrender.com/mcp
```

Claude initiates the OAuth flow, the user signs in at the hosted login page,
and Claude gets an access token tied to their Tipsoi account. No setup needed
on the client side.

---

## Example prompts

```
Was I late today?
Who was absent on 2026-06-22?
Show the monthly attendance report for May 2026.
What's the leave balance for everyone this quarter?
Apply 2 days annual leave for employee 348229 from 2026-07-01 to 2026-07-02.
Approve leave log 99012 with comment "Approved".
```

---

## Architecture

```
tipsoi-mcp/
├── tipsoi_mcp/
│   ├── server.py        # 19 tools (15 read + 4 write), combined app, ASGI middleware
│   ├── client.py        # Auth: sign-in, token refresh, GET + POST
│   ├── oauth_routes.py  # OAuth 2.1 endpoints + login page HTML
│   ├── token_store.py   # In-memory auth code + access token store (PKCE)
│   └── dates.py         # YYYY-MM-DD → Tipsoi epoch-ms (Asia/Dhaka)
├── Dockerfile
├── render.yaml
└── pyproject.toml
```

**Request flow (HTTP mode):**
1. Claude calls `POST /mcp` with `Authorization: Bearer <token>`
2. `_SessionMiddleware` reads the token, looks up the Tipsoi session, sets a `ContextVar`
3. Tool handler calls `_client()` → gets a `TipsoiClient` pre-loaded with that user's token
4. Client calls Tipsoi API, refreshing the token automatically on 401

---

## What still needs to be done

### Must-have before Connectors Directory submission

- [ ] **Persistent token storage** — the current in-memory store loses all
  sessions on server restart (Render free tier restarts frequently). Replace
  with Redis or a small SQLite/Postgres DB. Sessions survive restarts;
  users only need to re-authenticate when their Tipsoi token actually expires.

- [ ] **Token refresh in OAuth flow** — when a user's Tipsoi access token
  expires, they're currently logged out silently (tools return auth error).
  The server should use the stored `refreshToken` to get a new one
  transparently, the same way the single-account client already does.

- [ ] **Logo and branding assets** — Anthropic requires a logo, icon, and
  screenshots of the connector in action for the directory listing.

- [ ] **Privacy policy + support contact** — required by Anthropic before
  submission. Minimum: a privacy policy URL and a support email.

- [ ] **Production hosting** — Render free tier sleeps after 15 min of
  inactivity (30 sec cold start). Upgrade to $7/month Starter or move to a
  always-on host before submitting to the directory.

### Nice to have / Phase 4

- [ ] **More write tools** from the Postman collection:
  - `create_employee` / `update_employee`
  - `update_employee_status` (activate / deactivate)
  - `create_manual_attendance` (manual punch in/out)
  - `create_holiday` / `update_holiday`
  - `create_department` / `create_designation`

- [ ] **Role-gated tools** — check the authenticated user's Tipsoi role before
  allowing write actions. Employees should not be able to approve their own leave;
  managers should not touch data outside their office.

- [ ] **Audit log** — record every AI-initiated write action (who, what, when,
  which tool, what arguments) to a persistent log. Required for any serious
  enterprise deployment.

- [ ] **Rate limiting** — prevent a misconfigured Claude session from hammering
  the Tipsoi API. A simple per-token request counter is enough.

- [ ] **Multi-tenant isolation** — the current design uses one Render instance
  with one `.env`. For selling to multiple companies (each with their own
  `baseUrl`), the connector URL needs to encode or derive the Tipsoi instance.
  Options: subdomain routing, a path prefix per client, or a separate deployment
  per customer.

- [ ] **Test suite** — unit tests for the date helpers and OAuth PKCE validation,
  integration tests against the test account (`bugtitan@example.com`).
