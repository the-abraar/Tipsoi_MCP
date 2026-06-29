"""Per-key fixed-window rate limiter (in-memory, dependency-free)."""

from __future__ import annotations

import threading
import time


class RateLimiter:
    def __init__(self, window_seconds: int = 60):
        self.window = window_seconds
        self._state: dict[str, tuple[float, int]] = {}
        self._lock = threading.Lock()

    def check(self, key_id: str, limit: int) -> tuple[bool, int, float]:
        now = time.time()
        with self._lock:
            start, count = self._state.get(key_id, (now, 0))
            if now - start >= self.window:
                start, count = now, 0
            reset_in = self.window - (now - start)
            if count >= limit:
                return False, 0, reset_in
            count += 1
            self._state[key_id] = (start, count)
            return True, max(0, limit - count), reset_in
