"""Orchestration Engine: mission graphs, parallel eligibility, branchable execution.

Two properties distinguish this from linear delegation:

1. Dependency awareness. Agents may work in parallel only where the graph
   permits it, and the graph is derived from the approved specification.
2. Deliberation. Material decisions fan out into candidate branches which are
   separately costed, tested and witnessed, then resolved at the Captain's Gate
   rather than silently collapsed into the first generated answer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .domain import new_id, utc_now


class GraphError(ValueError):
    pass


@dataclass
class Task:
    id: str
    name: str
    agent: str
    depends_on: list[str] = field(default_factory=list)
    branch_of: str | None = None
    candidate_label: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    state: str = "pending"
    result: dict[str, Any] | None = None
    started_at: str | None = None
    finished_at: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "agent": self.agent,
            "depends_on": list(self.depends_on),
            "branch_of": self.branch_of,
            "candidate_label": self.candidate_label,
            "state": self.state,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "error": self.error,
        }


@dataclass
class MissionGraph:
    id: str = field(default_factory=lambda: new_id("msn"))
    tasks: dict[str, Task] = field(default_factory=dict)

    def add(self, name: str, agent: str, depends_on: list[str] | None = None, **payload: Any) -> Task:
        task = Task(id=new_id("task"), name=name, agent=agent, depends_on=list(depends_on or []), payload=payload)
        for parent in task.depends_on:
            if parent not in self.tasks:
                raise GraphError(f"task {name} depends on unknown task {parent}")
        self.tasks[task.id] = task
        return task

    def branch(self, base: Task, candidates: list[str], agent: str | None = None, **payload: Any) -> list[Task]:
        """Fork a decision into competing candidate implementations."""
        forks: list[Task] = []
        for label in candidates:
            task = Task(
                id=new_id("task"),
                name=f"{base.name} [{label}]",
                agent=agent or base.agent,
                depends_on=list(base.depends_on),
                branch_of=base.id,
                candidate_label=label,
                payload={**base.payload, **payload, "candidate": label},
            )
            self.tasks[task.id] = task
            forks.append(task)
        return forks

    # ------------------------------------------------------------- ordering
    def waves(self) -> list[list[Task]]:
        """Topologically ordered waves. Tasks inside one wave may run in parallel."""
        remaining = {task_id: set(task.depends_on) for task_id, task in self.tasks.items()}
        done: set[str] = set()
        waves: list[list[Task]] = []
        while remaining:
            ready = [task_id for task_id, deps in remaining.items() if deps <= done]
            if not ready:
                raise GraphError("dependency cycle detected in mission graph")
            waves.append([self.tasks[task_id] for task_id in sorted(ready)])
            for task_id in ready:
                done.add(task_id)
                remaining.pop(task_id)
        return waves

    def branch_groups(self) -> dict[str, list[Task]]:
        groups: dict[str, list[Task]] = {}
        for task in self.tasks.values():
            if task.branch_of:
                groups.setdefault(task.branch_of, []).append(task)
        return groups

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.id,
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "waves": [[task.id for task in wave] for wave in self.waves()],
        }


class Orchestrator:
    def __init__(self, runner: Callable[[Task], dict[str, Any]], on_event: Callable[[str, dict[str, Any]], None] | None = None) -> None:
        self.runner = runner
        self.on_event = on_event or (lambda event, payload: None)

    def execute(self, graph: MissionGraph, stop_on_error: bool = True) -> dict[str, Any]:
        summary = {"mission_id": graph.id, "waves": 0, "completed": 0, "failed": 0, "skipped": 0}
        failed: set[str] = set()

        for wave in graph.waves():
            summary["waves"] += 1
            for task in wave:
                if any(dep in failed for dep in task.depends_on):
                    task.state = "skipped"
                    summary["skipped"] += 1
                    self.on_event("task.skipped", task.to_dict())
                    continue
                task.state = "running"
                task.started_at = utc_now()
                self.on_event("task.started", task.to_dict())
                try:
                    task.result = self.runner(task)
                    task.state = "completed"
                    summary["completed"] += 1
                    self.on_event("task.completed", {**task.to_dict(), "result_keys": sorted((task.result or {}).keys())})
                except Exception as exc:  # noqa: BLE001 - failures are data, not crashes
                    task.state = "failed"
                    task.error = f"{type(exc).__name__}: {exc}"
                    failed.add(task.id)
                    summary["failed"] += 1
                    self.on_event("task.failed", task.to_dict())
                    if stop_on_error and not task.branch_of:
                        task.finished_at = utc_now()
                        summary["halted"] = True
                        return summary
                finally:
                    task.finished_at = utc_now()
        return summary
