# Two ways to use this with Gemini

## A. Tipsoi-flavored Gemini (recommended) — `gateway/gemini_proxy.py`
Your users use the **standard google-genai SDK** with one extra line
(`http_options.base_url`). The proxy injects the Tipsoi persona + KB and calls
real Gemini with your key. See `../USAGE.md` and `client_example.py`. This needs
no MCP server.

## B. MCP + Gemini bridge — `gemini_bridge.py`
If you specifically want Gemini to call the MCP **tools** (e.g. to also file
tickets via function-calling), run `gemini_bridge.py`. It lists the MCP tools,
hands them to Gemini as function declarations, executes calls through the MCP
session, and loops to a final answer. Run:

```bash
pip install -e .. google-genai
export GEMINI_API_KEY=...
python examples/gemini_bridge.py
```
