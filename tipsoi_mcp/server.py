"""
Tipsoi MCP Server — Phase 2 (per-user OAuth) + Phase 3 (write tools)

Phase 1: 15 read-only tools, single service account.
Phase 2: OAuth 2.1 proxy — each Claude user signs in with their own Tipsoi
         credentials. Every tool call uses that user's personal token.
Phase 3: Write tools — apply / approve / reject leave, manual attendance.

Run modes:
    python -m tipsoi_mcp.server            # stdio (Claude Desktop, single account)
    TIPSOI_TRANSPORT=http python -m tipsoi_mcp.server   # HTTP (remote connector, per-user OAuth)
"""

from __future__ import annotations

import os
from contextvars import ContextVar
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .client import TipsoiClient, TipsoiAPIError, TipsoiAuthError
from .dates import day_start_ms, day_end_ms, month_range_ms, year_range_ms
from .token_store import token_store, UserSession

_port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("tipsoi", host="0.0.0.0", port=_port)

# Service-account client (used in stdio mode or as fallback)
_service_client = TipsoiClient()

# Per-request user session (set by ASGI middleware in HTTP mode)
_current_session: ContextVar[UserSession | None] = ContextVar("current_session", default=None)

_ro = ToolAnnotations(readOnlyHint=True)


# ---------------------------------------------------------------------------
# ASGI middleware — reads Bearer token, sets _current_session ContextVar
# ---------------------------------------------------------------------------

class _SessionMiddleware:
    def __init__(self, app):
        self._app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = {k.lower(): v for k, v in scope.get("headers", [])}
            auth = headers.get(b"authorization", b"").decode("utf-8", errors="ignore")
            if auth.startswith("Bearer "):
                token = auth[7:].strip()
                session = token_store.get_session(token)
                _current_session.set(session)
            else:
                _current_session.set(None)
        await self._app(scope, receive, send)


# ---------------------------------------------------------------------------
# Per-request client resolver
# ---------------------------------------------------------------------------

def _client() -> TipsoiClient:
    """Return the TipsoiClient for the current request.

    In HTTP mode: returns a client built from the OAuth user's session.
    In stdio mode (or if no token present): falls back to service account.
    """
    session = _current_session.get()
    if session:
        return TipsoiClient.with_session(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user_id=session.user_id,
            office_id=session.office_id,
            company_id=session.company_id,
        )
    return _service_client


def _office_id(office_id: str | None, c: TipsoiClient) -> str:
    oid = office_id or c.default_office_id
    if not oid:
        raise ValueError("office_id is required. Pass it explicitly or set TIPSOI_OFFICE_ID.")
    return oid


async def _safe_get(path: str, params: dict[str, Any] | None = None) -> Any:
    try:
        return await _client().get(path, params)
    except TipsoiAuthError as e:
        return {"error": "authentication_failed", "detail": str(e)}
    except TipsoiAPIError as e:
        return {"error": "api_error", "status": e.status, "detail": e.detail}
    except Exception as e:
        return {"error": "unexpected", "detail": repr(e)}


async def _safe_post(path: str, body: dict[str, Any] | None = None) -> Any:
    try:
        return await _client().post(path, body)
    except TipsoiAuthError as e:
        return {"error": "authentication_failed", "detail": str(e)}
    except TipsoiAPIError as e:
        return {"error": "api_error", "status": e.status, "detail": e.detail}
    except Exception as e:
        return {"error": "unexpected", "detail": repr(e)}


async def _safe_post_form(path: str, post_body: dict[str, Any]) -> Any:
    try:
        return await _client().post_form(path, post_body)
    except TipsoiAuthError as e:
        return {"error": "authentication_failed", "detail": str(e)}
    except TipsoiAPIError as e:
        return {"error": "api_error", "status": e.status, "detail": e.detail}
    except Exception as e:
        return {"error": "unexpected", "detail": repr(e)}


# ---------------------------------------------------------------------------
# Phase 1 — Read-only tools (unchanged)
# ---------------------------------------------------------------------------

@mcp.tool(annotations=_ro)
async def list_employees(
    status: int = 1,
    page_number: int = 0,
    per_page: int = 200,
    order: str = "asc",
) -> Any:
    """List employees in the organization.

    Args:
        status: 1 = active, 0 = inactive. Default active.
        page_number: Zero-based page index.
        per_page: Records per page (keep modest, e.g. 50-500).
        order: 'asc' or 'desc'.
    """
    return await _safe_get(
        "employee",
        {"status": status, "pageNumber": page_number, "perPage": per_page, "order": order},
    )


