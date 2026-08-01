"""Witness Service: append-only, tamper-evident execution evidence.

Compatible with the wisegen-witness record shape: every entry binds its own
payload digest to the digest of the entry before it, so any edit, reorder or
deletion inside the chain is detectable by replay.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .domain import digest, utc_now

GENESIS = "sha256:" + "0" * 64


@dataclass
class WitnessEntry:
    seq: int
    at: str
    actor: str
    event: str
    payload: dict[str, Any]
    payload_digest: str
    prev_digest: str
    entry_digest: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "at": self.at,
            "actor": self.actor,
            "event": self.event,
            "payload": self.payload,
            "payload_digest": self.payload_digest,
            "prev_digest": self.prev_digest,
            "entry_digest": self.entry_digest,
        }


class WitnessChain:
    """Append-only hash chain persisted as JSON Lines."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------------- read
    def entries(self) -> list[WitnessEntry]:
        if not self.path.exists():
            return []
        rows: list[WitnessEntry] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(WitnessEntry(**json.loads(line)))
        return rows

    def head(self) -> str:
        rows = self.entries()
        return rows[-1].entry_digest if rows else GENESIS

    def __len__(self) -> int:
        return len(self.entries())

    # ---------------------------------------------------------------- write
    def append(self, actor: str, event: str, payload: dict[str, Any]) -> WitnessEntry:
        rows = self.entries()
        prev = rows[-1].entry_digest if rows else GENESIS
        seq = len(rows) + 1
        at = utc_now()
        payload_digest = digest(payload)
        entry_digest = digest(
            {
                "seq": seq,
                "at": at,
                "actor": actor,
                "event": event,
                "payload_digest": payload_digest,
                "prev_digest": prev,
            }
        )
        entry = WitnessEntry(
            seq=seq,
            at=at,
            actor=actor,
            event=event,
            payload=payload,
            payload_digest=payload_digest,
            prev_digest=prev,
            entry_digest=entry_digest,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.to_dict(), sort_keys=True) + "\n")
        return entry

    # --------------------------------------------------------------- verify
    def verify(self) -> dict[str, Any]:
        prev = GENESIS
        problems: list[str] = []
        rows = self.entries()
        for index, entry in enumerate(rows, start=1):
            if entry.seq != index:
                problems.append(f"entry {index}: sequence break (found {entry.seq})")
            if entry.prev_digest != prev:
                problems.append(f"entry {index}: broken link to predecessor")
            if entry.payload_digest != digest(entry.payload):
                problems.append(f"entry {index}: payload altered after sealing")
            recomputed = digest(
                {
                    "seq": entry.seq,
                    "at": entry.at,
                    "actor": entry.actor,
                    "event": entry.event,
                    "payload_digest": entry.payload_digest,
                    "prev_digest": entry.prev_digest,
                }
            )
            if recomputed != entry.entry_digest:
                problems.append(f"entry {index}: entry digest mismatch")
            prev = entry.entry_digest
        return {"ok": not problems, "length": len(rows), "head": prev, "problems": problems}

    def events(self, event: str) -> Iterable[WitnessEntry]:
        return (entry for entry in self.entries() if entry.event == event)
