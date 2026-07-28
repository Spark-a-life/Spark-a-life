from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4


@dataclass(frozen=True)
class CapabilityToken:
    token_id: str
    subject: str
    tool: str
    scope: list[str]
    expires_at: str

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= datetime.fromisoformat(self.expires_at)


def issue_token(subject: str, tool: str, scope: list[str], ttl_seconds: int = 900) -> CapabilityToken:
    if not subject.strip():
        raise ValueError("subject must not be empty")
    if not tool.strip():
        raise ValueError("tool must not be empty")
    if not scope:
        raise ValueError("scope must not be empty")
    expires = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    return CapabilityToken(str(uuid4()), subject, tool, list(scope), expires.isoformat())
