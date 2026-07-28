from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json

class WitnessChain:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.previous_digest = self._last_digest()

    def _last_digest(self) -> str:
        if not self.path.exists():
            return 'GENESIS'
        lines = [line for line in self.path.read_text(encoding='utf-8').splitlines() if line.strip()]
        if not lines:
            return 'GENESIS'
        return json.loads(lines[-1])['digest']

    def append(self, event_type: str, payload: dict) -> dict:
        record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': event_type,
            'previous_digest': self.previous_digest,
            'payload': payload,
        }
        record['digest'] = sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
        with self.path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        self.previous_digest = record['digest']
        return record
