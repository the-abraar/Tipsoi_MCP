import json
import os
import requests
from openai import OpenAI
from datetime import datetime, timedelta

# ================= CONFIG =================
# Load your real JWT token from your Tipsoi login session
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIs..."  # PASTE YOUR REAL TOKEN HERE
SPRING_BOOT_BASE_URL = "http://localhost:8080/api"  # Your real backend URL

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============ AGENT TOOLS (Wrap Your Real APIs) ============
def call_tipsoi_api(endpoint: str, params: dict):
    """Generic function to call your real Spring Boot endpoints."""
    url = f"{SPRING_BOOT_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

# Tool definitions for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_daily_attendance",
            "description": "Get daily attendance summary for employees",
            "parameters": {
                "type": "object",
                "properties": {
                    "office_id": {"type": "string", "description": "Office ID, e.g., '4397'"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD"}
                },
                "required": ["office_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_late_report",
            "description": "Get employees who arrived late",
            "parameters": {
                "type": "object",
                "properties": {
                    "office_id": {"type": "string"},
                    "from_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                    "to_date": {"type": "string", "description": "End date YYYY-MM-DD"}
                },
                "required": ["office_id", "from_date", "to_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_overtime_report",
            "description": "Get monthly overtime hours per employee",
            "parameters": {
                "type": "object",
                "properties": {
                    "office_id": {"type": "string"},
                    "month": {"type": "string", "description": "Month in YYYY-MM"}
                },
                "required": ["office_id", "month"]
            }
        }
    }
]

# ============ EXECUTION MAPPING (Maps LLM choice to your real API) ============
def execute_tool(tool_name, args):
    if tool_name == "get_daily_attendance":
        # Maps to your existing Spring Boot endpoint
        return call_tipsoi_api("/attendance/daily", {
            "officeId": args["office_id"],
            "date": args.get("date", datetime.today().strftime("%Y-%m-%d"))
        })
    elif tool_name == "get_late_report":
        return call_tipsoi_api("/attendance/late", {
            "officeId": args["office_id"],
            "from": args["from_date"],
            "to": args["to_date"]
        })
    elif tool_name == "get_overtime_report":
        return call_tipsoi_api("/overtime/monthly", {
            "officeId": args["office_id"],
            "month": args["month"]
        })
    return {"error": "Unknown tool"}

# ============ THE ORCHESTRATOR LOOP ============
def ask_agent(question):
    print(f"\n🤔 You asked: {question}")

    # Step 1: Send question + tools to LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Step 2: Check if the LLM wants to call an API
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f"🧠 AI decided to call: {tool_name} with {args}")

        # Step 3: Call your REAL Spring Boot API with the REAL JWT
        result = execute_tool(tool_name, args)

        # Step 4: Send the API result back to the LLM for a human-readable answer
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": question},
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)  # Your real API data
                }
            ]
        )
        print("\n✅ Final Answer:\n", final_response.choices[0].message.content)
    else:
        # No tool needed, just answer directly
        print("\n💬", message.content)

# ============ RUN THE DEMO ============
if __name__ == "__main__":
    # Test with a real question
    ask_agent("Who was late in the Dhaka office this week?")
    # ask_agent("Generate an overtime report for Factory A for May")