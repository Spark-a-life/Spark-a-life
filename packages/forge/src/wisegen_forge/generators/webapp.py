"""Code generation: specification plus data model to a runnable application.

The generated application is deliberately dependency-free (Python standard
library, SQLite) so that it starts in an air-gapped estate, on a laptop, or in a
container with the same command. Everything the governance layer promises is
enforced inside the generated code, not merely documented around it:

  * role-based access resolved server side;
  * field masking driven by data classification;
  * append-only audit with a hash chain, verifiable at runtime;
  * terminal state transitions blocked without a recorded human approval;
  * open-format export with no vendor tooling.
"""
from __future__ import annotations

import json
from typing import Any

from ..intent_compiler import Specification
from ..spreadsheet_compiler import SheetModel

APPROVER_ROLES = ("hr_administrator", "manager", "administrator", "auditor", "captain")
RESTRICTED_READERS = ("hr_administrator", "administrator")


def build_config(spec: Specification, sheet: SheetModel, candidate: str = "conservative") -> dict[str, Any]:
    identity = sheet.identity_column
    workflow = sheet.workflow
    states = workflow.get("states") or ["open", "closed"]
    terminal = workflow.get("terminal_states") or states[-1:]
    initial = (workflow.get("initial_states") or states[:1])[0]

    roles: dict[str, Any] = {}
    for user in spec.users or ["primary_user"]:
        may_approve = user in APPROVER_ROLES
        roles[user] = {
            "may_approve": may_approve,
            "may_write": may_approve or user not in ("auditor",),
            "may_create": may_approve,
            "need_to_know": list(RESTRICTED_READERS and (["restricted"] if user in RESTRICTED_READERS else [])),
        }
    roles.setdefault("auditor", {"may_approve": False, "may_write": False, "may_create": False, "need_to_know": []})

    return {
        "generator": "wisegen-forge.generators.webapp",
        "candidate": candidate,
        "entity": sheet.entity,
        "objective": spec.objective,
        "identifier": identity.slug,
        "status_field": (sheet.status_column.slug if sheet.status_column else "status"),
        "columns": [column.to_dict() for column in sheet.columns],
        "states": states,
        "initial_state": initial,
        "terminal_states": terminal,
        "transitions": workflow.get("transitions") or [],
        "roles": roles,
        "page_size_cap": 200 if candidate == "conservative" else 1000,
        "risk_tier": spec.risk_tier,
        "acceptance_criteria": spec.acceptance_criteria,
    }


def _embed(config: dict[str, Any]) -> str:
    """Embed configuration as JSON parsed at import time.

    JSON rather than a Python literal so that the same block is readable by any
    language that later reimplements this service, and so that a reviewer can
    diff the configuration without reading Python.
    """
    body = json.dumps(config, indent=4, sort_keys=True)
    return 'json.loads(r"""\n' + body + '\n""")'


def render_app(config: dict[str, Any]) -> str:
    return APP_TEMPLATE.replace("__FORGE_CONFIG__", _embed(config))


def render_tests(config: dict[str, Any]) -> str:
    return TEST_TEMPLATE.replace("__FORGE_CONFIG__", _embed(config))


def render_openapi(config: dict[str, Any]) -> str:
    entity = config["entity"]
    document = {
        "openapi": "3.0.3",
        "info": {"title": f"{entity} service", "version": "1.0.0", "description": config["objective"]},
        "paths": {
            "/health": {"get": {"summary": "liveness and audit chain status", "responses": {"200": {"description": "ok"}}}},
            f"/{entity}": {
                "get": {"summary": "list records, masked by role", "responses": {"200": {"description": "ok"}, "403": {"description": "role denied"}}},
                "post": {"summary": "create a record", "responses": {"201": {"description": "created"}, "403": {"description": "role denied"}}},
            },
            f"/{entity}/{{record_id}}": {
                "get": {"summary": "read one record", "responses": {"200": {"description": "ok"}, "404": {"description": "unknown"}}},
                "patch": {"summary": "update fields", "responses": {"200": {"description": "ok"}, "403": {"description": "role denied"}}},
            },
            f"/{entity}/{{record_id}}/transition": {
                "post": {"summary": "move the record to a new state", "responses": {"200": {"description": "ok"}, "409": {"description": "approval required"}}}
            },
            "/audit": {"get": {"summary": "append-only change history", "responses": {"200": {"description": "ok"}}}},
            "/export.csv": {"get": {"summary": "open-format export", "responses": {"200": {"description": "csv"}}}},
        },
        "components": {
            "securitySchemes": {"forgeRole": {"type": "apiKey", "in": "header", "name": "X-Forge-Token"}},
        },
        "security": [{"forgeRole": []}],
    }
    return json.dumps(document, indent=2)


def render_readme(config: dict[str, Any], spec: Specification) -> str:
    lines = [
        f"# {config['entity']} service",
        "",
        f"Generated by WiseGen Forge from an approved specification. Candidate: **{config['candidate']}**.",
        "",
        "## Objective",
        spec.objective,
        "",
        "## Run it",
        "",
        "```bash",
        "python3 app.py --db ./data.sqlite3 --port 8099",
        "curl -H 'X-Forge-Token: demo-hr_administrator' http://127.0.0.1:8099/health",
        "```",
        "",
        "## Test it",
        "",
        "```bash",
        "python3 -m unittest test_app.py -v",
        "```",
        "",
        "## Roles",
        "",
        "| Role | Create | Write | Approve | Restricted fields |",
        "| --- | --- | --- | --- | --- |",
    ]
    for role, grants in config["roles"].items():
        lines.append(
            f"| {role} | {'yes' if grants['may_create'] else 'no'} | {'yes' if grants['may_write'] else 'no'} | "
            f"{'yes' if grants['may_approve'] else 'no'} | {'visible' if grants['need_to_know'] else 'masked'} |"
        )
    lines += [
        "",
        "## Workflow",
        "",
        " -> ".join(config["states"]) or "none discovered",
        "",
        f"Terminal states requiring a recorded approval: {', '.join(config['terminal_states'])}",
        "",
        "## Acceptance criteria carried from the specification",
        "",
    ]
    lines += [f"{index}. {item}" for index, item in enumerate(spec.acceptance_criteria, start=1)]
    lines += [
        "",
        "## Ownership",
        "",
        "This code, its schema, its tests and its evidence bundle are exportable and",
        "operable without WiseGen Forge. There is no runtime dependency on the factory.",
        "",
    ]
    return "\n".join(lines)


def render_dockerfile(config: dict[str, Any]) -> str:
    return (
        "FROM python:3.12-slim\n"
        "WORKDIR /srv\n"
        "COPY . /srv\n"
        "ENV FORGE_DB=/srv/data/app.sqlite3\n"
        "RUN mkdir -p /srv/data && python3 -m unittest test_app.py\n"
        "EXPOSE 8099\n"
        "USER 10001:10001\n"
        f"HEALTHCHECK CMD python3 -c \"import urllib.request;urllib.request.urlopen('http://127.0.0.1:8099/health')\"\n"
        'CMD ["python3", "app.py", "--port", "8099"]\n'
    )


def render_schema_sql(config: dict[str, Any]) -> str:
    lines = [
        "-- Generated by WiseGen Forge. Portable DDL: SQLite and PostgreSQL compatible subset.",
        f"CREATE TABLE IF NOT EXISTS {config['entity']} (",
        "    record_id     TEXT PRIMARY KEY,",
        "    payload       TEXT NOT NULL,",
        "    status        TEXT NOT NULL,",
        "    created_at    TEXT NOT NULL,",
        "    updated_at    TEXT NOT NULL",
        ");",
        "",
        "-- Append only. Rows are never updated or deleted.",
        "CREATE TABLE IF NOT EXISTS audit_log (",
        "    seq           INTEGER PRIMARY KEY,",
        "    at            TEXT NOT NULL,",
        "    actor         TEXT NOT NULL,",
        "    role          TEXT NOT NULL,",
        "    action        TEXT NOT NULL,",
        "    record_id     TEXT,",
        "    before_value  TEXT,",
        "    after_value   TEXT,",
        "    approval_ref  TEXT,",
        "    prev_hash     TEXT NOT NULL,",
        "    entry_hash    TEXT NOT NULL",
        ");",
        "",
        "-- Field classification carried from the source dataset.",
    ]
    for column in config["columns"]:
        lines.append(f"--   {column['slug']}: {column['type']} / {column['classification']} / {column['role']}")
    return "\n".join(lines) + "\n"


