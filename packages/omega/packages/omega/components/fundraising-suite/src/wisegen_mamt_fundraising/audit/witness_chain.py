from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


class WitnessChain:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.previous_digest = self._last_digest()

    def _last_digest(self) -> str:
        if not self.path.exists():
            return "GENESIS"
        lines = [line for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return "GENESIS"
        try:
            return json.loads(lines[-1])["digest"]
        except (json.JSONDecodeError, KeyError) as exc:
            raise ValueError(f"Witness chain is corrupted: {self.path}") from exc

    def append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not event_type.strip():
            raise ValueError("event_type must not be empty")
        record: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "previous_digest": self.previous_digest,
            "payload": payload,
        }
        record["digest"] = sha256(
            json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.previous_digest = record["digest"]
        return record

    def verify(self) -> bool:
        previous = "GENESIS"
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            digest = record.pop("digest")
            if record["previous_digest"] != previous:
                return False
            expected = sha256(
                json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            if digest != expected:
                return False
            previous = digest
        return True
