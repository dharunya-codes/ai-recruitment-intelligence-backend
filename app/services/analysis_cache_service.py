from __future__ import annotations

import copy
import hashlib
import json
from collections import OrderedDict
from collections.abc import Callable
from threading import RLock
from typing import Any


ANALYSIS_CACHE_VERSION = "phase17-v1"
MAX_CACHE_ENTRIES = 128


class AnalysisCache:
    def __init__(self, max_entries: int = MAX_CACHE_ENTRIES) -> None:
        self._entries: OrderedDict[str, Any] = OrderedDict()
        self._lock = RLock()
        self.max_entries = max_entries
        self.hits = 0
        self.misses = 0

    def get_or_compute(self, key: str, compute: Callable[[], Any]) -> Any:
        with self._lock:
            if key in self._entries:
                self.hits += 1
                self._entries.move_to_end(key)
                return copy.deepcopy(self._entries[key])
            self.misses += 1
        value = compute()
        with self._lock:
            self._entries[key] = copy.deepcopy(value)
            self._entries.move_to_end(key)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)
        return copy.deepcopy(value)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self.hits = 0
            self.misses = 0

    def stats(self) -> dict[str, int]:
        with self._lock:
            return {"entries": len(self._entries), "hits": self.hits, "misses": self.misses}


analysis_cache = AnalysisCache()


def make_analysis_cache_key(
    *,
    owner_scope: str | int,
    resume_text: str,
    job_context: Any,
    target_role: str | None,
    config_version: str = ANALYSIS_CACHE_VERSION,
) -> str:
    payload = {
        "owner_scope": str(owner_scope),
        "resume_text": resume_text,
        "job_context": job_context,
        "target_role": target_role or "",
        "config_version": config_version,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()