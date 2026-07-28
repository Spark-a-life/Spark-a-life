"""Deployment Service: releases move through signed manifests, never chat.

A deployment cannot exist without an approval reference, an artefact digest, a
named rollback target and an evidence bundle. The manifest is signed with an
HMAC so that a manifest altered between approval and apply is rejected at the
boundary.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .domain import digest, utc_now
from .witness import WitnessChain

ESTATES = ("managed-cloud", "customer-vpc", "on-premises", "local-workstation", "air-gapped")


class DeploymentRefused(PermissionError):
    pass


INITIAL_RELEASE = "none (initial release, no prior version to reverse to)"


def signing_key() -> bytes:
    return os.environ.get("FORGE_SIGNING_KEY", "development-key-not-for-production").encode("utf-8")


@dataclass
class ReleaseManifest:
    release: str
    target_estate: str
    environment: str
    artefact_digest: str
    approvals: list[str]
    rollback_release: str | None
    evidence_bundle: str
    created_at: str = field(default_factory=utc_now)
    signature: str = ""
    egress: str = "denied-by-default"

    def payload(self) -> dict[str, Any]:
        return {
            "release": self.release,
            "target_estate": self.target_estate,
            "environment": self.environment,
            "artefact_digest": self.artefact_digest,
            "approvals": self.approvals,
            "rollback_release": self.rollback_release,
            "evidence_bundle": self.evidence_bundle,
            "created_at": self.created_at,
            "egress": self.egress,
        }

    def sign(self) -> "ReleaseManifest":
        body = json.dumps(self.payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.signature = hmac.new(signing_key(), body, hashlib.sha256).hexdigest()
        return self

    def verify(self) -> bool:
        body = json.dumps(self.payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        expected = hmac.new(signing_key(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, self.signature)

    def to_dict(self) -> dict[str, Any]:
        return {**self.payload(), "signature": self.signature}


class DeploymentService:
    def __init__(self, workspace: str | Path, witness: WitnessChain) -> None:
        self.workspace = Path(workspace)
        self.witness = witness

    def previous_release(self, exclude: str | None = None) -> str | None:
        """The most recent prior release recorded in this run store, if any."""
        folder = self.workspace / "releases"
        if not folder.exists():
            return None
        names = sorted(
            path.name[: -len(".manifest.json")]
            for path in folder.glob("*.manifest.json")
            if path.name[: -len(".manifest.json")] != exclude
        )
        return names[-1] if names else None

    def prepare(
        self,
        release: str,
        target_estate: str,
        environment: str,
        artefact_root: str | Path,
        approvals: list[str],
        evidence_bundle: str,
        rollback_release: str | None = None,
    ) -> ReleaseManifest:
        if target_estate not in ESTATES:
            raise ValueError(f"unknown estate: {target_estate}")
        if not approvals:
            self.witness.append("deployment-service", "deployment.refused", {"release": release, "reason": "no approval reference"})
            raise DeploymentRefused("deployment requires at least one approval reference")

        # Reversible autonomy: a release without a named way back is refused.
        # The only exception is a genuine first release, and it must say so.
        previous = self.previous_release(exclude=release)
        if not rollback_release:
            if previous:
                self.witness.append(
                    "deployment-service",
                    "deployment.refused",
                    {"release": release, "reason": "no rollback target while a prior release exists", "previous": previous},
                )
                raise DeploymentRefused(
                    f"release {release} names no rollback target although {previous} is available"
                )
            rollback_release = INITIAL_RELEASE

        manifest = ReleaseManifest(
            release=release,
            target_estate=target_estate,
            environment=environment,
            artefact_digest=self.digest_tree(artefact_root),
            approvals=list(approvals),
            rollback_release=rollback_release,
            evidence_bundle=evidence_bundle,
        ).sign()

        path = self.workspace / "releases" / f"{release}.manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")
        self.witness.append("deployment-service", "deployment.prepared", manifest.to_dict())
        return manifest

    def apply(self, manifest: ReleaseManifest, dry_run: bool = True) -> dict[str, Any]:
        if not manifest.verify():
            self.witness.append("deployment-service", "deployment.refused", {"release": manifest.release, "reason": "signature mismatch"})
            raise DeploymentRefused("manifest signature does not verify: refusing to apply")
        outcome = {
            "release": manifest.release,
            "estate": manifest.target_estate,
            "environment": manifest.environment,
            "mode": "dry-run" if dry_run else "applied",
            "at": utc_now(),
            "rollback_to": manifest.rollback_release,
            "reversible": manifest.rollback_release != INITIAL_RELEASE,
            "manifest": manifest.to_dict(),
            "runbook": self.runbook(manifest),
        }
        self.witness.append("deployment-service", "deployment.applied" if not dry_run else "deployment.dry_run", outcome)
        return outcome

    def rollback(self, manifest: ReleaseManifest, reason: str) -> dict[str, Any]:
        if not manifest.rollback_release:
            raise DeploymentRefused("no rollback target recorded for this release")
        outcome = {"from": manifest.release, "to": manifest.rollback_release, "reason": reason, "at": utc_now()}
        self.witness.append("deployment-service", "deployment.rolled_back", outcome)
        return outcome

    # ------------------------------------------------------------ helpers
    @staticmethod
    def digest_tree(root: str | Path) -> str:
        base = Path(root)
        entries = []
        for path in sorted(base.rglob("*")):
            if path.is_file():
                entries.append(
                    {"path": str(path.relative_to(base)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                )
        return digest(entries)

    @staticmethod
    def runbook(manifest: ReleaseManifest) -> list[str]:
        return [
            f"1. Verify manifest signature for release {manifest.release}.",
            f"2. Confirm approval reference(s) {', '.join(manifest.approvals)} exist in the witness chain.",
            "3. Restore or provision the data store, then apply migrations forward only.",
            f"4. Deploy the artefact digest {manifest.artefact_digest[:23]}... to {manifest.target_estate}.",
            "5. Run the generated test suite against the deployed instance before opening traffic.",
            "6. Confirm /health reports an intact audit chain.",
            f"7. If any check fails, roll back to {manifest.rollback_release or 'the previous release'} within 10 minutes.",
        ]
