# Using the Tipsoi Support MCP with the Gemini API

## The key idea

Claude connectors can point at an MCP server directly. **Gemini cannot** — the
Gemini API has no built-in MCP client. So you run the MCP server yourself and
put a small **bridge** between it and Gemini:

```
You ──► Gemini (Interactions API)
            │  emits function_call
            ▼
        Bridge  ◄──► MCP session  ──►  Tipsoi Support MCP server
            │  returns function_result        (search_kb / get_article /
            ▼                                   escalate_to_support …)
        Gemini final answer ──► You
```

The bridge does four things:

1. Starts/connects to the MCP server and lists its tools.
2. Converts each MCP tool into a Gemini **function declaration**.
3. Runs Gemini's function-calling loop: when Gemini asks to call a tool, the
   bridge executes it through the MCP session and feeds the result back.
4. Loads the server's `support_assistant_persona` prompt as the system
   instruction, so Gemini behaves like the Tipsoi Support Assistant.

A complete, working bridge is in **`gemini_bridge.py`** next to this file.

## Run it

```bash
# from the project root
python -m venv .venv && source .venv/bin/activate
pip install -e .                 # installs the MCP server + its deps
pip install google-genai          # the Gemini SDK

export GEMINI_API_KEY="your_key"
# optional: enable real ticket filing, same vars as Claude Desktop
export SUPPORT_TICKET_MODE=clickup_api
export CLICKUP_API_TOKEN=pk_...
export CLICKUP_LIST_ID=901800000000

python examples/gemini_bridge.py
```

Then chat:

```
You: device punches but no attendance shows today
  ↳ calling search_knowledge_base({'query': 'device punch no attendance dashboard', 'limit': 5})
Assistant: Here's what to check… (network / SIM balance / WiFi …)

You: still broken, please escalate. I'm Mahir at ACME Garments.
  ↳ calling escalate_to_support({'task_name': '…', 'client_name': 'ACME Garments', …})
Assistant: I've filed a ticket and our team will reach out. Support: +8809638017170 · support@inovacetech.com
```

## How tool conversion works

MCP tools expose a JSON-Schema `inputSchema`. Gemini function declarations want
roughly the same shape under `parameters`, but reject a few JSON-Schema keys.
The bridge strips `$schema`, `additionalProperties`, `title`, and `$defs`, then
wraps each tool as:

```python
{"type": "function", "name": tool.name,
 "description": tool.description, "parameters": cleaned_schema}
```

`required` fields and parameter `default`s are preserved, so Gemini knows which
arguments are mandatory.

## Notes & choices

- **Model:** defaults to `gemini-3.5-flash` (override with `GEMINI_MODEL`). Any
  function-calling-capable Gemini model works.
- **State:** the bridge uses the Interactions API's stateful chaining
  (`previous_interaction_id`), so the server keeps conversation history and the
  persona is sent only once, on the first turn.
- **Transport:** the example launches the server over **stdio** (simplest). To
  use a remote HTTP deployment instead, run the server with
  `TIPSOI_TRANSPORT=http` and swap the `stdio_client(...)` block for the MCP
  `streamablehttp_client(url)` client — the rest of the loop is identical.
- **Same guarantees as under Claude:** this MCP still reads no HRM data and only
  files a ticket on escalation. Running it under Gemini changes who the
  orchestrator is, not what the server can do.
- **`generateContent` alternative:** if you use Gemini's older `generateContent`
  API instead of the Interactions API, the `google-genai` SDK can accept an MCP
  `ClientSession` directly in `config.tools` and auto-run calls. The bridge here
  targets the Interactions API (the version in your docs) and works regardless
  of whether that auto-MCP path is available.

## Other languages

The same pattern works from the JS/TS SDK (`@google/genai` + the MCP TypeScript
SDK) or raw REST: list MCP tools → send them as `tools` in
`interactions.create` → on a `function_call` step, call the MCP tool → return a
`function_result`. Only the SDK calls differ; the loop is the same.
