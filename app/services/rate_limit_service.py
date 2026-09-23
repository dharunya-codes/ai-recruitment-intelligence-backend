from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import RLock


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._requests: dict[tuple[str, str], deque[float]] = defaultdict(deque)
        self._lock = RLock()

    def allow(self, identity: str, bucket: str, limit: int, window_seconds: int = 60) -> bool:
        now = time.monotonic()
        cutoff = now - window_seconds
        key = (identity, bucket)
        with self._lock:
            requests = self._requests[key]
            while requests and requests[0] <= cutoff:
                requests.popleft()
            if len(requests) >= limit:
                return False
            requests.append(now)
            return True

    def clear(self) -> None:
        with self._lock:
            self._requests.clear()


rate_limiter = InMemoryRateLimiter()