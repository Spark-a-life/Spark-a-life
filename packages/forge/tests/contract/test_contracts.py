"""Contract tests: the shapes other people depend on.

These lock the interfaces that outlive any one implementation, so a refactor
that quietly drops a required field fails here rather than in a customer's
audit six months later.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tests import AGENTS, POLICIES, REPO_ROOT

from wisegen_forge import mini_yaml
from wisegen_forge.agent_runtime import AgentRegistry
from wisegen_forge.domain import CLASSIFICATIONS, LIFECYCLE_STATES, Envelope, ForgeObject
from wisegen_forge.policy import LAYER_ORDER, PolicyEngine

VALID_LAYERS = {"council", "forge", "command", "commons", "market"}
ID_PATTERN = re.compile(r"^(kaie|gaie|paie|saie|raie|taie)\.[a-z0-9-]+$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class AgentRegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = mini_yaml.load_file(AGENTS)
        cls.registry = AgentRegistry(AGENTS)

    def test_registry_is_versioned(self) -> None:
        self.assertTrue(SEMVER.match(str(self.document["version"])))

    def test_every_role_carries_the_required_contract_fields(self) -> None:
        for entry in self.document["agents"]:
            with self.subTest(agent=entry.get("id")):
                for field in ("id", "version", "layer", "role", "mandate", "exit_artefact", "authority"):
                    self.assertIn(field, entry, f"missing {field}")
                self.assertIn("allowed", entry["authority"])
                self.assertIn("prohibited", entry["authority"])

    def test_ids_follow_the_taxonomy(self) -> None:
        """Role ids carry their _AIE estate prefix, so authority is readable at a glance."""
        for agent in self.registry.all():
            with self.subTest(agent=agent.id):
                self.assertTrue(ID_PATTERN.match(agent.id), f"{agent.id} does not follow <estate>.<role>")
                self.assertTrue(SEMVER.match(agent.version))
                self.assertIn(agent.layer, VALID_LAYERS)

    def test_ids_are_unique(self) -> None:
        ids = [entry["id"] for entry in self.document["agents"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate role id in the registry")

    def test_allow_and_prohibit_lists_do_not_overlap(self) -> None:
        for agent in self.registry.all():
            overlap = set(agent.allowed) & set(agent.prohibited)
            self.assertFalse(overlap, f"{agent.id} both allows and prohibits {overlap}")

    def test_every_role_names_an_exit_artefact(self) -> None:
        for agent in self.registry.all():
            self.assertNotEqual(agent.exit_artefact, "unspecified", f"{agent.id} has no exit artefact")

    def test_every_role_names_its_approval_gate(self) -> None:
        for agent in self.registry.all():
            self.assertIn(agent.approval_gate, {"captain", "self", "assurance", "none"})

    def test_wildcard_authority_is_never_granted(self) -> None:
        for agent in self.registry.all():
            self.assertNotIn("*", agent.allowed, f"{agent.id} holds unbounded authority")

    def test_all_five_layers_are_populated(self) -> None:
        for layer in VALID_LAYERS:
            self.assertTrue(self.registry.by_layer(layer), f"no role occupies the {layer} layer")

    def test_documentation_and_registry_agree(self) -> None:
        charter = (REPO_ROOT / "docs" / "ROLES.md").read_text(encoding="utf-8")
        for agent in self.registry.all():
            self.assertIn(agent.id, charter, f"{agent.id} is in the registry but not in the role charter")


class PolicyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = PolicyEngine(POLICIES)

    def test_every_rule_is_identifiable_and_explains_itself(self) -> None:
        for rule in self.engine.rules:
            with self.subTest(rule=rule.get("id")):
                self.assertTrue(rule.get("id"))
                self.assertIn(str(rule.get("effect", "deny")).lower(), {"allow", "deny", "require_approval"})
                self.assertTrue(rule.get("reason"), "a refusal a human cannot read is not governance")

    def test_rule_ids_are_unique(self) -> None:
        ids = [rule["id"] for rule in self.engine.rules]
        self.assertEqual(len(ids), len(set(ids)), "duplicate policy rule id")

    def test_constitutional_layer_exists_and_is_evaluated_first(self) -> None:
        self.assertEqual(LAYER_ORDER[0], "constitutional")
        self.assertTrue(self.engine.layers["constitutional"], "the constitution must not be empty")

    def test_policy_files_are_parseable_yaml_subset(self) -> None:
        for path in sorted(POLICIES.rglob("*.yaml")):
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertIsInstance(mini_yaml.load_file(path), dict)


class ObjectContractTests(unittest.TestCase):
    def test_envelope_carries_the_ten_governance_fields(self) -> None:
        envelope = Envelope(id="spec-1", kind="Specification")
        for field in (
            "id",
            "kind",
            "version",
            "owner",
            "created_at",
            "created_from",
            "classification",
            "lifecycle_state",
            "evidence_refs",
            "policy_refs",
            "retention_rule",
        ):
            self.assertTrue(hasattr(envelope, field), f"the envelope must carry {field}")

    def test_unknown_classification_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Envelope(id="x", kind="Specification", classification="whatever")

    def test_unknown_lifecycle_state_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Envelope(id="x", kind="Specification", lifecycle_state="vibes")

    def test_classification_ladder_is_ordered_and_complete(self) -> None:
        for level in ("public", "internal", "confidential", "restricted"):
            self.assertIn(level, CLASSIFICATIONS)

    def test_lifecycle_covers_the_full_journey(self) -> None:
        for state in ("draft", "proposed", "approved", "executing", "verified", "released", "superseded", "rejected"):
            self.assertIn(state, LIFECYCLE_STATES)

    def test_objects_serialise_losslessly(self) -> None:
        obj = ForgeObject.create("Evidence", {"gate": "tests.pass", "passed": True}, classification="confidential")
        restored = ForgeObject.from_dict(json.loads(json.dumps(obj.to_dict())))
        self.assertEqual(restored.to_dict(), obj.to_dict())


class EvidenceSchemaTests(unittest.TestCase):
    """Published schemas must match what the runtime actually writes."""

    def test_schemas_are_valid_json_and_declare_required_fields(self) -> None:
        folder = REPO_ROOT / "evidence" / "schemas"
        schemas = sorted(folder.glob("*.json"))
        self.assertTrue(schemas, "evidence schemas must be published for external auditors")
        for path in schemas:
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("$schema", schema)
                self.assertIn("title", schema)
                self.assertIn("required", schema)
                self.assertIn("properties", schema)
                for field in schema["required"]:
                    self.assertIn(field, schema["properties"], f"{field} required but not described")

    def test_witness_entry_schema_matches_the_runtime(self) -> None:
        schema = json.loads((REPO_ROOT / "evidence" / "schemas" / "witness-entry.schema.json").read_text())
        from wisegen_forge.witness import WitnessEntry

        entry = WitnessEntry(
            seq=1,
            at="2026-07-25T00:00:00+00:00",
            actor="captain",
            event="run.started",
            payload={},
            payload_digest="sha256:0",
            prev_digest="genesis",
            entry_digest="sha256:1",
        ).to_dict()
        for field in schema["required"]:
            self.assertIn(field, entry, f"the schema requires {field} but the runtime does not emit it")


if __name__ == "__main__":
    unittest.main()
