import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.orchestrator import config, runlog, sequencer
from scripts.orchestrator.sequencer import Step

_NOW = datetime(2026, 5, 28, 19, 0, 0, tzinfo=timezone.utc)


class TestPlanRoute(unittest.TestCase):
    def test_all_routes_resolve(self):
        routes = config.load_routing()
        self.assertEqual(len(routes), 7)
        for name in routes:
            steps = sequencer.plan_route(name)
            self.assertTrue(steps, f"route {name} produced no steps")
            for step in steps:
                self.assertTrue(step.contract, f"{name}/{step.agent} has no contract")
                self.assertTrue((config.repo_root() / step.contract).exists())

    def test_step_order_and_agents(self):
        steps = sequencer.plan_route("task_definition")
        self.assertEqual([s.agent for s in steps], ["researcher", "planner"])
        self.assertEqual([s.order for s in steps], [1, 2])
        self.assertEqual(steps[0].stage, "stages/01-task-definition")

    def test_unknown_route_raises(self):
        with self.assertRaises(sequencer.SequencerError):
            sequencer.plan_route("does_not_exist")


class TestResolvePrompt(unittest.TestCase):
    def test_each_agent_resolves_to_v1(self):
        for agent in ("researcher", "planner", "builder", "reviewer", "evaluator"):
            self.assertEqual(sequencer.resolve_prompt(agent), f"prompts/{agent}/v1.md")

    def test_unknown_agent_returns_none(self):
        self.assertIsNone(sequencer.resolve_prompt("nonexistent"))


class TestBuildContext(unittest.TestCase):
    def test_clean_bundle_for_every_step(self):
        for name in config.load_routing():
            for step in sequencer.plan_route(name):
                bundle = sequencer.build_context(step)
                self.assertEqual(bundle.missing, [], f"{name}/{step.agent}: {bundle.missing}")
                self.assertTrue(bundle.contract)
                self.assertTrue(bundle.prompt_version)
                self.assertIsNotNone(bundle.model_settings)
                self.assertTrue(bundle.inputs, "expected declared inputs from stage contract")
                self.assertTrue(bundle.outputs, "expected declared outputs from stage contract")

    def test_known_step_fields(self):
        step = sequencer.plan_route("task_definition")[1]  # planner
        bundle = sequencer.build_context(step)
        self.assertEqual(bundle.contract, "agents/planner.agent.md")
        self.assertEqual(bundle.prompt_version, "prompts/planner/v1.md")
        self.assertEqual(bundle.model_profile, "planning")
        self.assertEqual(bundle.model_settings["provider"], "claude")
        self.assertEqual(bundle.stage_contract, "stages/01-task-definition/CONTEXT.md")
        self.assertIn("output/task-definition.md", bundle.outputs)

    def test_missing_refs_reported_not_skipped(self):
        bogus = Step(
            route="bogus", stage="stages/99-nope", agent="nonexistent", order=1,
            contract="agents/nope.agent.md", default_skill=None, model_profile="nope",
        )
        bundle = sequencer.build_context(bogus)
        self.assertIsNone(bundle.prompt_version)
        self.assertIn("agents/nope.agent.md", bundle.missing)
        self.assertIn("stages/99-nope/CONTEXT.md", bundle.missing)
        self.assertIn("model_profile:nope", bundle.missing)


class TestDryRun(unittest.TestCase):
    def test_records_are_schema_valid_and_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            results = sequencer.dry_run("agent_design", runs_dir=d, now=_NOW)
            self.assertTrue(results)
            for bundle, record, path in results:
                self.assertEqual(record.validation["status"], "skipped")
                parsed = config.load_yaml_string(
                    runlog.extract_yaml_block(Path(path).read_text(encoding="utf-8"))
                )
                self.assertEqual(parsed, record.to_dict())
                self.assertEqual(parsed["validation"]["status"], "skipped")

    def test_missing_refs_surface_as_issues(self):
        bogus = Step(route="bogus", stage="stages/99-nope", agent="ghost", order=1,
                     contract="agents/ghost.md", default_skill=None, model_profile=None)
        record = sequencer._bundle_to_record(sequencer.build_context(bogus), _NOW)
        self.assertTrue(any(i["severity"] == "medium" for i in record.issues))


if __name__ == "__main__":
    unittest.main()