@mcp.tool(annotations=_ro)
async def get_employee(employee_id: str) -> Any:
    """Get the basic profile of a single employee by their numeric employee ID.

    Args:
        employee_id: The Tipsoi employee ID (string of digits).
    """
    return await _safe_get(f"employee/basic-profile/{employee_id}")


@mcp.tool(annotations=_ro)
async def monthly_attendance(
    year: int,
    month: int,
    office_id: str | None = None,
    employee_name: str = "",
    status: int = 1,
    per_page: int = 500,
    page_number: int = 0,
) -> Any:
    """Monthly attendance report for an office.

    Args:
        year: e.g. 2026.
        month: 1-12.
        office_id: Tipsoi office ID. Falls back to the logged-in user's office if omitted.
        employee_name: Optional name filter (substring).
        status: 1 = active employees.
        per_page / page_number: Pagination.
    """
    c = _client()
    start, end = month_range_ms(year, month)
    return await _safe_get(
        "attendance",
        {
            "officeId": _office_id(office_id, c),
            "employeeName": employee_name,
            "order": "asc",
            "pageNumber": page_number,
            "perPage": per_page,
            "reportType": "department",
            "sortKey": "reportPosition",
            "status": status,
            "from": start,
            "to": end,
        },
    )


@mcp.tool(annotations=_ro)
async def daily_attendance_summary(
    date: str,
    office_id: str | None = None,
    employee_name: str = "",
    status: int = 1,
    per_page: int = 500,
) -> Any:
    """Daily attendance summary for a single date.

    Args:
        date: YYYY-MM-DD.
        office_id: Falls back to the logged-in user's office if omitted.
        employee_name: Optional name filter.
        status: 1 = active employees.
        per_page: Pagination size.
    """
    c = _client()
    return await _safe_get(
        "attendance/daily-summary",
        {
            "officeId": _office_id(office_id, c),
            "employeeName": employee_name,
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "reportType": "daily",
            "sortKey": "reportPosition",
            "status": status,
            "from": day_start_ms(date),
            "to": day_end_ms(date),
        },
    )


@mcp.tool(annotations=_ro)
async def daily_absent_report(
    date: str,
    office_id: str | None = None,
    absent_type: int = 1,
    per_page: int = 500,
) -> Any:
    """Report of employees absent on a given date.

    Args:
        date: YYYY-MM-DD.
        office_id: Falls back to the logged-in user's office if omitted.
        absent_type: Tipsoi absent classification code (default 1).
        per_page: Pagination size.
    """
    c = _client()
    return await _safe_get(
        "attendance/daily-absent",
        {
            "absentType": absent_type,
            "officeId": _office_id(office_id, c),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "reportType": 3,
            "sortKey": "reportPosition",
            "status": 1,
            "from": day_start_ms(date),
            "to": day_end_ms(date),
        },
    )


@mcp.tool(annotations=_ro)
async def late_report(
    from_date: str,
    to_date: str,
    office_id: str | None = None,
    company_id: str | None = None,
    per_page: int = 500,
) -> Any:
    """Late / leave / absent combined report over a date range.

    Args:
        from_date: YYYY-MM-DD (inclusive).
        to_date: YYYY-MM-DD (inclusive).
        office_id: Falls back to the logged-in user's office.
        company_id: Falls back to the logged-in user's company.
        per_page: Pagination size.
    """
    c = _client()
    return await _safe_get(
        "attendance/leave-late-absent",
        {
            "companyId": company_id or c.default_company_id,
            "officeId": _office_id(office_id, c),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "reportType": 2,
            "sortKey": "reportPosition",
            "status": 1,
            "from": day_start_ms(from_date),
            "to": day_end_ms(to_date),
        },
    )


@mcp.tool(annotations=_ro)
async def mobile_punch_report(
    from_date: str,
    to_date: str,
    office_id: str | None = None,
    per_page: int = 500,
) -> Any:
    """Mobile punch (app-based check-in/out, incl. selfie attendance) report.

    Args:
        from_date: YYYY-MM-DD (inclusive).
        to_date: YYYY-MM-DD (inclusive).
        office_id: Falls back to the logged-in user's office.
        per_page: Pagination size.
    """
    c = _client()
    return await _safe_get(
        "mobile-punch",
        {
            "dinnerFilter": -1,
            "lunchFilter": -1,
            "officeId": _office_id(office_id, c),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "sortKey": "reportPosition",
            "status": 1,
            "from": day_start_ms(from_date),
            "to": day_end_ms(to_date),
        },
    )


