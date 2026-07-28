from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json


class WitnessChain:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.previous = self._last_digest()

    def _last_digest(self):
        if not self.path.exists():
            return "GENESIS"
        lines = [x for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]
        return json.loads(lines[-1])["digest"] if lines else "GENESIS"

    def append(self, mission_id, event_type, actor, payload):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mission_id": mission_id,
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "previous_digest": self.previous,
        }
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        record["digest"] = hashlib.sha256(canonical.encode()).hexdigest()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
        self.previous = record["digest"]
        return record


def verify(path):
    prev = "GENESIS"
    count = 0
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        digest = record.pop("digest")
        if record.get("previous_digest") != prev:
            return False, count
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if hashlib.sha256(canonical.encode()).hexdigest() != digest:
            return False, count
        prev = digest
        count += 1
    return True, count
