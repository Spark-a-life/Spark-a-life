"""Tool Gateway: every external action is mediated, scoped and witnessed.

Design rules:
  * network denied by default (a tool must be explicitly network-capable and
    explicitly permitted by policy for the actor);
  * filesystem writes are confined to the run workspace, path traversal is
    rejected before the policy check, not after;
  * every invocation is charged to the Cost Governor and written to the
    Witness Chain, including refusals.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .cost import BudgetExceeded, CostGovernor
from .policy import PolicyEngine
from .witness import WitnessChain


class ToolDenied(PermissionError):
    pass


@dataclass
class Tool:
    name: str
    handler: Callable[..., Any]
    network: bool = False
    writes: bool = False
    cost_sgd: float = 0.0
    description: str = ""


class ToolGateway:
    def __init__(
        self,
        workspace: str | Path,
        policy: PolicyEngine,
        witness: WitnessChain,
        governor: CostGovernor,
        allow_network: bool = False,
    ) -> None:
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.policy = policy
        self.witness = witness
        self.governor = governor
        self.allow_network = allow_network
        self.tools: dict[str, Tool] = {}
        self._register_builtins()

    # ------------------------------------------------------------ registry
    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def _register_builtins(self) -> None:
        self.register(Tool("fs_write", self._fs_write, writes=True, description="write a file inside the run workspace"))
        self.register(Tool("fs_read", self._fs_read, description="read a file inside the run workspace"))
        self.register(Tool("fs_list", self._fs_list, description="list workspace files"))
        self.register(Tool("run_tests", self._run_tests, cost_sgd=0.01, description="execute a generated test module"))
        self.register(Tool("py_compile", self._py_compile, description="syntax-check generated Python"))

    # ------------------------------------------------------------- invoke
    def invoke(self, actor: str, tool_name: str, **kwargs: Any) -> Any:
        tool = self.tools.get(tool_name)
        if tool is None:
            self._refuse(actor, tool_name, "unknown tool")
            raise ToolDenied(f"unknown tool: {tool_name}")

        if tool.network and not self.allow_network:
            self._refuse(actor, tool_name, "network denied by default")
            raise ToolDenied(f"network tool {tool_name} denied: network is off by default")

        decision = self.policy.evaluate(
            {
                "actor": actor,
                "action": f"tool:{tool_name}",
                "resource": kwargs.get("path", "-"),
                "classification": kwargs.get("classification", "internal"),
            }
        )
        if not decision.allowed:
            self._refuse(actor, tool_name, decision.reason, decision.rule_id)
            raise ToolDenied(f"{actor} may not call {tool_name}: {decision.reason}")

        try:
            self.governor.charge(actor, tool_calls=1, sgd=tool.cost_sgd)
        except BudgetExceeded as exc:
            self._refuse(actor, tool_name, str(exc), "cost.governor")
            raise

        try:
            result = tool.handler(**kwargs)
        except ToolDenied as exc:
            # A sandbox violation raised inside the handler is still a refusal.
            # It must leave an evidence record, or the trail understates what
            # the agent attempted.
            self._refuse(actor, tool_name, str(exc), "gateway.sandbox")
            raise
        except Exception as exc:  # noqa: BLE001 - failures are evidence too
            self.witness.append(
                actor,
                "tool.failed",
                {"tool": tool_name, "error": f"{type(exc).__name__}: {exc}"},
            )
            raise
        self.witness.append(
            actor,
            "tool.invoked",
            {
                "tool": tool_name,
                "arguments": {k: _summarise(v) for k, v in kwargs.items()},
                "rule_id": decision.rule_id,
                "requires_approval": decision.requires_approval,
                "result": _summarise(result),
            },
        )
        return result

    def _refuse(self, actor: str, tool_name: str, reason: str, rule_id: str = "gateway") -> None:
        self.witness.append(
            actor,
            "tool.refused",
            {"tool": tool_name, "reason": reason, "rule_id": rule_id},
        )

    # ----------------------------------------------------------- built-ins
    def _resolve(self, path: str) -> Path:
        candidate = (self.workspace / path).resolve()
        if not str(candidate).startswith(str(self.workspace)):
            raise ToolDenied(f"path escapes the workspace sandbox: {path}")
        return candidate

    def _fs_write(self, path: str, content: str, **_: Any) -> dict[str, Any]:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"path": str(target.relative_to(self.workspace)), "bytes": len(content.encode("utf-8"))}

    def _fs_read(self, path: str, **_: Any) -> str:
        return self._resolve(path).read_text(encoding="utf-8")

    def _fs_list(self, path: str = ".", **_: Any) -> list[str]:
        base = self._resolve(path)
        return sorted(
            str(item.relative_to(self.workspace)) for item in base.rglob("*") if item.is_file()
        )

    def _py_compile(self, path: str, **_: Any) -> dict[str, Any]:
        target = self._resolve(path)
        try:
            compile(target.read_text(encoding="utf-8"), str(target), "exec")
            return {"ok": True, "path": path}
        except SyntaxError as exc:
            return {"ok": False, "path": path, "error": f"{exc.msg} (line {exc.lineno})"}

    def _run_tests(self, path: str, **_: Any) -> dict[str, Any]:
        target = self._resolve(path)
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(target.parent), "-p", target.name, "-v"],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(target.parent),
        )
        output = (proc.stdout + proc.stderr).strip()
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "summary": output.splitlines()[-1] if output else "no output",
        }


def _summarise(value: Any, limit: int = 220) -> Any:
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + f"... [{len(value)} chars]"
    if isinstance(value, (list, tuple)) and len(value) > 12:
        return list(value[:12]) + [f"... {len(value) - 12} more"]
    return value
