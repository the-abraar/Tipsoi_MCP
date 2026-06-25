"""
Escalation to human support.

The support team tracks tickets in a ClickUp form/list:
  https://forms.clickup.com/90181467757/f/2kzkqzkd-6058/GE9FE9OPW76Q2J4MAQ
expecting: Task Name, Client Name, Client Reported Date, Reported By,
Task Description, Steps to reproduce, The Ask, Your Email Address,
Attachments, Task Type.

ClickUp does NOT expose a documented public-form submission API, and the
per-field IDs of a public form are workspace-specific UUIDs that can't be
guessed. So this module files the ticket through ClickUp's *documented*
REST API (create a task in the List the form feeds), which is stable and
supported. A generic webhook mode is provided for teams that prefer not to
put a ClickUp token in the server. In every case the formatted ticket and
the support contacts are returned, so an escalation is never silently lost.

Configuration (all via environment):
  SUPPORT_TICKET_MODE      auto | clickup_api | webhook | off   (default: auto)
  CLICKUP_API_TOKEN        ClickUp personal API token (pk_...)
  CLICKUP_LIST_ID          numeric List ID the support form creates tasks in
  CLICKUP_CUSTOM_FIELDS    optional JSON: {"client_name":"<uuid>", ...}
  SUPPORT_TICKET_WEBHOOK   generic HTTPS endpoint (Zapier/Make/n8n) for mode=webhook
  SUPPORT_PHONE            default +8809638017170
  SUPPORT_EMAIL            default support@inovacetech.com
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any

import httpx

CLICKUP_API = "https://api.clickup.com/api/v2"
FORM_URL = "https://forms.clickup.com/90181467757/f/2kzkqzkd-6058/GE9FE9OPW76Q2J4MAQ"

DEFAULT_PHONE = "+8809638017170"
DEFAULT_EMAIL = "support@inovacetech.com"

# Maps our snake_case ticket keys -> the human field labels on the ClickUp form.
FIELD_LABELS = {
    "client_name": "Client Name",
    "reported_date": "Client Reported Date",
    "reported_by": "Reported By",
    "task_description": "Task Description",
    "steps_to_reproduce": "Steps to reproduce the issue",
    "the_ask": "The Ask",
    "email": "Your Email Address",
    "task_type": "Task Type",
}


def support_contacts() -> dict[str, str]:
    return {
        "phone": os.environ.get("SUPPORT_PHONE", DEFAULT_PHONE),
        "email": os.environ.get("SUPPORT_EMAIL", DEFAULT_EMAIL),
    }


def _dhaka_today() -> str:
    return datetime.now(timezone(timedelta(hours=6))).strftime("%Y-%m-%d")


@dataclass
class Ticket:
    task_name: str
    client_name: str
    reported_by: str
    task_description: str
    task_type: str
    reported_date: str = ""
    steps_to_reproduce: str = ""
    the_ask: str = ""
    email: str = ""

    def __post_init__(self):
        if not self.reported_date:
            self.reported_date = _dhaka_today()

    def as_dict(self) -> dict[str, str]:
        return {
            "task_name": self.task_name,
            "client_name": self.client_name,
            "reported_date": self.reported_date,
            "reported_by": self.reported_by,
            "task_description": self.task_description,
            "steps_to_reproduce": self.steps_to_reproduce,
            "the_ask": self.the_ask,
            "email": self.email,
            "task_type": self.task_type,
        }

    def to_markdown(self) -> str:
        """Human-readable ticket — used as the ClickUp task description AND
        returned to the user so nothing is ever lost."""
        lines = [
            f"**Client Name:** {self.client_name}",
            f"**Client Reported Date:** {self.reported_date}",
            f"**Reported By:** {self.reported_by}",
            f"**Task Type:** {self.task_type}",
            "",
            "**Task Description**",
            self.task_description or "_(none provided)_",
        ]
        if self.steps_to_reproduce:
            lines += ["", "**Steps to reproduce the issue**", self.steps_to_reproduce]
        if self.the_ask:
            lines += ["", "**The Ask**", self.the_ask]
        if self.email:
            lines += ["", f"**Your Email Address:** {self.email}"]
        return "\n".join(lines)


def _resolve_mode() -> str:
    mode = os.environ.get("SUPPORT_TICKET_MODE", "auto").lower()
    if mode != "auto":
        return mode
    if os.environ.get("CLICKUP_API_TOKEN") and os.environ.get("CLICKUP_LIST_ID"):
        return "clickup_api"
    if os.environ.get("SUPPORT_TICKET_WEBHOOK"):
        return "webhook"
    return "off"


async def _submit_clickup_api(ticket: Ticket) -> dict[str, Any]:
    token = os.environ["CLICKUP_API_TOKEN"]
    list_id = os.environ["CLICKUP_LIST_ID"]
    body: dict[str, Any] = {
        "name": ticket.task_name,
        "description": ticket.to_markdown(),
    }
    # Optional: also populate native custom fields if the team supplies a map.
    cf_map_raw = os.environ.get("CLICKUP_CUSTOM_FIELDS")
    if cf_map_raw:
        try:
            cf_map: dict[str, str] = json.loads(cf_map_raw)
            data = ticket.as_dict()
            custom_fields = [
                {"id": uuid, "value": data[key]}
                for key, uuid in cf_map.items()
                if key in data and data[key]
            ]
            if custom_fields:
                body["custom_fields"] = custom_fields
        except (json.JSONDecodeError, KeyError):
            pass  # never let a bad map block the ticket

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"{CLICKUP_API}/list/{list_id}/task",
            headers={"Authorization": token, "Content-Type": "application/json"},
            json=body,
        )
    if resp.status_code in (200, 201):
        data = resp.json()
        return {
            "filed": True,
            "channel": "clickup_api",
            "ticket_id": data.get("id"),
            "ticket_url": data.get("url"),
        }
    return {
        "filed": False,
        "channel": "clickup_api",
        "error": f"ClickUp API returned {resp.status_code}: {resp.text[:300]}",
    }


async def _submit_webhook(ticket: Ticket) -> dict[str, Any]:
    url = os.environ["SUPPORT_TICKET_WEBHOOK"]
    payload = {
        "source": "tipsoi-support-mcp",
        "form_url": FORM_URL,
        "fields": {FIELD_LABELS.get(k, k): v for k, v in ticket.as_dict().items()},
        "task_name": ticket.task_name,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, json=payload)
    if 200 <= resp.status_code < 300:
        return {"filed": True, "channel": "webhook"}
    return {
        "filed": False,
        "channel": "webhook",
        "error": f"Webhook returned {resp.status_code}: {resp.text[:300]}",
    }


async def submit(ticket: Ticket) -> dict[str, Any]:
    """File the ticket through the configured channel. Always returns the
    formatted ticket and support contacts, regardless of submission outcome."""
    mode = _resolve_mode()
    result: dict[str, Any]
    try:
        if mode == "clickup_api":
            result = await _submit_clickup_api(ticket)
        elif mode == "webhook":
            result = await _submit_webhook(ticket)
        else:  # "off" or unknown
            result = {
                "filed": False,
                "channel": "none",
                "note": (
                    "No ticket backend configured (SUPPORT_TICKET_MODE=off). "
                    "The formatted ticket below should be filed at the ClickUp "
                    "support form manually."
                ),
            }
    except Exception as e:  # noqa: BLE001 — never let escalation crash
        result = {"filed": False, "channel": mode, "error": repr(e)}

    result.update(
        {
            "form_url": FORM_URL,
            "support_contacts": support_contacts(),
            "ticket": ticket.as_dict(),
            "ticket_markdown": ticket.to_markdown(),
        }
    )
    return result
