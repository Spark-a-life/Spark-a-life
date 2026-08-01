from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from wisegen_witl.storage.json_store import append_jsonl


def canonical_hash(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class WitnessChain:
    def __init__(self, log_path: str | Path = "audit/witness-chain.jsonl"):
        self.log_path = Path(log_path)

    def record(self, event_type: str, payload: Dict[str, Any]) -> str:
        event = {"event_type": event_type, "payload": payload}
        event_hash = canonical_hash(event)
        append_jsonl(self.log_path, {"hash": event_hash, **event})
        return event_hash

    def read(self) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []
        rows: List[Dict[str, Any]] = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows
