"""
Tipsoi MCP Server — Phase 1 (READ-ONLY)

Exposes a curated set of read-only Tipsoi HRM endpoints as MCP tools so that
Claude (or any MCP-capable client) can answer questions about employees,
attendance, leave, overtime, notifications, and org setup — without being able
to modify anything.

DESIGN NOTES
------------
- Every tool here is a GET. No create/update/delete endpoints are registered.
  This is the entire safety story for Phase 1: the server is physically
  incapable of taking a mutating action.
- Authentication uses ONE service account (env vars). True per-user OAuth is a
  Phase 2 concern. Treat the configured account's permissions as the ceiling of
  what the assistant can read.
- Date inputs are plain YYYY-MM-DD; conversion to Tipsoi's epoch-ms happens
  server-side.

Run modes:
    python -m tipsoi_mcp.server            # stdio (local testing / Claude Desktop)
    TIPSOI_TRANSPORT=http python -m tipsoi_mcp.server   # streamable HTTP (remote connector)
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .client import TipsoiClient, TipsoiAPIError, TipsoiAuthError
from .dates import day_start_ms, day_end_ms, month_range_ms

mcp = FastMCP("tipsoi")
_client = TipsoiClient()

_ro = ToolAnnotations(readOnlyHint=True)


# ---------------------------------------------------------------------------
# internal helpers
# ---------------------------------------------------------------------------

def _office_id(office_id: str | None) -> str:
    oid = office_id or _client.default_office_id
    if not oid:
        raise ValueError(
            "office_id is required. Pass it explicitly or set TIPSOI_OFFICE_ID."
        )
    return oid


async def _safe_get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Wrap client.get so tool callers receive readable error strings, not stack traces."""
    try:
        return await _client.get(path, params)
    except TipsoiAuthError as e:
        return {"error": "authentication_failed", "detail": str(e)}
    except TipsoiAPIError as e:
        return {"error": "api_error", "status": e.status, "detail": e.detail}
    except Exception as e:  # noqa: BLE001
        return {"error": "unexpected", "detail": repr(e)}


# ---------------------------------------------------------------------------
# Employees
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

    Returns the raw employee list payload (id, name, department, etc.).
    Use this to resolve an employee's name to their numeric ID before calling
    employee- or report-specific tools.
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


# ---------------------------------------------------------------------------
# Attendance reports
# ---------------------------------------------------------------------------

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
        office_id: Tipsoi office ID. Falls back to TIPSOI_OFFICE_ID if omitted.
        employee_name: Optional name filter (substring).
        status: 1 = active employees.
        per_page / page_number: Pagination.
    """
    start, end = month_range_ms(year, month)
    return await _safe_get(
        "attendance",
        {
            "officeId": _office_id(office_id),
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
        office_id: Falls back to TIPSOI_OFFICE_ID if omitted.
        employee_name: Optional name filter.
        status: 1 = active employees.
        per_page: Pagination size.
    """
    return await _safe_get(
        "attendance/daily-summary",
        {
            "officeId": _office_id(office_id),
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
        office_id: Falls back to TIPSOI_OFFICE_ID if omitted.
        absent_type: Tipsoi absent classification code (default 1).
        per_page: Pagination size.
    """
    return await _safe_get(
        "attendance/daily-absent",
        {
            "absentType": absent_type,
            "officeId": _office_id(office_id),
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
        office_id: Falls back to TIPSOI_OFFICE_ID.
        company_id: Falls back to TIPSOI_COMPANY_ID.
        per_page: Pagination size.
    """
    return await _safe_get(
        "attendance/leave-late-absent",
        {
            "companyId": company_id or _client.default_company_id,
            "officeId": _office_id(office_id),
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
        office_id: Falls back to TIPSOI_OFFICE_ID.
        per_page: Pagination size.
    """
    return await _safe_get(
        "mobile-punch",
        {
            "dinnerFilter": -1,
            "lunchFilter": -1,
            "officeId": _office_id(office_id),
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


# ---------------------------------------------------------------------------
# Leave
# ---------------------------------------------------------------------------

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
        office_id: Falls back to TIPSOI_OFFICE_ID.
        per_page: Pagination size.
    """
    return await _safe_get(
        "attendance/leave-balance",
        {
            "officeId": _office_id(office_id),
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
    """List applied leave requests and their statuses (READ-ONLY view).

    Args:
        keyword: Optional search term.
        statuses: List of status codes to include (e.g. [0,1] for pending+approved).
                  Defaults to [0, 1].
        page: Zero-based page index.
        count: Page size.

    NOTE: This only *reads* leave applications. Applying/approving/rejecting
    leave is a write action and is intentionally NOT available in Phase 1.
    """
    params: list[tuple[str, Any]] = [
        ("keyword", keyword),
        ("page", page),
        ("count", count),
    ]
    for s in (statuses if statuses is not None else [0, 1]):
        params.append(("status", s))
    from urllib.parse import urlencode
    qs = urlencode(params)
    return await _safe_get(f"leave-management/leave-history/?{qs}")


# ---------------------------------------------------------------------------
# Overtime
# ---------------------------------------------------------------------------

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
        office_id: Falls back to TIPSOI_OFFICE_ID.
        company_id: Falls back to TIPSOI_COMPANY_ID.
        per_page: Pagination size.
    """
    start, end = month_range_ms(year, month)
    return await _safe_get(
        "overtime/report",
        {
            "companyId": company_id or _client.default_company_id,
            "officeId": _office_id(office_id),
            "employeeName": "",
            "order": "asc",
            "pageNumber": 0,
            "perPage": per_page,
            "sortKey": "reportPosition",
            "from": start,
            "to": end,
        },
    )


# ---------------------------------------------------------------------------
# Org setup / reference data
# ---------------------------------------------------------------------------

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
# entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    transport = os.environ.get("TIPSOI_TRANSPORT", "stdio").lower()
    if transport in ("http", "streamable-http", "streamable_http"):
        port = int(os.environ.get("PORT", 8000))
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
