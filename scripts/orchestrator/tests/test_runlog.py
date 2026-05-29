import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.orchestrator import config, runlog
from scripts.orchestrator.runlog import RunRecord


def _sample() -> RunRecord:
    return RunRecord(
        run_id="20260528-120000-sample",
        created_at="2026-05-28T12:00:00Z",
        request="Dry-run sample step",
        agent="builder",
        skill="skills/build/build.md",
        prompt_version="prompts/builder/v1.md",
        model_profile="building",
        inputs=["configs/agents.yaml"],
        outputs=["runs/sample.md"],
        tool_actions=["assembled context bundle"],
        validation={"status": "skipped", "notes": "dry run"},
        evaluation={"rubric": "evals/rubrics/plan-quality.md", "score": 4.2, "notes": "ok"},
        issues=[{"severity": "low", "description": "none blocking"}],
        follow_up=["proceed to phase 02"],
    )


class TestRunLog(unittest.TestCase):
    def test_round_trip_full(self):
        record = _sample()
        with tempfile.TemporaryDirectory() as d:
            path = runlog.write(record, dir=d)
            self.assertTrue(str(path).endswith("20260528-120000-sample.md"))
            markdown = Path(path).read_text(encoding="utf-8")
        parsed = config.load_yaml_string(runlog.extract_yaml_block(markdown))
        self.assertEqual(parsed, record.to_dict())

    def test_round_trip_empty_collections(self):
        record = RunRecord(
            run_id="20260528-120001-empty",
            created_at="2026-05-28T12:00:01Z",
            request="empty",
            agent="planner",
        )
        with tempfile.TemporaryDirectory() as d:
            markdown = Path(runlog.write(record, dir=d)).read_text(encoding="utf-8")
        parsed = config.load_yaml_string(runlog.extract_yaml_block(markdown))
        self.assertEqual(parsed, record.to_dict())
        self.assertEqual(parsed["inputs"], [])
        self.assertIsNone(parsed["evaluation"])
        self.assertIsNone(parsed["skill"])

    def test_new_run_id(self):
        rid = runlog.new_run_id(
            "Health Endpoint Plan",
            now=datetime(2026, 5, 28, 10, 15, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(rid, "20260528-101500-health-endpoint-plan")


if __name__ == "__main__":
    unittest.main()
