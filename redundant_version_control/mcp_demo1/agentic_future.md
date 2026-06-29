# Tipsoi Agentic Future
## Where the MCP fits, what comes next, and the low-hanging fruits

*Inovace Technologies · June 2026*

---

## 1. Where We Are on the Map

The strategy dossier laid out three paths. Path B — an AI layer on top of the existing platform, additive not a rebuild — is the recommendation. For the architecture, it recommended Approach 2: a stable orchestrator routing to independent MCP agents.

**The MCP server we just built is the first working implementation of that architecture.**

But there is a nuance worth being clear about: the dossier imagined Tipsoi building its own orchestrator and chat UI. What we actually built is different and arguably better as a starting point — we used Claude itself as the orchestrator. The MCP connector plugs directly into Claude's reasoning engine, which means:

- The orchestrator already exists. Claude reads the tool list, understands intent, resolves context, calls the right tool, and formats the output. We did not build this — we got it for free.
- The chat UI already exists. Claude.ai and Claude Desktop are the interface. We did not build this either.
- The MCP is the domain layer. Our 19 tools (15 read + 4 write) are the Attendance Agent, Leave Agent, and OT Agent from the dossier — combined into one server for now, separable later.

Placed on the dossier's own map:

```
Vision map (Approach 2)
─────────────────────────────────────────────────────────────
User query
    │
    ▼
Orchestrator ◄──── Agent registry
    │
    ├── Attendance Agent  ←── [WE ARE HERE — combined in one MCP server]
    ├── Leave Agent       ←──
    ├── OT Agent          ←──
    ├── Payroll Agent     (blocked — API not yet exposed)
    └── Scheduler Agent   (not built)
    │
    ▼
Existing Tipsoi REST APIs
─────────────────────────────────────────────────────────────
```

The orchestrator and the first three agents are live. We skipped two months of build time by letting Claude be the orchestrator. The same MCP server can later be split into three separate services registered in a custom Tipsoi orchestrator — the interface contract (MCP) is already right.

---

## 2. What the MCP Proves Right Now

All 13 low-hanging-fruit use cases from the dossier are answerable today through the Claude connector, with no new backend work:

### Attendance (single API call each)
- "Who was absent today?" → `daily_absent_report`
- "Late arrivals this week for Dhaka office" → `late_report`
- "Monthly attendance summary for May" → `monthly_attendance`
- "Who punched in from mobile this month?" → `mobile_punch_report`

### Leave (single API call each)
- "Who is on leave this week?" → `applied_leave_list` (approved filter, current week)
- "Show all pending leave requests" → `applied_leave_list` (status=0)
- "How much leave balance does Rahim have?" → `leave_balance_report` + `list_employees` to resolve name

### Overtime (single API call each)
- "Who worked more than 20 OT hours this month?" → `monthly_overtime_report` (filter client-side)
- "Daily OT breakdown for last week" → `monthly_overtime_report` (date-filtered)

### Cross-domain (Claude combines two tools)
- "Late AND on overtime this month" → `late_report` + `monthly_overtime_report`, Claude intersects
- "Absenteeism trend, 3 months" → `daily_absent_report` called three times, Claude aggregates
- "Compare OT between Factory A and B" → `monthly_overtime_report` called twice
- ">5 leave days AND low attendance" → `leave_balance_report` + `monthly_attendance`, Claude joins

The dossier called medium-effort cases "multiple API calls + result merging." Claude does the merging. What was medium effort is now zero extra engineering.

---

## 3. What We Are Still Missing

### Missing from the MCP server itself

**Persistent token storage.** The OAuth token store is in-memory. A Render restart (which happens daily on the free tier) logs every user out. Until we add Redis or Postgres-backed storage, the connector is not production-grade for external clients.

**Token refresh.** When a user's Tipsoi access token expires mid-session, tools silently fail. The single-account client already handles refresh — the per-user OAuth path does not yet. This is a one-function fix but it has to happen before a client demo.

**The 13th use case is blocked.** "How much leave balance does Rahim have?" requires resolving a name to an employee ID reliably. The current `list_employees` call works but is slow and fragile for large orgs. The dossier identifies dedicated lookup/resolution endpoints as the single highest-value API addition Tipsoi backend can make.

### Missing from the broader vision

**The chat UI inside Tipsoi.** Right now users go to Claude.ai to query their HRM data. The vision is a chat box inside the Tipsoi admin panel. This is a frontend build — a text input that calls either Claude's API with the MCP server as a tool, or a custom orchestrator. The MCP server works identically in both cases.

**Scheduled reports.** The dossier's V2 is "save an approved report and auto-run it on a cadence." Claude's scheduled tasks feature can do a version of this today (run a prompt on a schedule), but it is not yet wired to the Tipsoi connector in a stable way. A proper implementation needs a Scheduler Agent that stores report configurations and triggers them via cron.