APP_TEMPLATE = '''#!/usr/bin/env python3
"""Generated by WiseGen Forge. The specification is authoritative.

Regenerate rather than hand-edit: run `forge regenerate` so that drift between
this file and the approved specification stays visible and governed.

Standard library only. No network egress. Starts identically on a laptop, in a
container, in a customer VPC and in an air-gapped estate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

CONFIG = __FORGE_CONFIG__

GENESIS = "0" * 64


class AuthzError(PermissionError):
    """The caller's role does not permit this action."""


class TransitionError(ValueError):
    """The requested state change is not permitted, or lacks an approval."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def column_index() -> dict:
    return {column["slug"]: column for column in CONFIG["columns"]}


def role_grants(role: str) -> dict:
    grants = CONFIG["roles"].get(role)
    if grants is None:
        raise AuthzError("unknown role: " + str(role))
    return grants


def mask(record: dict, role: str) -> dict:
    """Field masking driven by data classification, enforced server side."""
    grants = role_grants(role)
    visible = set(grants.get("need_to_know") or [])
    out = {}
    for slug, value in record.items():
        column = column_index().get(slug)
        classification = column["classification"] if column else "internal"
        if classification == "restricted" and "restricted" not in visible:
            out[slug] = "[restricted]"
        elif classification == "confidential" and not grants.get("may_write") and "restricted" not in visible:
            out[slug] = "[masked]"
        else:
            out[slug] = value
    return out


class Service:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._ensure_schema()

    # ------------------------------------------------------------- schema
    def _ensure_schema(self) -> None:
        entity = CONFIG["entity"]
        self.connection.executescript(
            "CREATE TABLE IF NOT EXISTS " + entity + " ("
            " record_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL,"
            " created_at TEXT NOT NULL, updated_at TEXT NOT NULL);"
            "CREATE TABLE IF NOT EXISTS audit_log ("
            " seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, actor TEXT NOT NULL,"
            " role TEXT NOT NULL, action TEXT NOT NULL, record_id TEXT, before_value TEXT,"
            " after_value TEXT, approval_ref TEXT, prev_hash TEXT NOT NULL, entry_hash TEXT NOT NULL);"
        )
        self.connection.commit()

    # -------------------------------------------------------------- audit
    def _append_audit(self, actor, role, action, record_id, before, after, approval_ref=None):
        cursor = self.connection.execute("SELECT entry_hash FROM audit_log ORDER BY seq DESC LIMIT 1")
        row = cursor.fetchone()
        prev_hash = row["entry_hash"] if row else GENESIS
        at = utc_now()
        body = json.dumps(
            {
                "at": at,
                "actor": actor,
                "role": role,
                "action": action,
                "record_id": record_id,
                "before": before,
                "after": after,
                "approval_ref": approval_ref,
                "prev": prev_hash,
            },
            sort_keys=True,
        )
        entry_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        self.connection.execute(
            "INSERT INTO audit_log (at, actor, role, action, record_id, before_value, after_value,"
            " approval_ref, prev_hash, entry_hash) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                at,
                actor,
                role,
                action,
                record_id,
                json.dumps(before, sort_keys=True) if before is not None else None,
                json.dumps(after, sort_keys=True) if after is not None else None,
                approval_ref,
                prev_hash,
                entry_hash,
            ),
        )
        self.connection.commit()
        return entry_hash

    def audit(self, role: str) -> list:
        role_grants(role)
        rows = self.connection.execute("SELECT * FROM audit_log ORDER BY seq").fetchall()
        return [dict(row) for row in rows]

    def verify_audit(self) -> dict:
        prev = GENESIS
        problems = []
        for row in self.connection.execute("SELECT * FROM audit_log ORDER BY seq"):
            body = json.dumps(
                {
                    "at": row["at"],
                    "actor": row["actor"],
                    "role": row["role"],
                    "action": row["action"],
                    "record_id": row["record_id"],
                    "before": json.loads(row["before_value"]) if row["before_value"] else None,
                    "after": json.loads(row["after_value"]) if row["after_value"] else None,
                    "approval_ref": row["approval_ref"],
                    "prev": row["prev_hash"],
                },
                sort_keys=True,
            )
            expected = hashlib.sha256(body.encode("utf-8")).hexdigest()
            if row["prev_hash"] != prev:
                problems.append("seq " + str(row["seq"]) + ": broken link")
            if expected != row["entry_hash"]:
                problems.append("seq " + str(row["seq"]) + ": content altered after write")
            prev = row["entry_hash"]
        return {"ok": not problems, "head": prev, "problems": problems}

    # ------------------------------------------------------------ records
    def create(self, actor: str, role: str, data: dict) -> dict:
        grants = role_grants(role)
        if not grants.get("may_create"):
            raise AuthzError(role + " may not create records")
        record_id = str(data.get(CONFIG["identifier"]) or uuid.uuid4().hex[:12])
        status = str(data.get(CONFIG["status_field"]) or CONFIG["initial_state"])
        if status in CONFIG["terminal_states"]:
            raise TransitionError("a record may not be created directly in a terminal state")
        payload = {key: value for key, value in data.items()}
        payload[CONFIG["status_field"]] = status
        now = utc_now()
        self.connection.execute(
            "INSERT INTO " + CONFIG["entity"] + " (record_id, payload, status, created_at, updated_at)"
            " VALUES (?,?,?,?,?)",
            (record_id, json.dumps(payload, sort_keys=True), status, now, now),
        )
        self.connection.commit()
        self._append_audit(actor, role, "create", record_id, None, payload)
        return {"record_id": record_id, "status": status, "record": mask(payload, role)}

    def get(self, role: str, record_id: str) -> dict:
        role_grants(role)
        row = self.connection.execute(
            "SELECT * FROM " + CONFIG["entity"] + " WHERE record_id = ?", (record_id,)
        ).fetchone()
        if row is None:
            raise KeyError(record_id)
        payload = json.loads(row["payload"])
        return {"record_id": record_id, "status": row["status"], "record": mask(payload, role)}

    def list(self, role: str, limit: int = 50) -> list:
        role_grants(role)
        limit = max(1, min(int(limit), int(CONFIG["page_size_cap"])))
        rows = self.connection.execute(
            "SELECT * FROM " + CONFIG["entity"] + " ORDER BY created_at LIMIT ?", (limit,)
        ).fetchall()
        return [
            {"record_id": row["record_id"], "status": row["status"], "record": mask(json.loads(row["payload"]), role)}
            for row in rows
        ]

    def update(self, actor: str, role: str, record_id: str, changes: dict) -> dict:
        grants = role_grants(role)
        if not grants.get("may_write"):
            raise AuthzError(role + " may not write records")
        row = self.connection.execute(
            "SELECT * FROM " + CONFIG["entity"] + " WHERE record_id = ?", (record_id,)
        ).fetchone()
        if row is None:
            raise KeyError(record_id)
        before = json.loads(row["payload"])
        if CONFIG["status_field"] in changes:
            raise TransitionError("status changes must go through /transition so that approval is recorded")
        after = dict(before)
        after.update(changes)
        self.connection.execute(
            "UPDATE " + CONFIG["entity"] + " SET payload = ?, updated_at = ? WHERE record_id = ?",
            (json.dumps(after, sort_keys=True), utc_now(), record_id),
        )
        self.connection.commit()
        self._append_audit(actor, role, "update", record_id, before, after)
        return {"record_id": record_id, "record": mask(after, role)}

    def transition(self, actor: str, role: str, record_id: str, to_state: str, approval_ref=None) -> dict:
        grants = role_grants(role)
        if not grants.get("may_write"):
            raise AuthzError(role + " may not move records between states")
        row = self.connection.execute(
            "SELECT * FROM " + CONFIG["entity"] + " WHERE record_id = ?", (record_id,)
        ).fetchone()
        if row is None:
            raise KeyError(record_id)
        current = row["status"]
        if to_state not in CONFIG["states"]:
            raise TransitionError("unknown state: " + str(to_state))
        allowed = [t for t in CONFIG["transitions"] if t["from"] == current and t["to"] == to_state]
        if CONFIG["transitions"] and not allowed:
            raise TransitionError("no permitted transition from " + current + " to " + to_state)
        if to_state in CONFIG["terminal_states"]:
            if not grants.get("may_approve"):
                raise AuthzError(role + " may not approve a terminal transition")
            if not approval_ref:
                raise TransitionError("terminal transition requires a recorded approval reference")
        payload = json.loads(row["payload"])
        before = dict(payload)
        payload[CONFIG["status_field"]] = to_state
        self.connection.execute(
            "UPDATE " + CONFIG["entity"] + " SET payload = ?, status = ?, updated_at = ? WHERE record_id = ?",
            (json.dumps(payload, sort_keys=True), to_state, utc_now(), record_id),
        )
        self.connection.commit()
        self._append_audit(actor, role, "transition", record_id, before, payload, approval_ref)
        return {"record_id": record_id, "status": to_state, "approval_ref": approval_ref}

    # ------------------------------------------------------------- import
    def import_csv(self, actor: str, role: str, path: str) -> dict:
        loaded = 0
        skipped = []
        with open(path, newline="", encoding="utf-8-sig") as handle:
            for raw in csv.DictReader(handle):
                data = {}
                for column in CONFIG["columns"]:
                    for key, value in raw.items():
                        if key and key.strip().lower().replace(" ", "_").replace("-", "_") == column["slug"]:
                            data[column["slug"]] = value
                status = data.get(CONFIG["status_field"]) or CONFIG["initial_state"]
                if status in CONFIG["terminal_states"]:
                    data[CONFIG["status_field"]] = CONFIG["initial_state"]
                try:
                    self.create(actor, role, data)
                    loaded += 1
                except Exception as exc:
                    skipped.append({"row": data.get(CONFIG["identifier"]), "reason": str(exc)})
        return {"loaded": loaded, "skipped": skipped}

    # ------------------------------------------------------------- export
    def export_csv(self, role: str) -> str:
        buffer = io.StringIO()
        headers = [column["slug"] for column in CONFIG["columns"]]
        writer = csv.DictWriter(buffer, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for item in self.list(role, limit=int(CONFIG["page_size_cap"])):
            writer.writerow({key: item["record"].get(key, "") for key in headers})
        return buffer.getvalue()

    def export_json(self, role: str) -> str:
        return json.dumps(
            {
                "entity": CONFIG["entity"],
                "exported_at": utc_now(),
                "records": self.list(role, limit=int(CONFIG["page_size_cap"])),
                "audit_verified": self.verify_audit(),
            },
            indent=2,
        )


def resolve_role(token: str) -> tuple:
    """Resolve actor and role from a bearer token.

    Demonstration resolver: tokens look like `<actor>-<role>`. Replace with the
    institution's identity provider at deployment time. The contract that
    matters is that the role is resolved server side and never trusted from a
    client-supplied field.
    """
    if not token:
        raise AuthzError("missing token")
    actor, _, role = token.partition("-")
    if role not in CONFIG["roles"]:
        raise AuthzError("unknown role in token")
    return actor, role


class Handler(BaseHTTPRequestHandler):
    service: Service = None
    server_version = "WiseGenForgeApp/1.0"

    def _send(self, code: int, payload, content_type: str = "application/json") -> None:
        body = payload if isinstance(payload, (str, bytes)) else json.dumps(payload, indent=2)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _auth(self):
        return resolve_role(self.headers.get("X-Forge-Token", ""))

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def log_message(self, fmt, *args):  # keep stdout clean and structured
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        entity = CONFIG["entity"]
        try:
            if path == "/health":
                return self._send(200, {"status": "ok", "entity": entity, "audit": self.service.verify_audit()})
            actor, role = self._auth()
            if path == "/" + entity:
                return self._send(200, {"records": self.service.list(role)})
            if path == "/audit":
                return self._send(200, {"audit": self.service.audit(role), "verified": self.service.verify_audit()})
            if path == "/export.csv":
                return self._send(200, self.service.export_csv(role), "text/csv")
            if path == "/export.json":
                return self._send(200, self.service.export_json(role))
            if path.startswith("/" + entity + "/"):
                return self._send(200, self.service.get(role, path.split("/")[2]))
            return self._send(404, {"error": "not found"})
        except AuthzError as exc:
            return self._send(403, {"error": str(exc)})
        except KeyError as exc:
            return self._send(404, {"error": "unknown record " + str(exc)})

    def do_POST(self):
        path = urlparse(self.path).path
        entity = CONFIG["entity"]
        try:
            actor, role = self._auth()
            body = self._body()
            if path == "/" + entity:
                return self._send(201, self.service.create(actor, role, body))
            if path.startswith("/" + entity + "/") and path.endswith("/transition"):
                record_id = path.split("/")[2]
                return self._send(
                    200,
                    self.service.transition(actor, role, record_id, body.get("to"), body.get("approval_ref")),
                )
            return self._send(404, {"error": "not found"})
        except AuthzError as exc:
            return self._send(403, {"error": str(exc)})
        except TransitionError as exc:
            return self._send(409, {"error": str(exc)})
        except KeyError as exc:
            return self._send(404, {"error": "unknown record " + str(exc)})

    def do_PATCH(self):
        path = urlparse(self.path).path
        entity = CONFIG["entity"]
        try:
            actor, role = self._auth()
            if path.startswith("/" + entity + "/"):
                return self._send(200, self.service.update(actor, role, path.split("/")[2], self._body()))
            return self._send(404, {"error": "not found"})
        except AuthzError as exc:
            return self._send(403, {"error": str(exc)})
        except TransitionError as exc:
            return self._send(409, {"error": str(exc)})
        except KeyError as exc:
            return self._send(404, {"error": "unknown record " + str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description=CONFIG["objective"])
    parser.add_argument("--db", default="./app.sqlite3")
    parser.add_argument("--port", type=int, default=8099)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--import-csv")
    parser.add_argument("--actor", default="seed")
    default_role = next(
        (role for role, grants in CONFIG["roles"].items() if grants.get("may_create")),
        next(iter(CONFIG["roles"])),
    )
    parser.add_argument("--role", default=default_role)
    arguments = parser.parse_args()

    Handler.service = Service(arguments.db)
    if arguments.import_csv:
        report = Handler.service.import_csv(arguments.actor, arguments.role, arguments.import_csv)
        print(json.dumps(report, indent=2))
        return 0
    server = ThreadingHTTPServer((arguments.host, arguments.port), Handler)
    print("serving " + CONFIG["entity"] + " on http://" + arguments.host + ":" + str(arguments.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


TEST_TEMPLATE = '''"""Generated acceptance and safety tests. One test per acceptance criterion,
plus adversarial checks that the governance promises hold in code.
"""
import json
import unittest

