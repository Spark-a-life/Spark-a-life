"""Canonical durable objects for WiseGen Forge.

The architecture revolves around durable objects, not chat history. Every object
carries the same governance envelope so that provenance, policy and retention
questions can be answered about anything the factory produces.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "0.1.0"

CLASSIFICATIONS = ("public", "internal", "confidential", "restricted")

LIFECYCLE_STATES = (
    "draft",
    "proposed",
    "approved",
    "executing",
    "verified",
    "released",
    "superseded",
    "rejected",
    "archived",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def digest(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class Envelope:
    """Governance envelope carried by every canonical object."""

    id: str
    kind: str
    version: str = "1.0.0"
    owner: str = "captain"
    created_at: str = field(default_factory=utc_now)
    created_from: str = "unspecified"
    classification: str = "internal"
    lifecycle_state: str = "draft"
    evidence_refs: list[str] = field(default_factory=list)
    policy_refs: list[str] = field(default_factory=list)
    retention_rule: str = "retain-7y"
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.classification not in CLASSIFICATIONS:
            raise ValueError(f"unknown classification: {self.classification}")
        if self.lifecycle_state not in LIFECYCLE_STATES:
            raise ValueError(f"unknown lifecycle state: {self.lifecycle_state}")


@dataclass
class ForgeObject:
    envelope: Envelope
    body: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, kind: str, body: dict[str, Any], **envelope_kwargs: Any) -> "ForgeObject":
        prefix = "".join(part[0] for part in kind.split("_"))[:4].lower() or "obj"
        envelope = Envelope(id=new_id(prefix), kind=kind, **envelope_kwargs)
        return cls(envelope=envelope, body=body)

    @property
    def id(self) -> str:
        return self.envelope.id

    @property
    def kind(self) -> str:
        return self.envelope.kind

    def to_dict(self) -> dict[str, Any]:
        return {"envelope": asdict(self.envelope), "body": self.body}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ForgeObject":
        return cls(envelope=Envelope(**data["envelope"]), body=data["body"])

    def digest(self) -> str:
        return digest(self.to_dict())

    def transition(self, state: str) -> "ForgeObject":
        """Return a new object at the requested lifecycle state.

        Transitions never mutate in place. The prior version stays intact so a
        reviewer can reconstruct what an object looked like when a decision was
        taken on it. The minor version is bumped on each transition.
        """
        if state not in LIFECYCLE_STATES:
            raise ValueError(f"unknown lifecycle state: {state}")
        envelope = Envelope(**asdict(self.envelope))
        envelope.lifecycle_state = state
        major, minor, patch = (envelope.version.split(".") + ["0", "0"])[:3]
        envelope.version = f"{major}.{int(minor) + 1}.{patch}"
        return ForgeObject(envelope=envelope, body=json.loads(json.dumps(self.body, default=str)))


OBJECT_KINDS = (
    "organisation",
    "workspace",
    "user",
    "role",
    "project",
    "mission",
    "specification",
    "decision",
    "task",
    "execution",
    "agent",
    "capability",
    "tool",
    "policy",
    "artefact",
    "evidence",
    "evaluation",
    "approval",
    "release",
    "deployment",
    "incident",
    "learning_record",
)