**Proactive alerts (V3).** The system waits to be asked. The vision has it surfacing anomalies unprompted — high absenteeism, attendance patterns suggesting attrition risk, overtime spikes. This requires a background process running daily/weekly queries and comparing against thresholds, then pushing alerts to the notification centre or email. Not blocked on the MCP; blocked on building the scheduler and the alerting pipeline.

**The Payroll Agent.** Explicitly blocked on the Tipsoi payroll API being exposed. Nothing to build until that exists. Once it does, adding the agent is registering a new MCP server — the orchestrator (Claude) picks it up automatically.

**Bangla language.** The dossier deferred this to after LLM provider evaluation. Claude's Bangla quality is reasonable but not validated against the accuracy bar required. English first is the right call.

---

## 4. The Actual Low-Hanging Fruits

These are ordered by impact and the engineering effort required. All of them use only what already exists.

### Fruit 1 — Pilot a real client today (effort: 0 days engineering)

The MCP connector at `https://tipsoi-mcp.onrender.com/mcp` is live. Any user on Claude Pro or above can add it and start querying their Tipsoi data. The only thing needed is credentials and a walkthrough. Pick the most enthusiastic HR manager, sit with them for 30 minutes, and document what they ask. This is the 6–8 week pilot the dossier asked for, compressed into a conversation.

### Fruit 2 — Fix token persistence (effort: ~1 day)

Swap the in-memory `TokenStore` dict for a Redis-backed store. Render has a free Redis add-on. This makes the OAuth session survive server restarts, which is the difference between a demo and something a client can depend on day-to-day.

### Fruit 3 — Wire up the 4 write tools to a pilot manager (effort: 0 days engineering)

`approve_leave`, `reject_leave`, `apply_leave`, and `adjust_leave` are already built and deployed. A manager on the pilot can say "approve Rahim's leave request" in Claude and it works. This is the confirm-before-action flow the old demo had to fake with UI cards — it is real now and requires no further engineering.

### Fruit 4 — Build the Tipsoi chat embed (effort: ~1 week frontend)

Add a chat widget to the Tipsoi admin panel that calls Claude's API with the MCP server registered as a tool. The backend is done. This is purely a frontend task: a text input, a streaming response display, and the API call wired up. Users stop needing a Claude account — they chat inside Tipsoi.

### Fruit 5 — Add the cross-domain tools the dossier identifies (effort: ~2 days)

The dossier lists specific cross-domain queries as medium-effort because they require merging API calls. Claude already does the merging. But wrapping the most common patterns as dedicated tools (e.g. `late_and_overtime_report`, `low_attendance_and_excessive_leave`) would make Claude's responses faster and more reliable — one tool call instead of two with client-side reasoning.

### Fruit 6 — Submit to the Claude Connectors Directory (effort: ~3 days)

The server is technically directory-ready except for four things: persistent token storage (Fruit 2), always-on hosting ($7/month Render upgrade), a logo + screenshots, and a privacy policy URL. Three of those are non-engineering tasks. Do this and Tipsoi appears in the Claude connector marketplace alongside Slack, Asana, and Figma — for free, as a distribution channel.

### Fruit 7 — Add a `report_summary` tool (effort: ~half a day)

A single tool that takes a date range and returns a one-paragraph narrative summary across attendance, leave, and overtime — the "Monday morning briefing" use case. HR managers ask for this naturally. Claude can already compose it from three tool calls, but a dedicated tool makes it one prompt away and sets up the scheduled-delivery use case cleanly.

---

## 5. The Strategic Position

The dossier asked whether Tipsoi leads the AI change in its market or follows someone who did. The honest answer right now: we are ahead of where the dossier projected we would be at this stage, on the MCP/connector path specifically.

What we have built in a few days is the functional equivalent of the dossier's "6–8 week prototype" goal — three domains, natural language queries, read-only with write tools in place, deployed, per-user auth, no new backend. The reason it was faster is that Claude-as-orchestrator collapsed two months of orchestrator build time to zero.

The remaining gap is not technical depth — it is surface area. The connector today is accessible to people who know what Claude is and have a Pro account. The vision is HRM users who have never heard of Claude asking questions inside the Tipsoi admin panel in Bangla, getting answers, and scheduling reports. That gap is:

1. The Tipsoi chat UI embed (frontend)
2. The scheduler (backend background jobs)
3. Proactive alerts (the system asks questions, not just answers them)
4. Payroll (blocked on API)

The MCP server is the data layer for all of it. It does not need to change to support any of those. The next thing to build is not more tools — it is the surface that puts those tools in front of users who do not know Claude exists.

---

*Prepared by Inovace Technologies Product Management · June 2026*