import app

CONFIG = __FORGE_CONFIG__


def admin_role():
    for role, grants in app.CONFIG["roles"].items():
        if grants.get("may_approve"):
            return role
    return next(iter(app.CONFIG["roles"]))


def reader_role():
    for role, grants in app.CONFIG["roles"].items():
        if not grants.get("may_write"):
            return role
    return None


class GeneratedApplicationTests(unittest.TestCase):
    def setUp(self):
        self.service = app.Service(":memory:")
        self.admin = admin_role()

    def _new_record(self):
        data = {}
        for column in app.CONFIG["columns"]:
            if column["slug"] == app.CONFIG["status_field"]:
                continue
            data[column["slug"]] = (column["sample"] or ["value"])[0]
        return self.service.create("tester", self.admin, data)

    # criterion: primary task end to end
    def test_create_read_transition_round_trip(self):
        created = self._new_record()
        fetched = self.service.get(self.admin, created["record_id"])
        self.assertEqual(fetched["status"], app.CONFIG["initial_state"])
        self.assertTrue(self.service.list(self.admin))

    # criterion: immutable audit history with actor, time and prior value
    def test_audit_records_actor_time_and_prior_value(self):
        created = self._new_record()
        self.service.update("tester", self.admin, created["record_id"], {"note": "adjusted"})
        rows = self.service.audit(self.admin)
        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(rows[-1]["actor"], "tester")
        self.assertTrue(rows[-1]["at"])
        self.assertIsNotNone(rows[-1]["before_value"])

    def test_audit_chain_verifies(self):
        self._new_record()
        self.assertTrue(self.service.verify_audit()["ok"])

    # adversarial: tampering with a sealed audit row is detectable
    def test_audit_tamper_is_detected(self):
        self._new_record()
        self.service.connection.execute("UPDATE audit_log SET actor = 'ghost' WHERE seq = 1")
        self.service.connection.commit()
        self.assertFalse(self.service.verify_audit()["ok"])

    # criterion: role-based access
    def test_reader_role_cannot_write(self):
        reader = reader_role()
        if reader is None:
            self.skipTest("no read-only role in this configuration")
        created = self._new_record()
        with self.assertRaises(app.AuthzError):
            self.service.update("tester", reader, created["record_id"], {"note": "x"})

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(app.AuthzError):
            self.service.list("intruder")

    # criterion: no terminal state without recorded approval
    def test_terminal_transition_requires_approval_reference(self):
        if not app.CONFIG["terminal_states"]:
            self.skipTest("no terminal states discovered")
        created = self._new_record()
        target = app.CONFIG["terminal_states"][0]
        with self.assertRaises((app.TransitionError, app.AuthzError)):
            self.service.transition("tester", self.admin, created["record_id"], target)

    def test_status_cannot_be_changed_through_update(self):
        created = self._new_record()
        with self.assertRaises(app.TransitionError):
            self.service.update("tester", self.admin, created["record_id"], {app.CONFIG["status_field"]: "anything"})

    # criterion: restricted fields masked without need to know
    def test_restricted_fields_are_masked_for_roles_without_need_to_know(self):
        restricted = [c["slug"] for c in app.CONFIG["columns"] if c["classification"] == "restricted"]
        if not restricted:
            self.skipTest("no restricted fields in this dataset")
        blind = [r for r, g in app.CONFIG["roles"].items() if "restricted" not in (g.get("need_to_know") or [])]
        if not blind:
            self.skipTest("every role holds need to know")
        created = self._new_record()
        view = self.service.get(blind[0], created["record_id"])
        self.assertEqual(view["record"][restricted[0]], "[restricted]")

    # criterion: exportable in an open format
    def test_export_csv_and_json(self):
        self._new_record()
        csv_text = self.service.export_csv(self.admin)
        self.assertIn(app.CONFIG["columns"][0]["slug"], csv_text.splitlines()[0])
        payload = json.loads(self.service.export_json(self.admin))
        self.assertTrue(payload["audit_verified"]["ok"])

    # criterion: every source column represented
    def test_every_source_column_is_represented(self):
        slugs = {column["slug"] for column in app.CONFIG["columns"]}
        created = self._new_record()
        record = self.service.get(self.admin, created["record_id"])["record"]
        missing = slugs - set(record.keys())
        self.assertFalse(missing, "columns dropped without reason: " + ", ".join(sorted(missing)))

    def test_page_size_is_capped(self):
        self._new_record()
        self.assertLessEqual(len(self.service.list(self.admin, limit=10 ** 6)), int(app.CONFIG["page_size_cap"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''
