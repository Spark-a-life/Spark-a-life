"""Policy Engine: policy-as-code decisions for every consequential action.

Policies are layered, and the most restrictive layer wins:

    constitutional  >  organisational  >  project

A constitutional deny can never be overridden by a lower layer. This is the
machine-readable form of the Captain Rule: AI proposes, human decides, and the
boundary of what AI may propose to do unattended is written down, versioned and
testable rather than held in a prompt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import mini_yaml

LAYER_ORDER = ("constitutional", "organisational", "project")


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    layer: str
    rule_id: str
    requires_approval: bool = False
    conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "layer": self.layer,
            "rule_id": self.rule_id,
            "requires_approval": self.requires_approval,
            "conditions": self.conditions,
        }


class PolicyEngine:
    def __init__(self, policy_root: str | Path) -> None:
        self.root = Path(policy_root)
        self.layers: dict[str, list[dict[str, Any]]] = {layer: [] for layer in LAYER_ORDER}
        self.load()

    def load(self) -> None:
        """Load every policy document under the root, honouring its declared layer.

        Directory names are a convenience for humans. The authoritative layer is
        the `layer:` field inside the document, defaulting to organisational.
        Routing configuration is not a policy set and is skipped here.
        """
        for path in sorted(self.root.rglob("*.yaml")):
            if "model-routing" in path.parts:
                continue
            document = mini_yaml.load_file(path) or {}
            if not isinstance(document, dict):
                continue
            layer = str(document.get("layer") or _layer_from_path(path, self.root) or "organisational")
            if layer not in self.layers:
                layer = "organisational"
            for rule in document.get("rules", []) or []:
                rule = dict(rule)
                rule.setdefault("id", f"{layer}.{path.stem}.{len(self.layers[layer])}")
                rule["_source"] = str(path.relative_to(self.root))
                self.layers[layer].append(rule)

    # ------------------------------------------------------------------ api
    @property
    def rules(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for layer in LAYER_ORDER:
            out.extend(self.layers[layer])
        return out

    def evaluate(self, request: dict[str, Any]) -> PolicyDecision:
        """Evaluate an action request against every layer.

        A request looks like::

            {"actor": "gaie.backend-engineer", "action": "deploy_production",
             "resource": "customer-vpc", "classification": "restricted"}
        """
        approval_conditions: list[str] = []
        requires_approval = False
        matched_allow: PolicyDecision | None = None

        for layer in LAYER_ORDER:
            for rule in self.layers[layer]:
                if not self._matches(rule, request):
                    continue
                effect = str(rule.get("effect", "deny")).lower()
                if effect == "deny":
                    return PolicyDecision(
                        allowed=False,
                        reason=str(rule.get("reason", "denied by policy")),
                        layer=layer,
                        rule_id=str(rule["id"]),
                    )
                if effect == "require_approval":
                    requires_approval = True
                    approval_conditions.append(str(rule.get("reason", rule["id"])))
                    matched_allow = matched_allow or PolicyDecision(
                        allowed=True,
                        reason=str(rule.get("reason", "permitted subject to approval")),
                        layer=layer,
                        rule_id=str(rule["id"]),
                    )
                elif effect == "allow" and matched_allow is None:
                    matched_allow = PolicyDecision(
                        allowed=True,
                        reason=str(rule.get("reason", "permitted by policy")),
                        layer=layer,
                        rule_id=str(rule["id"]),
                    )

        if matched_allow is None:
            return PolicyDecision(
                allowed=False,
                reason="no rule permits this action (default deny)",
                layer="constitutional",
                rule_id="default.deny",
            )
        matched_allow.requires_approval = requires_approval
        matched_allow.conditions = approval_conditions
        return matched_allow

    # ------------------------------------------------------------- matching
    @staticmethod
    def _matches(rule: dict[str, Any], request: dict[str, Any]) -> bool:
        match = rule.get("match") or {}
        if not isinstance(match, dict):
            return False
        for key, expected in match.items():
            actual = request.get(key)
            if expected in ("*", None):
                continue
            if isinstance(expected, list):
                if actual not in expected and "*" not in expected:
                    return False
            elif str(expected) != str(actual):
                return False
        return True


def _layer_from_path(path: Path, root: Path) -> str | None:
    relative = path.relative_to(root).parts
    return relative[0] if relative and relative[0] in LAYER_ORDER else None