@mcp.tool(annotations=_ro)
async def leave_balance_report(
    from_date: str,
    to_date: str,
    office_id: str | None = None,
    per_page: int = 500,
) -> Any:
    """Leave balance report across a date range.

    Args:
        from_date: YYYY-MM-DD.
        to_date: YYYY-MM-DD.
        office_id: Falls back to the logged-in user's office.
        per_page: Pagination size.
    """
    c = _client()
    return await _safe_get(
        "attendance/leave-balance",
        {
            "officeId": _office_id(office_id, c),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "sortKey": "reportPosition",
            "status": 1,
            "from": day_start_ms(from_date),
            "to": day_end_ms(to_date),
        },
    )


@mcp.tool(annotations=_ro)
async def applied_leave_list(
    keyword: str = "",
    statuses: list[int] | None = None,
    page: int = 0,
    count: int = 100,
) -> Any:
    """List applied leave requests and their approval statuses.

    Args:
        keyword: Optional search term.
        statuses: Status codes to include. Defaults to [0, 1] (pending + approved).
        page: Zero-based page index.
        count: Page size.
    """
    from urllib.parse import urlencode
    params: list[tuple[str, Any]] = [
        ("keyword", keyword),
        ("page", page),
        ("count", count),
    ]
    for s in (statuses if statuses is not None else [0, 1]):
        params.append(("status", s))
    qs = urlencode(params)
    return await _safe_get(f"leave-management/leave-history/?{qs}")


@mcp.tool(annotations=_ro)
async def monthly_overtime_report(
    year: int,
    month: int,
    office_id: str | None = None,
    company_id: str | None = None,
    per_page: int = 500,
) -> Any:
    """Monthly overtime report.

    Args:
        year: e.g. 2026.
        month: 1-12.
        office_id: Falls back to the logged-in user's office.
        company_id: Falls back to the logged-in user's company.
        per_page: Pagination size.
    """
    c = _client()
    start, end = month_range_ms(year, month)
    return await _safe_get(
        "overtime/report",
        {
            "companyId": company_id or c.default_company_id,
            "officeId": _office_id(office_id, c),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "sortKey": "reportPosition",
            "from": start,
            "to": end,
        },
    )


@mcp.tool(annotations=_ro)
async def list_workplaces() -> Any:
    """List all workplaces (offices/locations) configured in Tipsoi.

    Useful for discovering valid office_id values to pass to report tools.
    """
    return await _safe_get("workplace")


@mcp.tool(annotations=_ro)
async def list_departments(include_inactive: bool = True) -> Any:
    """List departments.

    Args:
        include_inactive: Include inactive departments. Default True.
    """
    return await _safe_get("department", {"includeInactive": str(include_inactive).lower()})


@mcp.tool(annotations=_ro)
async def list_designations() -> Any:
    """List all designations (job titles)."""
    return await _safe_get("designation")


@mcp.tool(annotations=_ro)
async def list_holidays() -> Any:
    """List configured holidays."""
    return await _safe_get("holiday")


@mcp.tool(annotations=_ro)
async def list_notifications(page_number: int = 0, per_page: int = 20) -> Any:
    """List recent notifications for the authenticated account.

    Args:
        page_number: Zero-based page index.
        per_page: Page size.
    """
    return await _safe_get("notification", {"pageNumber": page_number, "perPage": per_page})


