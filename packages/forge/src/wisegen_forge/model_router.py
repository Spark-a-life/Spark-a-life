"""Model Router: models are replaceable execution resources, not the platform.

Selection is by capability class, risk tier, cost ceiling and availability, in
that order. The default adapter is deterministic and offline, so the whole
factory runs, and its tests pass, with no vendor key and no network. Swapping in
a hosted or local model changes fidelity, never control flow.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable

from . import mini_yaml
from .cost import CostGovernor

CAPABILITY_CLASSES = ("reasoning", "coding", "extraction", "classification", "summarisation")
RISK_TIERS = ("low", "medium", "high", "critical")


@dataclass
class ModelSpec:
    id: str
    provider: str
    capability_classes: list[str]
    max_risk_tier: str = "medium"
    sgd_per_1k_tokens: float = 0.0
    local: bool = False
    available: Callable[[], bool] = lambda: True


@dataclass
class Completion:
    text: str
    model_id: str
    provider: str
    tokens: int
    sgd: float
    deterministic: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "provider": self.provider,
            "tokens": self.tokens,
            "sgd": round(self.sgd, 4),
            "deterministic": self.deterministic,
        }


def _env_key(name: str) -> Callable[[], bool]:
    return lambda: bool(os.environ.get(name))


DEFAULT_CATALOGUE = [
    ModelSpec("forge-deterministic", "wisegen", list(CAPABILITY_CLASSES), "critical", 0.0, local=True),
    ModelSpec("ollama-local", "ollama", ["reasoning", "coding", "summarisation"], "high", 0.0, local=True,
              available=_env_key("FORGE_OLLAMA_HOST")),
    ModelSpec("anthropic-reasoning", "anthropic", ["reasoning", "extraction", "summarisation"], "critical", 0.021,
              available=_env_key("ANTHROPIC_API_KEY")),
    ModelSpec("anthropic-coding", "anthropic", ["coding"], "high", 0.021,
              available=_env_key("ANTHROPIC_API_KEY")),
]


@dataclass
class ModelRouter:
    governor: CostGovernor
    catalogue: list[ModelSpec] = field(default_factory=lambda: list(DEFAULT_CATALOGUE))
    prefer_local: bool = True
    routing_policy: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_policy_file(cls, governor: CostGovernor, path) -> "ModelRouter":
        document = mini_yaml.load_file(path) or {}
        router = cls(governor=governor)
        router.routing_policy = document
        router.prefer_local = bool(document.get("prefer_local", True))
        return router

    # ------------------------------------------------------------- routing
    def select(self, capability: str, risk_tier: str = "medium", sgd_ceiling: float | None = None) -> ModelSpec:
        if capability not in CAPABILITY_CLASSES:
            raise ValueError(f"unknown capability class: {capability}")
        if risk_tier not in RISK_TIERS:
            raise ValueError(f"unknown risk tier: {risk_tier}")

        candidates = [
            spec
            for spec in self.catalogue
            if capability in spec.capability_classes
            and RISK_TIERS.index(spec.max_risk_tier) >= RISK_TIERS.index(risk_tier)
            and spec.available()
            and (sgd_ceiling is None or spec.sgd_per_1k_tokens <= sgd_ceiling)
        ]
        if not candidates:
            raise RuntimeError(f"no model available for {capability} at risk tier {risk_tier}")
        candidates.sort(key=lambda spec: (0 if (self.prefer_local and spec.local) else 1, spec.sgd_per_1k_tokens))
        return candidates[0]

    def complete(
        self,
        actor: str,
        prompt: str,
        capability: str = "reasoning",
        risk_tier: str = "medium",
        schema: dict[str, Any] | None = None,
    ) -> Completion:
        spec = self.select(capability, risk_tier)
        tokens = max(32, len(prompt) // 4)
        sgd = spec.sgd_per_1k_tokens * tokens / 1000.0
        self.governor.charge(actor, tokens=tokens, sgd=sgd)
        text = self._invoke(spec, prompt, schema)
        return Completion(
            text=text,
            model_id=spec.id,
            provider=spec.provider,
            tokens=tokens,
            sgd=sgd,
            deterministic=spec.provider == "wisegen",
        )

    # ------------------------------------------------------------ adapters
    def _invoke(self, spec: ModelSpec, prompt: str, schema: dict[str, Any] | None) -> str:
        if spec.provider == "wisegen":
            return self._deterministic(prompt, schema)
        if spec.provider == "anthropic":  # pragma: no cover - requires credentials
            return self._anthropic(spec, prompt)
        if spec.provider == "ollama":  # pragma: no cover - requires local runtime
            return self._ollama(spec, prompt)
        raise RuntimeError(f"no adapter for provider {spec.provider}")

    @staticmethod
    def _deterministic(prompt: str, schema: dict[str, Any] | None) -> str:
        """Reproducible, offline stand-in.

        Returns a stable structured echo so that pipeline behaviour, evidence
        and tests are identical on every machine. Fidelity comes from a hosted
        or local model; correctness of the governance path does not depend on it.
        """
        seed = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]
        if schema:
            return json.dumps({"_seed": seed, **schema}, sort_keys=True)
        return f"[deterministic:{seed}] {prompt.strip().splitlines()[0][:160]}"

    @staticmethod
    def _anthropic(spec: ModelSpec, prompt: str) -> str:  # pragma: no cover
        import urllib.request

        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(
                {
                    "model": os.environ.get("FORGE_ANTHROPIC_MODEL", "claude-sonnet-4-6"),
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ).encode("utf-8"),
            headers={
                "content-type": "application/json",
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return "".join(block.get("text", "") for block in payload.get("content", []))

    @staticmethod
    def _ollama(spec: ModelSpec, prompt: str) -> str:  # pragma: no cover
        import urllib.request

        host = os.environ.get("FORGE_OLLAMA_HOST", "http://127.0.0.1:11434")
        request = urllib.request.Request(
            f"{host}/api/generate",
            data=json.dumps(
                {"model": os.environ.get("FORGE_OLLAMA_MODEL", "qwen2.5-coder"), "prompt": prompt, "stream": False}
            ).encode("utf-8"),
            headers={"content-type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8")).get("response", "")
