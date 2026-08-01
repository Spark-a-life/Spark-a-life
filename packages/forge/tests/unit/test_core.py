"""Unit tests for the governance primitives.

These six modules carry no model dependency. They are arithmetic, hashing,
schema validation and policy evaluation, which is precisely why the platform's
guarantees survive an offline environment.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests import POLICIES

from wisegen_forge import mini_yaml
from wisegen_forge.cost import Budget, BudgetExceeded, CostGovernor
from wisegen_forge.domain import ForgeObject, digest, new_id
from wisegen_forge.policy import PolicyEngine
from wisegen_forge.witness import WitnessChain


class WitnessChainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.chain = WitnessChain(Path(self.tmp.name) / "witness-chain.jsonl")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_empty_chain_verifies(self) -> None:
        result = self.chain.verify()
        self.assertTrue(result["ok"])
        self.assertEqual(result["length"], 0)

    def test_append_links_entries(self) -> None:
        first = self.chain.append("captain", "run.opened", {"a": 1})
        second = self.chain.append("gaie.backend-engineer", "agent.started", {"b": 2})
        self.assertEqual(second.prev_digest, first.entry_digest)
        self.assertEqual(self.chain.head(), second.entry_digest)
        self.assertTrue(self.chain.verify()["ok"])

    def test_payload_tampering_is_detected(self) -> None:
        self.chain.append("captain", "run.opened", {"statement": "original"})
        self.chain.append("captain", "gate.decided", {"action": "approve"})
        path = self.chain.path
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[0]["payload"]["statement"] = "quietly rewritten"
        path.write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n")
        result = self.chain.verify()
        self.assertFalse(result["ok"], "a rewritten payload must break verification")
        self.assertTrue(result["problems"])

    def test_deletion_is_detected(self) -> None:
        for index in range(4):
            self.chain.append("captain", "event", {"i": index})
        path = self.chain.path
        rows = path.read_text().splitlines()
        del rows[2]
        path.write_text("\n".join(rows) + "\n")
        self.assertFalse(self.chain.verify()["ok"], "a removed link must break verification")

    def test_reordering_is_detected(self) -> None:
        for index in range(4):
            self.chain.append("captain", "event", {"i": index})
        path = self.chain.path
        rows = path.read_text().splitlines()
        rows[1], rows[2] = rows[2], rows[1]
        path.write_text("\n".join(rows) + "\n")
        self.assertFalse(self.chain.verify()["ok"], "reordering must break verification")


class PolicyEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = PolicyEngine(POLICIES)

    def test_policies_load(self) -> None:
        self.assertGreater(len(self.engine.rules), 5, "the shipped policy set must load")

    def test_deny_by_default(self) -> None:
        decision = self.engine.evaluate(
            {"actor": "unknown.agent", "action": "capability:invent_something", "resource": "-"}
        )
        self.assertFalse(decision.allowed)

    def test_no_agent_may_deploy_production_without_approval(self) -> None:
        decision = self.engine.evaluate(
            {
                "actor": "gaie.backend-engineer",
                "action": "deploy_production",
                "resource": "customer-vpc",
                "classification": "restricted",
            }
        )
        self.assertFalse(
            decision.allowed and not decision.requires_approval,
            "production deployment must be denied or gated for a generating role",
        )

    def test_deny_beats_a_later_allow(self) -> None:
        """Layer order is constitutional, then organisational, then project.

        A deny at any layer is final; no later rule can overturn it.
        """
        decision = self.engine.evaluate(
            {"actor": "gaie.adversary", "action": "modify_security_policy", "resource": "policies/constitutional"}
        )
        self.assertFalse(decision.allowed)


class CostGovernorTests(unittest.TestCase):
    def test_charge_accumulates(self) -> None:
        governor = CostGovernor(project_budget=Budget(tokens=1000, tool_calls=10, sgd=1.0))
        governor.charge("gaie.backend-engineer", tokens=100, sgd=0.10)
        governor.charge("gaie.backend-engineer", tokens=150)
        snapshot = governor.snapshot()
        self.assertAlmostEqual(snapshot["project"]["tokens"], 250.0)
        self.assertAlmostEqual(snapshot["by_actor"]["gaie.backend-engineer"]["sgd"], 0.10)

    def test_project_cap_halts_execution(self) -> None:
        governor = CostGovernor(project_budget=Budget(tokens=100, tool_calls=5, sgd=0.5))
        governor.charge("gaie.backend-engineer", tokens=90)
        with self.assertRaises(BudgetExceeded):
            governor.charge("gaie.backend-engineer", tokens=50)

    def test_unknown_dimension_is_rejected(self) -> None:
        governor = CostGovernor()
        with self.assertRaises(ValueError):
            governor.charge("gaie.backend-engineer", bananas=1)

    def test_escalation_is_raised_before_the_cap(self) -> None:
        governor = CostGovernor(project_budget=Budget(tokens=1000, escalate_at=0.5))
        governor.charge("gaie.backend-engineer", tokens=600)
        self.assertTrue(governor.escalations, "crossing the escalation threshold must be recorded")


class MiniYamlTests(unittest.TestCase):
    def test_nested_structures(self) -> None:
        text = """
        version: 1.0.0
        enabled: true
        retired: null
        agents:
          - id: kaie.captain
            authority:
              allowed: [approve_release, reject]
              prohibited:
                - generate_application
          - id: gaie.adversary
            layer: forge
        """
        data = mini_yaml.loads(text)
        self.assertEqual(data["version"], "1.0.0")
        self.assertIs(data["enabled"], True)
        self.assertIsNone(data["retired"])
        self.assertEqual(data["agents"][0]["authority"]["allowed"], ["approve_release", "reject"])
        self.assertEqual(data["agents"][0]["authority"]["prohibited"], ["generate_application"])
        self.assertEqual(data["agents"][1]["layer"], "forge")

    def test_comments_and_quotes(self) -> None:
        data = mini_yaml.loads('# leading comment\nreason: "denied: not authorised"  \nn: 3\n')
        self.assertEqual(data["reason"], "denied: not authorised")
        self.assertEqual(data["n"], 3)

    def test_round_trip(self) -> None:
        original = {"a": 1, "b": ["x", "y"], "c": {"d": True}}
        self.assertEqual(mini_yaml.loads(mini_yaml.dumps(original)), original)


class DomainTests(unittest.TestCase):
    def test_ids_are_unique_and_prefixed(self) -> None:
        ids = {new_id("spec") for _ in range(200)}
        self.assertEqual(len(ids), 200)
        self.assertTrue(all(i.startswith("spec-") for i in ids))

    def test_digest_is_order_independent(self) -> None:
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))

    def test_object_round_trip_and_transition(self) -> None:
        obj = ForgeObject.create("Specification", {"objective": "onboard staff"}, owner="captain")
        restored = ForgeObject.from_dict(json.loads(json.dumps(obj.to_dict())))
        self.assertEqual(restored.digest(), obj.digest())
        moved = obj.transition("approved")
        self.assertEqual(moved.envelope.lifecycle_state, "approved")
        self.assertEqual(obj.envelope.lifecycle_state, "draft", "transition must not mutate in place")
        self.assertNotEqual(moved.envelope.version, obj.envelope.version, "a transition must bump the version")


if __name__ == "__main__":
    unittest.main()
