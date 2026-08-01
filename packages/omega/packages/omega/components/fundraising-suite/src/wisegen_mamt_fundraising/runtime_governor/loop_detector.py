from __future__ import annotations

from collections import deque
from hashlib import sha256


class LoopDetector:
    def __init__(self, window: int = 5, maximum_repeats: int = 3):
        if window < 2:
            raise ValueError("window must be at least 2")
        if maximum_repeats < 2:
            raise ValueError("maximum_repeats must be at least 2")
        self.window = window
        self.maximum_repeats = maximum_repeats
        self._seen: deque[str] = deque(maxlen=window)

    def observe(self, action_signature: str) -> bool:
        digest = sha256(action_signature.strip().lower().encode("utf-8")).hexdigest()
        self._seen.append(digest)
        return list(self._seen).count(digest) >= self.maximum_repeats
