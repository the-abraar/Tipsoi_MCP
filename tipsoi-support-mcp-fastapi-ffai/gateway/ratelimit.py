"""
Per-key fixed-window rate limiter (in-memory).

Simple and dependency-free: each key gets ``rpm`` requests per rolling 60s
window. In-memory state resets on restart and is per-process — for multi-worker
or multi-instance deployments, back this with Redis (see README).
"""

from __future__ import annotations

import threading
import time


class RateLimiter:
    def __init__(self, window_seconds: int = 60):
        self.window = window_seconds
        self._state: dict[str, tuple[float, int]] = {}  # key_id -> (window_start, count)
        self._lock = threading.Lock()

    def check(self, key_id: str, limit: int) -> tuple[bool, int, float]:
        """Try to consume one request for key_id.

        Returns (allowed, remaining, reset_in_seconds).
        """
        now = time.time()
        with self._lock:
            start, count = self._state.get(key_id, (now, 0))
            if now - start >= self.window:
                start, count = now, 0  # new window
            reset_in = self.window - (now - start)
            if count >= limit:
                return False, 0, reset_in
            count += 1
            self._state[key_id] = (start, count)
            return True, max(0, limit - count), reset_in
