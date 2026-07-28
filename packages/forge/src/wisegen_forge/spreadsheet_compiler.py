"""Spreadsheet Compiler: the practical entry point into real organisations.

Most institutions do not start with clean APIs. They start with spreadsheets,
email threads and undocumented practice. This module converts a delimited file
into the four artefacts a governed application actually needs:

    schema  ->  data classification  ->  discovered workflow  ->  quality report

Field classification is conservative by design. When a column looks like it may
carry personal data, it is classified restricted and the generated application
masks it unless a role holds an explicit need-to-know.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)
PHONE_SG = re.compile(r"^\+?\d[\d\s\-]{6,14}$")
NRIC = re.compile(r"^[STFGM]\d{7}[A-Z]$", re.I)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_SLASH = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}$")
MONEY = re.compile(r"^-?(sgd|s\$|\$)?\s?\d+(\.\d{1,2})?$", re.I)

PII_NAME_HINTS = ("name", "email", "phone", "mobile", "nric", "fin", "passport", "address", "dob", "birth", "salary", "bank")
STATUS_HINTS = ("status", "stage", "state", "phase", "progress", "outcome")
OWNER_HINTS = ("owner", "manager", "approver", "assigned", "supervisor", "reviewer")
DATE_HINTS = ("date", "due", "start", "end", "joined", "completed")


@dataclass
class Column:
    name: str
    slug: str
    type: str
    nullable: bool
    classification: str
    distinct: int
    sample: list[str]
    role: str = "attribute"
    enum_values: list[str] = field(default_factory=list)
    quality_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "slug": self.slug,
            "type": self.type,
            "nullable": self.nullable,
            "classification": self.classification,
            "distinct": self.distinct,
            "role": self.role,
            "enum_values": self.enum_values,
            "quality_flags": self.quality_flags,
            "sample": self.sample[:3],
        }


@dataclass
class SheetModel:
    entity: str
    source: str
    row_count: int
    columns: list[Column]
    workflow: dict[str, Any]
    quality: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity": self.entity,
            "source": self.source,
            "row_count": self.row_count,
            "columns": [column.to_dict() for column in self.columns],
            "workflow": self.workflow,
            "quality": self.quality,
        }

    @property
    def status_column(self) -> Column | None:
        for column in self.columns:
            if column.role == "status":
                return column
        return None

    @property
    def identity_column(self) -> Column:
        for column in self.columns:
            if column.role == "identifier":
                return column
        return self.columns[0]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "column"


def _infer_type(values: list[str]) -> str:
    populated = [value for value in values if value.strip()]
    if not populated:
        return "text"
    checks = [
        ("email", lambda v: bool(EMAIL.match(v))),
        ("national_id", lambda v: bool(NRIC.match(v))),
        ("phone", lambda v: bool(PHONE_SG.match(v))),
        ("date", lambda v: bool(DATE.match(v) or DATE_SLASH.match(v))),
        ("money", lambda v: bool(MONEY.match(v))),
        ("integer", lambda v: v.lstrip("-").isdigit()),
        ("boolean", lambda v: v.strip().lower() in ("true", "false", "yes", "no", "y", "n", "0", "1")),
    ]
    for name, test in checks:
        if all(test(value.strip()) for value in populated):
            return name
    try:
        for value in populated:
            float(value)
        return "decimal"
    except ValueError:
        pass
    return "text"


def _classify(name: str, inferred_type: str) -> str:
    lowered = name.lower()
    if inferred_type in ("national_id",) or any(hint in lowered for hint in ("nric", "fin", "passport", "bank", "salary")):
        return "restricted"
    if inferred_type in ("email", "phone") or any(hint in lowered for hint in PII_NAME_HINTS):
        return "confidential"
    return "internal"


def _role(name: str, index: int, distinct: int, row_count: int, inferred_type: str) -> str:
    lowered = name.lower()
    if index == 0 and distinct == row_count and row_count > 0:
        return "identifier"
    if "id" == lowered or lowered.endswith("_id") or lowered.endswith(" id"):
        return "identifier"
    if any(hint in lowered for hint in STATUS_HINTS):
        return "status"
    if any(hint in lowered for hint in OWNER_HINTS):
        return "owner"
    if inferred_type == "date" or any(hint in lowered for hint in DATE_HINTS):
        return "temporal"
    return "attribute"


def compile_sheet(path: str | Path, entity: str | None = None) -> SheetModel:
    source = Path(path)
    with source.open(newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(handle, dialect=dialect))

    if not rows:
        raise ValueError(f"{source} contains no data rows")

    headers = list(rows[0].keys())
    row_count = len(rows)
    columns: list[Column] = []

    for index, header in enumerate(headers):
        values = [(row.get(header) or "") for row in rows]
        populated = [value for value in values if value.strip()]
        inferred = _infer_type(values)
        counter = Counter(value.strip() for value in populated)
        distinct = len(counter)
        column = Column(
            name=header,
            slug=slugify(header),
            type=inferred,
            nullable=len(populated) < row_count,
            classification=_classify(header, inferred),
            distinct=distinct,
            sample=[value for value in populated[:5]],
        )
        column.role = _role(header, index, distinct, row_count, inferred)
        if inferred == "text" and 0 < distinct <= max(2, row_count // 3) and distinct <= 12:
            column.enum_values = sorted(counter)
        if column.nullable and column.role in ("identifier", "status"):
            column.quality_flags.append("missing values in a load-bearing column")
        casings = {value.strip().lower(): value.strip() for value in populated}
        if column.enum_values and len(casings) < distinct:
            column.quality_flags.append("inconsistent casing across categorical values")
        columns.append(column)

    workflow = _discover_workflow(columns, rows)
    quality = _quality_report(columns, rows, headers)
    return SheetModel(
        entity=entity or slugify(source.stem),
        source=source.name,
        row_count=row_count,
        columns=columns,
        workflow=workflow,
        quality=quality,
    )


def _discover_workflow(columns: list[Column], rows: list[dict[str, str]]) -> dict[str, Any]:
    status = next((column for column in columns if column.role == "status"), None)
    if status is None:
        return {"discovered": False, "reason": "no status-like column found", "states": [], "transitions": []}

    observed = [str(row.get(status.name, "")).strip() for row in rows]
    states = [state for state in dict.fromkeys(observed) if state]
    terminal = [state for state in states if re.search(r"complete|done|closed|approved|rejected|exit", state, re.I)]
    initial = [state for state in states if re.search(r"new|pending|not started|draft|open", state, re.I)] or states[:1]
    middle = [state for state in states if state not in terminal and state not in initial]

    ordered = initial + middle + terminal
    transitions = [
        {"from": ordered[i], "to": ordered[i + 1], "requires_approval": ordered[i + 1] in terminal}
        for i in range(len(ordered) - 1)
    ]
    return {
        "discovered": True,
        "status_column": status.slug,
        "states": ordered,
        "initial_states": initial,
        "terminal_states": terminal,
        "transitions": transitions,
        "note": "Transitions inferred from observed values. Confirm with the process owner before release.",
    }


def _quality_report(columns: list[Column], rows: list[dict[str, str]], headers: list[str]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    total = len(rows)

    for column in columns:
        blanks = sum(1 for row in rows if not str(row.get(column.name, "")).strip())
        if blanks:
            issues.append(
                {
                    "column": column.name,
                    "issue": "missing values",
                    "count": blanks,
                    "share": round(blanks / total, 3),
                    "severity": "high" if column.role in ("identifier", "status") else "medium",
                }
            )
        for flag in column.quality_flags:
            issues.append({"column": column.name, "issue": flag, "count": None, "severity": "medium"})

    identity = next((column for column in columns if column.role == "identifier"), None)
    if identity is not None:
        seen = Counter(str(row.get(identity.name, "")).strip() for row in rows)
        duplicates = {key: count for key, count in seen.items() if key and count > 1}
        if duplicates:
            issues.append(
                {
                    "column": identity.name,
                    "issue": "duplicate identifiers",
                    "count": len(duplicates),
                    "severity": "critical",
                }
            )

    unnamed = [header for header in headers if not header.strip() or header.strip().lower().startswith("unnamed")]
    if unnamed:
        issues.append({"column": ", ".join(unnamed), "issue": "unnamed columns", "count": len(unnamed), "severity": "medium"})

    score = max(0.0, 1.0 - sum(_weight(issue["severity"]) for issue in issues) / max(1, len(columns)))
    return {
        "rows": total,
        "columns": len(columns),
        "issues": issues,
        "score": round(score, 3),
        "verdict": "acceptable" if score >= 0.6 and not any(i["severity"] == "critical" for i in issues) else "remediate",
    }


def _weight(severity: str) -> float:
    return {"critical": 0.5, "high": 0.25, "medium": 0.1, "low": 0.05}.get(severity, 0.1)
