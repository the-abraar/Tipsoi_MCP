"""
Date helpers.

Tipsoi report endpoints expect `from`/`to` as Unix epoch MILLISECONDS.
We never want the LLM to compute these. Tools accept plain YYYY-MM-DD strings
and convert here, using a configurable timezone (default Asia/Dhaka, UTC+6).

`from` is taken as start-of-day (00:00:00.000) and `to` as end-of-day
(23:59:59.999) in the configured timezone, matching the collection's examples.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

# Bangladesh Standard Time is UTC+6 with no DST.
def _tz() -> timezone:
    offset_hours = float(os.environ.get("TIPSOI_TZ_OFFSET_HOURS", "6"))
    return timezone(timedelta(hours=offset_hours))


def day_start_ms(date_str: str) -> int:
    """YYYY-MM-DD -> epoch ms at 00:00:00.000 local time."""
    d = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=_tz()
    )
    return int(d.timestamp() * 1000)


def day_end_ms(date_str: str) -> int:
    """YYYY-MM-DD -> epoch ms at 23:59:59.999 local time."""
    d = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=23, minute=59, second=59, microsecond=999000, tzinfo=_tz()
    )
    return int(d.timestamp() * 1000)


def month_range_ms(year: int, month: int) -> tuple[int, int]:
    """(year, month) -> (start_ms, end_ms) covering the whole month, local time."""
    start = datetime(year, month, 1, 0, 0, 0, tzinfo=_tz())
    if month == 12:
        nxt = datetime(year + 1, 1, 1, tzinfo=_tz())
    else:
        nxt = datetime(year, month + 1, 1, tzinfo=_tz())
    end = nxt - timedelta(milliseconds=1)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000)