# ---------------------------------------------------------------------------
# Phase 3 — Write tools
# ---------------------------------------------------------------------------

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
async def apply_leave(
    employee_id: str,
    leave_category_id: int,
    from_date: str,
    to_date: str,
    reason: str = "",
    is_half_day: bool = False,
    force_approval: bool = True,
    fiscal_year_start_date: str | None = None,
    fiscal_year_end_date: str | None = None,
) -> Any:
    """Apply for leave on behalf of an employee.

    Sends a multipart/form-data request with a `postBody` JSON field, as the
    Tipsoi apply-leave endpoint requires.

    Args:
        employee_id: Tipsoi employee ID.
        leave_category_id: Numeric ID of the leave category (e.g. annual, sick).
                           Discover valid IDs via the leave-category config.
        from_date: Leave start date, YYYY-MM-DD.
        to_date: Leave end date, YYYY-MM-DD (inclusive).
        reason: Optional reason / note for the leave request.
        is_half_day: True for a half-day leave request.
        force_approval: Whether to force-approve on apply (default True, per API example).
        fiscal_year_start_date: YYYY-MM-DD. Defaults to Jan 1 of from_date's year.
        fiscal_year_end_date: YYYY-MM-DD. Defaults to Dec 31 of from_date's year.
    """
    fy_start, fy_end = year_range_ms(from_date)
    if fiscal_year_start_date:
        fy_start = day_start_ms(fiscal_year_start_date)
    if fiscal_year_end_date:
        fy_end = day_end_ms(fiscal_year_end_date)
    post_body = {
        "leaveCategoryId": leave_category_id,
        "reason": reason,
        "forceApproval": force_approval,
        "fiscalYearStartDate": fy_start,
        "fiscalYearEndDate": fy_end,
        "startDate": day_start_ms(from_date),
        "endDate": day_end_ms(to_date),
        "isHalfDay": is_half_day,
    }
    return await _safe_post_form(f"leave-management/apply/employee/{employee_id}", post_body)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
async def approve_leave(
    leave_log_id: str,
    approver_comment: str = "",
) -> Any:
    """Approve a pending leave application.

    Args:
        leave_log_id: The leave log ID to approve. Get this from applied_leave_list.
        approver_comment: Optional comment from the approver.
    """
    return await _safe_post(
        f"leave-management/approve/{leave_log_id}",
        {"approverComment": approver_comment},
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
async def reject_leave(
    leave_log_id: str,
    cancellation_reason: str = "",
) -> Any:
    """Reject or cancel a leave application.

    Args:
        leave_log_id: The leave log ID to reject. Get this from applied_leave_list.
        cancellation_reason: Reason for rejection (shown to the employee).
    """
    return await _safe_post(
        f"leave-management/cancel/{leave_log_id}",
        {"cancellationReason": cancellation_reason},
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
async def adjust_leave(
    leave_log_id: str,
    leave_category_id: int,
    from_date: str,
    to_date: str,
    reason: str = "",
    is_half_day: bool = False,
    employee_identifier: str = "",
) -> Any:
    """Adjust an existing leave application (dates / category).

    Sends a multipart/form-data request with a `postBody` JSON field, as the
    Tipsoi adjust-leave endpoint requires.

    Args:
        leave_log_id: The leave log ID to adjust.
        leave_category_id: Numeric ID of the leave category for the adjusted leave.
        from_date: New start date, YYYY-MM-DD.
        to_date: New end date, YYYY-MM-DD.
        reason: Reason for the adjustment.
        is_half_day: True for a half-day leave.
        employee_identifier: Optional employee identifier (usually left blank).
    """
    post_body = {
        "leaveCategoryId": leave_category_id,
        "startDate": str(day_start_ms(from_date)),
        "endDate": str(day_end_ms(to_date)),
        "reason": reason,
        "employeeIdentifier": employee_identifier,
        "isHalfDay": is_half_day,
    }
    return await _safe_post_form(f"leave-management/adjust/{leave_log_id}", post_body)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    transport = os.environ.get("TIPSOI_TRANSPORT", "stdio").lower()

    if transport in ("http", "streamable-http", "streamable_http"):
        import uvicorn
        from contextlib import asynccontextmanager
        from starlette.applications import Starlette
        from starlette.routing import Mount

        from .oauth_routes import make_routes

        # Build combined app: OAuth routes + FastMCP
        fastmcp_app = mcp.streamable_http_app()

        # The StreamableHTTP session manager starts its task group inside the
        # FastMCP app's own lifespan. A parent Starlette does NOT run a mounted
        # sub-app's lifespan, so we must run the session manager ourselves here —
        # otherwise every /mcp request raises "Task group is not initialized".
        @asynccontextmanager
        async def lifespan(_app):
            async with mcp.session_manager.run():
                yield

        combined = Starlette(
            routes=[
                *make_routes(),
                Mount("/", app=fastmcp_app),
            ],
            lifespan=lifespan,
        )
        # Wrap with session middleware (reads Bearer token → sets ContextVar)
        app = _SessionMiddleware(combined)

        uvicorn.run(app, host="0.0.0.0", port=_port, log_level="info")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
